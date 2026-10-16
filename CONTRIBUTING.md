# Contributing

Suggest one project at a time with an original author URL, an explanation of what people can do with it, supported platforms, and relevant limitations. Use the resource issue template or edit `data/catalog.json` in a pull request.

Keep the two catalog dimensions separate:

- `uses`: showcase, training, evaluation. More than one is allowed.
- `implementation`: ai-built, ai-assisted, human-built, unknown. AI-development labels require an original author statement linked in `provenance_source`.

`source-reviewed` means original material was read. It does not mean the software was run, benchmark results were reproduced, or the project was independently audited. Unknown operating-system support stays untagged; host requirements and target operating systems are different.

Each entry needs concise original English and Chinese descriptions, practical limits, source URLs, and a review date. Prefer useful and representative projects over a large entry count. Never manufacture scores, endorsements, affiliation, licenses, or claims of AI authorship.

Run before proposing a change:

```sh
python3 scripts/build.py
python3 scripts/validate.py
node --check static/app.js
```

The static site is generated into `dist/`. Edit source files, not generated pages. Keep public catalog data and source separate from private account records or credentials.
