# 编程 Agent 的基准与训练环境

[网站版本](https://aicanwhat.com/zh/guides/coding-agent-benchmarks/) · 2026-10-16

按 Agent 修改的对象及结果检查方式，比较代码库修复、应用开发、终端任务和生成式训练环境。

先明确任务单位：代码库补丁、应用修改、方案选择，还是终端操作结果，再选择匹配的测试和环境状态。训练任务生成与保留集评测用途不同，即使它们都使用容器及可执行测试。

## 代码库修复

采用明确的问题描述和测试要求；测试通过只能证明被覆盖的行为，不能证明所有产品要求。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [SWE-bench](https://aicanwhat.com/zh/projects/swe-bench/) · [Source](https://www.swebench.com/) | 用项目测试评估真实代码库问题的修复。 | 衡量仓库级代码修复，并非图形界面操作或完整应用生成。Docker 评测需要较多资源，比较时应注明数据集变体和评测框架版本。 |

## 应用开发与方案选择

分别报告编码与决策赛道；面向 Android 源码的基准并不测量手机 Agent 的 GUI 导航能力。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [SWE-Lancer](https://aicanwhat.com/zh/projects/swe-lancer/) · [Source](https://github.com/openai/frontier-evals/blob/main/project/swelancer/README.md) | 分别比较应用代码修复与工程管理者的方案选择。 | 公开版本只是论文更大任务集合的子集。Diamond 的 463 项任务由 198 项编码任务和 265 项管理任务构成，不能将总包与子集相加。代码采用 MIT，底层应用另有条款。原始协议要求在 Linux 上禁用网络；Harbor 修改了提示及测试可见性，且不报告金额指标。 |
| [Android Bench](https://aicanwhat.com/zh/projects/android-bench/) · [Source](https://hub.harborframework.com/datasets/android-bench/android-bench/latest) | 用公开的 Android Bench1.0 构建和测试任务评估 Kotlin／Java 修改。 | 本条目覆盖公开 1.0 任务；Android Bench 2.0 另有私有的 30 项任务。原始 Apache-2.0 框架已归档并转向 Harbor；被测仓库保留各自许可，包括 GPL／AGPL。本地 Harbor 评测需要 x86_64／KVM 及较多资源；归档 README 与包元数据的最低 Python 版本不一致。 |

## 交互式终端工作

这些环境在多步执行中提供反馈；需固定任务镜像、可用命令及最终状态评分器。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [Terminal-Bench](https://aicanwhat.com/zh/projects/terminal-bench/) · [Source](https://www.tbench.ai/) | 在带版本的任务环境中评估多步命令行操作结果。 | 当前仓库是持续更新的基准，所链接论文描述的是 Terminal-Bench 2.0。比较结果时需固定数据集与评测框架版本。运行需要 Harbor 和受支持的沙盒后端；服务费用与任务依赖各不相同。仓库采用 Apache 2.0。 |
| [InterCode](https://aicanwhat.com/zh/projects/intercode/) · [Source](https://intercode-benchmark.github.io/) | 研究 Agent 如何利用编码任务中的错误及执行反馈。 | 需要 Python 3.8+、运行中的 Docker 服务及任务镜像。不同任务类型的配置流程不同；模型驱动的实验脚本需要相应服务访问。它基于实际执行反馈进行评测，并非静态代码数据集。仓库代码采用 MIT。 |

## 训练环境与任务合成

用于收集修复轨迹或构建训练任务；数据规模不等于保留集上的性能成绩。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [SWE-Gym](https://aicanwhat.com/zh/projects/swe-gym/) · [Source](https://github.com/SWE-Gym/SWE-Gym) | 收集经过测试检查的修复轨迹，并训练解法验证器。 | SWE-Gym 提供训练任务，与 SWE-bench 评测集不同。复现说明使用特定 OpenHands 分支，切换版本会影响结果。需要任务容器、仓库数据和模型计算资源。框架代码采用 Apache 2.0，所含项目保留各自许可。 |
| [SWE-smith](https://aicanwhat.com/zh/projects/swe-smith/) · [Source](https://github.com/SWE-bench/SWE-smith) | 基于导致测试失败的修改，合成代码库修复任务。 | 面向训练的任务不是独立保留的 SWE-bench 评测集。需固定任务版本及划分：发布数据规模已有变化，Harbor 的 100 项任务包只是子集。工具包和 Hub 数据声明 MIT，源代码库保留各自条款。需在受支持的 Ubuntu 上使用 Docker；作者不支持 Windows／macOS。Harbor 适配器提示部分合成参考补丁可能失败。 |

## 选择时的常见问题

### 能否将总包与子集的任务数相加？

不能。SWE-Lancer Diamond 的198项编码任务和265项管理任务合计463项。注册表的 all、IC 和 manager 包属于同一项目族，不是三个互不重叠的集合。

### 最新公告是否就是公开可运行的版本？

需检查实际产物。Android Bench 公开链接的是1.0任务集，2.0方法说明描述另一个私有任务集。应对齐可访问的数据、框架与已发布结果的版本。

### 基准适配到 Harbor 后可能改变什么？

封装可能改变提示、可见测试、工具、超时及指标。应保留适配版本及其明确差异；上游索引的项目关联并不证明分数等价。

## 继续查找

- [全部应用评测资料](https://aicanwhat.com/zh/apps/?use=evaluation)
- [Harbor 包索引](https://aicanwhat.com/zh/discover/?source=harbor-hub)
- [网页与游戏生成](https://aicanwhat.com/zh/guides/software-generation/)

本指南基于目录原始来源，使用 AI 辅助研究与写作。分组不是排名；未独立复现实验或验证所有运行功能。

[收录方法](https://aicanwhat.com/zh/about/)
