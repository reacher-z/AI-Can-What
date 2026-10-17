# Computer-use and mobile-agent benchmarks: environments versus datasets

[Website version](https://aicanwhat.com/guides/computer-mobile-agents/) · 2026-10-16

Choose desktop VMs, Android/iOS research apps or static GUI datasets while keeping target OS, host requirements, scoring and access limits separate.

Match the resource to the capability you need to measure. Whole-workflow evaluation needs an executable desktop or phone environment and a defined outcome. Grounding and action-program datasets isolate components. The host running an emulator is not necessarily the operating system an agent is being evaluated on.

## Executable desktop tasks

Start with the target OS and available virtualization. Check task revisions, application licensing and whether resets restore the state needed by the evaluator.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [OSWorld](https://aicanwhat.com/projects/osworld/) · [Source](https://github.com/xlang-ai/OSWorld) | Evaluate multi-application desktop workflows with final-state checks. | Requires VM images and supported providers. This entry covers original OSWorld and OSWorld-Verified; OSWorld 2.0/2.1 is a separate long-horizon benchmark with different tasks and scores. Identify the version when comparing results. Running on a macOS host does not imply macOS task coverage. |
| [OSWorld 2.0](https://aicanwhat.com/projects/osworld-2/) · [Source](https://github.com/xlang-ai/OSWorld-V2) | Study the separate long-horizon Ubuntu-and-web task set, with gated task/assets access and pinned release components. | Public Apache-2.0 harness; task code is auto-gated and labeled Apache-2.0. Complete assets are separately gated with no license declaration in their public card. The current osworld-v2.1 release needs Python >=3.12, an Ubuntu VM, matching self-hosted websites and some task-specific services. Pin all components; its tasks and scores differ from original OSWorld/Verified. The release manifest reports a Task029 setup timeout and incomplete Docker boot verification. |
| [Windows Agent Arena](https://aicanwhat.com/projects/windows-agent-arena/) · [Source](https://microsoft.github.io/WindowsAgentArena/) | Study Windows GUI workflows on the prescribed VM setup. | Setup requires a Windows VM image, Docker and dependencies. The documented evaluation ISO is a time-limited trial; Azure execution can incur costs. |
| [MacArena](https://aicanwhat.com/projects/macarena/) · [Source](https://github.com/MacPaw/MacArena) | Study native macOS interaction with Apple-hardware and VM requirements. | Requires Apple hardware and macOS VM setup. Tasks inherited from macOSWorld carry CC BY-NC 4.0 restrictions; application and OS licenses also apply. |

## Executable mobile workflows

These projects require prepared devices or emulators and particular applications. Keep simulation, real installed apps and scoring methods explicit.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [AndroidWorld](https://aicanwhat.com/projects/androidworld/) · [Source](https://google-research.github.io/android_world/) | Evaluate repeatable Android workflows with parameterized tasks. | Requires a configured Android emulator and the prescribed apps. Host compatibility differs from the Android target; Apple Silicon Docker setup has documented caveats. |
| [AndroidLab](https://aicanwhat.com/projects/androidlab/) · [Source](https://github.com/THUDM/Android-Lab) | Compare Android agents with the released images and instruction data. | Requires the prescribed Android images. Documented execution uses macOS arm64 AVDs or Linux x86_64 Docker; result generation uses a model judge and needs model access. |
| [AppSim-Bench](https://aicanwhat.com/projects/appsim-bench/) · [Source](https://github.com/Acrab-Agentic-Labs/AppSim) | Study controlled simulated Android apps and seeded task state. | These are research simulations, not the named commercial services. Build/install the separate app APKs and configure an Android device/emulator; the documented benchmark uses Android 13/API 33 and Python 3.11. Windows/macOS emulator guidance remains a TODO. No project-level framework license was found; app terms must be checked separately. |
| [iOSWorld](https://aicanwhat.com/projects/iosworld/) · [Source](https://github.com/ljang0/iOSWorld) | Evaluate tasks across seeded research apps in an iOS simulator. | Requires macOS, Xcode and an iOS simulator. These are seeded research apps, not App Store products; the default scoring path uses a model judge. |

## Static screenshots and trajectories

Use these when the research question concerns perception or action prediction. Downloading screenshots does not supply the applications or an executable operating system.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [ScreenSpot-Pro](https://aicanwhat.com/projects/screenspot-pro/) · [Source](https://github.com/likaixin2000/ScreenSpot-Pro-GUI-Grounding) | Measure target localization in high-resolution professional interfaces. | A static target-localization test rather than a desktop VM or task environment. Keep screenshot resolution and language settings comparable; the listed software is not bundled for use. |
| [OmniACT](https://aicanwhat.com/projects/omniact/) · [Source](https://huggingface.co/datasets/Writer/omniact) | Study screen-and-instruction conversion into action programs. | Static examples and reference-based action metrics, not a packaged desktop execution environment. Evaluation target boxes must not be used as test-time inputs. The dataset card declares MIT; platform tags identify screenshot sources. |
| [Android in the Wild](https://aicanwhat.com/projects/android-in-the-wild/) · [Source](https://github.com/google-research/google-research/tree/master/android_in_the_wild) | Study recorded Android demonstrations and action prediction. | Recorded demonstrations and offline action-matching metrics do not provide a live Android environment. Use the published episode splits; data spans Android versions and collection-time app states. |

## Selection questions

### Does running a benchmark on a Mac make it a macOS benchmark?

No. A Mac may host an Android emulator or another OS image. Read the target applications and task environment separately from host architecture, virtualization and driver requirements.

### Can I compare static grounding accuracy with task success?

They measure different units. A correctly localized control may still be followed by an incorrect action or plan. Compare the same task unit, inputs and evaluation protocol, and report component and workflow results separately.

### Are research app replicas the original commercial services?

No. Seeded or simulated apps provide controlled workflows and data. Their results should not be reported as demonstrated success on the named production services without separate evidence.

## Continue exploring

- [Windows evaluation](https://aicanwhat.com/apps/windows/?use=evaluation)
- [macOS evaluation](https://aicanwhat.com/apps/macos/?use=evaluation)
- [Android evaluation](https://aicanwhat.com/apps/android/?use=evaluation)
- [iOS evaluation](https://aicanwhat.com/apps/ios/?use=evaluation)

Compiled from catalog primary sources with AI-assisted research and writing. Groups are not rankings; experiments and complete runtime behavior have not been independently verified.

[Review method](https://aicanwhat.com/about/)
