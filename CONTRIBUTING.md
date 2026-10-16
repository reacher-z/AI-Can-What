# Contributing

Suggest one project at a time with an original author URL, an explanation of what people can do with it, supported platforms, and relevant limitations. Use the resource issue template or edit `data/catalog.json` in a pull request.

Keep the two catalog dimensions separate:

- `uses`: showcase, training, evaluation. More than one is allowed.
- `implementation`: ai-built, ai-assisted, human-built, unknown. AI-development labels require an original author statement linked in `provenance_source`.

`source-reviewed` means original material was read. It does not mean the software was run, benchmark results were reproduced, or the project was independently audited. Unknown operating-system support stays untagged; host requirements and target operating systems are different.

Use `resource_kind` to distinguish AI-generated outputs, environments with tasks, environment frameworks, benchmark suites, and static datasets. Games includes virtual worlds; Apps includes software, API simulations, and software-engineering tasks. Dataset platform tags describe the source of its examples, not an executable operating system.

Paper metadata lives in `data/papers.json` and maps back to stable catalog IDs. Preserve the original title and author order; dates are first arXiv submission dates. Journal dates and identifiers are separate fields. Keep summaries concise and original, and do not describe old model scores as current performance.

Each entry needs concise original English and Chinese descriptions, practical limits, source URLs, and a review date. Prefer useful and representative projects over a large entry count. Never manufacture scores, endorsements, affiliation, licenses, or claims of AI authorship.

Run before proposing a change:

```sh
python3 scripts/build.py
python3 scripts/validate.py
node --check static/app.js
```

The static site is generated into `dist/`. Edit source files, not generated pages. Keep public catalog data and source separate from private account records or credentials.

The build also updates the root READMEs, category/platform indexes under `catalog/`, and `references.bib`. Include those generated changes in the same pull request; CI checks that they are current.
