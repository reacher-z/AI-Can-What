#!/usr/bin/env python3
"""Capture factual upstream registry metadata. No upstream code is imported or run."""
from __future__ import annotations

import argparse
import ast
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
from urllib.parse import quote, urlencode, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / '.cache/discovery'
MAX_BYTES = 20_000_000
UA = 'AI-Can-What-Registry/1.0'


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def records_digest(records):
    return digest(json.dumps(records, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode())


def public_url(url):
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or any(c.isspace() for c in url):
        raise ValueError('Expected a public HTTPS source URL')
    return url


def fetch(url, *, headers=None):
    public_url(url)
    if urlsplit(url).hostname == 'api.github.com' and headers is None:
        # gh manages its own authentication; tokens are neither read nor retained here.
        result = subprocess.run(['gh', 'api', '--method', 'GET', url], capture_output=True, check=False)
        if result.returncode:
            raise ValueError('GitHub metadata request failed: ' + urlsplit(url).path)
        raw = result.stdout
        response_headers = {}
    else:
        with urlopen(Request(url, headers={'User-Agent': UA, **(headers or {})}), timeout=45) as response:
            if response.status not in (200, 206):
                raise ValueError('Unexpected registry response status')
            raw = response.read(MAX_BYTES + 1)
            response_headers = dict(response.headers.items())
    if len(raw) > MAX_BYTES:
        raise ValueError('Registry response exceeded the metadata size limit')
    return raw, response_headers


def capture(source_id, url, use_cache):
    path = CACHE / (source_id + '.raw')
    receipt_path = CACHE / (source_id + '.receipt.json')
    if use_cache and path.exists() and receipt_path.exists():
        receipt = json.loads(receipt_path.read_text())
        raw = path.read_bytes()
        if receipt.get('url') == url and receipt.get('sha256') == digest(raw):
            return raw, receipt
    raw, _ = fetch(url)
    receipt = {'url': url, 'captured_at': now(), 'bytes': len(raw), 'sha256': digest(raw)}
    path.write_bytes(raw)
    receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
    return raw, receipt


def record(source, key, name, url, **attributes):
    if not isinstance(key, str) or not key or not isinstance(name, str) or not name.strip():
        raise ValueError('Registry records need a stable key and name')
    return {'id': source['id'] + '-' + digest(key.encode())[:16], 'source_id': source['id'],
            'source_key': key, 'name': name, 'kind': source['kind'], 'url': public_url(url),
            'attributes': attributes}


def extract_constants(raw):
    values = {}
    wanted = {'DEFAULT_SUPABASE_URL', 'DEFAULT_SUPABASE_PUBLISHABLE_KEY'}
    for node in ast.parse(raw).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in wanted:
                    values[target.id] = ast.literal_eval(node.value)
    if set(values) != wanted or not all(isinstance(v, str) and v for v in values.values()):
        raise ValueError('Public Harbor client constants changed shape')
    return values


def validate_census(document, table):
    rows = document['records']
    if not isinstance(rows, list) or len(rows) != document['advertised_total'] or document['records_sha256'] != records_digest(rows):
        raise ValueError('Registry census count or cache digest mismatch')
    ids = []
    for row in rows:
        package = row if table == 'package' else row['package']
        if package.get('type') != 'dataset' or package.get('visibility') != 'public':
            raise ValueError('A census row is not an explicitly public dataset package')
        if not isinstance(package.get('org'), dict) or not package['org'].get('name') or not package.get('name'):
            raise ValueError('Missing package namespace or name')
        ids.append(package['id'])
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate package IDs across registry pages')
    return rows


def fetch_census(source, table, query, label, public_key, use_cache):
    path = CACHE / ('harbor-hub-' + label + '.json')
    if use_cache and path.exists():
        document = json.loads(path.read_text())
        validate_census(document, table)
        # Cached input must still be the configured public endpoint and visibility scope.
        for page in document['pages']:
            if not page['request_url'].startswith(source['api_origin'] + '/rest/v1/' + table + '?'):
                raise ValueError('Cached census belongs to a different source')
        return document
    rows, receipts, total = [], [], None
    while total is None or len(rows) < total:
        url = source['api_origin'] + '/rest/v1/' + table + '?' + urlencode({**query, 'limit': 100, 'offset': len(rows)})
        raw, headers = fetch(url, headers={'apikey': public_key, 'Prefer': 'count=exact'})
        content_range = next((value for name, value in headers.items() if name.lower() == 'content-range'), '')
        match = re.fullmatch(r'(\d+)-(\d+)/(\d+)', content_range)
        if not match:
            raise ValueError('Registry did not provide an exact paginated count')
        start, end, observed = map(int, match.groups())
        chunk = json.loads(raw)
        if total is not None and observed != total:
            raise ValueError('Registry changed during pagination; retain the prior published snapshot')
        total = observed
        if not isinstance(chunk, list) or not chunk or start != len(rows) or len(chunk) != end - start + 1 or total > 100_000:
            raise ValueError('Invalid registry pagination bounds')
        receipts.append({'request_url': url, 'content_range': content_range, 'bytes': len(raw), 'sha256': digest(raw)})
        rows.extend(chunk)
    document = {'fetched_at': now(), 'public_visibility_only': True, 'advertised_total': total,
                'pages': receipts, 'records': rows, 'records_sha256': records_digest(rows)}
    validate_census(document, table)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n')
    return document


def parse_harbor(source, packages, versions):
    package_rows = validate_census(packages, 'package')
    version_rows = validate_census(versions, 'dataset_version_tag')
    package_ids = {p['id'] for p in package_rows}
    version_by_id = {v['package']['id']: v for v in version_rows}
    if not set(version_by_id) <= package_ids:
        raise ValueError('Version metadata references packages outside the captured public census')
    records, missing = [], []
    for package in package_rows:
        key = package['org']['name'] + '/' + package['name']
        metadata = version_by_id.get(package['id'])
        if metadata and (metadata['package']['name'] != package['name'] or metadata['package']['org'] != package['org']):
            raise ValueError('Package identity changed between the package and version captures')
        if metadata and metadata.get('tag') != 'latest':
            raise ValueError('Unexpected version tag in latest metadata query')
        version = metadata.get('dataset_version') if metadata else None
        attributes = {'package_id': package['id'], 'namespace': package['org']['name'],
                      'version_status': 'available' if version else 'unavailable'}
        url = source['browse_url']
        if version:
            counts = version.get('dataset_version_task')
            if not isinstance(counts, list) or len(counts) != 1 or type(counts[0].get('count')) is not int or counts[0]['count'] < 0:
                raise ValueError('Invalid task-count metadata')
            if type(version.get('revision')) is not int or version['revision'] < 1 or not re.fullmatch(r'[a-f0-9]{64}', version.get('content_hash', '')):
                raise ValueError('Invalid immutable version metadata')
            attributes.update({'tag': 'latest', 'revision': version['revision'], 'version_id': version['id'],
                               'content_hash': version['content_hash'], 'task_count': counts[0]['count'],
                               'published_at': version.get('published_at'), 'yanked_at': version.get('yanked_at')})
            url += '/' + quote(package['org']['name'], safe='') + '/' + quote(package['name'], safe='') + '/latest'
        else:
            missing.append(package['id'])
        records.append(record(source, key, key, url, **attributes))
    return records, {'public_package_total': len(package_rows), 'latest_tag_rows': len(version_rows),
                     'missing_version_package_ids': missing, 'missing_version_count': len(missing)}


def harbor(source, use_cache):
    # Only upstream-published anonymous defaults are read. Local auth files and environment credentials are ignored.
    raw, receipt = capture('harbor-public-client', source['constants_url'], use_cache)
    values = extract_constants(raw)
    if values['DEFAULT_SUPABASE_URL'] != source['api_origin']:
        raise ValueError('Upstream Harbor backend changed; review the new public endpoint first')
    queries = [
        ('package', {'select': 'id,name,type,visibility,org:org_id!inner(name)', 'type': 'eq.dataset', 'visibility': 'eq.public', 'order': 'id.asc'}, 'packages'),
        ('dataset_version_tag', {'select': 'tag,package:package_id!inner(id,name,type,visibility,org:org_id!inner(name)),dataset_version:dataset_version_id(id,revision,content_hash,description,published_at,yanked_at,dataset_version_task(count))',
                                 'tag': 'eq.latest', 'package.type': 'eq.dataset', 'package.visibility': 'eq.public', 'order': 'package_id.asc'}, 'versions'),
    ]
    with ThreadPoolExecutor(max_workers=2) as pool:
        snapshots = list(pool.map(lambda args: fetch_census(source, *args, values['DEFAULT_SUPABASE_PUBLISHABLE_KEY'], use_cache), queries))
    records, coverage = parse_harbor(source, *snapshots)
    coverage['captured_at'] = max(snapshot['fetched_at'] for snapshot in snapshots)
    coverage['requests'] = [page for snapshot in snapshots for page in snapshot['pages']]
    coverage['implementation_source'] = {k: v for k, v in receipt.items() if k != 'captured_at'}
    return records, coverage


def parse_python_dictionary(source, raw):
    target = None
    for node in ast.parse(raw).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == source['dictionary'] for t in node.targets):
            target = node.value
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == source['dictionary']:
            target = node.value
    if not isinstance(target, ast.Dict):
        raise ValueError('Expected a literal benchmark configuration dictionary')
    records = []
    for key_node, value in zip(target.keys, target.values):
        key = ast.literal_eval(key_node)
        attributes = {'source_line': value.lineno}
        call = value.body if isinstance(value, ast.Lambda) else value
        if isinstance(call, ast.Call):
            for keyword in call.keywords:
                if keyword.arg in {'name', 'backends', 'is_multi_tab'}:
                    try:
                        literal = ast.literal_eval(keyword.value)
                    except (ValueError, TypeError):
                        continue
                    if isinstance(literal, (str, bool)) or isinstance(literal, list) and all(isinstance(x, str) for x in literal):
                        attributes['benchmark_name' if keyword.arg == 'name' else keyword.arg] = literal
        records.append(record(source, key, key, source['browse_url'] + '#L' + str(value.lineno), **attributes))
    return records


def parse_tree(source, document):
    if document.get('truncated') is not False or not isinstance(document.get('tree'), list):
        raise ValueError('GitHub tree is missing or truncated')
    blobs = {item['path']: item for item in document['tree'] if item.get('type') == 'blob' and item.get('mode') in {'100644', '100755'}}
    records = []
    base = 'https://github.com/' + source['repository']
    for path, item in sorted(blobs.items()):
        if not re.fullmatch(source['manifest_pattern'], path):
            continue
        attributes = {'manifest_path': path, 'manifest_blob': item['sha'],
                      'manifest_url': base + '/blob/' + source['revision'] + '/' + path}
        if source['id'] == 'openenv':
            key = path.split('/')[1]
            url = base + '/tree/' + source['revision'] + '/envs/' + key
        else:
            key = PurePosixPath(path).stem
            app_path = 'apps/' + key + '/index.html'
            attributes['matching_application_source'] = app_path in blobs
            if app_path in blobs:
                attributes['application_path'] = app_path
                attributes['application_blob'] = blobs[app_path]['sha']
                url = base + '/tree/' + source['revision'] + '/apps/' + key
            else:
                url = attributes['manifest_url']
        records.append(record(source, key, key, url, **attributes))
    if not records:
        raise ValueError('No manifests matched the reviewed inventory boundary')
    return records


def parse_farama(source, document):
    if not isinstance(document, list) or not document:
        raise ValueError('Expected a nonempty Farama project array')
    records = []
    for item in document:
        if item.get('type') not in {'core', 'mature', 'incubating'}:
            raise ValueError('Unknown upstream governance category')
        github = public_url(item['github'])
        url = item.get('website') or github
        records.append(record(source, github.lower().rstrip('/'), item['name'], url,
                              repository_url=github, upstream_category=item['type']))
    return records


def collect_source(source, use_cache):
    if source['adapter'] == 'harbor-hub':
        records, snapshot = harbor(source, use_cache)
    else:
        if source['adapter'] == 'github-manifests':
            url = 'https://api.github.com/repos/' + source['repository'] + '/git/trees/' + source['revision'] + '?recursive=1'
        elif source['adapter'] == 'python-dictionary':
            url = 'https://raw.githubusercontent.com/' + source['repository'] + '/' + source['revision'] + '/' + source['path']
        else:
            url = source['url']
        raw, receipt = capture(source['id'], url, use_cache)
        if source['adapter'] == 'github-manifests': records = parse_tree(source, json.loads(raw))
        elif source['adapter'] == 'python-dictionary': records = parse_python_dictionary(source, raw)
        elif source['adapter'] == 'farama-projects': records = parse_farama(source, json.loads(raw))
        else: raise ValueError('Unknown registry adapter')
        snapshot = {'captured_at': receipt['captured_at'], 'requests': [receipt]}
    if len({r['source_key'] for r in records}) != len(records):
        raise ValueError('Duplicate keys within a registry source')
    snapshot.update({'source_id': source['id'], 'record_count': len(records)})
    return records, snapshot


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Replace the public metadata snapshot after every source succeeds')
    parser.add_argument('--use-cache', action='store_true', help='Reuse intact matching captures; keep their original observation times')
    args = parser.parse_args()
    CACHE.mkdir(parents=True, exist_ok=True)
    sources = json.loads((ROOT / 'data/registry-sources.json').read_text())['sources']
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(lambda source: collect_source(source, args.use_cache), sources))
    records = sorted([row for rows, _ in results for row in rows], key=lambda r: (r['source_id'], r['source_key'].casefold()))
    if len({r['id'] for r in records}) != len(records):
        raise ValueError('Duplicate registry record IDs')
    document = {'schema_version': 1, 'assembled_at': now(), 'verification': 'upstream-metadata-only',
                'snapshots': [snapshot for _, snapshot in results], 'records': records}
    if args.write:
        destination = ROOT / 'data/registry-index.json'
        temporary = destination.with_suffix('.json.tmp')
        temporary.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n')
        temporary.replace(destination)
    print(json.dumps({'mode': 'written' if args.write else 'preview', 'records': len(records),
                      'sources': {snapshot['source_id']: snapshot['record_count'] for _, snapshot in results}}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
