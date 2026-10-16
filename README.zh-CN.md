# AI Can What?

**浏览 AI 创造的软件，寻找 Agent 学习与评测的环境。**

**[访问网站](https://aicanwhat.com/zh/) · [English](README.md) · [收录方法](https://aicanwhat.com/zh/about/)**

当前有 **102 条目录记录**，关联 **73 篇原始论文**。论文与项目记录有对应关系，数量不能相加。来源核查不代表已经运行或复现实验。

| 分类 | 条目 | 仓库索引 |
| --- | --- | --- |
| 游戏与虚拟世界 | 21 | [浏览](catalog/games/README.zh-CN.md) |
| 网站 | 25 | [浏览](catalog/websites/README.zh-CN.md) |
| 应用 | 56 | [浏览](catalog/apps/README.zh-CN.md) |

[研究文献](https://aicanwhat.com/zh/papers/) · [完整数据](data/catalog.json) · [贡献说明](CONTRIBUTING.md)

[上游注册表索引](https://aicanwhat.com/zh/discover/)另提供 **490 条来自 5 个来源的元数据记录**。它们包含版本、分支、清单与配置，尚未逐项核查，不能与精选项目数相加。[查看来源覆盖](catalog/registries/README.zh-CN.md)。

相关目录：[AwesomeREA](https://awesomerea.org/zh/resources/) 整理逆向工程工具、集成与软件重建研究。

软件作品、可运行环境、评测套件和静态数据集分别标注。AI 开发方式需要作者证据；平台、许可和运行限制以原始来源为准，未知信息保持未知。

## 本地构建

```sh
python3 scripts/build.py
python3 scripts/validate.py
node --check static/app.js
node --check static/registry.js
python3 -m unittest discover -s tests
```

数据来源是 `data/catalog.json` 与 `data/papers.json`。页面、引用和分类 README 由同一组数据生成；请修改源数据后重新构建。托管配置和搜索提交步骤见 [search-discovery.md](docs/search-discovery.md)。
