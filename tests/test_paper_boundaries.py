"""Guard against invented publication dates and accidental artifact claims."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from build import page_shell
from papers import bibliography, bibtex, paper_anchor, read_papers
from validate import Page


class PaperBoundaries(unittest.TestCase):
    def setUp(self):
        self.paper = {
            'id': '2401.01234', 'arxiv_url': 'https://arxiv.org/abs/2401.01234',
            'title': 'Example research record', 'authors': ['Ada Example'],
            'published_at': '2024-01-03', 'source_url': 'https://arxiv.org/abs/2401.01234',
            'description_en': 'A test citation.', 'description_zh': '测试引用。',
            'project_ids': ['example-project'],
        }
        self.entry = {'id': 'example-project', 'name': 'Example', 'paper_url': self.paper['arxiv_url']}

    def read(self, papers, entries):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'data').mkdir()
            (root / 'data/papers.json').write_text(json.dumps({'papers': papers}))
            return read_papers(root, entries)[1]

    def test_legacy_arxiv_links_remain_stable(self):
        records = self.read([self.paper], [self.entry])
        self.assertEqual(paper_anchor(records[0]), 'arxiv-2401.01234')
        self.assertIn('archivePrefix = {arXiv}', bibtex(records))

    def test_unlinked_paper_requires_explicit_artifact_boundary(self):
        paper = copy.deepcopy(self.paper)
        paper['project_ids'] = []
        with self.assertRaises(AssertionError):
            self.read([paper], [])
        paper.update(catalog_status='paper-only', reviewed_at='2024-02-01',
                     artifact_note_en='No reviewed artifact.', artifact_note_zh='尚无已核查产物。',
                     artifact_source_urls=['https://example.org/research'])
        records = self.read([paper], [])
        _, _, body = bibliography(records, [], 'en')
        self.assertIn('Paper record · no cataloged artifact', body)
        self.assertNotIn('/projects/', body)

    def test_year_only_citation_does_not_invent_a_full_date(self):
        paper = copy.deepcopy(self.paper)
        del paper['arxiv_url']
        paper.update(id='example-openreview', source_type='openreview',
                     url='https://openreview.net/forum?id=Example',
                     source_url='https://openreview.net/forum?id=Example', published_at=None,
                     publication_year=2025, date_note_en='Exact date unverified.', date_note_zh='具体日期未核实。')
        entry = dict(self.entry, paper_url=paper['url'])
        records = self.read([paper], [entry])
        title, description, body = bibliography(records, [entry], 'en')
        html = page_shell({'origin': 'https://example.org', 'name': 'Example', 'repository': 'https://github.com/example/repo'},
                          'en', '/papers/', title, description, body, papers=records)
        graph = Page(html).graphs[0]['@graph']
        article = next(item for item in graph if item['@type'] == 'ItemList')['itemListElement'][0]['item']
        self.assertNotIn('datePublished', article)
        self.assertIn('Publication year: 2025', body)
        self.assertNotIn('2025-01-01', html)
        self.assertIn('year = {2025}', bibtex(records))
        self.assertNotIn('archivePrefix', bibtex(records))

    def test_citation_must_match_the_project_source(self):
        entry = dict(self.entry, paper_url='https://openreview.net/forum?id=Different')
        with self.assertRaises(AssertionError):
            self.read([self.paper], [entry])

    def test_currency_in_a_title_does_not_start_tex_math(self):
        paper = dict(self.paper, title='Can Agents Earn $1 Million?')
        exported = bibtex([paper])
        self.assertIn(r'Earn \$1 Million?', exported)
        self.assertNotIn('Earn $1 Million?', exported)


if __name__ == '__main__':
    unittest.main()
