# Contributing

Suggest one project at a time with an original author URL, an explanation of what people can do with it, supported platforms, and relevant limitations. Use the resource issue template or edit `data/catalog.json` in a pull request.

Keep the two catalog dimensions separate:

- `uses`: showcase, training, evaluation. More than one is allowed.
- `implementation`: ai-built, ai-assisted, human-built, unknown. AI-development labels require an original author statement linked in `provenance_source`.

`source-reviewed` means original material was read. It does not mean the software was run, benchmark results were reproduced, or the project was independently audited. Unknown operating-system support stays untagged; host requirements and target operating systems are different.

Actual browser interactions belong in `data/observations.json`, with concrete steps, visible outcomes, date, environment, original screenshot and untested scope. Preserve `source-reviewed` on the catalog entry. Follow the [browser-observation method](docs/browser-observations.md); do not promote a short interaction into full runtime verification.

Use `resource_kind` to distinguish AI-generated outputs, environments with tasks, environment frameworks, benchmark suites, and static datasets. Games includes virtual worlds; Apps includes software, API simulations, and software-engineering tasks. Dataset platform tags describe the source of its examples, not an executable operating system.

Paper metadata lives in `data/papers.json`. Preserve the original title and author order; arXiv dates are first submissions. Other primary publications use their exact source URL and identified date meaning. If only a publication year is verified, set `published_at` to null and record `publication_year` with bilingual date notes; never invent a month/day or arXiv ID. Journal dates and identifiers stay separate. Keep summaries concise and original, and do not describe old scores as current performance.

Papers normally map to stable catalog IDs. Relevant research without a reviewed catalog artifact can use `catalog_status: paper-only` and empty `project_ids`, with bilingual artifact notes, a status-review date and original artifact-source links. This preserves literature while keeping unreleased, partial or unverified artifacts out of runnable-project claims. These papers do not add to the project count. When a reviewed artifact is later added, update its association rather than duplicate the paper.

Each entry needs concise original English and Chinese descriptions, practical limits, source URLs, and a review date. Prefer useful and representative projects over a large entry count. Never manufacture scores, endorsements, affiliation, licenses, or claims of AI authorship.

Run before proposing a change:

```sh
python3 scripts/build.py
python3 scripts/validate.py
node --check static/app.js
node --check static/search.js
node --check static/registry.js
python3 -m unittest discover -s tests
```

The static site is generated into `dist/`. Edit source files, not generated pages. Keep public catalog data and source separate from private account records or credentials.

The build also updates the root READMEs, category/platform indexes under `catalog/`, selection guides under `guides/`, and `references.bib`. Include those generated changes in the same pull request; CI checks that they are current. Edit selection guidance in `data/guides.json`: explain which question a resource answers, preserve setup limits and link existing catalog entries. A guide is not a ranking or another set of independent projects.

Registry metadata belongs in the separate upstream discovery index. Finding a manifest or package in a registry is not sufficient to promote it into the reviewed catalog or label it AI-built. Follow [registry-discovery.md](docs/registry-discovery.md) for source snapshots, immutable version evidence, refreshes, and the distinction between packages and independent projects.
