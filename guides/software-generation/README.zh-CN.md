# 网页与游戏生成评测：外观、交互和执行

[网站版本](https://aicanwhat.com/zh/guides/software-generation/) · 2026-10-16

按输入资料、生成产物、测试行为及已发布评测材料，比较网页重建和游戏开发基准。

先明确生成软件需要复现什么：截图、交互轨迹、局部修改，还是完整可运行项目。这些目标不同。视觉相似不代表功能等价；游戏可玩也不能自动证明主观质量或通用游戏策略。

## 网页重建

匹配输入及测试行为：静态图像、指定状态转换、视频轨迹或仪表盘探索；不要从视觉分数推断后端等价。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [Design2Code](https://aicanwhat.com/zh/projects/design2code/) · [Source](https://github.com/NoviScl/Design2Code) | 评估根据网页截图进行的视觉重建。 | 评估视觉还原，不验证后端功能或交互任务完成情况。作者限定研究用途；Design2Code 与 Design2Code-Hard 为不同测试集。 |
| [Interaction2Code](https://aicanwhat.com/zh/projects/interaction2code/) · [Source](https://github.com/WebPAI/Interaction2Code) | 同时评估指定交互与可见页面状态。 | 评估指定交互的状态变化，不能证明完整网站流程或后端等价。代码与数据可公开查看，但已核查的仓库及数据卡未注明项目级代码许可或数据许可。 |
| [IWR-Bench](https://aicanwhat.com/zh/projects/iwr-bench/) · [Source](https://github.com/SIGMME/IWR-Bench) | 重建视频演示的可见状态及交互。 | 采用预设轨迹和模型辅助评审，不能证明完整网站或后端等价。公开数据集标注 Apache 2.0；未找到基准代码的项目级许可。运行需配置浏览器与模型。 |
| [Dashboard2Code (DashboardMimic)](https://aicanwhat.com/zh/projects/dashboard2code/) · [Source](https://github.com/nth2000/Dashboard2Code) | 在明确数据访问限制的前提下研究仪表盘探索与生成。 | 数据访问要求共享联系信息并经人工批准，本次未访问受限内容。需配置模型适配器与评估脚本，包括默认空的批处理运行列表。未找到项目级代码许可或公开可见的数据许可。 |

## 游戏项目与世界产物

现有项目修改、完整游戏和生成的三维场景需要不同检查；解读比较结果前，应固定引擎及任务版本。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [GameDevBench](https://aicanwhat.com/zh/projects/gamedevbench/) · [Source](https://github.com/waynchi/gamedevbench) | 评估对已有 Godot 项目的限定范围修改。 | 测试游戏开发，而非 Agent 玩游戏的能力。正式比较要求严格使用 Godot 4.4.1 并固定任务集；需要 Python 3.10+，严格运行模式注明 Linux Bubblewrap/Xvfb 依赖。仓库采用 Apache 2.0。 |
| [GameCraft-Bench](https://aicanwhat.com/zh/projects/gamecraft-bench/) · [Source](https://github.com/FreedomIntelligence/gamecraft-bench) | 通过启动产物及输入重放评估完整二维 Godot 游戏。 | 覆盖二维 Godot 游戏生成，并不代表通用三维、Unity/Unreal 开发或主观乐趣评测。文档固定 Godot 4.6.2，要求 Python 3.12+、Harbor 及 Linux 显示和录制工具；评分使用模型评审。代码采用 Apache 2.0，素材许可分别记录。 |
| [V-GameGym (SKYLENAGE-GameCodeGym)](https://aicanwhat.com/zh/projects/v-gamegym/) · [Source](https://github.com/alibaba/SKYLENAGE-GameCodeGym) | 结合代码、截图及短时录像比较 Pygame 生成。 | 使用模型评审生成产物，并非评测长时游戏策略。README 命令示例与已发布脚本参数不同，需要配置路径和评审端点。要求 Python 3.10+、Pygame 和模型访问。代码及数据均声明 Apache 2.0。 |
| [GameCode4D (Code2Games)](https://aicanwhat.com/zh/projects/gamecode4d/) · [Source](https://huggingface.co/datasets/AIGeeksGroup/GameCode4D) | 查看游戏世界提示和 Blender 产物，同时保留未发布流程组件的说明。 | 当前数据卡列出 20 个提示变体，但公开 16 个 .blend 文件；论文评估的是 10 个提示。公开代码说明 Blender 输出，不能视为完整发布的 UE5 评测流程。需要外部场景、动画角色及素材或模型服务。已核查来源未注明代码或数据许可。 |

## 选择时的常见问题

### 哪类基准适合截图转代码？

可从 Design2Code 等视觉重建基准开始。如果要求包含状态变化或交互轨迹，应查看 Interaction2Code 或 IWR-Bench 及其具体测试的转换。

### 游戏开发和玩游戏是同一种评测吗？

不是。开发基准评估生成或修改的软件产物，游戏环境则评估 Agent 在世界中的行动。报告实验时应明确测量的是哪一种能力。

### 论文公开就代表完整评分流程已发布吗？

不是。需分别检查代码、任务数据、素材、访问审批和评审配置。Dashboard2Code 的数据需申请；已核查的 GameCode4D 发布仅覆盖所描述引擎流程的一部分。

## 继续查找

- [全部游戏评测资料](https://aicanwhat.com/zh/games/?use=evaluation)
- [全部网页评测资料](https://aicanwhat.com/zh/websites/?use=evaluation)

本指南基于目录原始来源，使用 AI 辅助研究与写作。分组不是排名；未独立复现实验或验证所有运行功能。

[收录方法](https://aicanwhat.com/zh/about/)
