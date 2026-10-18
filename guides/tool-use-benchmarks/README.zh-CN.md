# 工具与 API 评测：从调用到完整任务

[网站版本](https://aicanwhat.com/zh/guides/tool-use-benchmarks/) · 2026-10-17

按检查对象选择工具与 API 评测：参数构造、环境状态变化、用户协作或模拟服务响应。

先确定需要测量的结果。调用格式正确，不代表请求的流程已经完成。有状态任务检查操作后的环境；对话任务还受用户行为与策略影响。缓存或模型生成的服务响应也有自己的假设。比较结果前，应记录任务划分、执行设置及评分方法。

## 工具选择与参数构造

调用级评测适合单独检查工具选择、必要信息与参数；需确认哪些案例执行实现，哪些只比较调用表示。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [API-Bank](https://aicanwhat.com/zh/projects/api-bank/) · [Source](https://github.com/AlibabaResearch/DAMO-ConvAI/tree/main/api-bank) | 通过公开可运行评测工具比较规划、检索和调用；更大的训练 API 集合属于另一项资源。 | 可运行的评测工具与规模更大的训练 API 集合是不同资源，各难度等级使用不同评测脚本。作者指出 googletrans 与 Gradio 的依赖冲突可能导致本地演示失败。所属仓库采用 MIT，外部服务保留自身条款。 |
| [Berkeley Function Calling Leaderboard (BFCL)](https://aicanwhat.com/zh/projects/bfcl/) · [Source](https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard) | 选择固定版本的类别：AST 检查、模拟多轮执行及 agentic 答案评分衡量不同结果；Harbor 包仅覆盖套件的一部分。 | 须固定 v4 类别集合：单轮／live 使用 AST 检查，多轮核对模拟状态和返回结果，agentic 任务匹配答案。live 指用户贡献样本，并不代表真实 API 执行。记忆与搜索变体复用问题。Harbor 的 3,641 任务适配器不含多轮及 agentic 测试，其 123 任务 parity 子集不增加新任务。网页搜索需要 SerpAPI 或替代服务。旧单轮执行／REST／SQL 类别已停用；部分运行与加权汇总分数不能直接互换。 |

## 有状态的多工具流程

检查中间或最终应用状态，包括不期望的改动；模拟 API 世界不同于已安装桌面或生产账号。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [AppWorld](https://aicanwhat.com/zh/projects/appworld/) · [Source](https://appworld.dev/) | 通过代码或 API 协调互联的模拟应用，结合可执行任务检查及明确的数据划分限制。 | 应用以 API 模拟运行，并非原生图形界面。应遵循训练／开发／测试划分；受保护的应用与任务 bundle 另有加密再分发要求。 |
| [ToolSandbox](https://aicanwhat.com/zh/projects/toolsandbox/) · [Source](https://machinelearning.apple.com/research/toolsandbox-stateful-conversational-llm-benchmark) | 结合环境状态检查研究工具依赖和对话上下文；虽然名称含 Sandbox，实际执行位于宿主机。 | 虽然名称含 Sandbox，文档中的工具执行发生在主机上，而非 Docker 内。需要模型凭据，搜索场景还使用 RapidAPI。Apple 发布了定制许可条款，部分组件另有许可。它模拟设备状态，并不是 iOS 模拟器。 |
| [WorkBench](https://aicanwhat.com/zh/projects/workbench/) · [Source](https://github.com/olly-styles/WorkBench) | 检查可控的邮件、日程和项目管理状态，同时保留修订后的任务及评分器版本。 | 使用模拟办公工具，并非真实邮箱账户或桌面应用。2026 年的任务修订和评分器与原始版本不同，应报告标准答案及评分版本。 |
| [ToolTalk](https://aicanwhat.com/zh/projects/tooltalk/) · [Source](https://github.com/microsoft/ToolTalk) | 研究每轮重置状态并回放参考历史的模拟工具对话；模型错误不会在整段对话中自由累积。 | 公开版本含 28 个简单和 50 个困难对话，并非 78 个工具；工具清单为七类插件下的 28 个工具。每个助手回合前，评测器重置状态并重放参考历史，因此模型错误不会在整段对话中自由累积。成功要求覆盖全部参考调用，且没有成功执行但不匹配参考的状态修改动作。预测器采用旧 OpenAI SDK 接口，openai 依赖未固定；本次未测试兼容性或历史模型可用性。 |

## 用户协作与策略遵循

用户模拟器与领域策略也是实验的一部分。应记录用户能否改变状态，以及被评测的是文本、语音还是知识模式。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [τ-Bench](https://aicanwhat.com/zh/projects/tau-bench/) · [Source](https://github.com/sierra-research/tau2-bench) | 评估遵循策略的客服交互；当前 τ³ 仓库与 τ² 论文覆盖不同的发布范围。 | 原 tau-bench 仓库已明确停止更新任务，tau2-bench 现承载 τ³。需要 Python 3.12–3.13 和模型访问配置。banking 领域在 v1.0.1 前后的结果不可直接比较。文字、语音和知识模式依赖不同；代码采用 MIT。 |

## 缓存与生成的服务环境

模拟可以让工具响应更可控。需检查响应和奖励如何生成，并将合成环境中的完成结果与真实服务结果分别报告。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [StableToolBench](https://aicanwhat.com/zh/projects/stabletoolbench/) · [Source](https://github.com/THUNLP-MT/StableToolBench) | 结合具体服务器、缓存和评分配置，研究缓存或模型模拟的 API 响应。 | 模拟或缓存的 API 响应不能证明真实服务会执行相同动作。仓库现提供 MirrorAPI 与 GPT 两类方案，模型、缓存和评审方式不同。运行需下载工具数据，并准备模型服务或 API 访问。代码采用 Apache 2.0。 |
| [Agent World Model](https://aicanwhat.com/zh/projects/agent-world-model/) · [Source](https://github.com/Snowflake-Labs/agent-world-model) | 在合成 SQLite／MCP 场景中训练或评测；注明纯代码与模型辅助校验的差别，以及封装的结束语义。 | 这些是合成 SQLite／MCP 场景，并非真实生产服务；发布资料区分 1,000 个环境和 10,000 项任务。纯代码与 SQL 加模型评审提供不同证据，应注明模式。OpenEnv 属于集成，不是另一套任务；其 done 动作不会自动评测。所查项目元数据未明确流水线代码许可。 |
| [ToolEmu](https://aicanwhat.com/zh/projects/toolemu/) · [Source](https://github.com/ryoungj/ToolEmu) | 通过模型模拟的工具效果及模型评审研究风险场景，并将模拟与实际执行证据分别记录。 | 工具效果和评分由语言模型生成，并非真实 API 副作用，也不构成独立安全保证。固定版本的资产含 144 个案例，使用 38 个工具包／330 个工具规格；README 的 36／311 是较早清单。须记录模拟器、评审器及模型设置。安装依赖 PromptCoder 和较旧的固定版本库。根 LICENSE 为 Apache-2.0，但 setup.py 的 MIT 分类与之冲突，不应声称许可完全一致。 |

## 选择时的常见问题

### 有效的函数调用能证明任务成功吗？

不能。调用表示可能正确，但工具执行失败、使用了错误状态或改动了错误对象。应将调用级检查与实际流程结果及必要状态约束分别报告。

### 使用 MCP 接口是否让不同环境等价？

不是。接口说明工具如何暴露；任务状态、重置、外部依赖和校验仍由具体环境决定。例如 Agent World Model 的 OpenEnv done 动作本身并不执行校验。

### 比较工具使用分数时需要保留什么条件？

固定任务与评分器版本、划分、工具 schema、初始状态、模型与用户模拟器版本、缓存响应及评审设置。注明调用实际执行、被模拟还是仅做结构检查。统一成功的测量单位，不要把封装记录或版本子集当成独立新任务累加。

## 继续查找

- [应用与工具评测资料](https://aicanwhat.com/zh/apps/?use=evaluation)
- [Harbor 包索引](https://aicanwhat.com/zh/discover/?source=harbor-hub)
- [浏览器交互评测](https://aicanwhat.com/zh/guides/browser-agent-benchmarks/)

本指南基于目录原始来源，使用 AI 辅助研究与写作。分组不是排名；未独立复现实验或验证所有运行功能。

[收录方法](https://aicanwhat.com/zh/about/)
