# AI Can What?

**浏览 AI 创造的软件，寻找 Agent 学习与评测的环境。**

**[访问网站](https://aicanwhat.com/zh/) · [English](README.md) · [收录方法](https://aicanwhat.com/zh/about/)**

当前有 **213 条目录记录、149 篇原始论文**，两类数量不能相加。其中 3 篇尚无对应的已核查产物条目，文献页单独说明发布状态。来源核查不代表已经运行或复现实验。

| 分类 | 条目 | 仓库索引 |
| --- | --- | --- |
| 游戏与虚拟世界 | 56 | [浏览](catalog/games/README.zh-CN.md) |
| 网站 | 39 | [浏览](catalog/websites/README.zh-CN.md) |
| 应用 | 118 | [浏览](catalog/apps/README.zh-CN.md) |

[研究文献](papers/README.zh-CN.md) · [网页文献筛选](https://aicanwhat.com/zh/papers/) · [完整数据](data/catalog.json) · [贡献说明](CONTRIBUTING.md)

[选择指南](guides/README.zh-CN.md)按用途和证据比较 AI 软件作品、浏览器与电脑／手机任务、软件生成、编程 Agent 以及数据工作流。

另有 **5 条浏览器操作记录，覆盖 5 个项目**，包含步骤、可见结果、截图及未测试范围；不代表整个应用已完成验证。[操作记录](data/observations.json) · [记录方法](docs/browser-observations.md)。

[上游注册表索引](https://aicanwhat.com/zh/discover/)另提供 **490 条来自 5 个来源的元数据记录**。它们包含版本、分支、清单与配置，尚未逐项核查，不能与精选项目数相加。[查看来源覆盖](catalog/registries/README.zh-CN.md)。

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
