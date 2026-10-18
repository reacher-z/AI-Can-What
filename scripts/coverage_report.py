"""Explain catalog coverage with explicit counting units and source boundaries."""
from collections import Counter
from datetime import datetime, timezone
from html import escape
import json

from guides import guide_project_ids
from registries import related_projects


def coverage_data(entries, papers, observations, guides, sources, registry_document):
    apps = [e for e in entries if e['content_type'] == 'app']
    observed = {o['project_id'] for o in observations}
    linked = {identifier for p in papers for identifier in p['project_ids']}
    guide_ids = [identifier for g in guides for identifier in guide_project_ids(g)]
    records = registry_document['records']
    snapshots = {s['source_id']: s for s in registry_document['snapshots']}
    relations = {r['id']: related_projects(r, entries) for r in records}
    kinds = sorted({e['resource_kind'] for e in entries})
    categories = sorted({e['content_type'] for e in entries})
    return {
        'schema_version': 1,
        'counting_units': {
            'catalog': 'Entries, not independent project families or unique benchmark tasks.',
            'uses': 'Overlapping entry tags; counts are not additive.',
            'platforms': 'Overlapping tags on app entries, not verified installations or host compatibility.',
            'papers': 'Research records; linked papers and project entries overlap.',
            'development_provenance': 'Author-attributed development labels across all entries, not the number of software showcases.',
            'observations': 'Scoped interaction records; distinct entries are counted separately.',
            'registries': 'Frozen upstream metadata records; not individually reviewed catalog entries.',
        },
        'review_dates': {'earliest': min(e['reviewed_at'] for e in entries),
                         'latest': max(e['reviewed_at'] for e in entries)},
        'catalog': {
            'entries': len(entries),
            'by_category': dict(sorted(Counter(e['content_type'] for e in entries).items())),
            'by_resource_kind': dict(sorted(Counter(e['resource_kind'] for e in entries).items())),
            'resource_kind_by_category': {kind: {category: sum(e['resource_kind'] == kind and e['content_type'] == category for e in entries)
                                                 for category in categories} for kind in kinds},
            'by_use': dict(sorted(Counter(use for e in entries for use in e['uses']).items())),
            'by_development_provenance': dict(sorted(Counter(e['implementation'] for e in entries).items())),
        },
        'app_platforms': {
            'app_entries': len(apps),
            'with_any_platform_tag': sum(bool(e['platforms']) for e in apps),
            'without_platform_tag': sum(not e['platforms'] for e in apps),
            'by_platform': {platform: {
                'entries': sum(platform in e['platforms'] for e in apps),
                'software_showcases': sum(platform in e['platforms'] and e['resource_kind'] == 'ai-generated-output' for e in apps),
                'other_resources': sum(platform in e['platforms'] and e['resource_kind'] != 'ai-generated-output' for e in apps),
            } for platform in sorted({platform for e in apps for platform in e['platforms']})},
        },
        'research': {
            'papers': len(papers),
            'linked_papers': sum(bool(p['project_ids']) for p in papers),
            'paper_only_records': sum(not p['project_ids'] for p in papers),
            'catalog_associations': sum(len(p['project_ids']) for p in papers),
            'distinct_catalog_entries_linked': len(linked),
        },
        'observations': {'records': len(observations), 'distinct_catalog_entries': len(observed),
                         'entries_without_observation_records': len(entries) - len(observed),
                         'earliest_date': min((o['observed_on'] for o in observations), default=None),
                         'latest_date': max((o['observed_on'] for o in observations), default=None)},
        'guides': {'guides': len(guides), 'project_associations': len(guide_ids),
                   'distinct_catalog_entries': len(set(guide_ids))},
        'upstream_registries': {
            'records': len(records), 'source_count': len(sources),
            'records_with_related_catalog_notes': sum(bool(relations[r['id']]) for r in records),
            'sources': [{
                'id': source['id'], 'name': source['name'], 'url': source['browse_url'],
                'records': sum(r['source_id'] == source['id'] for r in records),
                'records_with_related_catalog_notes': sum(r['source_id'] == source['id'] and bool(relations[r['id']]) for r in records),
                'captured_at': snapshots[source['id']]['captured_at'],
            } for source in sources],
        },
        'source_files': ['data/catalog.json', 'data/papers.json', 'data/observations.json',
                         'data/guides.json', 'data/registry-index.json', 'data/registry-sources.json'],
    }


def coverage_sections(report, language, types, kinds, platforms, uses):
    zh = language == 'zh'
    i = int(zh)
    prefix = '/zh' if zh else ''
    catalog = report['catalog']
    slugs = {'game': 'games', 'website': 'websites', 'app': 'apps'}
    kinds_rows = []
    for kind, labels in kinds.items():
        counts = catalog['resource_kind_by_category'].get(kind, {})
        cells = [labels[i]]
        for category in types:
            number = counts.get(category, 0)
            cells.append((number, prefix + '/' + slugs[category] + '/?kind=' + kind) if number else 0)
        cells.append((catalog['by_resource_kind'].get(kind, 0), prefix + '/?kind=' + kind))
        kinds_rows.append(cells)
    kinds_rows.append([('全部条目' if zh else 'All entries'),
                       *[catalog['by_category'].get(category, 0) for category in types], catalog['entries']])
    platform_rows = []
    for key, label in platforms.items():
        row = report['app_platforms']['by_platform'].get(key)
        if row:
            url = prefix + '/apps/' + key + '/'
            platform_rows.append([(label, url), row['entries'],
                                  (row['software_showcases'], url + '?use=showcase'), row['other_resources']])
    research = report['research']
    observations = report['observations']
    guides = report['guides']
    def captured_utc(value):
        timestamp = datetime.fromisoformat(value)
        assert timestamp.tzinfo is not None, 'Capture timestamps must include a timezone'
        return timestamp.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    return [
        {'id': 'resource-types', 'title': '分类与资源类型' if zh else 'Categories and resource types',
         'note': '每条目录记录恰属一个分类和一种资源类型；本表可按行或列求和。条目数不等于独立任务族数。' if zh else
                 'Each entry has one category and one resource type, so rows and columns add up here. Entry counts are not counts of independent task families.',
         'headers': [('资源类型' if zh else 'Resource type'), *[label[i] for label in types.values()], ('合计' if zh else 'Total')], 'rows': kinds_rows},
        {'id': 'uses', 'title': '用途标签' if zh else 'Use tags',
         'note': '同一条目可同时支持训练与评测，因此下列数量不能相加。作品展示不等于环境用途。' if zh else
                 'An entry can support both training and evaluation, so these counts are not additive. Showcase and environment use describe different things.',
         'headers': ['用途' if zh else 'Use', '条目数' if zh else 'Entries'],
         'rows': [[(labels[i], prefix + '/?use=' + key), catalog['by_use'].get(key, 0)] for key, labels in uses.items()]},
        {'id': 'platforms', 'title': '应用资源的平台覆盖' if zh else 'Platform tags on app resources',
         'note': (f"本表仅覆盖 {report['app_platforms']['app_entries']} 条应用资源。同一条目可有多个平台，平台行不能相加；标签可指应用目标或数据截图来源。{report['app_platforms']['without_platform_tag']} 条未指定平台，这不等于不支持任何平台。" if zh else
                  f"This table covers only {report['app_platforms']['app_entries']} app entries. Platform tags overlap and can name application targets or screenshot sources; do not sum the rows. {report['app_platforms']['without_platform_tag']} entries have no assigned platform, which does not mean no platform is supported."),
         'headers': ['平台' if zh else 'Platform', '条目数' if zh else 'Entries', 'AI 软件作品' if zh else 'AI software showcases', '其他资源' if zh else 'Other resources'],
         'rows': platform_rows},
        {'id': 'evidence', 'title': '文献、指南与操作证据' if zh else 'Research, guides and interaction evidence',
         'note': '一篇论文可关联多个条目，一个条目也可有多篇论文或操作记录。操作记录仅证明其列出的步骤，不代表完整应用验证。未附记录不等于没有公开演示。' if zh else
                 'Papers and entries can have many-to-many relationships; an entry can also have several observation records. Observations cover their stated steps, not whole applications. No observation record does not mean no public demo.',
         'headers': ['统计项' if zh else 'Measure', '数量' if zh else 'Count', '单位' if zh else 'Unit'],
         'rows': [[('文献' if zh else 'Research papers', prefix + '/papers/'), research['papers'], '文献记录' if zh else 'Paper records'],
                  [('有目录关联的文献' if zh else 'Papers with catalog links', prefix + '/papers/?status=linked-project'), research['linked_papers'], '文献记录' if zh else 'Paper records'],
                  [('尚无产物条目的文献' if zh else 'Papers without artifact entries', prefix + '/papers/?status=paper-only'), research['paper_only_records'], '文献记录' if zh else 'Paper records'],
                  ['被文献关联的条目' if zh else 'Entries linked from papers', research['distinct_catalog_entries_linked'], '不同目录条目' if zh else 'Distinct catalog entries'],
                  ['论文与条目关联' if zh else 'Paper-to-entry associations', research['catalog_associations'], '关联次数' if zh else 'Associations'],
                  [('限定范围的操作记录' if zh else 'Scoped browser observations', '/observations.json'), observations['records'], '操作记录' if zh else 'Observation records'],
                  ['有操作记录的条目' if zh else 'Entries with observations', observations['distinct_catalog_entries'], '不同目录条目' if zh else 'Distinct catalog entries'],
                  ['未附操作记录的条目' if zh else 'Entries without observations', observations['entries_without_observation_records'], '不同目录条目' if zh else 'Distinct catalog entries'],
                  [('选择指南' if zh else 'Selection guides', prefix + '/guides/'), guides['guides'], '指南' if zh else 'Guides'],
                  ['指南中的项目关联' if zh else 'Guide project associations', guides['project_associations'], '关联次数' if zh else 'Associations'],
                  ['指南涉及的条目' if zh else 'Entries covered by guides', guides['distinct_catalog_entries'], '不同目录条目' if zh else 'Distinct catalog entries']]},
        {'id': 'registries', 'title': '上游快照覆盖' if zh else 'Upstream snapshot coverage',
         'note': '这些是上游元数据，可能含版本、分支、封装及非目标资料；不能与已核查目录数量相加。有相关说明也不表示任务内容、评分或运行方式完全等价。日期是采集时间，不是本次构建时间。' if zh else
                 'These metadata records can include versions, forks, wrappers and out-of-scope material; do not add them to the reviewed catalog. Related notes do not establish equivalent tasks, scores or runtime. Dates identify capture time, not this build.',
         'headers': ['来源' if zh else 'Source', '记录数' if zh else 'Records', '关联目录说明' if zh else 'With related notes', '采集时间（UTC）' if zh else 'Captured (UTC)'],
         'rows': [[(s['name'], prefix + '/discover/?source=' + s['id']), s['records'], s['records_with_related_catalog_notes'], captured_utc(s['captured_at'])]
                  for s in report['upstream_registries']['sources']]},
    ]


def coverage_page(report, language, types, kinds, platforms, uses, repository):
    zh = language == 'zh'
    title = '目录覆盖与证据' if zh else 'Catalog coverage and evidence'
    description = (f"{report['catalog']['entries']} 条目录记录的分类、平台和证据覆盖，另列论文与上游元数据的计数口径。" if zh else
                   f"Category, platform and evidence coverage for {report['catalog']['entries']} catalog entries, with separate counting units for papers and upstream metadata.")
    intro = ('以下数字由同一份目录数据生成，不代表全网覆盖率、质量排名或运行成功率。范围不同的数量不能直接相加。' if zh else
             'These counts come from the same catalog data. They do not measure coverage of the whole web, quality rankings or runtime success. Different units must not be added together.')
    filename = 'README.zh-CN.md' if zh else 'README.md'
    body = f'<article class="coverage-main"><p class="eyebrow">{("范围、单位与证据" if zh else "SCOPE, UNITS & EVIDENCE")}</p><h1>{title}</h1><p class="lead">{description}</p><p>{intro}</p><p class="coverage-dates">{("条目来源核查日期" if zh else "Entry source-review dates")}: {report["review_dates"]["earliest"]} – {report["review_dates"]["latest"]}</p><div class="coverage-actions"><a href="/coverage.json">{("下载统计 JSON" if zh else "Download coverage JSON")} ↓</a><a href="{repository}/blob/main/catalog/coverage/{filename}">{("GitHub 覆盖说明" if zh else "Coverage on GitHub")} ↗</a></div>'
    def cell(value):
        if isinstance(value, tuple):
            return f'<a href="{escape(value[1], quote=True)}">{escape(str(value[0]))}</a>'
        return escape(str(value))
    for section in coverage_sections(report, language, types, kinds, platforms, uses):
        rows = ''.join('<tr>' + ''.join(('<th scope="row">' if i == 0 else '<td>') + cell(v) + ('</th>' if i == 0 else '</td>') for i, v in enumerate(row)) + '</tr>' for row in section['rows'])
        headers = ''.join('<th scope="col">' + escape(h) + '</th>' for h in section['headers'])
        body += f'<section id="{section["id"]}"><h2>{section["title"]}</h2><p>{section["note"]}</p><div class="coverage-table-wrap" tabindex="0" role="region" aria-label="{section["title"]}"><table><caption class="visually-hidden">{section["title"]}</caption><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table></div></section>'
    body += '<p class="coverage-method"><a href="' + ('/zh/about/' if zh else '/about/') + '">' + ('阅读收录方法' if zh else 'Read the review method') + '</a> · <a href="' + repository + '/blob/main/docs/coverage.md">' + ('已知缺口与收录边界' if zh else 'Known gaps and inclusion boundaries') + '</a></p></article>'
    return title, description, body


def build_coverage_docs(root, report, origin, types, kinds, platforms, uses):
    folder = root / 'catalog/coverage'
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'coverage.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    for language in ('en', 'zh'):
        zh = language == 'zh'
        prefix = '/zh' if zh else ''
        filename = 'README.zh-CN.md' if zh else 'README.md'
        lines = ['# ' + ('目录覆盖与证据' if zh else 'Catalog coverage and evidence'), '',
                 f'[{("网页统计" if zh else "Website coverage")}]({origin}{prefix}/coverage/) · [JSON](coverage.json) · [{("收录边界" if zh else "Inclusion boundaries")}](../../docs/coverage.md)', '',
                 ('不同单位的数量不能相加。这是目录的覆盖说明，不代表全网完整性、质量排名或运行成功率。' if zh else
                  'Counts with different units are not additive. This describes catalog coverage, not completeness of the web, quality rankings or runtime success.'), '',
                 ('条目来源核查日期：' if zh else 'Entry source-review dates: ') + report['review_dates']['earliest'] + ' – ' + report['review_dates']['latest'], '']
        def cell(value):
            if isinstance(value, tuple):
                return f'[{value[0]}]({origin + value[1]})'
            return str(value).replace('|', '&#124;')
        for section in coverage_sections(report, language, types, kinds, platforms, uses):
            lines.extend(['## ' + section['title'], '', section['note'], '', '| ' + ' | '.join(section['headers']) + ' |',
                          '| ' + ' | '.join('---' for _ in section['headers']) + ' |'])
            lines.extend('| ' + ' | '.join(cell(v) for v in row) + ' |' for row in section['rows'])
            lines.append('')
        lines.extend([('生成来源：' if zh else 'Generated from: ') + ', '.join(f'[`{path}`](../../{path})' for path in report['source_files']), ''])
        (folder / filename).write_text('\n'.join(lines), encoding='utf-8')
