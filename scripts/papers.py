"""Validated bibliography rendering and citations for original arXiv records."""
from datetime import date
from html import escape
import json
import re
from urllib.parse import urlsplit

CORPORATE_AUTHORS = {'Scale Red Team'}


def read_papers(root, entries):
    document = json.loads((root / 'data/papers.json').read_text())
    papers = document['papers']
    ids = {entry['id'] for entry in entries}
    assert len({p['id'] for p in papers}) == len(papers), 'Duplicate paper IDs'
    for paper in papers:
        assert re.fullmatch(r'\d{4}\.\d{4,5}', paper['id']), paper['id']
        assert paper['arxiv_url'] == 'https://arxiv.org/abs/' + paper['id'], paper['id']
        assert paper['authors'] and all(isinstance(a, str) and a.strip() for a in paper['authors']), paper['id']
        assert paper['project_ids'] and set(paper['project_ids']) <= ids, paper['id']
        assert date.fromisoformat(paper['published_at']) <= date.today(), paper['id']
        for key in ('title', 'description_en', 'description_zh', 'source_url'):
            assert isinstance(paper[key], str) and paper[key].strip(), (paper['id'], key)
        for key in ('source_url', 'publisher_url'):
            if paper.get(key):
                parsed = urlsplit(paper[key])
                assert parsed.scheme == 'https' and parsed.hostname and not parsed.username and not parsed.password and not any(c.isspace() for c in paper[key]), (paper['id'], key)
        if paper.get('journal_published_at'):
            date.fromisoformat(paper['journal_published_at'])
    paper_projects = {identifier for paper in papers for identifier in paper['project_ids']}
    assert {e['id'] for e in entries if e.get('paper_url')} <= paper_projects, 'A catalog paper lacks bibliography metadata'
    return document, sorted(papers, key=lambda p: (p['published_at'], p['id']), reverse=True)


def bibliography(papers, entries, language):
    zh = language == 'zh'
    prefix = '/zh' if zh else ''
    by_id = {entry['id']: entry for entry in entries}
    title = '项目背后的研究' if zh else 'Research behind the projects'
    description = (f'{len(papers)} 篇关联原始论文，提供作者、首次提交日期、双语简介与可下载引用。' if zh else
                   f'{len(papers)} original papers behind the catalog, with authors, first-submission dates, concise summaries, and downloadable citations.')
    cards = []
    for paper in papers:
        projects = ' · '.join(f'<a href="{prefix}/projects/{identifier}/">{escape(by_id[identifier]["name"])}</a>' for identifier in paper['project_ids'])
        publisher = ''
        if paper.get('publisher_url'):
            publisher = f'<a href="{escape(paper["publisher_url"], quote=True)}">{("期刊版本" if zh else "Journal version")} ↗</a>'
        date_note = ''
        if paper.get('journal_published_at'):
            date_note = (' · 期刊发表：' if zh else ' · Journal publication: ') + escape(paper['journal_published_at'])
        cards.append(f'''<article class="paper-entry" id="arxiv-{paper['id']}" data-paper="{paper['id']}"><p class="paper-meta">arXiv:{paper['id']} · {('首次提交' if zh else 'First submitted')}: {paper['published_at']}{date_note}</p><h2><a href="{paper['arxiv_url']}">{escape(paper['title'])}</a></h2><p class="paper-authors">{escape(' · '.join(paper['authors']))}</p><p class="paper-summary">{escape(paper['description_' + language])}</p><div class="paper-links"><a href="{paper['arxiv_url']}">{('原始论文' if zh else 'Original paper')} ↗</a>{publisher}<span>{('目录项目：' if zh else 'In the catalog: ')}{projects}</span></div></article>''')
    intro = ('论文支持目录条目的背景说明，不代表我们已经复现实验。日期以首次 arXiv 提交为准；如有单独的期刊日期，会另外标注。' if zh else
             'These papers provide background for catalog entries; inclusion is not independent reproduction. Dates refer to first arXiv submission, with journal dates shown separately when recorded.')
    body = f'<section class="paper-main"><p class="eyebrow">{("原始研究与引用" if zh else "PRIMARY RESEARCH & CITATIONS")}</p><h1>{title}</h1><p class="lead">{description}</p><p>{intro}</p><a class="paper-download" href="/references.bib" download>{("下载 BibTeX" if zh else "Download BibTeX")} ↓</a>' + '\n'.join(cards) + '</section>'
    return title, description, body


def bibtex(papers):
    def tex(value):
        escapes = {'\\': r'\textbackslash{}', '{': r'\{', '}': r'\}', '&': r'\&', '%': r'\%', '#': r'\#', '_': r'\_'}
        return ''.join(escapes.get(character, character) for character in value)
    records = []
    for paper in papers:
        authors = ' and '.join('{' + tex(author) + '}' if author in CORPORATE_AUTHORS else tex(author) for author in paper['authors'])
        records.append(f'''@misc{{arxiv{paper['id'].replace('.', '')},
  title = {{{{{tex(paper['title'])}}}}},
  author = {{{authors}}},
  year = {{{paper['published_at'][:4]}}},
  archivePrefix = {{arXiv}},
  eprint = {{{paper['id']}}},
  url = {{{paper['arxiv_url']}}}
}}''')
    return '% These entries cite the arXiv versions; dates are first submission dates.\n\n' + '\n\n'.join(records) + '\n'
