# AI Can What?

**See what AI builds. Explore where agents learn.**

**[Explore aicanwhat.com](https://aicanwhat.com/) · [中文目录](https://aicanwhat.com/zh/) · [Review method](https://aicanwhat.com/about/)**

A source-backed directory of AI-built software and environments, benchmarks, and datasets for training and evaluating agents, organized into **Games & virtual worlds**, **Websites**, and **Apps**. Every entry has an original source, review date, practical limits, and its own static page.

<!-- BEGIN GENERATED INDEX -->
**124 catalog entries · 86 referenced papers.** Paper references overlap the catalog; these counts are not additive. Every entry links its evidence and records known limits.

## Browse

| Category | Entries | Repository index |
| --- | --- | --- |
| [Games & virtual worlds](https://aicanwhat.com/games/) | 42 | [Browse](catalog/games/README.md) |
| [Websites](https://aicanwhat.com/websites/) | 25 | [Browse](catalog/websites/README.md) |
| [Apps](https://aicanwhat.com/apps/) | 57 | [Browse](catalog/apps/README.md) |

[Research bibliography](https://aicanwhat.com/papers/) · [Catalog data](data/catalog.json) · [Contributing](CONTRIBUTING.md)

**2 scoped browser observations across 2 projects** record interaction steps, visible outcomes, screenshots and untested scope. These are not whole-application verification. [Observation data](data/observations.json) · [Method](docs/browser-observations.md).

[Upstream registry index](https://aicanwhat.com/discover/): **490 metadata records from 5 sources**. These include versions, forks, manifests, and configurations; they are not individually reviewed projects and must not be added to the catalog count. [Source coverage](catalog/registries/README.md).
<!-- END GENERATED INDEX -->

## How the directory works

Showcase describes software made with AI. Training and Evaluation describe environment uses; they do not imply that AI created the environment. Development provenance is recorded separately. Platform tags reflect the cited project's documentation, and unknown values stay unknown.

The directory links to upstream code and demos. It does not host or claim to have independently tested every application. Read each entry's limits and the upstream license before using it.

## Build locally

Python 3.10+ and Node.js, with no installed dependencies:

```sh
python3 scripts/build.py
python3 scripts/validate.py
node --check static/app.js
node --check static/registry.js
python3 -m unittest discover -s tests
python3 -m http.server 8768 --bind 127.0.0.1 --directory dist
```

The website is bilingual. Static HTML contains the complete directory and project details; JavaScript adds keyword search and resource type, purpose, and platform filters. Canonical URLs, reciprocal language links, structured metadata, robots.txt and the sitemap are generated from the same source data. `llms.txt` is an optional navigation aid, not an indexing guarantee.

## Source layout

```text
data/catalog.json          Reviewed entries and supporting sources
data/papers.json           Original research metadata and summaries
data/observations.json     Scoped browser actions, results and screenshot evidence
data/registry-index.json   Separately labeled upstream registry metadata
data/registry-sources.json Source definitions and inventory boundaries
catalog/                   Generated category and platform README indexes
references.bib             Generated bibliography
static/                    Browser assets
scripts/build.py           Static page generator
scripts/validate.py        Source and generated-page checks
site.json                  Canonical origin and public repository
.openai/hosting.json        Sites deployment identity
```

Keep the canonical origin in `site.json` aligned with the actual published domain. Run validation after changing data or templates. Search-engine submissions happen after a successful deployment and are recorded separately from crawl, index, or citation outcomes.

Read [scope and coverage](docs/coverage.md) for inclusion rules and known gaps. App resources have static platform pages and matching repository folders for macOS, Windows, iOS, Android, Linux, and Web.


[Search discovery and submission workflow](docs/search-discovery.md)

For reverse-engineering tools, integrations, and software-reconstruction research, browse the companion [AwesomeREA directory](https://awesomerea.org/).
