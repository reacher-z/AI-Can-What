# AI 软件作品：从案例找到开发证据

[网站版本](https://aicanwhat.com/zh/guides/ai-built-software/) · 2026-10-16

从游戏、网站和原生应用中寻找有作者 AI 开发说明的作品，区分源码、演示与有限操作证据。

先找具体作品，再看创作者的开发记录。公开演示能展示界面，源码能展示实现，两者都不能单独证明开发方式。下列项目均有明确作者证据，并保留 AI 参与范围及实际限制。

## 游戏与互动作品

对照原创演示、重建作品及使用人工素材的作品，留意各自开发声明覆盖的组件。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [Tic Tac Toe — Imperium Edition](https://aicanwhat.com/zh/projects/gpt5-tic-tac-toe-game/) · [Source](https://github.com/openai/gpt-5-coding-examples/tree/main/apps/tic-tac-toe-game) | 查看公开生成提示、单文件游戏及一局双人操作记录。 | 电脑对手使用包含 minimax 的游戏逻辑，并非 LLM 服务。该展示作品没有基准协议。独立浏览器记录覆盖一局本地双人获胜过程；未测试电脑策略及其他模式。仓库代码采用 MIT。 |
| [Three.js Quake](https://aicanwhat.com/zh/projects/threejs-quake/) · [Source](https://github.com/mrdoob/three-quake) | 研究 AI 辅助浏览器移植，同时保留原游戏作者及独立素材权利。 | AI 开发声明针对移植工作，原作由 id Software 创作。仓库包含第一章共享版数据，完整游戏内容需使用正版注册版数据。 |
| [Firewood Splitting Simulator](https://aicanwhat.com/zh/projects/firewood-splitting-simulator/) · [Source](https://screen.toys/firewood/) | 了解生成实现如何结合作者的扫描、动画及声音素材。 | 本条目仅覆盖浏览器版本。实体扫描、动画及声音由作者采集和编辑，未找到公开源码仓库或代码复用许可。 |

## 网站与浏览器工具

这些案例将具体用途与可追溯的作者说明关联；托管界面不代表后端正确或已授予复用许可。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [Aldi Prices](https://aicanwhat.com/zh/projects/aldi-prices/) · [Source](https://aldi-prices.lawruk.com/) | 查看数据网站及独立记录的搜索到历史页面流程。 | 作者将其描述为个人价格记录。CSV 并非完整或实时的零售商价格源，覆盖范围和时效取决于记录的数据。 本轮查阅的仓库中未确认源代码复用许可。 |
| [Social Media Card Cropper](https://aicanwhat.com/zh/projects/social-media-card-cropper/) · [Source](https://tools.simonwillison.net/social-media-cropper) | 追溯图片裁切工具公开记录的实现过程。 | 工具使用第三方浏览器库，并可能从 CDN 加载图片编码器。导出支持及速度取决于浏览器；本轮未上传或处理图片。 仓库代码采用 Apache 2.0 许可，外部库保留各自条款。 |
| [CSV To Charts](https://aicanwhat.com/zh/projects/gpt5-csv-to-charts/) · [Source](https://github.com/openai/gpt-5-coding-examples/tree/77f6322723703941f0b884d1a1cb77c60aad5187/apps/csv-to-charts) | 查看文件转图表演示及独立记录的样例图表操作；文件导入与 PNG 输出仍未验证。 | 独立浏览器记录覆盖内置样例、图表类型切换及数据列显隐。文件导入和 PNG 输出未验证。Chart.js 从未固定版本的 CDN 加载。源码显示空字符串会转成零，逗号会被删除；无效数值在饼图／环形图中被跳过，在柱状图／折线图中变为缺口。未确立分析正确性及 CSV 兼容性。 |
| [Markdown → Slides](https://aicanwhat.com/zh/projects/gpt5-markdown-to-slides/) · [Source](https://github.com/openai/gpt-5-coding-examples/tree/77f6322723703941f0b884d1a1cb77c60aad5187/apps/markdown-to-slides) | 查看输入 Markdown 的预览工具及两页翻页记录；该工具没有内置文件导出。 | 这个预览与演示示例使用简化的自定义 Markdown 解析器，没有内置 PPTX、PDF 或 HTML 导出。localStorage 只保存主题，文档会从示例重新初始化。独立浏览器记录覆盖两页合成文本及前后翻页，不代表完整 Markdown 兼容性；远程图片可能需要联网。 |

## 桌面与移动软件

检查应用实际分发目标；浏览器客户端、原生安装包和命令行封装的安装与开发来源边界不同。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [Context](https://aicanwhat.com/zh/projects/context-mcp/) · [Source](https://github.com/indragiek/Context) | 查看有作者开发证据和公开源码的原生 macOS MCP 客户端。 | 需要 macOS 15 及以上版本。已核查的 README 列有尚未支持或开发中的协议功能；预编译版本默认启用 Sentry 崩溃报告。 源代码采用 MIT 许可。 |
| [Davit](https://aicanwhat.com/zh/projects/davit/) · [Source](https://davit.app/) | 查看管理 Linux 容器的原生 Mac 界面，区分应用平台与被管理的运行环境。 | 需要 Apple Silicon Mac、macOS 15 及以上版本和 Apple 容器平台。macOS 标签指桌面应用，受管理的容器运行 Linux。 源代码采用 MIT 许可。 |
| [A9 Voice](https://aicanwhat.com/zh/projects/a9-voice/) · [Source](https://a9voice.com/) | 对照有公开版本历史、但源码专有的打包 Windows 应用。 | 需要 64 位 Windows 10/11。听写免费，Notes 试用后需付费许可。选择云服务时，相应音频或文本会发送给提供方，许可检查也需要联网。 |
| [RhoUnpacker](https://aicanwhat.com/zh/projects/rhounpacker/) · [Source](https://github.com/w1426421352/RhoUnpacker) | 研究围绕独立人工库构建的 AI 生成 Windows 命令行层。 | AI 生成的是命令行层，核心解包库 KartLibrary 由人工编写。文档中的 Native AOT 目标为 Windows x64，项目采用 GPLv3。 |
| [Shelly](https://aicanwhat.com/zh/projects/shelly-android/) · [Source](https://github.com/RYOITABASHI/Shelly) | 查看有预发布分发说明的 Android 终端应用。 | 维护者将其列为预发布软件，后台自主执行循环仅记录过一次 Galaxy Z Fold6 验证。文档指定 android-latest 滚动发布为 APK 来源；本次核查的清单版本为 8.1.1。仓库代码采用 GPLv3。 |

## 选择时的常见问题

### AI 构建是否代表所有素材和依赖都由 AI 生成？

不是。应查看作者声明的具体范围。生成界面可能使用人工编写的库，生成游戏也可能包含人工模型、音乐和原创设计。

### 如何找到某个平台的更多作品？

进入应用平台索引并选择“AI 软件作品”。较大的分类还包含环境和数据集，这些条目的平台标签含义不同。

### 哪些案例有实际操作记录？

井字棋、Aldi Prices、CSV To Charts 和 Markdown → Slides 记录了特定浏览器交互的日期、步骤与截图。各记录区分可见结果与未测试功能，不构成完整应用认证。

## 继续查找

- [全部软件作品](https://aicanwhat.com/zh/?kind=ai-generated-output)
- [Windows 作品](https://aicanwhat.com/zh/apps/windows/?kind=ai-generated-output)
- [macOS 作品](https://aicanwhat.com/zh/apps/macos/?kind=ai-generated-output)
- [iOS 作品](https://aicanwhat.com/zh/apps/ios/?kind=ai-generated-output)
- [Android 作品](https://aicanwhat.com/zh/apps/android/?kind=ai-generated-output)

本指南基于目录原始来源，使用 AI 辅助研究与写作。分组不是排名；未独立复现实验或验证所有运行功能。

[收录方法](https://aicanwhat.com/zh/about/)
