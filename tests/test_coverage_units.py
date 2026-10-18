"""Keep entry, association, observation and snapshot units distinct."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from coverage_report import coverage_data


class CoverageUnits(unittest.TestCase):
    def setUp(self):
        self.entries = [
            {'id': 'a', 'content_type': 'app', 'resource_kind': 'ai-generated-output',
             'uses': ['showcase'], 'platforms': ['macos', 'windows', 'linux'],
             'implementation': 'ai-built', 'reviewed_at': '2024-04-02', 'primary_url': 'https://example.org/a'},
            {'id': 'b', 'content_type': 'app', 'resource_kind': 'environment-and-benchmark',
             'uses': ['training', 'evaluation'], 'platforms': [],
             'implementation': 'unknown', 'reviewed_at': '2024-04-03'},
            {'id': 'c', 'content_type': 'website', 'resource_kind': 'dataset',
             'uses': ['training'], 'platforms': ['web'],
             'implementation': 'unknown', 'reviewed_at': '2024-04-03'},
        ]
        papers = [{'project_ids': ['a', 'b']}, {'project_ids': ['b']}, {'project_ids': []}]
        observations = [{'project_id': 'a', 'observed_on': '2024-04-01'},
                        {'project_id': 'a', 'observed_on': '2024-04-02'}]
        guides = [{'groups': [{'choices': [{'project_id': 'b'}, {'project_id': 'c'}]}]},
                  {'groups': [{'choices': [{'project_id': 'b'}]}]}]
        sources = [{'id': 'fixture', 'name': 'Fixture', 'browse_url': 'https://example.org/registry'}]
        registry = {'records': [
            {'id': 'r1', 'source_id': 'fixture', 'source_key': 'a', 'url': 'https://example.org/a', 'attributes': {}},
            {'id': 'r2', 'source_id': 'fixture', 'source_key': 'unknown', 'url': 'https://example.org/other', 'attributes': {}},
        ], 'snapshots': [{'source_id': 'fixture', 'captured_at': '2020-01-01T01:02:03+00:00'}]}
        self.report = coverage_data(self.entries, papers, observations, guides, sources, registry)

    def test_platform_and_use_tags_do_not_become_independent_entries(self):
        self.assertEqual(self.report['catalog']['entries'], 3)
        self.assertEqual(self.report['catalog']['by_use'], {'evaluation': 1, 'showcase': 1, 'training': 2})
        app = self.report['app_platforms']
        self.assertEqual(app['app_entries'], 2)
        self.assertEqual(app['with_any_platform_tag'], 1)
        self.assertEqual(app['without_platform_tag'], 1)
        self.assertEqual(sum(row['entries'] for row in app['by_platform'].values()), 3)
        self.assertNotIn('web', app['by_platform'])

    def test_records_and_associations_keep_their_own_denominators(self):
        self.assertEqual(self.report['research'], {'papers': 3, 'linked_papers': 2, 'paper_only_records': 1,
                                                 'catalog_associations': 3, 'distinct_catalog_entries_linked': 2})
        self.assertEqual(self.report['observations']['records'], 2)
        self.assertEqual(self.report['observations']['distinct_catalog_entries'], 1)
        self.assertEqual(self.report['observations']['entries_without_observation_records'], 2)
        self.assertEqual(self.report['guides'], {'guides': 2, 'project_associations': 3, 'distinct_catalog_entries': 2})

    def test_snapshot_date_and_note_mapping_do_not_imply_source_review(self):
        registry = self.report['upstream_registries']
        self.assertEqual(registry['records'], 2)
        self.assertEqual(registry['records_with_related_catalog_notes'], 1)
        self.assertEqual(registry['sources'][0]['captured_at'], '2020-01-01T01:02:03+00:00')
        self.assertEqual(self.report['review_dates'], {'earliest': '2024-04-02', 'latest': '2024-04-03'})


if __name__ == '__main__':
    unittest.main()
