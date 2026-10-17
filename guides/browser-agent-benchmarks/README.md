# Browser agent benchmarks: controlled sites, live tasks and recorded data

[Website version](https://aicanwhat.com/guides/browser-agent-benchmarks/) · 2026-10-16

Compare browser-agent resources by interaction setting, scoring and setup: self-hosted sites, live-web evaluation, recorded trajectories and shared frameworks.

Choose the evaluation setting before choosing a benchmark. Controlled sites let you reset task state; live-web tasks expose changing content and dependencies; recorded trajectories test predictions without an open-ended browser run. A shared framework can connect these resources without making their scores interchangeable.

## Controlled interaction tasks

Choose these when resettable state and a specified task outcome are central to the experiment. Hosting and approved instance access are part of the setup.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [MiniWoB++](https://aicanwhat.com/projects/miniwob-plusplus/) · [Source](https://miniwob.farama.org/) | Isolate short web-control skills in synthetic tasks. | Synthetic tasks isolate interaction skills rather than full production workflows. The project is in maintenance mode; its Python interface documents Linux/macOS and Chrome or Chromium setup. |
| [WebArena](https://aicanwhat.com/projects/webarena/) · [Source](https://webarena.dev/) | Evaluate multi-step work on self-hosted sites with outcome checks. | Reproducible evaluation requires self-hosted services and controlled state resets; shared demos do not replace that setup. WebArena-Verified separately revises the same task family and evaluator. Original/Verified and full/Hard task counts are not additive, and evaluator versions must accompany reported scores. |
| [WebArena-Verified](https://aicanwhat.com/projects/webarena-verified/) · [Source](https://github.com/ServiceNow/webarena-verified) | Use the separately maintained evaluator and trace artifacts for the same WebArena task family; do not add its task counts to the original. | This revises the original WebArena task family. Its 812 full tasks and 258-task Hard subset in v1.2.3 are not independent tasks to add to WebArena. Offline scoring requires the expected response and trace artifacts; new trajectories still need sites and resets. Pin evaluator/data/image versions; scores need not match the original evaluator. |
| [VisualWebArena](https://aicanwhat.com/projects/visualwebarena/) · [Source](https://jykoh.com/vwa) | Add image-dependent reasoning to controlled website tasks. | Requires hosting the provided sites and matching the task configuration. The repository documents Python-version constraints; no hosted evaluation service is claimed. |
| [WorkArena](https://aicanwhat.com/projects/workarena/) · [Source](https://github.com/ServiceNow/WorkArena) | Study enterprise workflows when the required ServiceNow access is available. | ServiceNow instances currently require approved access through the authors' gated dataset. WorkArena++ extends the original suite; task versions must be reported. |

## Live-web evaluation

These settings exercise current external websites. Preserve dates and judge details; changes outside the agent can affect a run.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [WebVoyager](https://aicanwhat.com/projects/webvoyager/) · [Source](https://github.com/MinorJerry/WebVoyager) | Study multimodal browsing trajectories with an automated visual judge. | Depends on changing external websites, Chrome/Selenium and model access. Its automated evaluation uses a vision-language judge; results are not deterministic state-check scores. |
| [Online-Mind2Web](https://aicanwhat.com/projects/online-mind2web/) · [Source](https://github.com/OSU-NLP-Group/Online-Mind2Web) | Evaluate current-site task completion with recorded action and screenshot evidence. | Live sites and task definitions change; retain the task revision and run date. Automatic judging is model-based, and leaderboard human review has its own submission and pricing policies. |
| [ClawBench](https://aicanwhat.com/projects/clawbench/) · [Source](https://github.com/TIGER-AI-Lab/ClawBench) | Study live workflows with request and trajectory evidence; task-specific interception does not block every external action. | Runs touch production websites and may need accounts or external services. Interception blocks only requests matching a task schema; nonmatching requests continue live, and placeholder schemas do not block submissions. A blocked request plus judge approval is not a committed real-world result. Current V1/V2 folders have 152/129 tasks; historical counts and scoring protocols differ. |
| [Mind2Web 2](https://aicanwhat.com/projects/mind2web-2/) · [Source](https://github.com/OSU-NLP-Group/Mind2Web-2) | Evaluate long-horizon search and cited answers with judge agents; the full task/evaluator distribution is gated. | Distinct from offline Mind2Web action prediction and Online-Mind2Web navigation. Public Git code includes 10 development evaluators; current full task/evaluator files on Hub are auto-gated and were not accessed. Full evaluator release was announced in October 2025, so the paper-era private-test description is historical. Live pages and model judgments require version/date controls. |
| [WebBench](https://aicanwhat.com/projects/webbench/) · [Source](https://github.com/Halluminate/WebBench) | Find versioned live-site instructions while supplying your own agent, authorized accounts and outcome assessment. | The repository publishes CSV tasks and results, not a complete resettable environment or evaluator package. WRITE tasks change real account state and need appropriate test-account authorization. The current main CSV has 2,647 records while the README reports 2,454; pin the file. All 315 HITL rows also occur in the main collection. |

## Recorded demonstrations

Use these for action prediction, instruction following or component studies. They are not substitutes for running an agent freely on a live website.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [Mind2Web](https://aicanwhat.com/projects/mind2web/) · [Source](https://osu-nlp-group.github.io/Mind2Web/) | Study generalization across held-out tasks, sites and domains using recorded actions. | The original benchmark evaluates recorded actions rather than executing live websites. Dataset and code licenses differ; use the stated splits and macro-average metrics for paper comparisons. |
| [WebLINX](https://aicanwhat.com/projects/weblinx/) · [Source](https://mcgill-nlp.github.io/weblinx/) | Study multi-turn browsing instructions and demonstrated actions. | Evaluation follows recorded demonstrations rather than freely executing live websites. Data uses CC BY-NC-SA 4.0; BrowserGym/WebLINX 1.1 changes evaluated steps and must be distinguished from 1.0. |

## Shared experiment interface

A common interface can reduce integration work while leaving each benchmark’s environment and scoring assumptions intact.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [BrowserGym](https://aicanwhat.com/projects/browsergym/) · [Source](https://github.com/ServiceNow/BrowserGym) | Connect supported web benchmarks to a common research interface. | A research framework rather than a new website task collection. Each integrated benchmark keeps its own setup, access and evaluation requirements. |

## Selection questions

### Can a screenshot or recorded action benchmark prove end-to-end task completion?

No. Target localization and action prediction measure components. End-to-end completion needs an executed trajectory and the benchmark’s outcome check or stated judging procedure.

### What should an evaluation report preserve?

Record the benchmark revision, task split, browser observation/action interface, reset procedure, model and tool access, judge configuration and run date. Changing these can change what the score measures.

### Is BrowserGym itself another independent task set?

It is a framework integrating multiple resources. Each benchmark retains its own setup and access requirements. Do not add framework integrations to the underlying task counts as new independent projects.

## Continue exploring

- [All web evaluation resources](https://aicanwhat.com/websites/?use=evaluation)
- [BrowserGym upstream configurations](https://aicanwhat.com/discover/?source=browsergym)

Compiled from catalog primary sources with AI-assisted research and writing. Groups are not rankings; experiments and complete runtime behavior have not been independently verified.

[Review method](https://aicanwhat.com/about/)
