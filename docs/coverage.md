# Catalog scope and coverage

This directory covers software made with AI and resources used to train or evaluate agents across games/virtual worlds, websites, and applications. Applications includes desktop/mobile software, simulated APIs, and software-engineering tasks. It does not claim to be the largest or exhaustive collection.

The generated [coverage report](../catalog/coverage/README.md) and [statistics JSON](../catalog/coverage/coverage.json) show category, platform, research and observation counts from the same inputs as the website. Platform/use tags overlap; papers, associations and upstream metadata have separate counting units. Source-file hashes identify the data used for a snapshot. Source-review dates and registry capture dates are preserved rather than replaced with a fresh build date.

## What counts as an entry

A distinct authored application, environment, framework, benchmark, or dataset with a primary source and a specific use. Two named apps in one published example collection can be distinct entries; two links to the same app are merged. A separately maintained evaluator or new task release can have its own entry while sharing a project family. For example, WebArena-Verified revises WebArena's task family, and its full and Hard counts are not additive. Catalog totals count entries, not independent task universes. Papers and their associated entries are counted separately and are not additive.

Record resource type, intended use, development provenance, and platform independently. A screenshot dataset is not a runnable OS; an environment built with AI is not automatically a consumer-software showcase. Unknown facts remain unknown.

Use the Dataset type for a corpus without an established evaluation task or benchmark protocol. Dataset + benchmark means the resource also defines an evaluation setting; it does not imply that all metrics, runtime images or evaluators are publicly released. For example, OS-Atlas Data is grounding pretraining material, while VideoGUI defines benchmark tasks but has not released its official metric implementation.

## Coverage still worth improving

- More native Windows software with clear first-party AI-development evidence, beyond the first documented applications, scripts, and CLI tools. Native Windows, an interpreter-based script, and a WSL setup are different distribution/runtime claims.
- A broader range of AI-assisted native mobile and desktop applications. The current collection includes creator accounts and release/store evidence for macOS, iOS, and Android examples.
- Publicly runnable examples from a broader range of independent creators, with explicit licensing and setup information.
- Recently released environments and benchmark versions, while preserving the version/date context of earlier papers.
- Additional scoped browser observations of accessible examples, recorded as separate receipts rather than inferred from documentation or an HTTP 200 response. Current observations cover one game round, a product-search/history flow, sample chart controls, synthetic Markdown-slide navigation and a local task-card creation/search/reload flow; see [the method and limits](browser-observations.md).
- Search indexing and actual AI citations, measured separately from sitemap discovery and submission receipts.

## Maintenance

Use the generated category and platform indexes to find gaps. Check the original project or paper before changing a claim, and preserve the source URL and review date. Avoid adding a large weakly relevant batch merely to increase the count. Publish meaningful updates with matching evidence, then notify search engines of the new or changed canonical URLs.

The website and repository both expose platform indexes for app resources. A platform may describe a runnable application, an environment target, or screenshots in a dataset. Each index shows those resource types separately, and the website reports its software-showcase coverage explicitly.

[Selection guides](../guides/README.md) connect existing projects to concrete goals: finding AI-made software, testing browser agents, testing computer/mobile use, evaluating software generation, studying coding agents, comparing data workflows and testing tool/API use. Their groupings explain distinct tasks and evidence requirements; they are not additional projects or quality rankings. Guides and project notes link in both directions, and each comparison preserves the catalog's current setup limits.

The [upstream registry index](https://aicanwhat.com/discover/) captures a broader discovery surface with source-specific boundaries. Those records are metadata only, can include versions, wrappers, test packages and off-topic datasets, and are not added to the reviewed project count. See the [registry method](registry-discovery.md) for coverage and refresh rules.

Primary-source corrections in the current collection include distinguishing WorkBench project-management tools from document editing, AgentBench's text-based ALFWorld tasks from visual embodiment, and VirtualHome's household simulation from desktop application use. Supporting sources are recorded with those entries.

Development evidence is specific to the artifact: a marketing-site commit is not proof that AI wrote the native app, a maker's account is attributed rather than independently authenticated, and a public repository is not automatically licensed for reuse. Current research summaries also distinguish the τ² paper from later τ³ repository features and Terminal-Bench 2.0 from subsequent benchmark releases.
