# Browser observations

Source review and interaction evidence answer different questions. The catalog's `verification: source-reviewed` label means that original material was read. It is not changed by a short browser check.

`data/observations.json` separately records actions performed on a public demo, the visible result of each action, the date, environment, target URL and untested scope. Project pages show the same records in English and Chinese. A successful HTTP response alone is not an interaction observation.

Each record includes an original screenshot, its SHA-256 digest and attribution. The image is one moment in the interaction, not visual proof of every preceding step. Steps are the observer's account. No deployed source commit was exposed for the initial observations; `deployment_commit` remains null. A repository commit must not be substituted for an unidentified deployed version.

## Current observations

- [Tic Tac Toe](https://aicanwhat.com/projects/gpt5-tic-tac-toe-game/#browser-observations): one default local two-player round, occupied-cell handling, a top-row X win, score update and terminal-state handling. Computer-opponent strategy, draws, persistence and mobile behavior were not tested.
- [Aldi Prices](https://aicanwhat.com/projects/aldi-prices/#browser-observations): product search and navigation to a dated history table and chart. Price accuracy, calculations, completeness, freshness and mobile behavior were not tested. The captured chart has a clipped label at its right edge.
- [CSV To Charts](https://aicanwhat.com/projects/gpt5-csv-to-charts/#browser-observations): the embedded sample changed from a line chart to a bar chart, and deselecting Profit left Sales visible. No file was uploaded. The image-save button was clicked, but download completion and PNG output were not verified; this is not a confirmed export failure.
- [Markdown → Slides](https://aicanwhat.com/projects/gpt5-markdown-to-slides/#browser-observations): a synthetic two-slide document updated the preview, rendered a heading/paragraph/list, and navigated forward and back. Broader Markdown syntax, images, fullscreen, persistence and mobile behavior were not tested. The source has no built-in file-export feature.

These records do not establish AI authorship, general reliability, benchmark scores, a security audit or ongoing availability. They also do not expand the catalog's project count. Preserve observed defects and limitations alongside successful steps.

## Adding a record

Use a bounded, non-sensitive interaction with an already identified project. Record concrete actions and visible outcomes; do not infer results from source code or screenshots alone. Attribute the creator, preserve the original capture, and exclude personal information or credentials. Match the target to the reviewed demo host, provide both languages, and state what was not checked.

The build validates project associations, dates, complete steps, screenshot digests and rendered links. A changed screenshot requires a consciously updated receipt, not silent replacement. Re-observations belong in new dated records rather than overwriting previous outcomes.
