#!/usr/bin/env python3
"""Build a bilingual, source-backed software and agent-environment directory."""
from __future__ import annotations

from collections import Counter
from datetime import date
from html import escape
import hashlib
import json
from pathlib import Path
import re
import shutil
from urllib.parse import urlsplit
from xml.sax.saxutils import escape as xml_escape

from catalog_docs import build_catalog_docs
from papers import CORPORATE_AUTHORS, bibliography, bibtex, read_papers

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
TYPES = {'game': ('Games & virtual worlds', '游戏与虚拟世界'), 'website': ('Websites', '网站'), 'app': ('Apps', '应用')}
SLUGS = {'game': 'games', 'website': 'websites', 'app': 'apps'}
USES = {'showcase': ('Showcase', '作品展示'), 'training': ('Training', '训练'), 'evaluation': ('Evaluation', '评测')}
PLATFORMS = {'web': 'Web', 'macos': 'macOS', 'windows': 'Windows', 'linux': 'Linux', 'ios': 'iOS', 'android': 'Android'}
IMPLEMENTATIONS = {'ai-built': ('AI-built, author-reported', '作者报告为 AI 构建'), 'ai-assisted': ('AI-assisted, author-reported', '作者报告为 AI 辅助开发'), 'human-built': ('Human-built, author-reported', '作者报告为人工开发'), 'unknown': ('Development provenance not established', '开发方式未确认')}
KINDS = {'ai-generated-output': ('AI-built software', 'AI 软件作品'), 'environment-and-benchmark': ('Environment + benchmark', '环境与评测'), 'environment-framework': ('Environment framework', '环境框架'), 'benchmark-suite': ('Benchmark suite', '评测套件'), 'dataset-and-benchmark': ('Dataset + benchmark', '数据集与评测')}


def read_inputs():
    config = json.loads((ROOT / 'site.json').read_text())
    origin = urlsplit(config['origin'])
    assert origin.scheme == 'https' and origin.hostname and origin.path in {'', '/'} and not origin.query and not origin.fragment and not origin.username and not origin.password, 'Canonical origin must be a bare public HTTPS origin.'
    document = json.loads((ROOT / 'data/catalog.json').read_text())
    entries = document['entries']
    assert entries, 'The public directory needs real entries.'
    assert len({e['id'] for e in entries}) == len(entries), 'Duplicate project IDs'
    for e in entries:
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', e['id']), e['id']
        assert e['content_type'] in TYPES and e['implementation'] in IMPLEMENTATIONS, e['id']
        assert e['resource_kind'] in KINDS, e['id']
        if e['resource_kind'] == 'ai-generated-output' or 'showcase' in e['uses']:
            assert e['implementation'] in {'ai-built', 'ai-assisted'}, f"Showcases need explicit AI-development evidence: {e['id']}"
        assert e['uses'] and set(e['uses']) <= USES.keys(), e['id']
        assert isinstance(e['platforms'], list) and set(e['platforms']) <= PLATFORMS.keys(), e['id']
        assert e['verification'] == 'source-reviewed', e['id']
        assert date.fromisoformat(e['reviewed_at']) <= date.today(), e['id']
        for key in ('name', 'description_en', 'description_zh', 'limits_en', 'limits_zh', 'enables_en', 'enables_zh'):
            assert isinstance(e[key], str) and e[key].strip(), (e['id'], key)
        if e['implementation'] in {'ai-built', 'ai-assisted'}:
            assert e.get('provenance_source'), f"Missing development evidence: {e['id']}"
        for key in ('primary_url', 'repo_url', 'demo_url', 'paper_url', 'provenance_source'):
            value = e.get(key)
            if value is None and key != 'primary_url':
                continue
            parsed = urlsplit(value)
            assert parsed.scheme == 'https' and parsed.hostname and not parsed.username and not parsed.password, (e['id'], key)
            assert not any(c.isspace() for c in value), (e['id'], key)
    return config, document, entries


def structured(graph):
    text = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False)
    return '<script type="application/ld+json">' + text.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026') + '</script>'


def lang_path(language, path='/'):
    return ('/zh' if language == 'zh' else '') + path


def project_path(language, entry):
    return lang_path(language, '/projects/' + entry['id'] + '/')


def use_pills(entry, language):
    index = int(language == 'zh')
    return ''.join(f'<span class="pill {value}">{USES[value][index]}</span>' for value in entry['uses'])


def render_row(entry, language):
    zh = language == 'zh'
    search = ' '.join([entry['name'], entry['description_en'], entry['description_zh'], entry['content_type'], *KINDS[entry['resource_kind']], *entry['uses'], *entry['platforms']]).lower()
    platforms = ', '.join(PLATFORMS[p] for p in entry['platforms']) or ('见上游说明' if zh else 'See upstream')
    return f'''<tr data-project="{entry['id']}" data-kind="{entry['resource_kind']}" data-search="{escape(search, quote=True)}" data-uses="{' '.join(entry['uses'])}" data-platforms="{' '.join(entry['platforms'])}">
<td class="project-cell"><a class="project-name" href="{project_path(language, entry)}">{escape(entry['name'])}<span class="arrow" aria-hidden="true">↗</span></a><span class="project-kind">{KINDS[entry['resource_kind']][int(zh)]}</span><p class="project-description">{escape(entry['description_' + language])}</p></td>
<td class="type-cell"><span class="type-label">{TYPES[entry['content_type']][int(zh)]}</span></td>
<td class="use-cell">{use_pills(entry, language)}</td>
<td class="platform-cell">{escape(platforms)}</td>
<td class="evidence-cell"><a class="evidence-link" href="{escape(entry['primary_url'], quote=True)}">{('查看原始来源 ↗' if zh else 'Original source ↗')}</a><time class="review-date" datetime="{entry['reviewed_at']}">{entry['reviewed_at']}</time></td>
</tr>'''


def page_shell(config, language, path, title, description, body, *, items=None, detail=None, papers=None, asset_revision=''):
    zh = language == 'zh'
    origin = config['origin'].rstrip('/')
    canonical = origin + lang_path(language, path)
    locale = 'zh-CN' if zh else 'en'
    homepage = origin + '/'
    graph = [
        {'@type': 'WebSite', '@id': homepage + '#website', 'url': homepage, 'name': config['name'], 'inLanguage': ['en', 'zh-CN']},
        {'@type': 'CollectionPage' if items is not None else 'WebPage', '@id': canonical + '#page', 'url': canonical,
         'name': title, 'description': description, 'inLanguage': locale, 'isPartOf': {'@id': homepage + '#website'}},
    ]
    if items is not None:
        graph[1]['mainEntity'] = {'@id': canonical + '#list'}
        graph.append({'@type': 'ItemList', '@id': canonical + '#list', 'numberOfItems': len(items),
                      'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': e['name'], 'url': origin + project_path(language, e)} for i, e in enumerate(items)]})
    if detail:
        graph[1]['about'] = {'@type': 'CreativeWork', 'name': detail['name'], 'url': detail['primary_url']}
        graph[1]['citation'] = [u for u in dict.fromkeys([detail['primary_url'], detail.get('paper_url'), detail.get('repo_url')]) if u]
    if papers is not None:
        graph[1]['@type'] = 'CollectionPage'
        graph[1]['mainEntity'] = {'@id': canonical + '#list'}
        graph.append({'@type': 'ItemList', '@id': canonical + '#list', 'numberOfItems': len(papers), 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'item': {'@type': 'ScholarlyArticle', 'name': p['title'], 'url': p['arxiv_url'],
             'author': [{'@type': 'Organization' if author in CORPORATE_AUTHORS else 'Person', 'name': author} for author in p['authors']], 'datePublished': p['published_at']}}
            for i, p in enumerate(papers)]})
    if path != '/':
        graph[1]['breadcrumb'] = {'@id': canonical + '#breadcrumbs'}
        graph.append({'@type': 'BreadcrumbList', '@id': canonical + '#breadcrumbs', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': '目录' if zh else 'Directory', 'item': origin + lang_path(language)},
            {'@type': 'ListItem', 'position': 2, 'name': title, 'item': canonical},
        ]})
    home = lang_path(language)
    counterpart = lang_path('en' if zh else 'zh', path)
    full_title = title if title == config['name'] else title + ' · ' + config['name']
    return f'''<!doctype html>
<html lang="{locale}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#f8f9f4">
<title>{escape(full_title)}</title><meta name="description" content="{escape(description, quote=True)}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{origin + path}"><link rel="alternate" hreflang="zh-CN" href="{origin + '/zh' + path}"><link rel="alternate" hreflang="x-default" href="{origin + path}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{escape(config['name'], quote=True)}"><meta property="og:title" content="{escape(full_title, quote=True)}"><meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:locale" content="{('zh_CN' if zh else 'en_US')}">
<meta name="twitter:card" content="summary"><meta name="twitter:title" content="{escape(full_title, quote=True)}"><meta name="twitter:description" content="{escape(description, quote=True)}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/styles.css?v={asset_revision}">
<script src="/app.js?v={asset_revision}" defer></script>{structured(graph)}
</head>
<body>
<a class="skip" href="#main">{('跳到正文' if zh else 'Skip to content')}</a>
<header class="masthead"><div class="shell header-inner"><a class="brand" href="{home}" aria-label="AI Can What? home"><span class="brand-mark" aria-hidden="true">?</span>AI can <span>what?</span></a><nav class="header-nav" aria-label="{('主导航' if zh else 'Main navigation')}"><a class="explore-link" href="{home}">{('浏览目录' if zh else 'Explore')}</a><a href="{lang_path(language, '/papers/')}">{('论文' if zh else 'Research')}</a><a href="{lang_path(language, '/about/')}">{('收录方法' if zh else 'Our method')}</a><a href="{counterpart}" hreflang="{('en' if zh else 'zh-CN')}" lang="{('en' if zh else 'zh-CN')}">{('EN' if zh else '中文')}</a><a class="repo-link" href="{config['repository']}">GitHub ↗</a></nav></div></header>
<main id="main" class="shell">{body}</main>
<footer class="site-footer"><div class="shell footer-inner"><span>AI Can What? · {('用来源说话的目录。' if zh else 'A directory with receipts.')}</span><nav class="footer-links" aria-label="{('更多信息' if zh else 'More information')}"><a href="{lang_path(language, '/about/')}">{('关于与收录方法' if zh else 'About & method')}</a><a href="/catalog.json">{('下载数据' if zh else 'Download catalog')}</a><a href="{config['repository']}">GitHub ↗</a><a href="{config['repository']}/issues/new?template=resource.yml">{('建议条目' if zh else 'Suggest an entry')} ↗</a></nav></div></footer>
</body></html>
'''


def directory(config, entries, language, category=None):
    zh = language == 'zh'
    index = int(zh)
    visible = [e for e in entries if not category or e['content_type'] == category]
    counts = Counter(e['content_type'] for e in entries)
    if category:
        title = TYPES[category][index]
        headings = {
            'game': ('Games to build.<br><em>Worlds to learn in.</em>', 'AI 创造游戏，<br><em>也在游戏里学习。</em>'),
            'website': ('Websites it builds.<br><em>Tasks it takes on.</em>', '从构建网站，<br><em>到完成网站任务。</em>'),
            'app': ('Apps and tools.<br><em>Workflows to test.</em>', '应用与工具，<br><em>真实的任务与评测。</em>'),
        }
        heading = headings[category][index]
    else:
        title = config['name']
        heading = 'AI 做出的软件，<br><em>AI 学习的环境。</em>' if zh else 'Software it builds.<br><em>Worlds it learns in.</em>'
    description = ('探索 AI 参与开发的软件，以及 Agent 训练与评测所用的环境、基准和数据集。每条记录都有原始来源。' if zh else
                   'Explore AI-built software, agent environments, benchmarks, and datasets. Every entry links back to its source.')
    if category:
        description = ({'game': '游戏作品与交互式学习环境，附原始代码、论文或作者演示。', 'website': 'AI 网站作品、浏览器环境，以及网页生成和交互相关的数据集与基准。', 'app': '应用、模拟应用 API，以及计算机操作、工具使用和软件工程评测。'} if zh else
                       {'game': 'Game showcases and interactive learning environments, with original code, papers, or author demos.', 'website': 'AI-created websites, browser environments, and datasets and benchmarks for web generation and interaction.', 'app': 'Applications, simulated app APIs, and benchmarks for computer use, tool use and software engineering.'})[category]
    tabs = [f'<a href="{lang_path(language)}"' + (' aria-current="page"' if not category else '') + f'>{("全部" if zh else "All projects")}<span class="count">{len(entries)}</span></a>']
    for key, labels in TYPES.items():
        tabs.append(f'<a href="{lang_path(language, "/" + SLUGS[key] + "/")}"' + (' aria-current="page"' if category == key else '') + f'>{labels[index]}<span class="count">{counts[key]}</span></a>')
    options_uses = ''.join(f'<option value="{key}">{labels[index]}</option>' for key, labels in USES.items())
    options_kinds = ''.join(f'<option value="{key}">{labels[index]}</option>' for key, labels in KINDS.items())
    options_platforms = ''.join(f'<option value="{key}">{label}</option>' for key, label in PLATFORMS.items())
    rows = '\n'.join(render_row(e, language) for e in visible)
    body = f'''<section class="hero"><div><p class="eyebrow">{('AI 软件与 Agent 环境目录' if zh else 'THE SOFTWARE & AGENT ENVIRONMENT INDEX')}</p><h1>{heading}</h1><p class="hero-copy">{description}</p></div><aside class="hero-note"><div class="two-lanes"><span>{('看 AI 构建' if zh else 'See it build')}</span><span class="lane-arrow" aria-hidden="true">↔</span><span>{('看 AI 行动' if zh else 'See it act')}</span></div><p>{('同一个目录，两个视角。浏览有据可查的作品，找到可供 Agent 训练与评测的环境。' if zh else 'Two sides of the same question. Discover what people build with AI, and where agents learn to get things done.')}</p><p><span class="pill">{('原始来源已查阅' if zh else 'Primary sources reviewed')}</span></p></aside></section>
<div class="stats"><span><strong>{len(entries)}</strong> {('个项目' if zh else 'projects')}</span><span><strong>{counts['game']}</strong> {('游戏与虚拟世界' if zh else 'games / worlds')}</span><span><strong>{counts['website']}</strong> {('网站' if zh else 'websites')}</span><span><strong>{counts['app']}</strong> {('应用' if zh else 'apps')}</span><span class="updated">{('来源核查' if zh else 'Sources reviewed')} · {max(e['reviewed_at'] for e in entries)}</span></div>
<section class="directory" aria-labelledby="directory-title"><div class="directory-top"><div class="directory-heading"><h2 id="directory-title">{('浏览目录' if zh else 'Explore the directory')}</h2><a href="{config['repository']}/issues/new?template=resource.yml">{('建议一个项目' if zh else 'Suggest a project')} ↗</a></div><nav class="category-tabs" aria-label="{('项目类型' if zh else 'Project category')}">{''.join(tabs)}</nav>
<div class="filters"><label class="search-box"><span aria-hidden="true">⌕</span><span class="visually-hidden">{('搜索项目' if zh else 'Search projects')}</span><input id="catalog-search" type="search" placeholder="{('搜索项目、任务、平台…' if zh else 'Search projects, tasks, platforms…')}" autocomplete="off"></label><label class="visually-hidden" for="kind-filter">{('资源类型' if zh else 'Resource type')}</label><select id="kind-filter"><option value="">{('所有资源类型' if zh else 'All resource types')}</option>{options_kinds}</select><label class="visually-hidden" for="use-filter">{('用途' if zh else 'Use')}</label><select id="use-filter"><option value="">{('所有用途' if zh else 'All uses')}</option>{options_uses}</select><label class="visually-hidden" for="platform-filter">{('平台' if zh else 'Platform')}</label><select id="platform-filter"><option value="">{('所有平台' if zh else 'All platforms')}</option>{options_platforms}</select><button id="reset-filters" class="reset" type="button" hidden>{('重置' if zh else 'Reset')}</button></div>
<div class="results-line"><span id="result-count" role="status" aria-live="polite">{len(visible)} {('个项目' if zh else 'projects')}</span><span>{('来源核查 ≠ 运行验证' if zh else 'Source review ≠ runtime verification')}</span></div></div>
<div class="table-wrap"><table><thead><tr><th>{('项目' if zh else 'Project')}</th><th>{('类别' if zh else 'Type')}</th><th>{('用途' if zh else 'Use')}</th><th class="platform-head">{('平台' if zh else 'Platform')}</th><th>{('证据与日期' if zh else 'Evidence / reviewed')}</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="empty" id="empty-state" hidden><h3>{('没有匹配的项目。' if zh else 'No projects match yet.')}</h3><p>{('换一个关键词，或重置筛选条件。' if zh else 'Try a different search or reset the filters.')}</p></div><noscript><p class="no-script">{('所有项目与链接均可直接浏览；搜索和筛选需要 JavaScript。' if zh else 'Every project and link is available here. Search and filtering use JavaScript.')}</p></noscript></section>
<section class="note-strip" aria-label="{('目录说明' if zh else 'Reading the directory')}"><article><h3>{('作品、环境与评测资料。' if zh else 'Software, environments, and benchmarks.')}</h3><p>{('作品展示 AI 参与开发的成果；环境支持交互任务；基准和数据集提供评测材料。资源类型与开发方式分别标注。' if zh else 'Showcases document software made with AI. Environments support interaction; benchmarks and datasets support evaluation. Resource types and development provenance are labeled separately.')}</p></article><article><h3>{('从每条记录回到证据。' if zh else 'Follow every entry back to its evidence.')}</h3><p>{('我们记录原始链接、核查日期和已知限制。演示和代码由上游项目提供。' if zh else 'We record original links, review dates, and known limits. Demos and code belong to their upstream projects.')} <a href="{lang_path(language, '/about/')}">{('了解收录方法' if zh else 'Read our method')} ↗</a></p></article></section>'''
    return title, description, body, visible


def detail_page(config, entry, entries, language):
    zh = language == 'zh'
    index = int(zh)
    platforms = ', '.join(PLATFORMS[p] for p in entry['platforms']) or ('请查阅上游说明' if zh else 'Consult upstream documentation')
    category_path = lang_path(language, '/' + SLUGS[entry['content_type']] + '/')
    links = [(entry['primary_url'], '原始项目' if zh else 'Original project', True)]
    for field, labels in [('repo_url', ('Source code', '源代码')), ('demo_url', ('Author demo', '作者演示')), ('paper_url', ('Original paper', '原始论文')), ('provenance_source', ('Development evidence', '开发方式证据'))]:
        if entry.get(field) and entry[field] != entry['primary_url']:
            links.append((entry[field], labels[index], False))
    source_links = ''.join(f'<a href="{escape(url, quote=True)}"' + (' class="primary-action"' if primary else '') + f'>{label} ↗</a>' for url, label, primary in links)
    related = [e for e in entries if e['content_type'] == entry['content_type'] and e['id'] != entry['id']]
    related.sort(key=lambda e: (-(2 * (e['resource_kind'] == entry['resource_kind']) + 2 * len(set(e['platforms']) & set(entry['platforms'])) + len(set(e['uses']) & set(entry['uses']))), e['name'].casefold()))
    related = related[:3]
    related_html = ''.join(f'<a href="{project_path(language, e)}">{escape(e["name"])}<small>{" / ".join(USES[u][index] for u in e["uses"])}</small></a>' for e in related)
    provenance = IMPLEMENTATIONS[entry['implementation']][index]
    body = f'''<nav class="breadcrumb" aria-label="{('当前位置' if zh else 'Breadcrumb')}"><a href="{lang_path(language)}">{('目录' if zh else 'Directory')}</a><span>/</span><a href="{category_path}">{TYPES[entry['content_type']][index]}</a><span>/</span><span aria-current="page">{escape(entry['name'])}</span></nav>
<header class="detail-header"><p class="eyebrow">{TYPES[entry['content_type']][index]} · {('项目档案' if zh else 'PROJECT NOTES')}</p><h1>{escape(entry['name'])}</h1><p class="lead">{escape(entry['description_' + language])}</p><div class="detail-tags">{use_pills(entry, language)}<span class="pill">{escape(platforms)}</span></div></header>
<div class="detail-layout"><div class="detail-content"><section><h2>{('它可以用来做什么？' if zh else 'What can you do with it?')}</h2><p>{escape(entry['enables_' + language])}</p></section><section><h2>{('使用前需要知道什么？' if zh else 'What should you know before using it?')}</h2><p>{escape(entry['limits_' + language])}</p></section><section><h2>{('我们核查了什么？' if zh else 'What is verified here?')}</h2><p>{('本条目依据原始项目材料整理，未独立运行或复现结果。AI 参与开发的描述来自作者说明；上游版本、运行条件和许可应以原始来源为准。' if zh else 'This entry was reviewed against original project material. We have not independently run the software or reproduced its results. AI-development claims are author-reported; check upstream for current versions, setup requirements, and licenses.')}</p><dl class="facts"><dt>{('资源类型' if zh else 'Resource type')}</dt><dd>{KINDS[entry['resource_kind']][index]}</dd><dt>{('开发方式' if zh else 'Provenance')}</dt><dd>{provenance}</dd><dt>{('来源核查' if zh else 'Reviewed')}</dt><dd><time datetime="{entry['reviewed_at']}">{entry['reviewed_at']}</time></dd><dt>{('平台' if zh else 'Platforms')}</dt><dd>{escape(platforms)}</dd></dl></section></div><aside class="source-card"><h2>{('原始链接' if zh else 'Go to the source')}</h2>{source_links}<p class="updated-badge">{('外部链接 · 上游项目负责维护' if zh else 'External links · maintained upstream')}</p></aside></div>
<h2 class="bottom-heading">{('继续浏览同类项目' if zh else 'More in this category')}</h2><div class="related">{related_html}</div>'''
    return body


def about_page(config, language):
    zh = language == 'zh'
    if zh:
        title = '关于目录与收录方法'
        description = '了解 AI Can What 的收录范围、证据标准和作品与环境的区别。'
        content = f'''<h1>好奇心，<br><em>需要证据。</em></h1><p class="lead">AI Can What? 收录 AI 参与开发的软件作品，以及用于 Agent 训练和评测的环境、基准与数据集。</p><h2>两类内容，一个目录</h2><p>Showcase 是有作者说明支持的 AI 构建或 AI 辅助开发作品。Training 与 Evaluation 描述环境的用途，不表示该环境一定由 AI 开发。开发方式与用途分别记录，未知就保持未知。</p><h2>数据集是否等于可运行环境？</h2><p>不是。静态数据集可以提供截图、轨迹或任务样本，通常没有可交互的系统。目录明确标注资源类型；平台标签可能描述应用目标，也可能描述数据集中的截图来源。运行条件应查看条目的具体说明。</p><h2>我们怎样收录？</h2><ol><li>优先查阅作者的项目页、仓库和原始论文。</li><li>说明项目能做什么、支持的平台以及有实际意义的限制。</li><li>只有原始来源明确支持时，才标注 AI-built、AI-assisted 或具体平台。</li><li>记录来源核查日期，并保留代码、论文和演示入口。</li></ol><h2>“来源核查”意味着什么？</h2><p>我们阅读了项目材料，但没有独立安装全部软件、运行所有环境或复现论文结果。目录不提供质量排名。运行条件、许可和安全使用要求以各项目的上游说明为准。</p><h2>这些演示由谁提供？</h2><p>代码、环境与外部演示属于原作者。本目录提供介绍和导航；我们不声称托管所有项目，也不代表项目获得任何机构背书。</p><h2>如何复用、核查和修正？</h2><p>每个项目有独立网址、核查日期和原始来源。完整目录可下载为 <a href="/catalog.json">JSON</a>，网站源码与条目变更在 <a href="{config['repository']}">GitHub</a> 维护。发现错误或想推荐项目，可<a href="{config['repository']}/issues/new?template=resource.yml">提交带来源的建议</a>。</p>'''
    else:
        title = 'About & method'
        description = 'How AI Can What reviews evidence and separates AI-built showcases from agent training and evaluation environments.'
        content = f'''<h1>Curiosity,<br><em>with receipts.</em></h1><p class="lead">AI Can What? collects software made with AI, agent environments, benchmarks, and datasets.</p><h2>Two kinds of entries. One directory.</h2><p>A Showcase documents AI-built or AI-assisted software with an author source. Training and Evaluation describe what an environment is for; they do not imply that AI wrote it. Development provenance and intended use are recorded separately, with unknown facts left unknown.</p><h2>Is a dataset a runnable environment?</h2><p>No. Static datasets can provide screenshots, trajectories, or task examples without an interactive system. Every entry labels its resource type. Platform tags can describe an application target or the source of dataset screenshots; consult the entry for its actual setup.</p><h2>How are entries selected?</h2><ol><li>Start with the author’s project page, repository, or original paper.</li><li>Describe what people can do with the project, its supported platforms, and practical limits.</li><li>Use AI-built, AI-assisted, or platform labels only when the original material supports them.</li><li>Record the source-review date and preserve links to code, papers, and author demos.</li></ol><h2>What does source-reviewed mean?</h2><p>We read the project material. We have not independently installed every application, run every environment, or reproduced paper results. This is a directory, not a quality ranking. Consult upstream documentation for current setup requirements, licenses, and appropriate use.</p><h2>Who provides the demos?</h2><p>Code, environments, and external demos belong to their original creators. This directory provides descriptions and navigation. It does not claim to host every project or imply endorsement by another institution.</p><h2>How can I inspect, reuse, or correct an entry?</h2><p>Every project has its own URL, source-review date, and original evidence. Download the <a href="/catalog.json">JSON catalog</a> or inspect the website source and changes on <a href="{config['repository']}">GitHub</a>. To report an error or suggest a project, <a href="{config['repository']}/issues/new?template=resource.yml">send a source-backed suggestion</a>.</p>'''
    return title, description, '<article class="prose">' + content + '</article>'


def build():
    config, document, entries = read_inputs()
    paper_document, papers = read_papers(ROOT, entries)
    OUT.mkdir(exist_ok=True)
    # This directory is a generated build artifact, owned entirely by this builder.
    for child in OUT.iterdir():
        if child.is_dir(): shutil.rmtree(child)
        else: child.unlink()
    for child in (ROOT / 'static').iterdir():
        if child.is_file(): shutil.copy2(child, OUT / child.name)
    revision = hashlib.sha256((OUT / 'styles.css').read_bytes() + (OUT / 'app.js').read_bytes()).hexdigest()[:12]
    pages = {}
    for language in ('en', 'zh'):
        for category in (None, *TYPES):
            title, description, body, visible = directory(config, entries, language, category)
            if category and not visible:
                continue
            path = '/' if not category else '/' + SLUGS[category] + '/'
            pages[lang_path(language, path)] = page_shell(config, language, path, title, description, body, items=visible, asset_revision=revision)
        for entry in entries:
            path = '/projects/' + entry['id'] + '/'
            pages[lang_path(language, path)] = page_shell(config, language, path, entry['name'], entry['description_' + language], detail_page(config, entry, entries, language), detail=entry, asset_revision=revision)
        title, description, body = about_page(config, language)
        pages[lang_path(language, '/about/')] = page_shell(config, language, '/about/', title, description, body, asset_revision=revision)
        title, description, body = bibliography(papers, entries, language)
        pages[lang_path(language, '/papers/')] = page_shell(config, language, '/papers/', title, description, body, papers=papers, asset_revision=revision)
    for path, html in pages.items():
        destination = OUT / path.lstrip('/') / 'index.html'
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(html, encoding='utf-8')
    origin = config['origin'].rstrip('/')
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += '\n'.join(f'<url><loc>{xml_escape(origin + path)}</loc></url>' for path in pages) + '\n</urlset>\n'
    (OUT / 'sitemap.xml').write_text(sitemap)
    (OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {origin}/sitemap.xml\n')
    (OUT / 'catalog.json').write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n')
    (OUT / 'papers.json').write_text(json.dumps(paper_document, ensure_ascii=False, indent=2) + '\n')
    citations = bibtex(papers)
    (OUT / 'references.bib').write_text(citations, encoding='utf-8')
    (ROOT / 'references.bib').write_text(citations, encoding='utf-8')
    (OUT / 'llms.txt').write_text(f'''# AI Can What?

> A source-backed directory of AI-built software and agent training/evaluation environments.

Showcase entries describe author-reported AI development. Training and Evaluation describe intended uses. Resource kinds distinguish interactive environments, frameworks, benchmark suites, and static datasets. Source-reviewed means original material was read, not independently executed. Unknown development provenance stays unknown.

## Browse
- [Directory]({origin}/)
- [Games]({origin}/games/)
- [Websites]({origin}/websites/)
- [Apps]({origin}/apps/)
- [Review method]({origin}/about/)
- [Original research papers]({origin}/papers/)
- [BibTeX citations]({origin}/references.bib)
- [中文目录]({origin}/zh/)
- [Machine-readable catalog]({origin}/catalog.json)
- [Source repository]({config['repository']})
''')
    (OUT / '404.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="robots" content="noindex"><title>Page not found · AI Can What?</title><body><h1>That page is not in the directory.</h1><p><a href="/">Browse AI Can What?</a></p></body></html>')
    build_catalog_docs(ROOT, config, entries, papers, TYPES, KINDS, PLATFORMS, USES)
    print(json.dumps({'entries': len(entries), 'papers': len(papers), 'pages': len(pages), 'origin': origin, 'output': str(OUT)}))


if __name__ == '__main__':
    build()
