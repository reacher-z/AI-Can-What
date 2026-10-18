# Catalog coverage and evidence

[Website coverage](https://aicanwhat.com/coverage/) · [JSON](coverage.json) · [Inclusion boundaries](../../docs/coverage.md)

Counts with different units are not additive. This describes catalog coverage, not completeness of the web, quality rankings or runtime success.

Entry source-review dates: 2026-10-16 – 2026-10-17

## Categories and resource types

Each entry has one category and one resource type, so rows and columns add up here. Entry counts are not counts of independent task families.

| Resource type | Games & virtual worlds | Websites | Apps | Total |
| --- | --- | --- | --- | --- |
| Software made with AI | [14](https://aicanwhat.com/games/?kind=ai-generated-output) | [10](https://aicanwhat.com/websites/?kind=ai-generated-output) | [38](https://aicanwhat.com/apps/?kind=ai-generated-output) | [62](https://aicanwhat.com/?kind=ai-generated-output) |
| Environment + benchmark | [15](https://aicanwhat.com/games/?kind=environment-and-benchmark) | [8](https://aicanwhat.com/websites/?kind=environment-and-benchmark) | [40](https://aicanwhat.com/apps/?kind=environment-and-benchmark) | [63](https://aicanwhat.com/?kind=environment-and-benchmark) |
| Environment framework | [22](https://aicanwhat.com/games/?kind=environment-framework) | [2](https://aicanwhat.com/websites/?kind=environment-framework) | [8](https://aicanwhat.com/apps/?kind=environment-framework) | [32](https://aicanwhat.com/?kind=environment-framework) |
| Benchmark suite | [3](https://aicanwhat.com/games/?kind=benchmark-suite) | [9](https://aicanwhat.com/websites/?kind=benchmark-suite) | [11](https://aicanwhat.com/apps/?kind=benchmark-suite) | [23](https://aicanwhat.com/?kind=benchmark-suite) |
| Dataset + benchmark | [2](https://aicanwhat.com/games/?kind=dataset-and-benchmark) | [10](https://aicanwhat.com/websites/?kind=dataset-and-benchmark) | [19](https://aicanwhat.com/apps/?kind=dataset-and-benchmark) | [31](https://aicanwhat.com/?kind=dataset-and-benchmark) |
| Dataset | 0 | 0 | [2](https://aicanwhat.com/apps/?kind=dataset) | [2](https://aicanwhat.com/?kind=dataset) |
| All entries | 56 | 39 | 118 | 213 |

## Use tags

An entry can support both training and evaluation, so these counts are not additive. Showcase and environment use describe different things.

| Use | Entries |
| --- | --- |
| [Showcase](https://aicanwhat.com/?use=showcase) | 62 |
| [Training](https://aicanwhat.com/?use=training) | 75 |
| [Evaluation](https://aicanwhat.com/?use=evaluation) | 148 |

## Platform tags on app resources

This table covers only 118 app entries. Platform tags overlap and can name application targets or screenshot sources; do not sum the rows. 45 entries have no assigned platform, which does not mean no platform is supported.

| Platform | Entries | AI software showcases | Other resources |
| --- | --- | --- | --- |
| [Web](https://aicanwhat.com/apps/web/) | 20 | [10](https://aicanwhat.com/apps/web/?use=showcase) | 10 |
| [macOS](https://aicanwhat.com/apps/macos/) | 22 | [15](https://aicanwhat.com/apps/macos/?use=showcase) | 7 |
| [Windows](https://aicanwhat.com/apps/windows/) | 25 | [13](https://aicanwhat.com/apps/windows/?use=showcase) | 12 |
| [Linux](https://aicanwhat.com/apps/linux/) | 24 | [13](https://aicanwhat.com/apps/linux/?use=showcase) | 11 |
| [iOS](https://aicanwhat.com/apps/ios/) | 12 | [9](https://aicanwhat.com/apps/ios/?use=showcase) | 3 |
| [Android](https://aicanwhat.com/apps/android/) | 23 | [5](https://aicanwhat.com/apps/android/?use=showcase) | 18 |

## Research, guides and interaction evidence

Papers and entries can have many-to-many relationships; an entry can also have several observation records. Observations cover their stated steps, not whole applications. No observation record does not mean no public demo.

| Measure | Count | Unit |
| --- | --- | --- |
| [Research papers](https://aicanwhat.com/papers/) | 149 | Paper records |
| [Papers with catalog links](https://aicanwhat.com/papers/?status=linked-project) | 146 | Paper records |
| [Papers without artifact entries](https://aicanwhat.com/papers/?status=paper-only) | 3 | Paper records |
| Entries linked from papers | 142 | Distinct catalog entries |
| Paper-to-entry associations | 147 | Associations |
| [Scoped browser observations](https://aicanwhat.com/observations.json) | 5 | Observation records |
| Entries with observations | 5 | Distinct catalog entries |
| Entries without observations | 208 | Distinct catalog entries |
| [Selection guides](https://aicanwhat.com/guides/) | 7 | Guides |
| Guide project associations | 88 | Associations |
| Entries covered by guides | 88 | Distinct catalog entries |

## Upstream snapshot coverage

These metadata records can include versions, forks, wrappers and out-of-scope material; do not add them to the reviewed catalog. Related notes do not establish equivalent tasks, scores or runtime. Dates identify capture time, not this build.

| Source | Records | With related notes | Captured (UTC) |
| --- | --- | --- | --- |
| [Harbor Hub](https://aicanwhat.com/discover/?source=harbor-hub) | 355 | 26 | 2026-10-16 12:10:39 |
| [OpenEnv](https://aicanwhat.com/discover/?source=openenv) | 40 | 10 | 2026-10-16 12:10:29 |
| [BrowserGym](https://aicanwhat.com/discover/?source=browsergym) | 15 | 15 | 2026-10-16 12:10:29 |
| [Farama Foundation](https://aicanwhat.com/discover/?source=farama) | 16 | 10 | 2026-10-16 12:10:29 |
| [OpenAI coding examples](https://aicanwhat.com/discover/?source=openai-examples) | 64 | 11 | 2026-10-16 12:10:30 |

Generated from: [`data/catalog.json`](../../data/catalog.json), [`data/papers.json`](../../data/papers.json), [`data/observations.json`](../../data/observations.json), [`data/guides.json`](../../data/guides.json), [`data/registry-index.json`](../../data/registry-index.json), [`data/registry-sources.json`](../../data/registry-sources.json)
