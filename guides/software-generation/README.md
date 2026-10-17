# Web and game generation benchmarks: appearance, interaction and execution

[Website version](https://aicanwhat.com/guides/software-generation/) · 2026-10-16

Compare webpage reconstruction and game-development benchmarks by supplied inputs, generated artifact, tested behavior and released evaluation materials.

Specify what the generated software must reproduce: a written specification, a screenshot, an interaction trace, a scoped edit or a complete runnable project. These are different targets. Visual similarity does not establish functional equivalence, and a playable game does not automatically demonstrate subjective quality or a general game-playing policy.

## Webpage reconstruction

Match the input and tested behavior: a written specification, still image, specified state transitions, video trajectory or dashboard exploration. Do not infer backend equivalence from a visual score.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [WebGen-Bench](https://aicanwhat.com/projects/webgen-bench/) · [Source](https://github.com/mnluzimu/WebGen-Bench) | Evaluate interactive websites generated from instructions using functional and appearance checks. | Functional scoring uses a WebVoyager VLM judge, so outcomes can vary with the judge and configuration. Requires a generator, browser stack and model access. Public Hub data is MIT-labeled; no project-wide license for the original code was located. Harbor changes timeouts and uses work-in-progress reference apps; report the harness and judge. |
| [Design2Code](https://aicanwhat.com/projects/design2code/) · [Source](https://github.com/NoviScl/Design2Code) | Evaluate visual reconstruction from supplied webpage screenshots. | Evaluates visual reconstruction rather than working backend features or interactive task completion. The authors specify research-only use; Design2Code and Design2Code-Hard are distinct test sets. |
| [Interaction2Code](https://aicanwhat.com/projects/interaction2code/) · [Source](https://github.com/WebPAI/Interaction2Code) | Evaluate specified interactions as well as visible page states. | Evaluates specified interaction transitions rather than complete site workflows or backend equivalence. Code and data are public, but no project-level code license or dataset license was found in the reviewed repository and data card. |
| [IWR-Bench](https://aicanwhat.com/projects/iwr-bench/) · [Source](https://github.com/SIGMME/IWR-Bench) | Reconstruct visible states and interactions demonstrated in a video. | Uses predefined trajectories and model-assisted judging, not proof of complete site or backend equivalence. The public dataset is marked Apache 2.0; no project-level license was found for the benchmark code. Requires browser and model setup. |
| [Dashboard2Code (DashboardMimic)](https://aicanwhat.com/projects/dashboard2code/) · [Source](https://github.com/nth2000/Dashboard2Code) | Inspect dashboard exploration and generation with explicit data-access constraints. | Dataset access requires shared contact details and manual approval; gated contents were not accessed. Model adapters and evaluation scripts need configuration, including an empty batch-run list. No project-level code or publicly visible dataset license was found. |

## Game projects and game-world artifacts

An existing-project edit, a complete game and a generated 3D scene call for different checks. Pin engine and task versions before interpreting comparisons.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [GameDevBench](https://aicanwhat.com/projects/gamedevbench/) · [Source](https://github.com/waynchi/gamedevbench) | Evaluate scoped edits to existing Godot projects. | Tests game development, not an agent's ability to play a game. Official comparisons require exactly Godot 4.4.1 and a pinned task set. Python 3.10+ is required; strict runs document Linux Bubblewrap/Xvfb dependencies. Repository license is Apache 2.0. |
| [GameCraft-Bench](https://aicanwhat.com/projects/gamecraft-bench/) · [Source](https://github.com/FreedomIntelligence/gamecraft-bench) | Evaluate complete 2D Godot games through launched artifacts and replayed input. | Covers 2D Godot generation, not general 3D/Unity/Unreal development or subjective fun. The documented setup pins Godot 4.6.2, Python 3.12+, Harbor and Linux display/recording tools. Scoring uses a model judge. Code is Apache 2.0; asset licenses are recorded separately. |
| [V-GameGym (SKYLENAGE-GameCodeGym)](https://aicanwhat.com/projects/v-gamegym/) · [Source](https://github.com/alibaba/SKYLENAGE-GameCodeGym) | Compare Pygame generation using code, screenshots and short recordings. | Measures generated artifacts with model judges, not long-horizon game-playing policies. README command examples differ from the shipped script arguments, so paths and judge endpoints need configuration. Requires Python 3.10+, Pygame and model access. Code and dataset declare Apache 2.0. |
| [GameCode4D (Code2Games)](https://aicanwhat.com/projects/gamecode4d/) · [Source](https://huggingface.co/datasets/AIGeeksGroup/GameCode4D) | Inspect game-world prompts and Blender artifacts while tracking missing pipeline components. | The current data card lists 20 prompt variants but exposes 16 .blend files; the paper evaluated 10 prompts. Public code documents Blender outputs, not a complete released UE5 evaluation pipeline. Requires external scenes, animated characters and asset/model services. No code or dataset license was stated in the reviewed sources. |

## Selection questions

### Which benchmark matches screenshot-to-code work?

Start with a visual reconstruction benchmark such as Design2Code. If the requirement includes state changes or interaction traces, inspect Interaction2Code or IWR-Bench and their exact tested transitions.

### Are game development and game playing the same evaluation?

No. Development benchmarks evaluate generated or edited software artifacts. Game-playing environments evaluate an agent’s actions inside a world. Report which side of that boundary the experiment measures.

### Does a public paper mean the complete evaluator is available?

No. Inspect code, task data, assets, access approval and judge configuration separately. Dashboard2Code has gated data; the reviewed GameCode4D release exposes only part of the described engine pipeline.

## Continue exploring

- [All game evaluation resources](https://aicanwhat.com/games/?use=evaluation)
- [All web evaluation resources](https://aicanwhat.com/websites/?use=evaluation)

Compiled from catalog primary sources with AI-assisted research and writing. Groups are not rankings; experiments and complete runtime behavior have not been independently verified.

[Review method](https://aicanwhat.com/about/)
