# AI Can What?

**See what AI builds. Explore where agents learn.**

A source-backed directory of AI-built software and environments for training and evaluating agents, organized into **Games**, **Websites**, and **Apps**. Every entry has an original source, review date, practical limits, and its own static page.

The first collection contains **16 projects**: 4 games, 4 websites, and 8 applications. It includes four author-reported AI-built showcases and twelve entries linked to original papers. Source review is distinct from runtime verification.

## Browse

| Category | Initial entries |
| --- | --- |
| Games | Asteroid Game, Crafter, TextWorld, MiniHack |
| Websites | WebArena, VisualWebArena, WorkArena, BrowserGym |
| Apps | Tiny Kanban, Claude's C Compiler, FastRender, OSWorld, AndroidWorld, Windows Agent Arena, iOSWorld, MacArena |

[Catalog and evidence](data/catalog.json) · [Contributing](CONTRIBUTING.md)

## How the directory works

Showcase describes software made with AI. Training and Evaluation describe environment uses; they do not imply that AI created the environment. Development provenance is recorded separately. Platform tags reflect the cited project's documentation, and unknown values stay unknown.

The directory links to upstream code and demos. It does not host or claim to have independently tested every application. Read each entry's limits and the upstream license before using it.

## Build locally

Python 3.10+ and Node.js, with no installed dependencies:

```sh
python3 scripts/build.py
python3 scripts/validate.py
node --check static/app.js
python3 -m http.server 8768 --bind 127.0.0.1 --directory dist
```

The website is bilingual. Static HTML contains the complete directory and project details; JavaScript adds keyword search and purpose/platform filters. Canonical URLs, reciprocal language links, structured metadata, robots.txt and the sitemap are generated from the same source data. `llms.txt` is an optional navigation aid, not an indexing guarantee.

## Source layout

```text
data/catalog.json          Reviewed entries and supporting sources
static/                    Browser assets
scripts/build.py           Static page generator
scripts/validate.py        Source and generated-page checks
site.json                  Canonical origin and public repository
.openai/hosting.json        Sites deployment identity
```

Keep the canonical origin in `site.json` aligned with the actual published domain. Run validation after changing data or templates. Search-engine submissions happen after a successful deployment and are recorded separately from crawl, index, or citation outcomes.
