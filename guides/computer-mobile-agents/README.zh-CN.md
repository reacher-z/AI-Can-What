# 电脑与手机 Agent 评测：交互环境与静态数据

[网站版本](https://aicanwhat.com/zh/guides/computer-mobile-agents/) · 2026-10-16

比较桌面虚拟机、Android/iOS 研究应用及静态 GUI 数据集，区分目标系统、宿主要求、评分和访问限制。

按需要测量的能力选择资料。完整流程评测需要可执行的桌面或手机环境及明确结果；定位和动作程序数据集用于单独研究组件。运行模拟器的宿主系统，不一定是 Agent 任务所针对的操作系统。

## 可执行桌面任务

先看目标系统与可用虚拟化条件，再确认任务版本、应用许可，以及重置是否恢复评分器需要的状态。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [OSWorld](https://aicanwhat.com/zh/projects/osworld/) · [Source](https://github.com/xlang-ai/OSWorld) | 通过最终状态检查评估跨应用桌面流程。 | 需要虚拟机镜像及受支持的运行方式。本条目覆盖原始 OSWorld 和 OSWorld-Verified；OSWorld 2.0／2.1 是任务及评分口径不同的独立长流程基准。比较结果时需注明版本。Mac 主机支持不等于 macOS 任务覆盖。 |
| [OSWorld 2.0](https://aicanwhat.com/zh/projects/osworld-2/) · [Source](https://github.com/xlang-ai/OSWorld-V2) | 研究独立的 Ubuntu 与网页长流程任务集，留意任务／资产访问门槛和固定组件版本。 | 公开框架采用 Apache-2.0；任务代码需通过自动批准的访问门槛，标注 Apache-2.0。完整资产另设访问门槛，公开卡片未声明许可。当前 osworld-v2.1 需 Python >=3.12、Ubuntu 虚拟机、配套自建网站及部分任务专属服务。需固定所有组件版本；任务及成绩不能与原始 OSWorld／Verified 混用。 该发布清单记录 Task029 初始化超时，Docker 启动验证未完成。 |
| [Windows Agent Arena](https://aicanwhat.com/zh/projects/windows-agent-arena/) · [Source](https://microsoft.github.io/WindowsAgentArena/) | 在指定虚拟机配置上研究 Windows GUI 流程。 | 需要 Windows 虚拟机镜像、Docker 和配套依赖。文档使用有期限的评估版 ISO；Azure 运行可能产生费用。 |
| [MacArena](https://aicanwhat.com/zh/projects/macarena/) · [Source](https://github.com/MacPaw/MacArena) | 在满足 Apple 硬件和虚拟机要求的条件下研究原生 macOS 交互。 | 需要 Apple 硬件和 macOS 虚拟机配置。继承自 macOSWorld 的任务采用 CC BY-NC 4.0，另需遵守系统和应用许可。 |

## 科学与工程桌面任务

分别检查任务覆盖和实际可获取的虚拟机镜像。商业软件许可及应用专用产物检查会影响哪些实验可以开展。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [ScienceBoard](https://aicanwhat.com/zh/projects/scienceboard/) · [Source](https://github.com/OS-Copilot/ScienceBoard) | 通过公开的原始虚拟机研究科学工作流；较新的预构建 Docker 镜像仍属于私有评审产物。 | 原始 Ubuntu 虚拟机公开。当前源码新增 Docker 原生后端，但预构建 Docker 镜像被文档列为等待再分发审查的私有评审资产。部分任务依赖 Google 登录或会变化的网页服务。上游报告的 20 项 Docker 验收仅是子集检查，不代表本站复现整个基准。 |
| [CADWorld](https://aicanwhat.com/zh/projects/cadworld/) · [Source](https://github.com/Zdong104/CADWORLD) | 通过保存的产物评估 GUI 驱动的 FreeCAD 操作；CAM 任务需要宿主 FreeCAD 控制台。 | 需要 Linux／KVM Docker 主机及 Ubuntu FreeCAD 虚拟机。CAM 任务的在线评分和离线重评需要主机上的 FreeCAD 1.1.x 控制台；大多数其他检查通过 Python 解析文件。缺失 FreeCAD 可能影响 CAM 评分。200 项 GUI 基准应与论文中的 50 项纯终端消融分别比较。所查根目录及包元数据未找到项目级代码许可。 |
| [EngiWorld](https://aicanwhat.com/zh/projects/engiworld/) · [Source](https://github.com/Hongcheng-Gao/EngiWorld) | 研究工程任务定义，同时考虑公开 Ubuntu 软件镜像覆盖范围更小。 | 发布内容包含 1,301 项任务定义，论文主要实验使用其中 306 项。公开镜像仅覆盖 15 个开源软件环境，所查清单均为 Ubuntu；专有软件镜像需另行取得合许可访问或自行准备。须遵循每项任务的 GUI／CLI 接口要求，并固定任务分类、资产及匹配镜像。 |
| [DeskCraft](https://aicanwhat.com/zh/projects/deskcraft/) · [Source](https://github.com/mrwwk/DeskCraft) | 比较标准 Ubuntu 工作流与独立的交互任务划分；后者由模型驱动的用户模拟器回复。 | 已发布任务的虚拟机系统为 Ubuntu；继承的虚拟机后端代码不能证明存在同等的 Windows 或 macOS 任务集。交互回复使用模型驱动的用户模拟器，可选完成触发器也会调用模型，需固定这些配置。公开虚拟机与任务缓存分别下载。README 推荐 Python 3.10+，包元数据则要求 3.12+，部分交互示例仍用旧路径。代码及缓存卡声明 Apache-2.0，虚拟机仓库未声明许可。本次仅核查来源，未运行任务。 |

## 可执行移动流程

这些项目需要准备设备或模拟器和特定应用；应明确区分模拟应用、真实安装应用及评分方式。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [AndroidWorld](https://aicanwhat.com/zh/projects/androidworld/) · [Source](https://google-research.github.io/android_world/) | 通过参数化任务评估可重复的 Android 流程。 | 需要配置 Android 模拟器及指定应用。主机兼容性与 Android 目标平台应分开理解，Apple Silicon 的 Docker 方案有已知限制。 |
| [AndroidLab](https://aicanwhat.com/zh/projects/androidlab/) · [Source](https://github.com/THUDM/Android-Lab) | 使用发布的镜像和指令数据比较 Android Agent。 | 需要指定 Android 镜像。文档提供 macOS arm64 AVD 与 Linux x86_64 Docker 两种运行方式；结果生成使用模型评审，需要模型访问。 |
| [AppSim-Bench](https://aicanwhat.com/zh/projects/appsim-bench/) · [Source](https://github.com/Acrab-Agentic-Labs/AppSim) | 研究可控模拟 Android 应用及预置任务状态。 | 这些是研究模拟应用，不是对应名称的商业服务。需单独构建或安装应用 APK 并配置 Android 设备或模拟器；文档基准使用 Android 13/API 33 和 Python 3.11。Windows/macOS 模拟器说明仍为 TODO。未找到框架项目级许可，各应用条款需分别检查。 |
| [iOSWorld](https://aicanwhat.com/zh/projects/iosworld/) · [Source](https://github.com/ljang0/iOSWorld) | 在 iOS 模拟器中评估预置研究应用的跨应用任务。 | 需要 macOS、Xcode 和 iOS 模拟器。应用使用预置研究数据，并非 App Store 产品；默认评分流程采用模型评审。 |
| [OS-Sentinel / MobileRisk-Live](https://aicanwhat.com/zh/projects/os-sentinel/) · [Source](https://github.com/OS-Copilot/OS-Sentinel) | 研究移动操作和轨迹的安全检测；APK 配置缺口及许可冲突与安全性声明分别记录。 | 代码及任务场景已公开，但需另行准备 Android 应用。root.py 中四个 APK 下载地址仍为占位符，需人工按版本文件准备。安全检测不等于安全行为或任务完成保证。README 的 MIT 徽章与 Apache-2.0 LICENSE 冲突；MobileRisk 数据未提供公开许可卡。 |

## 静态截图与轨迹

当问题涉及感知或动作预测时使用此类资料；下载截图并不会获得对应应用或可执行操作系统。

| 项目与证据 | 适合研究的问题 | 配置与限制 |
| --- | --- | --- |
| [ScreenSpot-Pro](https://aicanwhat.com/zh/projects/screenspot-pro/) · [Source](https://github.com/likaixin2000/ScreenSpot-Pro-GUI-Grounding) | 在高分辨率专业界面中测量目标定位能力。 | 属于静态目标定位测试，并非桌面虚拟机或任务环境。比较时应保持截图分辨率与语言设置一致；不提供所列专业软件的使用副本。 |
| [OmniACT](https://aicanwhat.com/zh/projects/omniact/) · [Source](https://huggingface.co/datasets/Writer/omniact) | 研究从屏幕及指令到动作程序的转换。 | 提供静态样本和基于参考的动作指标，并非打包好的桌面执行环境。测试时不能将评估用目标框作为输入。数据卡标注 MIT；平台标签表示截图来源。 |
| [Android in the Wild](https://aicanwhat.com/zh/projects/android-in-the-wild/) · [Source](https://github.com/google-research/google-research/tree/master/android_in_the_wild) | 研究记录的 Android 演示与动作预测。 | 记录式演示及离线动作匹配指标不等同于可运行的 Android 环境。应遵循公开的 episode 划分；数据包含不同 Android 版本和采集时的应用状态。 |

## 选择时的常见问题

### 在 Mac 上运行基准，就代表评测 macOS 吗？

不是。Mac 可能承载 Android 模拟器或其他系统镜像。应将目标应用及任务环境，与宿主架构、虚拟化和驱动要求分别检查。

### 静态定位准确率能和任务成功率直接比较吗？

两者的测量单位不同。控件定位正确后仍可能出现错误动作或计划。比较时应统一任务单位、输入和评测协议，并分别报告组件与完整流程结果。

### 研究应用仿真就是原商业服务吗？

不是。预置或模拟应用提供可控流程和数据，未经独立证明，不能把实验结果描述为在相应生产服务上完成任务。

## 继续查找

- [Windows 评测](https://aicanwhat.com/zh/apps/windows/?use=evaluation)
- [macOS 评测](https://aicanwhat.com/zh/apps/macos/?use=evaluation)
- [Android 评测](https://aicanwhat.com/zh/apps/android/?use=evaluation)
- [iOS 评测](https://aicanwhat.com/zh/apps/ios/?use=evaluation)

本指南基于目录原始来源，使用 AI 辅助研究与写作。分组不是排名；未独立复现实验或验证所有运行功能。

[收录方法](https://aicanwhat.com/zh/about/)
