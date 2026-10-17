# 浏览器 Agent 评测：可控网站、在线任务与记录数据

[网站版本](https://aicanwhat.com/zh/guides/browser-agent-benchmarks/) · 2026-10-16

按交互方式、评分及配置比较浏览器 Agent 资料：自行部署网站、真实网页评测、记录轨迹和统一框架。

先决定评测设置，再选择基准。可控网站支持重置任务状态，真实网页任务会受到内容和外部依赖变化影响，记录轨迹则在没有开放式浏览器执行的情况下测试预测能力。统一框架能连接这些资料，但不会让分数天然可比。

## 可控交互任务

当可重置状态及明确任务结果是实验核心时，从此类资料开始；托管与实例访问许可也是配置的一部分。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [MiniWoB++](https://aicanwhat.com/zh/projects/miniwob-plusplus/) · [Source](https://miniwob.farama.org/) | 在合成任务中单独研究短程网页控制能力。 | 合成任务主要隔离测试交互技能，不能等同于完整生产流程。项目处于维护模式；Python 接口文档要求 Linux/macOS 及 Chrome 或 Chromium 配置。 |
| [WebArena](https://aicanwhat.com/zh/projects/webarena/) · [Source](https://webarena.dev/) | 在自行部署的网站上通过结果检查评估多步操作。 | 可复现评测需要自行部署服务并控制状态重置，共享演示不能替代。WebArena-Verified 单独修订同一任务族及评分器。原始／Verified 及完整／Hard 数量不能相加，报告成绩应注明评分器版本。 |
| [WebArena-Verified](https://aicanwhat.com/zh/projects/webarena-verified/) · [Source](https://github.com/ServiceNow/webarena-verified) | 使用单独维护的评分器及轨迹产物评估同一 WebArena 任务族；不要与原始任务数相加。 | 它修订原始 WebArena 任务族。v1.2.3 的812项完整任务及258项 Hard 子集，不是可叠加到 WebArena 的新独立任务。离线判分需指定的答案和轨迹产物；收集新轨迹仍需网站及重置。应固定评分器、数据和镜像版本，成绩不一定与原始评分器一致。 |
| [VisualWebArena](https://aicanwhat.com/zh/projects/visualwebarena/) · [Source](https://jykoh.com/vwa) | 在可控网站任务中加入依赖图像的推理。 | 需要部署配套站点并匹配任务配置；仓库还列有 Python 版本限制。此处不提供托管评测服务。 |
| [WorkArena](https://aicanwhat.com/zh/projects/workarena/) · [Source](https://github.com/ServiceNow/WorkArena) | 在具备所需 ServiceNow 访问权限时研究企业流程。 | 当前需通过作者的受限数据集申请 ServiceNow 实例访问。WorkArena++ 扩展了原始套件，报告结果时应注明版本。 |

## 真实网页评测

此类设置使用当时的外部网站。需保留日期与评审细节，Agent 之外的变化也会影响执行。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [WebVoyager](https://aicanwhat.com/zh/projects/webvoyager/) · [Source](https://github.com/MinorJerry/WebVoyager) | 研究使用自动视觉评审的多模态浏览轨迹。 | 依赖持续变化的外部网站、Chrome/Selenium 和模型访问。自动评估使用视觉语言模型评审，结果并非确定性的状态检查分数。 |
| [Online-Mind2Web](https://aicanwhat.com/zh/projects/online-mind2web/) · [Source](https://github.com/OSU-NLP-Group/Online-Mind2Web) | 结合动作及截图证据评估真实网站上的任务完成。 | 在线网站和任务定义会变化，应记录任务版本与运行日期。自动评分采用模型评审；排行榜人工审核另有提交和收费规则。 |
| [ClawBench](https://aicanwhat.com/zh/projects/clawbench/) · [Source](https://github.com/TIGER-AI-Lab/ClawBench) | 结合请求和轨迹证据研究在线流程；任务级拦截不会阻止所有外部操作。 | 运行涉及真实生产网站，可能需要账号或外部服务。拦截仅阻止匹配任务规则的请求；未匹配请求仍发送到真实网站，占位规则不会阻止提交。请求被拦截且评审通过，不代表真实结果已提交。当前 V1／V2 目录有152／129项任务，历史数量及评分协议不同。 |
| [Mind2Web 2](https://aicanwhat.com/zh/projects/mind2web-2/) · [Source](https://github.com/OSU-NLP-Group/Mind2Web-2) | 用评审 Agent 评估长流程搜索及带引用回答；完整任务和评分器分发有访问门槛。 | 区别于离线 Mind2Web 动作预测和 Online-Mind2Web 导航。公开 Git 代码包含10个开发集评分器；Hub 当前完整任务／评分文件设有自动批准的访问门槛，本次未访问。完整评分器于2025年10月宣布发布，因此论文时期的私有测试集说明属于历史状态。实时网页及模型判分需固定版本和日期。 |
| [WebBench](https://aicanwhat.com/zh/projects/webbench/) · [Source](https://github.com/Halluminate/WebBench) | 查找有版本记录的在线网站指令，并自行准备 Agent、获准使用的账号及结果评估。 | 仓库发布 CSV 任务及结果，并未提供完整可重置环境或评分器软件包。WRITE 任务会改变真实账号状态，需相应测试账号授权。当前主 CSV 有2,647条记录，README 则写2,454；应固定文件版本。315行 HITL 记录也全部存在于主集合。 |

## 记录的演示数据

适用于动作预测、指令跟随或组件研究，不能替代 Agent 在真实网站上的自由执行。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [Mind2Web](https://aicanwhat.com/zh/projects/mind2web/) · [Source](https://osu-nlp-group.github.io/Mind2Web/) | 通过记录动作研究跨任务、网站和领域的泛化。 | 原始基准评估记录中的操作，并不实际执行在线网站。数据集和代码采用不同许可；对比论文时应使用指定划分与宏平均指标。 |
| [WebLINX](https://aicanwhat.com/zh/projects/weblinx/) · [Source](https://mcgill-nlp.github.io/weblinx/) | 研究多轮浏览指令及演示动作。 | 评估依据记录式演示，不是自由执行在线网站。数据采用 CC BY-NC-SA 4.0；BrowserGym/WebLINX 1.1 改变了评估步骤，应与 1.0 区分。 |

## 统一实验接口

统一接口可以减少集成工作，但仍应保留各基准的环境及评分假设。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [BrowserGym](https://aicanwhat.com/zh/projects/browsergym/) · [Source](https://github.com/ServiceNow/BrowserGym) | 将支持的网页基准接入统一研究接口。 | 这是研究框架，并非另一套独立网页任务；接入的各个基准仍有各自的部署、访问和评测要求。 |

## 选择时的常见问题

### 截图或记录动作基准能证明完整任务完成吗？

不能。目标定位和动作预测衡量局部能力，完整任务完成需要实际执行轨迹，并使用基准的结果检查或明确评分流程。

### 评测报告应保留哪些条件？

记录基准版本、任务划分、浏览器观察与动作接口、重置步骤、模型和工具权限、评审配置及运行日期；这些条件变化会改变分数含义。

### BrowserGym 本身是另一套独立任务吗？

它是集成多种资料的框架，各基准保留自己的配置与访问要求，不能把框架集成数量再当作独立项目叠加到原始任务数中。

## 继续查找

- [全部网页评测资料](https://aicanwhat.com/zh/websites/?use=evaluation)
- [BrowserGym 上游配置](https://aicanwhat.com/zh/discover/?source=browsergym)

本指南基于目录原始来源，使用 AI 辅助研究与写作。分组不是排名；未独立复现实验或验证所有运行功能。

[收录方法](https://aicanwhat.com/zh/about/)
