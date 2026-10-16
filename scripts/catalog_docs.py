"""Generate browsable repository indexes from the same catalog as the website."""
from collections import Counter
from html import escape
import os


def build_catalog_docs(root, config, entries, papers, types, kinds, platforms, uses):
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
    summary = f'**{len(entries)} catalog entries · {len(papers)} referenced papers.** Paper references overlap the catalog; these counts are not additive. Every entry links its evidence and records known limits.\n\n## Browse\n\n| Category | Entries | Repository index |\n| --- | --- | --- |\n'
    for category, labels in types.items():
        slug = {'game': 'games', 'website': 'websites', 'app': 'apps'}[category]
        summary += f'| [{labels[0]}]({origin}/{slug}/) | {counts[category]} | [Browse](catalog/{slug}/README.md) |\n'
    summary += '\n[Research bibliography](' + origin + '/papers/) · [Catalog data](data/catalog.json) · [Contributing](CONTRIBUTING.md)\n'
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

当前有 **{len(entries)} 条目录记录**，关联 **{len(papers)} 篇原始论文**。论文与项目记录有对应关系，数量不能相加。来源核查不代表已经运行或复现实验。

| 分类 | 条目 | 仓库索引 |
| --- | --- | --- |
| {types['game'][1]} | {counts['game']} | [浏览](catalog/games/README.zh-CN.md) |
| 网站 | {counts['website']} | [浏览](catalog/websites/README.zh-CN.md) |
| 应用 | {counts['app']} | [浏览](catalog/apps/README.zh-CN.md) |

[研究文献]({origin}/zh/papers/) · [完整数据](data/catalog.json) · [贡献说明](CONTRIBUTING.md)

相关目录：[AwesomeREA](https://awesomerea.org/zh/resources/) 整理逆向工程工具、集成与软件重建研究。

软件作品、可运行环境、评测套件和静态数据集分别标注。AI 开发方式需要作者证据；平台、许可和运行限制以原始来源为准，未知信息保持未知。

## 本地构建

```sh
python3 scripts/build.py
python3 scripts/validate.py
node --check static/app.js
```

数据来源是 `data/catalog.json` 与 `data/papers.json`。页面、引用和分类 README 由同一组数据生成；请修改源数据后重新构建。托管配置和搜索提交步骤见 [search-discovery.md](docs/search-discovery.md)。
'''
    (root / 'README.zh-CN.md').write_text(chinese, encoding='utf-8')
