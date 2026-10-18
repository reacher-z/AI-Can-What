"""Generate browsable repository indexes from the same catalog as the website."""
from collections import Counter
from html import escape
import os


def build_catalog_docs(root, config, entries, papers, types, kinds, platforms, uses, registry_sources, registry_document, observations):
    origin = config['origin'].rstrip('/')
    def table(records, language='en'):
        zh = language == 'zh'
        lines = ['| 项目 | 资源类型 | 用途 | 原始来源 |' if zh else '| Project | Resource type | Use | Primary source |', '| --- | --- | --- | --- |']
        for entry in sorted(records, key=lambda e: e['name'].casefold()):
            name = escape(entry['name']).replace('|', '&#124;').replace('[', '&#91;').replace(']', '&#93;')
            url = origin + ('/zh' if zh else '') + '/projects/' + entry['id'] + '/'
            lines.append(f'| [{name}]({url}) | {kinds[entry["resource_kind"]][int(zh)]} | {", ".join(uses[u][int(zh)] for u in entry["uses"])} | [Source]({entry["primary_url"]}) |')
        return '\n'.join(lines)
    for category, labels in types.items():
        directory = root / 'catalog' / {'game': 'games', 'website': 'websites', 'app': 'apps'}[category]
        directory.mkdir(parents=True, exist_ok=True)
        records = [e for e in entries if e['content_type'] == category]
        for language in ('en', 'zh'):
            zh = language == 'zh'
            filename = 'README.zh-CN.md' if zh else 'README.md'
            back = os.path.relpath(root / filename, directory)
            intro = ('来源核查不等于实际运行；资源类型区分软件、环境、评测套件和数据集。' if zh else 'Source review is not execution verification. Resource types distinguish software, environments, benchmark suites, and datasets.')
            navigation = ''
            if category == 'app':
                navigation = ('按平台浏览：' if zh else 'Browse by platform: ') + ' · '.join(f'[{label}]({platform}/{filename})' for platform, label in platforms.items() if any(platform in e['platforms'] for e in records)) + '\n\n'
            text = f'# {labels[int(zh)]}\n\n[{("返回目录" if zh else "Back to the collection")}]({back})\n\n{len(records)} {("个条目" if zh else "entries")}. {intro}\n\n' + navigation + table(records, language) + '\n'
            (directory / filename).write_text(text, encoding='utf-8')
    app_records = [e for e in entries if e['content_type'] == 'app']
    for platform, label in platforms.items():
        records = [e for e in app_records if platform in e['platforms']]
        if not records:
            continue
        directory = root / 'catalog/apps' / platform
        directory.mkdir(parents=True, exist_ok=True)
        for language in ('en', 'zh'):
            zh = language == 'zh'
            filename = 'README.zh-CN.md' if zh else 'README.md'
            title = label + (' 应用与评测资源' if zh else ' apps and evaluation resources')
            intro = (f'{len(records)} 个条目。平台标签可能指可运行应用、环境目标或数据集中的截图来源；请同时查看资源类型和限制。' if zh else f'{len(records)} entries. Platform tags can describe a runnable application, an environment target, or a dataset’s screenshot source; read each entry’s resource type and limits.')
            url = origin + ('/zh' if zh else '') + '/apps/' + platform + '/'
            text = f'# {title}\n\n[{("全部应用资源" if zh else "All app resources")}](../{filename}) · [{("网站索引" if zh else "Website index")}]({url})\n\n{intro}\n\n' + table(records, language) + '\n'
            (directory / filename).write_text(text, encoding='utf-8')
    counts = Counter(e['content_type'] for e in entries)
    paper_only_count = sum(paper.get('catalog_status') == 'paper-only' for paper in papers)
    summary = f'**{len(entries)} catalog entries · {len(papers)} research papers.** These counts are not additive. {paper_only_count} papers have no corresponding reviewed artifact entry; their release-status notes stay in the bibliography. Every catalog entry links evidence and records known limits.\n\n## Browse\n\n| Category | Entries | Repository index |\n| --- | --- | --- |\n'
    for category, labels in types.items():
        slug = {'game': 'games', 'website': 'websites', 'app': 'apps'}[category]
        summary += f'| [{labels[0]}]({origin}/{slug}/) | {counts[category]} | [Browse](catalog/{slug}/README.md) |\n'
    summary += '\n[Research bibliography](papers/README.md) · [Search papers on the website](' + origin + '/papers/) · [Catalog data](data/catalog.json) · [Contributing](CONTRIBUTING.md)\n'
    summary += '\n[Coverage and counting units](catalog/coverage/README.md) · [Coverage JSON](catalog/coverage/coverage.json)\n'
    summary += '\n[Selection guides](guides/README.md) compare AI software examples, browser and computer/mobile tasks, software generation, coding agents, data workflows and tool/API use by purpose and evidence.\n'
    observed_ids = {record['project_id'] for record in observations}
    summary += f'\n**{len(observations)} scoped browser observations across {len(observed_ids)} projects** record interaction steps, visible outcomes, screenshots and untested scope. These are not whole-application verification. [Observation data](data/observations.json) · [Method](docs/browser-observations.md).\n'
    registry_count = len(registry_document['records'])
    summary += f'\n[Upstream registry index]({origin}/discover/): **{registry_count} metadata records from {len(registry_sources)} sources**. These include versions, forks, manifests, and configurations; they are not individually reviewed projects and must not be added to the catalog count. [Source coverage](catalog/registries/README.md).\n'
    readme = root / 'README.md'
    text = readme.read_text()
    begin, end = '<!-- BEGIN GENERATED INDEX -->', '<!-- END GENERATED INDEX -->'
    if begin in text:
        before, rest = text.split(begin, 1)
        _, after = rest.split(end, 1)
    else:
        before, rest = text.split('The first collection contains', 1)
        _, after = rest.split('## How the directory works', 1)
        after = '\n\n## How the directory works' + after
    readme.write_text(before + begin + '\n' + summary + end + after, encoding='utf-8')
    chinese = f'''# AI Can What?

**浏览 AI 创造的软件，寻找 Agent 学习与评测的环境。**

**[访问网站]({origin}/zh/) · [English](README.md) · [收录方法]({origin}/zh/about/)**

当前有 **{len(entries)} 条目录记录、{len(papers)} 篇原始论文**，两类数量不能相加。其中 {paper_only_count} 篇尚无对应的已核查产物条目，文献页单独说明发布状态。来源核查不代表已经运行或复现实验。

| 分类 | 条目 | 仓库索引 |
| --- | --- | --- |
| {types['game'][1]} | {counts['game']} | [浏览](catalog/games/README.zh-CN.md) |
| 网站 | {counts['website']} | [浏览](catalog/websites/README.zh-CN.md) |
| 应用 | {counts['app']} | [浏览](catalog/apps/README.zh-CN.md) |

[研究文献](papers/README.zh-CN.md) · [网页文献筛选]({origin}/zh/papers/) · [完整数据](data/catalog.json) · [贡献说明](CONTRIBUTING.md)

[选择指南](guides/README.zh-CN.md)按用途和证据比较 AI 软件作品、浏览器与电脑／手机任务、软件生成、编程 Agent、数据工作流与工具／API 使用。

[覆盖统计与计数口径](catalog/coverage/README.zh-CN.md) · [统计 JSON](catalog/coverage/coverage.json)

另有 **{len(observations)} 条浏览器操作记录，覆盖 {len(observed_ids)} 个项目**，包含步骤、可见结果、截图及未测试范围；不代表整个应用已完成验证。[操作记录](data/observations.json) · [记录方法](docs/browser-observations.md)。

[上游注册表索引]({origin}/zh/discover/)另提供 **{registry_count} 条来自 {len(registry_sources)} 个来源的元数据记录**。它们包含版本、分支、清单与配置，尚未逐项核查，不能与精选项目数相加。[查看来源覆盖](catalog/registries/README.zh-CN.md)。

相关目录：[AwesomeREA](https://awesomerea.org/zh/resources/) 整理逆向工程工具、集成与软件重建研究。

软件作品、可运行环境、评测套件和静态数据集分别标注。AI 开发方式需要作者证据；平台、许可和运行限制以原始来源为准，未知信息保持未知。

## 本地构建

```sh
python3 scripts/build.py
python3 scripts/validate.py
node --check static/app.js
node --check static/search.js
node --check static/registry.js
node --check static/papers.js
python3 -m unittest discover -s tests
```

数据来源是 `data/catalog.json`、`data/papers.json` 和单独保存操作证据的 `data/observations.json`。页面、引用和分类 README 由同一组数据生成；请修改源数据后重新构建。托管配置和搜索提交步骤见 [search-discovery.md](docs/search-discovery.md)。
'''
    (root / 'README.zh-CN.md').write_text(chinese, encoding='utf-8')
    directory = root / 'catalog/registries'
    directory.mkdir(parents=True, exist_ok=True)
    snapshots = {snapshot['source_id']: snapshot for snapshot in registry_document['snapshots']}
    for language in ('en', 'zh'):
        zh = language == 'zh'
        filename = 'README.zh-CN.md' if zh else 'README.md'
        lines = ['# ' + ('上游注册表索引' if zh else 'Upstream registry index'), '',
                 f'[{("网站索引" if zh else "Browse the index")}]({origin}{("/zh" if zh else "")}/discover/) · [{("元数据快照" if zh else "Metadata snapshot")}](../../data/registry-index.json)', '',
                 ('以下是上游元数据记录，不是逐项复核或运行验证的项目。版本、分支与配置可能重叠，数量不能与精选目录相加。' if zh else 'These are upstream metadata records, not individually reviewed or execution-verified projects. Versions, forks and configurations can overlap; counts are not additive with the curated catalog.'), '',
                 '| 来源 | 记录数 | 采集日期 |' if zh else '| Source | Records | Captured |', '| --- | --- | --- |']
        for source in registry_sources:
            snapshot = snapshots[source['id']]
            lines.append(f'| [{source["name"]}]({source["browse_url"]}) | {snapshot["record_count"]} | {snapshot["captured_at"][:10]} |')
        lines += ['', '[Method, limitations, and refresh workflow](../../docs/registry-discovery.md)', '']
        (directory / filename).write_text('\n'.join(lines), encoding='utf-8')
