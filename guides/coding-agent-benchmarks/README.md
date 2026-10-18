# Coding-agent benchmarks and training environments

[Website version](https://aicanwhat.com/guides/coding-agent-benchmarks/) · 2026-10-16

Compare repository repair, application development, terminal tasks and generated training environments by what the agent changes and how outcomes are checked.

First identify the work unit: a repository patch, an application change, a proposal decision or a terminal outcome. Then choose matching tests and environment state. Training-task generation and held-out evaluation serve different purposes, even when both use containers and executable tests.

## Repository repair

Use a defined issue and test contract. Passing tests establishes only the behavior those tests cover, not every product requirement.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [SWE-bench](https://aicanwhat.com/projects/swe-bench/) · [Source](https://www.swebench.com/) | Evaluate real repository issue resolution against project tests. | Measures repository-level code repair, not GUI operation or complete app generation. Docker evaluation needs substantial resources; identify the dataset variant and harness version in comparisons. |
| [SWE-bench Pro](https://aicanwhat.com/projects/swe-bench-pro/) · [Source](https://github.com/scaleapi/SWE-bench_Pro-os) | Evaluate the distinct long-horizon repair corpus with pinned V2 tasks and re-grading; older Harbor packages are not proven equivalent. | Current public V2 has 642 tasks; HARD-51 is a subset, and legacy v1 has 731. The paper's broader collection includes nonpublic tracks. Frozen Harbor packages still advertise 731 and are not proven equivalent to V2. V2's reported protocol keeps the agent phase offline and re-grades captured patches in fresh containers. Do not combine versions, subsets or namespaces into an additive task count. |

## Application development and proposal decisions

Keep coding and decision tracks separate. A benchmark targeting Android source code does not measure a phone agent navigating the GUI.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [SWE-Lancer](https://aicanwhat.com/projects/swe-lancer/) · [Source](https://github.com/openai/frontier-evals/blob/main/project/swelancer/README.md) | Compare application-code fixes and engineering-manager proposal choices as separate tracks. | The public release is a subset of the paper's broader task collection. Diamond's 463 tasks comprise 198 coding and 265 manager tasks; combined and split packages must not be added together. Code is MIT, with underlying application terms separate. Valid original runs disable internet on Linux. Harbor changes prompts/test visibility and omits the monetary metric. |
| [Android Bench](https://aicanwhat.com/projects/android-bench/) · [Source](https://hub.harborframework.com/datasets/android-bench/android-bench/latest) | Evaluate Kotlin/Java changes with the public Android Bench 1.0 build-and-test tasks. | This entry covers public 1.0 tasks; Android Bench 2.0 has a separate private 30-task set. The original Apache-2.0 harness is archived and points to Harbor. Evaluated repositories retain their own licenses, including GPL/AGPL. Local Harbor evaluation requires x86_64/KVM and substantial resources; the archived README and package metadata disagree on Python minimums. |

## Interactive terminal work

These environments return execution feedback over multiple steps. Pin task images, available commands and the final-state verifier.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [Terminal-Bench](https://aicanwhat.com/projects/terminal-bench/) · [Source](https://www.tbench.ai/) | Evaluate multi-step command-line outcomes in versioned task environments. | The current repository is a continuously updated benchmark, while the linked paper describes Terminal-Bench 2.0. Pin dataset and harness versions for comparisons. Harbor and a supported sandbox backend are required; provider costs and task dependencies vary. Repository license is Apache 2.0. |
| [InterCode](https://aicanwhat.com/projects/intercode/) · [Source](https://intercode-benchmark.github.io/) | Study how an agent reacts to errors and execution feedback in coding tasks. | Requires Python 3.8+ and a running Docker service with task images. Included task types and setup paths differ; model-driven experiment scripts require configured provider access. This is execution-based evaluation rather than a static code dataset. Repository code is MIT. |

## Correctness-preserving optimization

Runtime improvement is meaningful only alongside correctness evidence and controlled hardware, dependencies and timing conditions.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [AlgoTune](https://aicanwhat.com/projects/algotune/) · [Source](https://algotune.io/) | Measure solver speedups with generated held-out inputs; an adapter reward of 1.0 alone does not establish a correct solution. | Timing depends on hardware, library versions, calibration and parallel contention. The 154 task families each generate many inputs; input counts are not additional tasks. Original aggregate speedup, AlgoTune-Pass resolve rate and Harbor rewards are different measures. Harbor documents a 1.0 floor for invalid or slower solutions, so that reward alone does not prove correctness. |

## Training environments and task synthesis

Use these to collect repair trajectories or construct training tasks. Their size is not a held-out performance score.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [SWE-Gym](https://aicanwhat.com/projects/swe-gym/) · [Source](https://github.com/SWE-Gym/SWE-Gym) | Collect test-verified repair trajectories and train solution verifiers. | SWE-Gym supplies training tasks and is distinct from SWE-bench evaluation sets. Reproduction instructions use a specific OpenHands fork; switching versions can change outcomes. Task containers, repository data and model compute are required. Framework code is Apache 2.0; bundled projects retain their licenses. |
| [SWE-smith](https://aicanwhat.com/projects/swe-smith/) · [Source](https://github.com/SWE-bench/SWE-smith) | Synthesize repository repair tasks from test-failing changes. | Training-oriented tasks are not a held-out SWE-bench evaluation set. Pin the task revision and partition: published dataset sizes have changed, and Harbor's 100-task package is only a slice. Toolkit and Hub data declare MIT; source repositories retain their terms. Requires Docker on supported Ubuntu; the authors do not support Windows/macOS. Harbor's adapter reports some synthetic oracle failures. |

## Test generation and DevOps stages

An issue-reproducing test and a repair patch are different deliverables. In operational workflows, also separate individual stage success from a verified composed pipeline.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [SWT-Bench](https://aicanwhat.com/projects/swt-bench/) · [Source](https://github.com/logic-star-ai/swt-bench) | Generate tests that distinguish an unfixed issue from its repair; preserve unit-test versus reproduction-script scoring and shared SWE-bench issue families. | The issue families derive from SWE-bench; Lite, Verified and Full are filtered variants, not independent task universes. Unit-test mode and standalone reproduction-script mode have different checks; script mode uses exit status and does not run the suite. Upstream lists 276 Lite, 433 Verified and 2,294 Full instances. Pin the dataset and filters. Harness MIT does not replace the licenses of evaluated repositories. No Docker build, generated test or coverage result was reproduced here. |
| [DevOps-Gym](https://aicanwhat.com/projects/devops-gym/) · [Source](https://github.com/ucsb-mlsec/DevOps-Gym) | Explore build, monitoring, repair and test-generation stages while checking task-version and composed-workflow coverage explicitly. | Pin the task revision: the README reports 704 tasks, the inspected tree has 733 direct task directories, and the frozen Harbor package reports 728; these are not established equivalent runnable counts. Issue-repair and test-generation directories reuse issue IDs. An end_to_end folder name alone does not prove a four-stage pipeline: the inspected gogs cpu-usage instruction asks for monitoring. Published image references were not pulled or executed. README declares MIT, but its linked LICENSE file is absent at this revision. |

## Selection questions

### Can I add combined and split package counts?

No. SWE-Lancer Diamond combines 198 coding and 265 manager tasks into 463 total tasks. Registry packages for all, IC and manager are views of one family, not three disjoint collections.

### Does the latest announcement identify the public runnable release?

Check the released artifact. Android Bench publicly links its 1.0 task set, while the 2.0 methodology describes a separate private task set. Keep the accessible dataset, harness and published result version aligned.

### What changes when a benchmark is adapted to Harbor?

Packaging can change prompts, visible tests, tools, timeouts and metrics. Preserve the adapter revision and its documented differences. A family association in the upstream index does not prove score equivalence.

## Continue exploring

- [All app evaluation resources](https://aicanwhat.com/apps/?use=evaluation)
- [Harbor package inventory](https://aicanwhat.com/discover/?source=harbor-hub)
- [Website and game generation](https://aicanwhat.com/guides/software-generation/)

Compiled from catalog primary sources with AI-assisted research and writing. Groups are not rankings; experiments and complete runtime behavior have not been independently verified.

[Review method](https://aicanwhat.com/about/)
