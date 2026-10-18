# Tool-use benchmarks: calls, state and simulated services

[Website version](https://aicanwhat.com/guides/tool-use-benchmarks/) · 2026-10-17

Choose tool-use and API benchmarks by what is checked: argument construction, world-state changes, user coordination or simulated-service responses.

Start with the outcome you need to measure. A correctly formed call does not establish that the requested workflow completed. Stateful tasks inspect the world after actions; conversational tasks also depend on user behavior and policy. Cached or model-generated service responses add their own assumptions. Record the task split, execution setting and scoring method before comparing results.

## Tool selection and arguments

Use call-level evaluation to isolate tool choice, required information and arguments. Check which cases execute implementations and which compare a call representation.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [API-Bank](https://aicanwhat.com/projects/api-bank/) · [Source](https://github.com/AlibabaResearch/DAMO-ConvAI/tree/main/api-bank) | Compare planning, retrieval and calls against the released runnable evaluation tools; the larger training API collection is a separate resource. | The runnable evaluation tools and the larger training API collection are different resources. Evaluation levels use different scripts. The authors report a googletrans/Gradio dependency conflict that can break the local demo. The enclosing repository is MIT licensed; external services retain their terms. |
| [Berkeley Function Calling Leaderboard (BFCL)](https://aicanwhat.com/projects/bfcl/) · [Source](https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard) | Select a versioned category: AST checks, simulated multi-turn execution and agentic answer scoring measure different outcomes; the Harbor package covers only part of the suite. | Pin the v4 category set: single-turn/live uses AST checks, multi-turn checks simulated state and responses, and agentic tasks match answers. 'Live' means user-contributed examples, not live API execution. Memory/search variants reuse questions. Harbor's 3,641-task adapter excludes multi-turn and agentic tests; its 123-task parity subset adds no new tasks. Web search needs SerpAPI or a replacement. Older single-turn execution/REST/SQL categories are inactive; partial runs and weighted summary scores are not interchangeable. |

## Stateful multi-tool workflows

Inspect intermediate or final application state, including unwanted changes. A simulated API world is different from an installed desktop or a production account.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [AppWorld](https://aicanwhat.com/projects/appworld/) · [Source](https://appworld.dev/) | Coordinate connected simulated apps through code or APIs, with executable task checks and explicit split restrictions. | Apps are API simulations rather than native GUIs. Follow train/dev/test restrictions; protected app and task bundles have an additional encrypted-redistribution requirement. |
| [ToolSandbox](https://aicanwhat.com/projects/toolsandbox/) · [Source](https://machinelearning.apple.com/research/toolsandbox-stateful-conversational-llm-benchmark) | Study tool dependencies and conversational context with world-state checks; execution is on the host, despite the project name. | Despite its name, documented tool execution runs on the host rather than inside Docker. Model credentials are needed, and search scenarios also use RapidAPI. Apple publishes custom license terms plus separately licensed components. It simulates device state; it is not an iOS emulator. |
| [WorkBench](https://aicanwhat.com/projects/workbench/) · [Source](https://github.com/olly-styles/WorkBench) | Check controlled email, scheduling and project-management state while preserving corrected task and evaluator revisions. | Uses simulated workplace tools rather than real email accounts or desktop apps. The 2026 task corrections and evaluator differ from the original release; report the ground-truth and scoring versions. |
| [ToolTalk](https://aicanwhat.com/projects/tooltalk/) · [Source](https://github.com/microsoft/ToolTalk) | Study conversational simulated tools with per-turn state resets and reference replay; model mistakes do not freely accumulate across the whole dialogue. | The release has 28 easy and 50 hard conversations, not 78 tools; the tool inventory has 28 tools in seven plugins. Before each assistant turn the evaluator resets state and replays reference history, so model errors do not freely accumulate across the whole conversation. Success requires all reference calls and no unmatched successful state-changing calls. The predictor uses legacy OpenAI SDK interfaces with unpinned openai; compatibility and historical model availability were not tested. |

## User coordination and policy

A user simulator and domain policies are part of the experiment. Record whether users can change state and whether the evaluated mode is text, voice or knowledge-based.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [τ-Bench](https://aicanwhat.com/projects/tau-bench/) · [Source](https://github.com/sierra-research/tau2-bench) | Evaluate policy-following customer-service interaction; the current τ³ repository and the τ² paper describe different release scopes. | The original tau-bench repository is explicitly outdated; tau2-bench now hosts τ³. Requires Python 3.12–3.13 and configured model access. Banking results before and after v1.0.1 are not comparable. Text, voice and knowledge modes have different dependencies; code is MIT. |

## Cached and generated service worlds

Simulation can make tool responses more controllable. Check how responses and rewards are produced, and keep synthetic completion separate from outcomes on a real service.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [StableToolBench](https://aicanwhat.com/projects/stabletoolbench/) · [Source](https://github.com/THUNLP-MT/StableToolBench) | Study cached or model-simulated API responses with the specific server, cache and evaluator configuration. | Simulated or cached API responses do not establish that live services perform the same actions. The repository now offers MirrorAPI and GPT-based paths with different models, caches and evaluators. Setup requires downloaded tool data and either model hosting or API access. Code is Apache 2.0. |
| [Agent World Model](https://aicanwhat.com/projects/agent-world-model/) · [Source](https://github.com/Snowflake-Labs/agent-world-model) | Train or evaluate in synthetic SQLite/MCP scenarios; identify pure-code versus model-assisted verification and the wrapper’s completion semantics. | These are synthetic SQLite/MCP scenarios, not real production services. The release distinguishes 1,000 environments from 10,000 tasks. Pure-code and SQL-plus-model verification produce different evidence and must be identified. OpenEnv is an integration, not another task set; its done action does not run verification. No explicit pipeline-code license was located in inspected project metadata. |
| [ToolEmu](https://aicanwhat.com/projects/toolemu/) · [Source](https://github.com/ryoungj/ToolEmu) | Study risky scenarios through model-emulated tool effects and model-judged outcomes; keep emulation and execution evidence distinct. | Tool effects and grades are produced by language models, not real API side effects or an independent security guarantee. The pinned assets contain 144 cases using 38 toolkits/330 tool specifications; the README's 36/311 figures describe an older inventory. Record emulator, evaluator and model settings. Setup depends on PromptCoder and older pinned libraries. Root LICENSE is Apache-2.0 but setup.py's MIT classifier conflicts; do not describe licensing as uniformly resolved. |

## Selection questions

### Does a valid function call prove a task succeeded?

No. A call representation may be well formed while the tool fails, uses the wrong state or changes the wrong object. Report call-level checks separately from executed workflow outcomes and required state constraints.

### Does an MCP interface make different environments equivalent?

No. The interface says how tools are exposed. Task state, resets, external dependencies and verification still belong to the underlying environment. Agent World Model’s OpenEnv done action, for example, does not itself run verification.

### What must I preserve to compare tool-use scores?

Pin task and evaluator revisions, splits, tool schemas, initial state, model and user-simulator versions, cached responses and judge settings. State whether calls were executed, simulated or checked structurally. Compare the same success unit; do not add wrapper records or versioned subsets as new independent tasks.

## Continue exploring

- [App and tool evaluation resources](https://aicanwhat.com/apps/?use=evaluation)
- [Harbor package inventory](https://aicanwhat.com/discover/?source=harbor-hub)
- [Browser interaction benchmarks](https://aicanwhat.com/guides/browser-agent-benchmarks/)

Compiled from catalog primary sources with AI-assisted research and writing. Groups are not rankings; experiments and complete runtime behavior have not been independently verified.

[Review method](https://aicanwhat.com/about/)
