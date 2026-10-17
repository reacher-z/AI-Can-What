"""Validate and render a separately attributed index of upstream registry records."""
from collections import Counter
from datetime import datetime
from html import escape
import json
import re
from urllib.parse import urlsplit

KINDS = {
    'dataset-package': ('Dataset package', '数据集包'),
    'environment-manifest': ('Environment manifest', '环境清单'),
    'benchmark-configuration': ('Benchmark configuration', '基准配置'),
    'foundation-project': ('Foundation project', '基金会项目'),
    'coding-example-manifest': ('Coding example manifest', '编程示例清单'),
}

HARBOR_RELATED = {
    'swe-bench/swe-bench-verified': 'swe-bench',
    'meta/mlgym-bench': 'mlgym',
    'gaia/gaia': 'gaia',
    'theagentcompany/theagentcompany': 'the-agent-company',
    'sierra-research/tau3-bench': 'tau-bench',
    'xlang-ai/osworld-verified': 'osworld',
    'terminal-bench/terminal-bench': 'terminal-bench',
    'terminal-bench/terminal-bench-2': 'terminal-bench',
    'terminal-bench/terminal-bench-2-1': 'terminal-bench',
    'terminal-bench/terminal-bench-cpu-only': 'terminal-bench',
}
OPENENV_RELATED = {'atari_env': 'arcade-learning-environment', 'browsergym_env': 'browsergym',
                   'harbor_env': 'harbor', 'openspiel_env': 'open-spiel', 'tau2_env': 'tau-bench', 'tbench2_env': 'terminal-bench',
                   'openapp_env': 'openapps'}


def validate_url(value):
    if not isinstance(value, str):
        raise ValueError('Registry URL must be text')
    parsed = urlsplit(value)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or any(c.isspace() for c in value):
        raise ValueError('Invalid public registry URL')


def identity(url):
    """Match exact artifact paths across main/master/pinned refs, never arbitrary repo descendants."""
    parsed = urlsplit(url)
    path = parsed.path.rstrip('/')
    if parsed.netloc.casefold() == 'github.com':
        parts = path.lstrip('/').split('/')
        if len(parts) >= 4 and parts[2] in {'tree', 'blob'} and (parts[3] in {'main', 'master'} or re.fullmatch('[a-f0-9]{40}', parts[3])):
            parts = parts[:2] + parts[4:]
        if parts and parts[-1] == 'index.html': parts.pop()
        # GitHub owners/repositories are case-insensitive; artifact paths are not.
        if len(parts) >= 2:
            parts = [parts[0].casefold(), parts[1].removesuffix('.git').casefold(), *parts[2:]]
        return 'github.com/' + '/'.join(parts)
    return parsed.netloc.casefold() + path + ('?' + parsed.query if parsed.query else '')


def related_projects(record, entries):
    urls = [record['url'], record['attributes'].get('repository_url')]
    identities = {identity(url) for url in urls if url}
    matches = {entry['id'] for entry in entries if any(identity(entry[key]) in identities for key in ('primary_url', 'repo_url') if entry.get(key))}
    key, source = record['source_key'], record['source_id']
    if source == 'harbor-hub' and key in HARBOR_RELATED:
        matches.add(HARBOR_RELATED[key])
    if source == 'openenv' and key in OPENENV_RELATED:
        matches.add(OPENENV_RELATED[key])
    if source == 'browsergym':
        for prefix, identifier in [('miniwob', 'miniwob-plusplus'), ('visualwebarena', 'visualwebarena'),
                                   ('webarena', 'webarena'), ('workarena', 'workarena'),
                                   ('assistantbench', 'assistantbench'), ('weblinx', 'weblinx'),
                                   ('knows', 'knows'), ('timewarp', 'timewarp')]:
            if key == prefix or key.startswith(prefix + '_'):
                matches.add(identifier)
    return [entry for entry in entries if entry['id'] in matches]


def read_registries(root):
    source_doc = json.loads((root / 'data/registry-sources.json').read_text())
    document = json.loads((root / 'data/registry-index.json').read_text())
    if source_doc.get('schema_version') != 1 or document.get('schema_version') != 1 or document.get('verification') != 'upstream-metadata-only':
        raise ValueError('Unsupported registry metadata schema')
    sources, records, snapshots = source_doc['sources'], document['records'], document['snapshots']
    source_ids = {source['id'] for source in sources}
    if len(source_ids) != len(sources) or {s['source_id'] for s in snapshots} != source_ids:
        raise ValueError('Registry sources and snapshots do not match')
    if len({r['id'] for r in records}) != len(records) or len({(r['source_id'], r['source_key']) for r in records}) != len(records):
        raise ValueError('Duplicate registry records')
    for source in sources:
        if not re.fullmatch('[a-z][a-z0-9-]*', source['id']): raise ValueError('Invalid registry source ID')
        validate_url(source['browse_url'])
        for key in ('name', 'note_en', 'note_zh', 'rights_en', 'rights_zh'):
            if not isinstance(source.get(key), str) or not source[key].strip(): raise ValueError('Incomplete source explanation')
    for row in records:
        if not re.fullmatch('[a-z][a-z0-9-]*-[a-f0-9]{16}', row['id']): raise ValueError('Invalid registry record ID')
        if row['source_id'] not in source_ids or row['kind'] not in KINDS or not isinstance(row['attributes'], dict):
            raise ValueError('Invalid registry record type')
        for key in ('id', 'name', 'source_key'):
            if not isinstance(row.get(key), str) or not row[key].strip() or any(ord(c) < 32 for c in row[key]): raise ValueError('Invalid registry identifier')
        validate_url(row['url'])
        for key in ('repository_url', 'manifest_url'):
            if row['attributes'].get(key): validate_url(row['attributes'][key])
        if row['source_id'] == 'harbor-hub':
            a = row['attributes']
            if a.get('version_status') not in {'available', 'unavailable'}: raise ValueError('Missing Harbor version status')
            if a['version_status'] == 'available':
                if type(a.get('task_count')) is not int or a['task_count'] < 0 or type(a.get('revision')) is not int or a['revision'] < 1:
                    raise ValueError('Invalid Harbor task count or revision')
                if not re.fullmatch('[a-f0-9]{64}', a.get('content_hash', '')): raise ValueError('Missing Harbor content hash')
            elif any(key in a for key in ('task_count', 'content_hash', 'revision')):
                raise ValueError('Unavailable version must not have invented metadata')
    counts = Counter(r['source_id'] for r in records)
    for snapshot in snapshots:
        if snapshot['record_count'] != counts[snapshot['source_id']]: raise ValueError('Snapshot count mismatch')
        datetime.fromisoformat(snapshot['captured_at'])
        for request in snapshot['requests']:
            validate_url(request.get('url') or request['request_url'])
            if not re.fullmatch('[a-f0-9]{64}', request.get('sha256', '')): raise ValueError('Missing source response digest')
        if snapshot['source_id'] == 'harbor-hub':
            missing = [r['attributes']['package_id'] for r in records if r['source_id'] == 'harbor-hub' and r['attributes']['version_status'] == 'unavailable']
            if snapshot['public_package_total'] != counts['harbor-hub'] or set(snapshot['missing_version_package_ids']) != set(missing) or snapshot['missing_version_count'] != len(missing):
                raise ValueError('Harbor missing-version coverage mismatch')
    return source_doc, document, sources, records


def registry_page(sources, document, records, entries, language):
    zh = language == 'zh'
    prefix = '/zh' if zh else ''
    idx = int(zh)
    by_source = {s['id']: s for s in sources}
    snapshots = {s['source_id']: s for s in document['snapshots']}
    title = '上游注册表索引' if zh else 'Upstream registry index'
    description = (f'{len(records)} 条来自 {len(sources)} 个上游来源的环境、数据集包与编程示例记录，保留版本、来源快照和相关项目说明。'
                   if zh else f'{len(records)} upstream records across {len(sources)} sources: environment manifests, dataset packages, configurations and coding examples, with snapshot and version metadata.')
    source_cards = []
    for source in sources:
        snapshot = snapshots[source['id']]
        source_cards.append(f'<article class="registry-source"><a href="?source={source["id"]}#registry-results"><strong>{snapshot["record_count"]}</strong><span>{escape(source["name"])}</span></a><p>{escape(KINDS[source["kind"]][idx])}</p></article>')
    rows, items = [], []
    related_count = 0
    for row in sorted(records, key=lambda r: (r['name'].casefold(), r['source_id'])):
        source, a = by_source[row['source_id']], row['attributes']
        related = related_projects(row, entries)
        if related: related_count += 1
        notes = ' · '.join(f'<a href="{prefix}/projects/{e["id"]}/">{escape(e["name"])}</a>' for e in related) or ('暂无关联说明' if zh else 'No related notes yet')
        status = a.get('version_status', 'not-applicable')
        details = ''
        if row['source_id'] == 'harbor-hub':
            if status == 'available':
                details = (f'观察版本 r{a["revision"]} · {a["task_count"]:,} 项注册任务' if zh else f'Observed r{a["revision"]} · {a["task_count"]:,} registered tasks')
                if a.get('yanked_at'): details += (' · 上游已撤回' if zh else ' · Withdrawn upstream')
            else:
                details = '缺少可见的 latest 版本资料' if zh else 'No visible latest-version metadata'
        elif row['source_id'] == 'farama':
            details = ('上游分类：' if zh else 'Upstream category: ') + escape(a['upstream_category'])
        elif row['source_id'] == 'browsergym':
            details = ('配置键：' if zh else 'Configuration: ') + escape(row['source_key'])
        elif row['source_id'] == 'openai-examples':
            details = ('有匹配的应用源码' if zh else 'Matching application source present') if a['matching_application_source'] else ('未匹配到应用源码' if zh else 'No matching application source found')
        else:
            details = escape(a['manifest_path'])
        if a.get('manifest_url'):
            details += f'<br><a href="{escape(a["manifest_url"], quote=True)}">{("查看清单" if zh else "View manifest")} ↗</a>'
        date = snapshots[row['source_id']]['captured_at'][:10]
        searchable = ' '.join([row['name'], source['name'], *KINDS[row['kind']], row['source_key'], *[e['name'] for e in related]]).casefold()
        permalink = prefix + '/discover/#' + row['id']
        rows.append(f'''<tr id="{row['id']}" data-registry="{row['id']}" data-source="{source['id']}" data-version-status="{status}" data-notes="{('yes' if related else 'no')}" data-search="{escape(searchable, quote=True)}">
<td class="project-cell"><a class="project-name" href="{escape(row['url'], quote=True)}">{escape(row['name'])}<span class="arrow" aria-hidden="true">↗</span></a><a class="registry-permalink" href="{permalink}" aria-label="{('本条记录链接' if zh else 'Link to this record')}">#</a><span class="project-kind">{KINDS[row['kind']][idx]}</span><p class="registry-related">{notes}</p></td>
<td class="registry-metadata">{details}</td><td class="evidence-cell"><a class="evidence-link" href="{escape(source['browse_url'], quote=True)}">{escape(source['name'])} ↗</a><time class="review-date" datetime="{date}">{('采集' if zh else 'Captured')} {date}</time></td></tr>''')
        items.append({'id': row['id'], 'name': row['name'], 'url': permalink})
    source_options = ''.join(f'<option value="{s["id"]}">{escape(s["name"])}</option>' for s in sources)
    boundaries = []
    for source in sources:
        snapshot = snapshots[source['id']]
        extra = ''
        if source['id'] == 'harbor-hub':
            extra = (f'本次采集 {snapshot["public_package_total"]} 个公开包、{snapshot["latest_tag_rows"]} 条 latest 标签记录；{snapshot["missing_version_count"]} 个包缺少可见版本资料。' if zh else f'This capture contains {snapshot["public_package_total"]} public packages and {snapshot["latest_tag_rows"]} latest-tag records; {snapshot["missing_version_count"]} packages lack visible version metadata.')
        revision = '<p class="registry-revision">' + (('查询客户端代码版本：' if zh else 'Query client code revision: ') if source['id'] == 'harbor-hub' else ('固定仓库修订：' if zh else 'Pinned repository revision: ')) + escape(source['revision']) + (' · ' + escape(source['revision_date']) if source.get('revision_date') else '') + '</p>' if source.get('revision') else ''
        boundaries.append(f'<article><h3><a href="{escape(source["browse_url"], quote=True)}">{escape(source["name"])}</a></h3><p>{escape(source["note_" + language])}</p><p>{extra}</p><p>{escape(source["rights_" + language])}</p>{revision}<p class="registry-revision">{("采集时间：" if zh else "Captured: ")}{escape(snapshot["captured_at"])}</p></article>')
    body = f'''<section class="registry-hero"><p class="eyebrow">{('上游来源与发现' if zh else 'UPSTREAM SOURCES & DISCOVERY')}</p><h1>{('从上游注册表，<br><em>继续发现项目。</em>' if zh else 'Follow the upstream<br><em>registries.</em>')}</h1><p class="lead">{description}</p><p>{('这些是自动采集的元数据，条目尚未逐项完成项目资料核查或运行验证。版本、分支与封装可能重复，记录数不能与精选项目数相加。' if zh else 'These are automatically captured metadata records, without individual project review or execution verification. Versions, forks and wrappers can overlap; do not add this count to the reviewed project count.')}</p><div class="registry-actions"><a href="{prefix}/">{('浏览已核查项目' if zh else 'Browse reviewed projects')} ↗</a><a href="/registry-index.json">{('下载注册表快照 JSON' if zh else 'Download registry snapshot JSON')} ↓</a><a href="#registry-sources">{('来源与覆盖范围' if zh else 'Sources and coverage')}</a></div></section>
<div class="registry-sources-grid">{''.join(source_cards)}</div>
<section class="directory registry-directory" id="registry-results" aria-labelledby="registry-title"><div class="directory-top"><div class="directory-heading"><h2 id="registry-title">{('搜索上游记录' if zh else 'Search upstream records')}</h2><span class="registry-note-count">{related_count} {('条记录有相关项目说明' if zh else 'records link to related project notes')}</span></div><div class="filters"><label class="search-box"><span aria-hidden="true">⌕</span><span class="visually-hidden">{('搜索上游记录' if zh else 'Search registry records')}</span><input id="registry-search" type="search" autocomplete="off" placeholder="{('搜索名称、配置、相关项目…' if zh else 'Search names, configurations, related projects…')}"></label>
<label class="visually-hidden" for="registry-source">{('来源' if zh else 'Registry source')}</label><select id="registry-source"><option value="">{('所有来源' if zh else 'All sources')}</option>{source_options}</select>
<label class="visually-hidden" for="registry-notes">{('相关项目说明' if zh else 'Related project notes')}</label><select id="registry-notes"><option value="">{('所有记录' if zh else 'All records')}</option><option value="yes">{('有相关项目说明' if zh else 'Has related notes')}</option><option value="no">{('暂无相关项目说明' if zh else 'No related notes')}</option></select>
<label class="visually-hidden" for="registry-version">{('Harbor 版本资料' if zh else 'Harbor version metadata')}</label><select id="registry-version"><option value="">{('所有版本状态' if zh else 'All version states')}</option><option value="available">{('Harbor：可见版本' if zh else 'Harbor: version visible')}</option><option value="unavailable">{('Harbor：版本资料缺失' if zh else 'Harbor: version missing')}</option></select><button id="registry-reset" class="reset" type="button" hidden>{('重置' if zh else 'Reset')}</button></div>
<div class="results-line"><span id="registry-count" role="status" aria-live="polite">{len(records)} {('条来源记录' if zh else 'source records')}</span><span>{('上游元数据 · 采集快照' if zh else 'Upstream metadata snapshot')}</span></div></div><div class="table-wrap"><table class="registry-table"><thead><tr><th>{('名称与相关说明' if zh else 'Name / related notes')}</th><th>{('观察到的元数据' if zh else 'Observed metadata')}</th><th>{('来源与采集日期' if zh else 'Source / captured')}</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div><div class="empty" id="registry-empty" hidden><h3>{('没有匹配的记录。' if zh else 'No matching records.')}</h3><p>{('修改关键词或重置筛选。' if zh else 'Change your search or reset the filters.')}</p></div><noscript><p class="no-script">{('全部记录及链接已在页面中；筛选需要 JavaScript。' if zh else 'Every record and link is present here; filtering requires JavaScript.')}</p></noscript></section>
<section class="registry-boundaries" id="registry-sources"><h2>{('来源与覆盖范围' if zh else 'Sources and coverage')}</h2><p>{('每次采集保留响应哈希与来源信息。包的公开可见性不等于宽松许可或可直接运行；请查看上游的具体要求。' if zh else 'Captures retain response hashes and source references. Public package visibility does not establish permissive licensing or immediate runtime availability; inspect the upstream requirements.')} <a href="/registry-sources.json">{('来源配置 JSON' if zh else 'Source configuration JSON')} ↗</a></p>{''.join(boundaries)}</section>'''
    return title, description, body, items
