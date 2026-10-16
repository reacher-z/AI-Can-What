"""Scoped browser observations, kept separate from project source review."""
from datetime import date
import hashlib
from html import escape
import json
import re
from urllib.parse import urlsplit


def read_observations(root, entries):
    document = json.loads((root / 'data/observations.json').read_text())
    assert document['schema_version'] == 1
    records = document['observations']
    projects = {entry['id']: entry for entry in entries}
    seen = set()
    for record in records:
        identifier = record['id']
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', identifier) and identifier not in seen, identifier
        seen.add(identifier)
        assert record['project_id'] in projects, identifier
        assert date.fromisoformat(record['observed_on']) <= date.today(), identifier
        target = urlsplit(record['target_url'])
        assert target.scheme == 'https' and target.hostname and not target.username and not target.password, identifier
        entry = projects[record['project_id']]
        hosts = {urlsplit(entry[key]).hostname for key in ('primary_url', 'demo_url') if entry.get(key)}
        assert target.hostname in hosts, (identifier, 'Observation must identify the reviewed demo host')
        assert record['deployment_commit'] is None, 'These browser observations do not establish a deployed commit.'
        assert record['steps'], identifier
        for language in ('en', 'zh'):
            for key in ('environment', 'summary', 'scope'):
                assert isinstance(record[key + '_' + language], str) and record[key + '_' + language].strip(), (identifier, key)
            for step in record['steps']:
                for key in ('action', 'result'):
                    assert isinstance(step[key + '_' + language], str) and step[key + '_' + language].strip(), (identifier, key)
        screenshot = record['screenshot']
        # Only a direct static image filename is accepted, never arbitrary paths.
        assert re.fullmatch(r'/observation-[a-z0-9-]+\.jpg', screenshot['url']), identifier
        raw = (root / 'static' / screenshot['url'][1:]).read_bytes()
        assert raw.startswith(b'\xff\xd8\xff'), (identifier, 'Expected an original JPEG capture')
        assert hashlib.sha256(raw).hexdigest() == screenshot['sha256'], (identifier, 'Capture changed')
        for language in ('en', 'zh'):
            assert screenshot['caption_' + language].strip(), identifier
    return document, records


def render_observations(records, language):
    if not records:
        return ''
    zh = language == 'zh'
    heading = '浏览器操作记录' if zh else 'Browser observations'
    intro = ('以下是特定日期、公开演示上的有限操作记录。它们不构成整个应用的验证，也没有确认演示对应的源码提交。' if zh else
             'These are limited interactions with a public demo on a stated date. They do not verify the whole application or establish which source commit was deployed.')
    cards = []
    for record in records:
        steps = ''.join('<li><strong>' + escape(step['action_' + language]) + '</strong><p>' + escape(step['result_' + language]) + '</p></li>' for step in record['steps'])
        shot = record['screenshot']
        cards.append(f'''<article class="observation" id="{record['id']}" data-observation="{record['id']}">
<p class="observation-meta"><time datetime="{record['observed_on']}">{record['observed_on']}</time> · {escape(record['environment_' + language])}</p>
<h3>{escape(record['summary_' + language])}</h3>
<p><a href="{escape(record['target_url'], quote=True)}">{('访问记录中的演示' if zh else 'Open the observed demo')} ↗</a> · <a href="#{record['id']}">{('本条记录链接' if zh else 'Link to this observation')}</a></p>
<ol class="observation-steps">{steps}</ol>
<p><strong>{('范围与限制：' if zh else 'Scope and limits: ')}</strong>{escape(record['scope_' + language])}</p>
<figure><a href="{shot['url']}"><img src="{shot['url']}" alt="{escape(shot['caption_' + language], quote=True)}" loading="lazy" width="1728" height="851"></a><figcaption>{escape(shot['caption_' + language])}</figcaption></figure>
</article>''')
    return f'<section id="browser-observations"><h2>{heading}</h2><p>{intro}</p>{"".join(cards)}<p><a href="/observations.json">{("下载操作步骤与截图校验值" if zh else "Download steps and screenshot checksums")} ↗</a></p></section>'
