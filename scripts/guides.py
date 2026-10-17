"""Purpose-led guides connecting project evidence to concrete selection decisions."""
from datetime import date
from html import escape
import json
import re
from urllib.parse import urlsplit


def guide_project_ids(guide):
    return [choice['project_id'] for group in guide['groups'] for choice in group['choices']]


def read_guides(root, entries):
    document = json.loads((root / 'data/guides.json').read_text())
    assert document['schema_version'] == 1
    guides = document['guides']
    known = {entry['id']: entry for entry in entries}
    assert guides and len({guide['id'] for guide in guides}) == len(guides), 'Duplicate guide IDs'
    for guide in guides:
        identifier = guide['id']
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', identifier), identifier
        assert date.fromisoformat(guide['reviewed_at']) <= date.today(), identifier
        for language in ('en', 'zh'):
            for field in ('title', 'label', 'description', 'answer'):
                assert isinstance(guide[field + '_' + language], str) and guide[field + '_' + language].strip(), (identifier, field)
        ids = guide_project_ids(guide)
        assert len(ids) == len(set(ids)) and set(ids) <= known.keys(), (identifier, 'Missing or repeated project')
        assert guide['groups'] and guide['questions'], identifier
        assert len({group['id'] for group in guide['groups']}) == len(guide['groups']), identifier
        for group in guide['groups']:
            assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', group['id']) and group['choices'], identifier
            for language in ('en', 'zh'):
                assert group['title_' + language].strip() and group['intro_' + language].strip(), identifier
                assert all(choice['fit_' + language].strip() for choice in group['choices']), identifier
        for question in guide['questions']:
            for language in ('en', 'zh'):
                assert question['question_' + language].strip() and question['answer_' + language].strip(), identifier
        for link in guide['browse']:
            parsed = urlsplit(link['path'])
            assert link['path'].startswith('/') and not parsed.scheme and not parsed.netloc, identifier
            assert link['label_en'].strip() and link['label_zh'].strip(), identifier
        if identifier == 'ai-built-software':
            assert all(known[key]['resource_kind'] == 'ai-generated-output' and known[key].get('provenance_source') for key in ids), identifier
        else:
            assert all('evaluation' in known[key]['uses'] or known[key]['resource_kind'] == 'environment-framework' for key in ids), identifier
    return document, guides


def guide_cards(guides, language):
    prefix = '/zh' if language == 'zh' else ''
    return '<div class="guide-grid">' + ''.join(
        f'<article class="guide-card" data-guide="{guide["id"]}"><h2><a href="{prefix}/guides/{guide["id"]}/">{escape(guide["label_" + language])} <span aria-hidden="true">↗</span></a></h2><p>{escape(guide["description_" + language])}</p></article>'
        for guide in guides) + '</div>'


def guide_shortcuts(guides, language):
    if not guides:
        return ''
    zh = language == 'zh'
    prefix = '/zh' if zh else ''
    links = ''.join(f'<a href="{prefix}/guides/{guide["id"]}/">{escape(guide["label_" + language])} ↗</a>' for guide in guides)
    return f'<nav class="guide-shortcuts" aria-label="{("按目标查找" if zh else "Browse by goal")}"><a class="guide-shortcuts-title" href="{prefix}/guides/">{("按目标查找" if zh else "Start with a goal")}</a>{links}</nav>'


def guides_index(guides, language):
    zh = language == 'zh'
    title = '按目标选择资料' if zh else 'Choose resources for your goal'
    description = ('从具体用途出发，区分软件作品、可交互环境、静态数据和生成评测。' if zh else
                   'Start with your use case, then distinguish software examples, interactive environments, static data and generation benchmarks.')
    intro = ('这些指南解释不同资料能回答什么问题、如何比较，以及使用前需要检查什么。它们是目录中的选择路径，不是质量排名或完整运行认证。' if zh else
             'These guides explain which questions different resources answer, how to compare them and what to check before using them. They are routes through the catalog, not rankings or certification of complete runtime behavior.')
    body = f'<section class="guide-index"><p class="eyebrow">{("用途、证据与选择" if zh else "PURPOSE, EVIDENCE & CHOICE")}</p><h1>{title}</h1><p class="lead">{description}</p><p class="guide-intro">{intro}</p>{guide_cards(guides, language)}</section>'
    items = [{'name': guide['label_' + language], 'url': ('/zh' if zh else '') + '/guides/' + guide['id'] + '/'} for guide in guides]
    return title, description, body, items


def guide_page(guide, entries, language, kinds):
    zh = language == 'zh'
    prefix = '/zh' if zh else ''
    by_id = {entry['id']: entry for entry in entries}
    sections = []
    for group in guide['groups']:
        rows = []
        for choice in group['choices']:
            entry = by_id[choice['project_id']]
            rows.append(f'''<tr data-project="{entry['id']}"><th scope="row"><a href="{prefix}/projects/{entry['id']}/">{escape(entry['name'])}</a><span class="guide-kind">{kinds[entry['resource_kind']][int(zh)]}</span><a class="guide-source" href="{escape(entry['primary_url'], quote=True)}">{("原始来源" if zh else "Original source")} ↗</a></th><td data-label="{("适合研究的问题" if zh else "Use it to study")}">{escape(choice['fit_' + language])}</td><td data-label="{("配置与限制" if zh else "Setup and limits")}">{escape(entry['limits_' + language])}</td></tr>''')
        sections.append(f'''<section class="guide-section" id="{group['id']}"><h2>{escape(group['title_' + language])}</h2><p class="guide-intro">{escape(group['intro_' + language])}</p><div class="guide-table-wrap"><table class="guide-table"><caption class="visually-hidden">{escape(group['title_' + language])}</caption><thead><tr><th>{("项目与证据" if zh else "Project and evidence")}</th><th>{("适合研究的问题" if zh else "Use it to study")}</th><th>{("配置与限制" if zh else "Setup and limits")}</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>''')
    questions = ''.join(f'<section><h3>{escape(q["question_" + language])}</h3><p>{escape(q["answer_" + language])}</p></section>' for q in guide['questions'])
    toc = ''.join(f'<a href="#{group["id"]}">{escape(group["title_" + language])}</a>' for group in guide['groups'])
    note = ('基于目录中的原始来源整理，使用 AI 辅助研究与写作。分组体现用途差异，不表示排名。项目详情保留作者证据和已知限制；实验、平台支持和许可应以对应版本为准。' if zh else
            'Compiled from the catalog’s primary sources with AI-assisted research and writing. Groups describe different uses, not rankings. Project notes retain author evidence and known limits; experiments, platform support and licenses depend on the specific version.')
    browse = '<nav class="guide-toc" aria-label="' + ('继续查找' if zh else 'Continue exploring') + '">' + ''.join('<a href="' + escape(prefix + link['path'], quote=True) + '">' + escape(link['label_' + language]) + ' ↗</a>' for link in guide['browse']) + '</nav>'
    body = f'''<article class="guide-main"><nav class="breadcrumb" aria-label="{("当前位置" if zh else "Breadcrumb")}"><a href="{prefix}/guides/">{("选择指南" if zh else "Selection guides")}</a><span>/</span><span>{escape(guide['label_' + language])}</span></nav><header class="guide-header"><p class="eyebrow">{("用途与选择指南" if zh else "RESOURCE SELECTION GUIDE")}</p><h1>{escape(guide['title_' + language])}</h1><p class="lead">{escape(guide['description_' + language])}</p><p class="guide-date">{("资料核查" if zh else "Sources reviewed")} · <time datetime="{guide['reviewed_at']}">{guide['reviewed_at']}</time></p><p class="guide-answer">{escape(guide['answer_' + language])}</p></header><nav class="guide-toc" aria-label="{("本文导航" if zh else "On this page")}">{toc}<a href="#selection-questions">{("选择时的常见问题" if zh else "Selection questions")}</a></nav>{''.join(sections)}<section class="guide-questions" id="selection-questions"><h2>{("选择时的常见问题" if zh else "Selection questions")}</h2>{questions}</section><aside class="guide-method"><h2>{("来源与方法" if zh else "Sources and method")}</h2><p>{note}</p><p><a href="{prefix}/about/">{("收录方法" if zh else "Review method")}</a> · <a href="/guides.json">{("下载指南数据" if zh else "Download guide data")}</a> · <a href="{prefix}/">{("浏览完整目录" if zh else "Browse the full catalog")}</a></p></aside></article>'''
    body = body.replace('<aside class="guide-method">', browse + '<aside class="guide-method">')
    return guide['title_' + language], guide['description_' + language], body, [by_id[key] for key in guide_project_ids(guide)]


def guide_markdown(guide, entries, language, origin):
    zh = language == 'zh'
    prefix = '/zh' if zh else ''
    by_id = {entry['id']: entry for entry in entries}
    def md(value):
        return value.replace('|', '&#124;').replace('[', '&#91;').replace(']', '&#93;')
    lines = ['# ' + guide['title_' + language], '', f'[{("网站版本" if zh else "Website version")}]({origin}{prefix}/guides/{guide["id"]}/) · {guide["reviewed_at"]}', '', guide['description_' + language], '', guide['answer_' + language], '']
    for group in guide['groups']:
        lines += ['## ' + group['title_' + language], '', group['intro_' + language], '',
                  '| 项目与证据 | 适合研究的问题 | 配置与限制 |' if zh else '| Project and evidence | Use it to study | Setup and limits |', '| --- | --- | --- |']
        for choice in group['choices']:
            entry = by_id[choice['project_id']]
            lines.append(f'| [{md(entry["name"])}]({origin}{prefix}/projects/{entry["id"]}/) · [Source]({entry["primary_url"]}) | {md(choice["fit_" + language])} | {md(entry["limits_" + language])} |')
        lines.append('')
    lines += ['## ' + ('选择时的常见问题' if zh else 'Selection questions'), '']
    for question in guide['questions']:
        lines += ['### ' + question['question_' + language], '', question['answer_' + language], '']
    lines += ['## ' + ('继续查找' if zh else 'Continue exploring'), '']
    lines += ['- [' + link['label_' + language] + '](' + origin + prefix + link['path'] + ')' for link in guide['browse']]
    lines.append('')
    lines += [('本指南基于目录原始来源，使用 AI 辅助研究与写作。分组不是排名；未独立复现实验或验证所有运行功能。' if zh else 'Compiled from catalog primary sources with AI-assisted research and writing. Groups are not rankings; experiments and complete runtime behavior have not been independently verified.'), '', f'[{("收录方法" if zh else "Review method")}]({origin}{prefix}/about/)', '']
    return '\n'.join(lines)


def build_guide_docs(root, guides, entries, origin):
    folder = root / 'guides'
    folder.mkdir(exist_ok=True)
    for language in ('en', 'zh'):
        zh = language == 'zh'
        filename = 'README.zh-CN.md' if zh else 'README.md'
        lines = ['# ' + ('按目标选择资料' if zh else 'Choose resources for your goal'), '',
                 ('从用途、交互方式和证据边界选择资料；下列分组不代表质量排名。' if zh else 'Choose by purpose, interaction setting and evidence boundaries. These guides are not quality rankings.'), '']
        for guide in guides:
            target = folder / guide['id']
            target.mkdir(exist_ok=True)
            (target / filename).write_text(guide_markdown(guide, entries, language, origin), encoding='utf-8')
            lines += [f'- [{guide["label_" + language]}]({guide["id"]}/{filename}): {guide["description_" + language]}']
        lines += ['', '[Source data](../data/guides.json) · [Full catalog](../' + filename + ')', '']
        (folder / filename).write_text('\n'.join(lines), encoding='utf-8')
