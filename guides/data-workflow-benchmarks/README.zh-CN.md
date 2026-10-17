# 数据 Agent 评测：数据库、笔记本与研究流程

[网站版本](https://aicanwhat.com/zh/guides/data-workflow-benchmarks/) · 2026-10-16

比较数据工程、代码执行分析与机器学习实验资料，区分最终答案检查、工作流程验证和环境验证。

先定义正确结果，再选择环境。数据工程任务可能检查结果表，分析基准可能只给最终答案评分，桌面流程则可能检查应用状态。这些检查暴露的错误不同，不宜混合成一个不加区分的分数。

## 数据库与数据转换

区分本地数据库副本与操作真实云账号的任务；应对齐数据库版本、初始化及具体结果表或查询检查。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [ADE-bench](https://aicanwhat.com/zh/projects/ade-bench/) · [Source](https://github.com/dbt-labs/ade-bench) | 通过数据库测试及预期结果评估 dbt／项目修改。 | DuckDB 任务会把本地数据库复制到任务容器。Snowflake 任务使用真实账号，创建或替换试验数据库、用户及角色，且会保留这些对象；上游建议使用独立测试账号。数据库及项目变体因任务而异。固定的 Harbor 包含 48 项 DuckDB+dbt 任务，不能代表当前源码中的全部任务。 |
| [BIRD-Interact](https://aicanwhat.com/zh/projects/bird-interact/) · [Source](https://bird-interact.github.io/) | 在交互式数据库环境中研究需求澄清及 SQL 执行。 | 完整评测需要向作者单独申请真值与测试文件。旧版和 ADK 运行器、数据集及任务数量不同，应核对所选版本及数据库初始化。ADK 是该基准的一种实现，不另算一套基准。代码采用 MIT，数据采用 CC BY-SA 4.0。 |

## 代码执行型分析

执行环境让计算得以完成，答案评分器判断报告结果是否匹配参考值；两者都需要检查。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [BixBench](https://aicanwhat.com/zh/projects/bixbench/) · [Source](https://github.com/Future-House/BixBench) | 使用公开笔记本环境及选定答案评分器评估计算生物学分析。 | v1.5 修订并展平为 205 道问题；v1.0 有 296 道问题，两者成绩不能直接等同。公开划分名为 train，但包含基准答案及不得进入训练语料的声明。开放式答案可能需要模型判分。论文、README 与当前元数据的胶囊数量不一致；Harbor 的笔记本／CLI 变体也改变了工具、提示及评分细节。 |
| [DABstep](https://aicanwhat.com/zh/projects/dabstep/) · [Source](https://huggingface.co/datasets/adyen/DABstep) | 结合公开 Agent 基线和答案评分协议，研究多文件业务数据推理。 | 公开 default 文件有 450 道问题，答案字段为空；10 道附答案的 dev 题中有 6 个 ID 与其重叠。评分检查最终答案，不验证笔记本正确性或 GUI 任务完成。Harbor 从已评分的公开提交重建 default 标签，其成绩尚不能视作官方隐藏答案评测的等价结果。当前 Space 已关闭新的人工验证申请，但仍开放未验证提交。 |

## 电子表格产物与办公工具

文件正确性和工具协作不同于原生 GUI 导航。应记录工作簿重算、评分后端，以及邮件和日历操作是否为模拟。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [SpreadsheetBench](https://aicanwhat.com/zh/projects/spreadsheetbench/) · [Source](https://github.com/RUCKBReasoning/SpreadsheetBench) | 通过工作簿测试案例评估表格编辑；Verified 是原始发布的子集。 | 完整发布包含 912 条指令；Verified 是经专家标注的 400 项子集，不是新增 400 项任务。代码仍保留较早的 200 示例配置路径。判分前需通过 LibreOffice 或 Excel 重算公式结果，并记录工作簿版本及计算后端。这是文件编辑评测，不是封装好的 GUI 导航基准。 |
| [SpreadsheetBench 2](https://aicanwhat.com/zh/projects/spreadsheetbench-2/) · [Source](https://github.com/RUCKBReasoning/SpreadsheetBench-2) | 评估独立的商业表格工作流；VLM 图表评分可直接接收 PNG，XLSX 图表提取则需要 Windows Excel/WPS COM。 | 这是新的工作流任务集，不是原基准的 Verified 子集。评分前需重算输入、参考及输出工作簿。从 XLSX 提取图表进行视觉语言模型评分，需要 Windows 上的 Excel／WPS COM；评分器也直接接受 PNG 输出。数据标注 MIT，但未找到原创评测代码的根目录许可。README 的根目录 Dockerfile 命令与文件实际位于 SWE-agent/ 的位置不符。 |
| [OfficeBench](https://aicanwhat.com/zh/projects/officebench/) · [Source](https://github.com/zlwang-cs/OfficeBench) | 研究本地文档及模拟邮件／日历文件上的结构化工具协作，区别于原生 Office GUI 会话。 | 发布的“应用”是在 Docker 工作区内由 Python 实现的工具，不是原生 Microsoft Office GUI 会话。邮件操作写入本地 .eml 文件，日历操作写入 .ics 文件，并非真实账号集成。需 Python 3.10、Docker、文档／OCR 依赖及模型访问；旧镜像配置需要本地模型密钥文件，且 Ubuntu 基础镜像未固定版本。 |

## 桌面流程与机器学习实验

这些资料涉及更广泛的应用或实验状态；账号、算力与任务资产可能是环境组成部分，而不只是输入文件。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [Spider2-V](https://aicanwhat.com/zh/projects/spider2-v/) · [Source](https://spider2-v.github.io/) | 评估结合图形工具、代码和状态检查的数据流程。 | 需要预设 Ubuntu 虚拟机和配套依赖。部分任务需要真实云账户及凭证；有账户／无账户、简要／详细指令属于不同评测设置。 |
| [MLGym](https://aicanwhat.com/zh/projects/mlgym/) · [Source](https://github.com/facebookresearch/MLGym) | 研究修改机器学习方法并进行迭代实验的 Agent。 | 截至本次核查，作者仓库已归档，虽然旧 README 仍有维护说明。实验依赖 Docker/Podman，以及具体任务所需的 GPU 和数据。多数代码采用 CC BY-NC 4.0，部分组件采用 MIT/Apache，并非统一允许商业使用。 |

## 选择时的常见问题

### 划分名为 train 是否代表可用于训练或能保证评测有效？

名称并不足够。BixBench 的公开划分叫 train，但含有不得纳入训练语料的防污染声明。应保留作者使用说明，并与数据许可分别记录。

### 本地适配器的标签总是官方隐藏答案吗？

不是。DABstep 的 default 文件不提供答案，其中六道题也出现在附答案的 dev 集中。已核查的 Harbor 适配器从已评分公开提交重建标签，尚不能认定与官方评测等价。

### 应怎样报告数据规模？

注明单位与版本：问题、唯一任务 ID、胶囊、ready 任务目录或适配器选中的任务。开发划分可能与测试 ID 重叠，一个胶囊也可能包含多道问题；应保留差异，避免直接累加。

## 继续查找

- [全部应用评测资料](https://aicanwhat.com/zh/apps/?use=evaluation)
- [Harbor 包索引](https://aicanwhat.com/zh/discover/?source=harbor-hub)
- [编程 Agent 资料](https://aicanwhat.com/zh/guides/coding-agent-benchmarks/)

本指南基于目录原始来源，使用 AI 辅助研究与写作。分组不是排名；未独立复现实验或验证所有运行功能。

[收录方法](https://aicanwhat.com/zh/about/)
