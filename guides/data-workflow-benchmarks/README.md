# Data-agent benchmarks: databases, notebooks and research workflows

[Website version](https://aicanwhat.com/guides/data-workflow-benchmarks/) · 2026-10-16

Compare data engineering, code-executing analysis and ML experiment resources while separating final-answer checks from workflow and environment validation.

Choose what a correct result means before choosing the environment. A data-engineering task may check resulting tables, an analysis benchmark may score final answers, and a desktop workflow may inspect application state. These checks expose different failures and should not be combined into an undifferentiated score.

## Database and transformation work

Separate local database copies from tasks touching real cloud accounts. Match the database version, initialization and exact expected-table or query checks.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [ADE-bench](https://aicanwhat.com/projects/ade-bench/) · [Source](https://github.com/dbt-labs/ade-bench) | Evaluate dbt/project changes through database-backed tests and expected outputs. | DuckDB tasks copy a local database into a task container. Snowflake tasks use a real account, create or replace trial databases/users/roles, and leave objects behind; upstream advises a separate test account. Database/project variants differ by task. The frozen Harbor package has 48 DuckDB+dbt tasks and does not represent every task in the current source. |
| [BIRD-Interact](https://aicanwhat.com/projects/bird-interact/) · [Source](https://bird-interact.github.io/) | Study clarification and SQL execution in an interactive database setting. | Full evaluation needs ground-truth/test files requested separately from the authors. Legacy and ADK runners, datasets and task counts differ; verify the chosen version and database initialization. ADK is an implementation of this benchmark, not a separate benchmark. Code is MIT; data is CC BY-SA 4.0. |

## Code-executing analysis

An execution environment allows a calculation to be performed; an answer scorer decides whether the reported result matches its reference. Inspect both.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [BixBench](https://aicanwhat.com/projects/bixbench/) · [Source](https://github.com/Future-House/BixBench) | Evaluate computational-biology analyses with the released notebook environment and chosen answer grader. | v1.5 revises and flattens the benchmark to 205 questions; v1.0 has 296 questions and is not score-equivalent. The public split is named train but includes benchmark answers and a no-training-corpus notice. Open answers can require model judging. Capsule counts differ across paper, README and current metadata. Harbor notebook/CLI variants alter tools, prompts and grading details. |
| [DABstep](https://aicanwhat.com/projects/dabstep/) · [Source](https://huggingface.co/datasets/adyen/DABstep) | Study multi-file business-data reasoning with a public agent baseline and answer-scoring protocol. | The public default file has 450 questions with empty answer fields; the 10 answered dev questions share six of those IDs. Scoring checks final answers, not notebook validity or GUI completion. Harbor reconstructs default labels from scored public submissions, so its scores are not established as equivalent to official hidden-answer evaluation. The current Space closes new manual validation requests while keeping unvalidated submissions open. |

## Spreadsheet artifacts and office tools

File correctness and coordinated tool use are different from native GUI navigation. Preserve workbook recalculation, scoring backend and whether email/calendar operations are simulations.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [SpreadsheetBench](https://aicanwhat.com/projects/spreadsheetbench/) · [Source](https://github.com/RUCKBReasoning/SpreadsheetBench) | Evaluate spreadsheet edits across workbook test cases; Verified is a subset of the original release. | The complete release has 912 instructions; Verified is an expert-annotated 400-instance subset, not 400 additional tasks. The code also retains older 200-example setup paths. Formula results need recalculation through LibreOffice or Excel before checking; record the workbook release and calculation backend. This is artifact editing, not a packaged GUI-navigation benchmark. |
| [SpreadsheetBench 2](https://aicanwhat.com/projects/spreadsheetbench-2/) · [Source](https://github.com/RUCKBReasoning/SpreadsheetBench-2) | Evaluate distinct business spreadsheet workflows; VLM chart grading accepts PNGs directly, while XLSX chart extraction needs Windows Excel/WPS COM. | This is a new workflow task set, not the original benchmark's Verified subset. Recalculate input, reference and output workbooks before scoring. Extracting charts from XLSX for VLM grading requires Windows Excel/WPS COM; the evaluator also accepts PNG outputs directly. Data is MIT-labeled, but no root license for original evaluation code was found. The README's root Dockerfile command disagrees with its actual SWE-agent/ location. |
| [OfficeBench](https://aicanwhat.com/projects/officebench/) · [Source](https://github.com/zlwang-cs/OfficeBench) | Study coordinated structured tools over local documents and simulated email/calendar files, rather than native Office GUI sessions. | The released applications are Python-backed tools in a Docker workspace, not native Microsoft Office GUI sessions. Email writes local .eml files and calendar actions write .ics files; they are not live account integrations. Setup requires Python 3.10, Docker, document/OCR dependencies and model access. The legacy image recipe expects a local model-key file and uses an unpinned Ubuntu base. |

## Desktop workflows and ML experiments

These resources include broader application or experiment state. Accounts, compute and task assets can be part of the environment rather than merely input files.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [Spider2-V](https://aicanwhat.com/projects/spider2-v/) · [Source](https://spider2-v.github.io/) | Evaluate data workflows that combine graphical tools, code and state checks. | Requires the prepared Ubuntu VM and setup dependencies. Some tasks need real cloud accounts and credentials; account/non-account and abstract/verbose instruction subsets are different evaluation settings. |
| [MLGym](https://aicanwhat.com/projects/mlgym/) · [Source](https://github.com/facebookresearch/MLGym) | Study agents that modify ML methods and run iterative experiments. | The author repository is archived as of this review, despite older README maintenance language. Experiments require Docker/Podman and task-dependent GPU/data resources. Most code is CC BY-NC 4.0, with MIT/Apache components; it is not uniformly licensed for commercial use. |

## Selection questions

### Does a split named train establish training permission or evaluation validity?

The label is not enough. BixBench’s public split is named train but carries a no-training-corpus contamination notice. Preserve author usage guidance and keep it distinct from the declared data license.

### Are local adapter labels always the official hidden answers?

No. DABstep’s default file omits answers, while six of its questions also appear in the answered dev set. The reviewed Harbor adapter reconstructs labels from scored public submissions; equivalence to official evaluation has not been established.

### How should I report dataset size?

State the unit and version: questions, unique task IDs, capsules, ready task folders or adapter-selected tasks. Development splits can overlap test IDs, and a capsule can contain several questions. Record discrepancies rather than silently summing them.

## Continue exploring

- [All app evaluation resources](https://aicanwhat.com/apps/?use=evaluation)
- [Harbor package inventory](https://aicanwhat.com/discover/?source=harbor-hub)
- [Coding-agent resources](https://aicanwhat.com/guides/coding-agent-benchmarks/)

Compiled from catalog primary sources with AI-assisted research and writing. Groups are not rankings; experiments and complete runtime behavior have not been independently verified.

[Review method](https://aicanwhat.com/about/)
