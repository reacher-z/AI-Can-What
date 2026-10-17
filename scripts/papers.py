"""Original paper citations with explicit publication and artifact boundaries."""
from datetime import date, datetime, timezone
from html import escape
import json
import re
from urllib.parse import urlsplit

CORPORATE_AUTHORS = {'Scale Red Team'}


def paper_url(paper):
    return paper.get('arxiv_url') or paper['url']


def publication_year(paper):
    return int(paper['published_at'][:4]) if paper.get('published_at') else paper['publication_year']


def paper_anchor(paper):
    return ('arxiv-' if paper.get('arxiv_url') else 'paper-') + paper['id']


def read_papers(root, entries):
    document = json.loads((root / 'data/papers.json').read_text())
    papers = document['papers']
    ids = {entry['id'] for entry in entries}
    today = datetime.now(timezone.utc).date()
    assert len({p['id'] for p in papers}) == len(papers), 'Duplicate paper IDs'
    assert len({paper_url(p) for p in papers}) == len(papers), 'Duplicate primary paper URLs'
    for paper in papers:
        if paper.get('arxiv_url'):
            assert re.fullmatch(r'\d{4}\.\d{4,5}', paper['id']), paper['id']
            assert paper['arxiv_url'] == 'https://arxiv.org/abs/' + paper['id'], paper['id']
            assert paper.get('source_type', 'arxiv') == 'arxiv' and paper.get('published_at'), paper['id']
        else:
            assert re.fullmatch(r'[a-z][a-z0-9-]+', paper['id']), paper['id']
            assert paper['source_type'] in {'openreview', 'publisher'}, paper['id']
            if paper['source_type'] == 'openreview':
                assert urlsplit(paper_url(paper)).hostname == 'openreview.net', paper['id']
        assert paper['authors'] and all(isinstance(a, str) and a.strip() for a in paper['authors']), paper['id']
        assert isinstance(paper['project_ids'], list) and set(paper['project_ids']) <= ids, paper['id']
        assert len(paper['project_ids']) == len(set(paper['project_ids'])), paper['id']
        status = paper.get('catalog_status', 'linked-project')
        assert status in {'linked-project', 'paper-only'}, paper['id']
        assert bool(paper['project_ids']) == (status == 'linked-project'), (paper['id'], 'Unlinked papers must be explicitly paper-only')
        if status == 'paper-only':
            assert paper.get('artifact_source_urls'), paper['id']
            assert paper.get('artifact_note_en', '').strip() and paper.get('artifact_note_zh', '').strip(), paper['id']
            assert date.fromisoformat(paper['reviewed_at']) <= today, paper['id']
        if paper.get('published_at'):
            assert date.fromisoformat(paper['published_at']) <= today, paper['id']
        else:
            assert type(paper.get('publication_year')) is int and 1900 <= paper['publication_year'] <= today.year, paper['id']
            assert paper.get('date_note_en', '').strip() and paper.get('date_note_zh', '').strip(), paper['id']
        for key in ('title', 'description_en', 'description_zh', 'source_url'):
            assert isinstance(paper[key], str) and paper[key].strip(), (paper['id'], key)
        urls = [paper_url(paper), paper['source_url'], paper.get('publisher_url'), *paper.get('artifact_source_urls', [])]
        for url in filter(None, urls):
            parsed = urlsplit(url)
            assert parsed.scheme == 'https' and parsed.hostname and not parsed.username and not parsed.password and not any(c.isspace() for c in url), (paper['id'], url)
        if paper.get('journal_published_at'):
            date.fromisoformat(paper['journal_published_at'])
    paper_projects = {identifier for paper in papers for identifier in paper['project_ids']}
    assert {e['id'] for e in entries if e.get('paper_url')} <= paper_projects, 'A catalog paper lacks bibliography metadata'
    by_id = {paper['id']: paper for paper in papers}
    for entry in entries:
        if not entry.get('paper_url'):
            continue
        source = urlsplit(entry['paper_url'])
        if source.hostname == 'arxiv.org':
            match = re.fullmatch(r'/(?:abs|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?(?:\.pdf)?', source.path)
            assert match and match.group(1) in by_id, (entry['id'], 'Original paper is missing')
            assert entry['id'] in by_id[match.group(1)]['project_ids'], (entry['id'], 'Original paper maps to a different project')
        else:
            assert any(entry['id'] in paper['project_ids'] and entry['paper_url'] in {paper_url(paper), paper.get('source_url'), paper.get('publisher_url')} for paper in papers), (entry['id'], 'Publisher paper is missing')
    return document, sorted(papers, key=lambda p: (publication_year(p), p.get('published_at') or '', p['id']), reverse=True)


def bibliography(papers, entries, language):
    zh = language == 'zh'
    prefix = '/zh' if zh else ''
    by_id = {entry['id']: entry for entry in entries}
    title = '研究文献与发布状态' if zh else 'Research papers and release status'
    description = (f'{len(papers)} 篇原始论文，提供作者、已知发表日期、双语简介、产物状态与可下载引用。' if zh else
                   f'{len(papers)} original papers with authors, known publication dates, concise summaries, artifact notes and downloadable citations.')
    cards = []
    for paper in papers:
        projects = ' · '.join(f'<a href="{prefix}/projects/{identifier}/">{escape(by_id[identifier]["name"])}</a>' for identifier in paper['project_ids'])
        url = escape(paper_url(paper), quote=True)
        source_label = 'arXiv:' + paper['id'] if paper.get('arxiv_url') else {'openreview': 'OpenReview', 'publisher': 'Publisher'}[paper['source_type']]
        if paper.get('published_at'):
            label = ('首次提交' if zh else 'First submitted') if paper.get('arxiv_url') else paper.get('date_label_' + language, '发表日期' if zh else 'Published')
            date_text = label + ': ' + paper['published_at']
        else:
            date_text = ('发表年份' if zh else 'Publication year') + ': ' + str(paper['publication_year']) + ' · ' + paper['date_note_' + language]
        catalog_link = '<span>' + ('目录项目：' if zh else 'In the catalog: ') + projects + '</span>' if projects else ''
        artifact_note = ''
        if paper.get('catalog_status') == 'paper-only':
            sources = ' · '.join(f'<a href="{escape(source, quote=True)}">{("状态来源" if zh else "Status source")} {i + 1} ↗</a>' for i, source in enumerate(paper['artifact_source_urls']))
            artifact_note = '<div class="paper-artifact-note"><strong>' + ('论文记录 · 尚无已核查产物条目' if zh else 'Paper record · no cataloged artifact') + '</strong><p>' + escape(paper['artifact_note_' + language]) + '</p><p>' + sources + '</p><small>' + ('状态核查：' if zh else 'Status checked: ') + paper['reviewed_at'] + '</small></div>'
        publisher = ''
        if paper.get('publisher_url'):
            publisher = f'<a href="{escape(paper["publisher_url"], quote=True)}">{("期刊版本" if zh else "Journal version")} ↗</a>'
        date_note = ''
        if paper.get('journal_published_at'):
            date_note = (' · 期刊发表：' if zh else ' · Journal publication: ') + escape(paper['journal_published_at'])
        cards.append(f'''<article class="paper-entry" id="{paper_anchor(paper)}" data-paper="{paper['id']}"><p class="paper-meta">{escape(source_label)} · {escape(date_text)}{date_note}</p><h2><a href="{url}">{escape(paper['title'])}</a></h2><p class="paper-authors">{escape(' · '.join(paper['authors']))}</p><p class="paper-summary">{escape(paper['description_' + language])}</p>{artifact_note}<div class="paper-links"><a href="{url}">{('原始论文' if zh else 'Original paper')} ↗</a>{publisher}{catalog_link}</div></article>''')
    paper_only_count = sum(p.get('catalog_status') == 'paper-only' for p in papers)
    intro = ((f'论文支持研究背景，不代表实验已复现。其中 {paper_only_count} 篇仅有论文记录，尚无对应的已核查产物条目，不计入目录条目数。arXiv 日期为首次提交；其他来源保留其已知日期，未知日月不会补造。' if zh else
              f'Inclusion provides research context, not reproduced results. {paper_only_count} papers have no corresponding reviewed artifact entry and do not add to the catalog entry count. arXiv dates are first submissions; other sources retain their known dates without invented months or days.'))
    body = f'<section class="paper-main"><p class="eyebrow">{("原始研究与引用" if zh else "PRIMARY RESEARCH & CITATIONS")}</p><h1>{title}</h1><p class="lead">{description}</p><p>{intro}</p><a class="paper-download" href="/references.bib" download>{("下载 BibTeX" if zh else "Download BibTeX")} ↓</a>' + '\n'.join(cards) + '</section>'
    return title, description, body


def bibtex(papers):
    def tex(value):
        escapes = {'\\': r'\textbackslash{}', '{': r'\{', '}': r'\}', '&': r'\&', '%': r'\%', '#': r'\#', '_': r'\_', '$': r'\$', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
        return ''.join(escapes.get(character, character) for character in value)
    records = []
    for paper in papers:
        authors = ' and '.join('{' + tex(author) + '}' if author in CORPORATE_AUTHORS else tex(author) for author in paper['authors'])
        key = 'arxiv' + paper['id'].replace('.', '') if paper.get('arxiv_url') else re.sub('[^A-Za-z0-9]', '', paper['id'])
        source_fields = f"  archivePrefix = {{arXiv}},\n  eprint = {{{paper['id']}}},\n" if paper.get('arxiv_url') else '  howpublished = {' + tex('OpenReview' if paper['source_type'] == 'openreview' else 'Publisher record') + '},\n'
        if paper.get('venue'):
            source_fields += '  note = {' + tex(paper['venue']) + '},\n'
        records.append(f'''@misc{{{key},
  title = {{{{{tex(paper['title'])}}}}},
  author = {{{authors}}},
  year = {{{publication_year(paper)}}},
{source_fields}  url = {{{paper_url(paper)}}}
}}''')
    return '% Entries cite the listed source versions. arXiv dates are first submissions; other dates follow their cited records.\n\n' + '\n\n'.join(records) + '\n'
