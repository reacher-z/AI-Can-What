"""Checks for misleading joins, incomplete snapshots and accidental upstream execution."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from registries import identity, validate_url
from sync_registries import parse_harbor, parse_python_dictionary, parse_tree, records_digest, validate_census


class RegistryBoundaries(unittest.TestCase):
    def setUp(self):
        self.source = {'id': 'harbor-hub', 'kind': 'dataset-package', 'browse_url': 'https://hub.harborframework.com/datasets'}
        self.packages = [
            {'id': 'first', 'name': 'same-name', 'type': 'dataset', 'visibility': 'public', 'org': {'name': 'author-a'}},
            {'id': 'second', 'name': 'same-name', 'type': 'dataset', 'visibility': 'public', 'org': {'name': 'author-b'}},
        ]
        self.versions = [{'tag': 'latest', 'package': self.packages[0], 'dataset_version': {
            'id': 'revision-a', 'revision': 2, 'content_hash': 'a' * 64,
            'published_at': None, 'yanked_at': None, 'dataset_version_task': [{'count': 17}],
        }}]

    def census(self, rows):
        return {'records': rows, 'advertised_total': len(rows), 'records_sha256': records_digest(rows)}

    def test_missing_version_remains_unknown_and_namespaces_stay_distinct(self):
        records, coverage = parse_harbor(self.source, self.census(self.packages), self.census(self.versions))
        self.assertEqual(len(records), 2)
        self.assertNotEqual(records[0]['id'], records[1]['id'])
        missing = records[1]
        self.assertEqual(missing['attributes']['version_status'], 'unavailable')
        self.assertNotIn('task_count', missing['attributes'])
        self.assertEqual(missing['url'], self.source['browse_url'])
        self.assertEqual(coverage['missing_version_count'], 1)

    def test_duplicate_or_incomplete_census_is_rejected(self):
        duplicate = self.census([self.packages[0], self.packages[0]])
        with self.assertRaises(ValueError): validate_census(duplicate, 'package')
        partial = self.census(self.packages)
        partial['advertised_total'] += 1
        with self.assertRaises(ValueError): validate_census(partial, 'package')

    def test_private_package_cannot_enter_public_capture(self):
        private = copy.deepcopy(self.packages)
        private[0]['visibility'] = 'private'
        with self.assertRaises(ValueError): validate_census(self.census(private), 'package')

    def test_identity_change_between_censuses_is_rejected(self):
        changed = copy.deepcopy(self.versions)
        changed[0]['package']['org']['name'] = 'different-author'
        with self.assertRaises(ValueError): parse_harbor(self.source, self.census(self.packages), self.census(changed))

    def test_source_code_is_parsed_without_running_it(self):
        source = {'id': 'browsergym', 'kind': 'benchmark-configuration', 'dictionary': 'DEFAULT_BENCHMARKS', 'browse_url': 'https://example.org/config.py'}
        code = b'raise RuntimeError("must never execute")\nDEFAULT_BENCHMARKS = {"tiny": lambda: Benchmark(name="tiny", backends=["web"])}\n'
        records = parse_python_dictionary(source, code)
        self.assertEqual(records[0]['attributes']['benchmark_name'], 'tiny')
        self.assertEqual(records[0]['attributes']['backends'], ['web'])

    def test_truncated_tree_is_not_a_complete_inventory(self):
        with self.assertRaises(ValueError): parse_tree({}, {'truncated': True, 'tree': []})

    def test_pinned_artifact_matching_does_not_collapse_sibling_apps(self):
        first = identity('https://github.com/example/apps/tree/' + 'a' * 40 + '/apps/one')
        self.assertEqual(first, identity('https://github.com/example/apps/tree/main/apps/one'))
        self.assertNotEqual(first, identity('https://github.com/example/apps/tree/main/apps/two'))
        self.assertNotEqual(first, identity('https://github.com/example/apps'))
        self.assertNotEqual(first, identity('https://github.com/example/apps/tree/main/apps/One'))
        self.assertEqual(first, identity('https://github.com/EXAMPLE/Apps/tree/main/apps/one'))

    def test_non_web_or_credential_urls_are_rejected(self):
        for url in ('javascript:alert(1)', 'https://user:password@example.org/x'):
            with self.assertRaises(ValueError): validate_url(url)


if __name__ == '__main__':
    unittest.main()
