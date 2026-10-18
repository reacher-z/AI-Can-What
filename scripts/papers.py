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
        metadata_evidence = paper.get('metadata_evidence', [])
        assert isinstance(metadata_evidence, list), paper['id']
        assert all(isinstance(e, dict) and isinstance(e.get('supports'), str) and e['supports'].strip() and e.get('url') for e in metadata_evidence), paper['id']
        urls = [paper_url(paper), paper['source_url'], paper.get('publisher_url'), *paper.get('artifact_source_urls', []),
                *[e['url'] for e in metadata_evidence]]
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


def bibliography(papers, entries, language, *, repository=None):
    zh = language == 'zh'
    prefix = '/zh' if zh else ''
    by_id = {entry['id']: entry for entry in entries}
    title = '研究文献与发布状态' if zh else 'Research papers and release status'
    description = (f'{len(papers)} 篇原始论文，提供作者、已知发表日期、双语简介、产物状态与可下载引用。' if zh else
                   f'{len(papers)} original papers with authors, known publication dates, concise summaries, artifact notes and downloadable citations.')
    cards = []
    for paper in papers:
        source_type = 'arxiv' if paper.get('arxiv_url') else paper['source_type']
        search_text = ' '.join([paper['id'], paper['title'], *paper['authors'],
                                paper['description_en'], paper['description_zh'],
                                *[by_id[identifier]['name'] for identifier in paper['project_ids']],
                                paper.get('artifact_note_en', ''), paper.get('artifact_note_zh', '')])
        projects = ' · '.join(f'<a href="{prefix}/projects/{identifier}/">{escape(by_id[identifier]["name"])}</a>' for identifier in paper['project_ids'])
        url = escape(paper_url(paper), quote=True)
        source_label = 'arXiv:' + paper['id'] if paper.get('arxiv_url') else {'openreview': 'OpenReview', 'publisher': 'Publisher'}[paper['source_type']]
        if paper.get('published_at'):
            label = ('首次提交' if zh else 'First submitted') if paper.get('arxiv_url') else paper.get('date_label_' + language, '发表日期' if zh else 'Published')
            date_text = label + ': ' + paper['published_at']
            if paper.get('date_note_' + language):
                date_text += ' · ' + paper['date_note_' + language]
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
        for i, evidence in enumerate(paper.get('metadata_evidence', [])):
            publisher += f'<a href="{escape(evidence["url"], quote=True)}">{("文献信息来源" if zh else "Citation metadata source")} {i + 1} ↗</a>'
        date_note = ''
        if paper.get('journal_published_at'):
            date_note = (' · 期刊发表：' if zh else ' · Journal publication: ') + escape(paper['journal_published_at'])
        cards.append(f'''<article class="paper-entry" id="{paper_anchor(paper)}" data-paper="{paper['id']}" data-search="{escape(search_text, quote=True)}" data-source="{source_type}" data-catalog-status="{paper.get('catalog_status', 'linked-project')}" data-year="{publication_year(paper)}"><p class="paper-meta">{escape(source_label)} · {escape(date_text)}{date_note}</p><h2><a href="{url}">{escape(paper['title'])}</a></h2><p class="paper-authors">{escape(' · '.join(paper['authors']))}</p><p class="paper-summary">{escape(paper['description_' + language])}</p>{artifact_note}<div class="paper-links"><a href="{url}">{('原始论文' if zh else 'Original paper')} ↗</a>{publisher}{catalog_link}</div></article>''')
    paper_only_count = sum(p.get('catalog_status') == 'paper-only' for p in papers)
    intro = ((f'论文支持研究背景，不代表实验已复现。其中 {paper_only_count} 篇仅有论文记录，尚无对应的已核查产物条目，不计入目录条目数。arXiv 日期为首次提交；其他来源保留其已知日期，未知日月不会补造。' if zh else
              f'Inclusion provides research context, not reproduced results. {paper_only_count} papers have no corresponding reviewed artifact entry and do not add to the catalog entry count. arXiv dates are first submissions; other sources retain their known dates without invented months or days.'))
    years = sorted({publication_year(p) for p in papers}, reverse=True)
    source_types = {'arxiv' if p.get('arxiv_url') else p['source_type'] for p in papers}
    source_names = {'arxiv': 'arXiv', 'openreview': 'OpenReview', 'publisher': '出版机构' if zh else 'Publisher'}
    source_options = ''.join(f'<option value="{source}">{source_names[source]}</option>' for source in sorted(source_types))
    year_options = ''.join(f'<option value="{year}">{year}</option>' for year in years)
    tools = f'''<div class="paper-tools"><div class="filters">
<label class="search-box"><span aria-hidden="true">⌕</span><span class="visually-hidden">{('搜索文献' if zh else 'Search papers')}</span><input id="paper-search" type="search" autocomplete="off" aria-describedby="paper-search-hint" placeholder="{('标题、作者、项目或关键词…' if zh else 'Title, author, project or keyword…')}"></label>
<label class="visually-hidden" for="paper-year">{('发表年份' if zh else 'Publication year')}</label><select id="paper-year"><option value="">{('所有年份' if zh else 'All years')}</option>{year_options}</select>
<label class="visually-hidden" for="paper-source">{('文献来源' if zh else 'Paper source')}</label><select id="paper-source"><option value="">{('所有来源' if zh else 'All sources')}</option>{source_options}</select>
<label class="visually-hidden" for="paper-status">{('目录关联' if zh else 'Catalog linkage')}</label><select id="paper-status"><option value="">{('全部关联状态' if zh else 'Any catalog link')}</option><option value="linked-project">{('已有目录条目' if zh else 'With catalog entry')}</option><option value="paper-only">{('尚无产物条目' if zh else 'No artifact entry')}</option></select>
<button id="paper-reset" class="reset" type="button" hidden>{('重置' if zh else 'Reset')}</button></div>
<p id="paper-search-hint" class="search-hint">{('关键词可组合搜索；用英文引号查找完整短语。年份采用文献记录的日期口径。' if zh else 'Combine keywords or put a phrase in double quotes. Years follow each citation’s stated date basis.')}</p>
<div class="results-line"><span id="paper-count" role="status" aria-live="polite">{len(papers)} {('篇文献' if zh else 'papers')}</span></div></div>
<div class="empty" id="paper-empty" hidden></div>
<noscript><p>{('全部文献与引用均可直接浏览；搜索和筛选需要 JavaScript。' if zh else 'Every paper and citation is available below. Search and filtering use JavaScript.')}</p></noscript>'''
    repository_link = ''
    if repository:
        filename = 'README.zh-CN.md' if zh else 'README.md'
        repository_link = f'<a href="{escape(repository, quote=True)}/blob/main/papers/{filename}">{("GitHub 文献目录" if zh else "Bibliography on GitHub")} ↗</a>'
    body = f'<section class="paper-main"><p class="eyebrow">{("原始研究与引用" if zh else "PRIMARY RESEARCH & CITATIONS")}</p><h1>{title}</h1><p class="lead">{description}</p><p>{intro}</p><div class="paper-actions"><a class="paper-download" href="/references.bib" download>{("下载全部引用 BibTeX" if zh else "Download all citations · BibTeX")} ↓</a>{repository_link}</div>' + tools + '\n'.join(cards) + '</section>'
    return title, description, body


def build_paper_docs(root, config, papers, entries):
    """Keep a readable repository bibliography available alongside HTML and BibTeX."""
    directory = root / 'papers'
    directory.mkdir(exist_ok=True)
    by_id = {entry['id']: entry for entry in entries}
    paper_only_count = sum(p.get('catalog_status') == 'paper-only' for p in papers)

    def markdown(value):
        return re.sub(r'([\\`*_\[\]<>])', r'\\\1', value)

    for language in ('en', 'zh'):
        zh = language == 'zh'
        origin = config['origin'].rstrip('/') + ('/zh' if zh else '')
        filename = 'README.zh-CN.md' if zh else 'README.md'
        counterpart = 'README.md' if zh else 'README.zh-CN.md'
        title = '研究文献与发布状态' if zh else 'Research papers and release status'
        catalog_readme = '../README.zh-CN.md' if zh else '../README.md'
        lines = ['# ' + title, '',
                 f'[{("返回目录" if zh else "Catalog")}]({catalog_readme}) · [{("网页筛选" if zh else "Search on the website")}]({origin}/papers/) · [BibTeX](../references.bib) · [{("English" if zh else "中文")}]({counterpart})', '',
                 (f'**{len(papers)} 篇文献，其中 {paper_only_count} 篇尚无对应的已核查产物条目。** 文献与目录记录数量不能相加。收录提供研究背景，不代表已运行软件或复现实验。' if zh else
                  f'**{len(papers)} papers; {paper_only_count} have no corresponding reviewed artifact entry.** Paper and catalog counts are not additive. Inclusion provides research context, not software execution or reproduced results.'), '',
                 ('arXiv 日期为首次提交；其他来源保留已知日期或年份，不补造未知日月。全文、作者与具体发布状态以链接来源为准。' if zh else
                  'arXiv dates are first submissions. Other sources retain their known date or year without invented months or days. Follow the linked sources for full text, authorship and artifact status.'), '']
        current_year = None
        for paper in papers:
            year = publication_year(paper)
            if year != current_year:
                lines.extend(['## ' + str(year), ''])
                current_year = year
            lines.extend([f"### [{markdown(paper['title'])}](<{paper_url(paper)}>)", '',
                          ('作者：' if zh else 'Authors: ') + ' · '.join(markdown(a) for a in paper['authors']), ''])
            if paper.get('published_at'):
                date_label = ('首次提交' if zh else 'First submitted') if paper.get('arxiv_url') else paper.get('date_label_' + language, '发表日期' if zh else 'Published')
                date_text = date_label + ': ' + paper['published_at']
                if paper.get('date_note_' + language):
                    date_text += ' · ' + paper['date_note_' + language]
            else:
                date_text = ('发表年份' if zh else 'Publication year') + ': ' + str(year) + ' · ' + paper['date_note_' + language]
            if paper.get('journal_published_at'):
                date_text += (' · 期刊发表：' if zh else ' · Journal publication: ') + paper['journal_published_at']
            lines.extend([markdown(date_text), '', markdown(paper['description_' + language]), ''])
            if paper.get('catalog_status') == 'paper-only':
                lines.extend(['**' + ('论文记录 · 尚无已核查产物条目' if zh else 'Paper record · no cataloged artifact') + '**', '',
                              markdown(paper['artifact_note_' + language]), '',
                              ('状态核查：' if zh else 'Status checked: ') + paper['reviewed_at'] + ' · ' +
                              ' · '.join(f'[{("状态来源" if zh else "Status source")} {i + 1}](<{url}>)' for i, url in enumerate(paper['artifact_source_urls'])), ''])
            else:
                links = ' · '.join(f'[{markdown(by_id[identifier]["name"])}]({origin}/projects/{identifier}/)' for identifier in paper['project_ids'])
                lines.extend([('目录关联：' if zh else 'In the catalog: ') + links, ''])
            if paper.get('publisher_url'):
                lines.extend([f'[{("期刊版本" if zh else "Journal version")}]({paper["publisher_url"]})', ''])
            for evidence in paper.get('metadata_evidence', []):
                lines.extend([f'[{("文献信息来源" if zh else "Citation metadata source")}]({evidence["url"]})', ''])
        lines.extend(['---', '', ('由 `data/papers.json` 和 `data/catalog.json` 自动生成；修改源数据后运行构建。' if zh else
                                 'Generated from `data/papers.json` and `data/catalog.json`; edit the source data and rebuild.'), ''])
        (directory / filename).write_text('\n'.join(lines), encoding='utf-8')


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
