# Upstream registry discovery

The reviewed catalog and upstream registry index answer different questions. The catalog contains project-level descriptions checked against original materials. The registry index helps people find additional artifacts and configurations through factual upstream metadata. Registry records are not individually reviewed projects, and neither collection currently claims independent execution verification.

## Source boundaries

| Source | Recorded unit | Boundary |
| --- | --- | --- |
| [Harbor Hub](https://hub.harborframework.com/datasets) | Public dataset package in an org/name namespace | A full paginated public-package census and a separate visible `latest`-tag metadata census. Includes community uploads, experiments, forks and non-software datasets. |
| [OpenEnv](https://github.com/huggingface/OpenEnv) | Tracked environment manifest | Regular `envs/<name>/openenv.yaml` files at the recorded commit. External repositories and hosted deployments are outside this inventory. |
| [BrowserGym](https://github.com/ServiceNow/BrowserGym) | Named benchmark configuration | Literal keys of `DEFAULT_BENCHMARKS` at the recorded commit. Tiny/lite/curriculum variants are configurations, not independent projects. |
| [Farama](https://farama.org/projects) | Foundation project record | The deployed public project JSON, including libraries, environments, compatibility layers and offline-data infrastructure. Governance labels are attributed to Farama. |
| [OpenAI coding examples](https://github.com/openai/gpt-5-coding-examples) | Example manifest | YAML manifest paths at the recorded commit, with matching application source paths checked in the same Git tree. Model variants may repeat one idea. |

The initial current-Hub capture observed 355 public packages and 344 visible latest-tag records. The 11 packages without visible version metadata remain in the index with an explicit unavailable state; they are not assigned zero tasks or a fabricated version URL. The older root `registry.json` in Harbor's repository is a custom-registry snapshot, so it is not used as a current Hub census.

Package names, namespaces, paths, category labels, revisions and task counts are factual metadata. Task counts are reported by the upstream registry, are not quality scores, and must not be summed across overlapping packages. An upstream namespace is not independently verified author identity. No README bodies, prompt bodies, screenshots or dataset task files are republished by this pipeline. A public package or code repository does not imply a permissive reuse license.

## Capture and validation

Definitions and reviewed Git revisions live in `data/registry-sources.json`; the generated public snapshot is `data/registry-index.json`. Every source has capture time, request URLs, response byte counts and SHA-256 digests. Harbor additionally records observed version IDs, revisions and content hashes. Its mutable `latest` page can later change; the saved metadata describes the captured version.

Harbor reads use anonymous publishable defaults extracted as literals from the pinned first-party client source. Personal Hub login files, personal tokens and environment credentials are not read. The PostgREST schema is an implementation-derived public interface, not a promised stable API. Requests explicitly restrict both package and version joins to public dataset packages. Pagination checks exact totals, unique package IDs, contiguous ranges and matching identities across joins. It is not a transactionally frozen service snapshot; concurrent changes cause a failed refresh when detected.

GitHub trees must be complete, and manifests must be regular tracked files. BrowserGym configuration is parsed with Python's AST; upstream modules, lambdas and entry points are never executed. Exact artifact-path matching connects registry records to related catalog notes without collapsing sibling applications into a repository-level match. Related notes do not establish that a particular wrapper, configuration or package version was separately reviewed.

## Refresh

From the repository root, with Python 3.10+ and an authenticated `gh` CLI for public GitHub metadata:

```sh
python3 scripts/sync_registries.py
python3 scripts/sync_registries.py --write
python3 scripts/build.py
python3 scripts/validate.py
python3 -m unittest discover -s tests
node --check static/registry.js
```

The first command previews counts without replacing the public snapshot. Raw captures stay in ignored `.cache/discovery/`. `--use-cache` reuses intact matching captures and retains their original observation times; it is useful for reproducible development, not a freshness claim. A write occurs only after all configured sources succeed. Failed or partial requests leave the previously published snapshot intact.

GitHub inventory revisions are deliberately pinned. Inspect upstream changes and update the corresponding source definition before refreshing a pinned inventory; rerunning a capture does not make an old Git revision current. Review count changes, new namespaces, missing-version cases and source-boundary changes before publication. Promote promising records through the normal project-level contribution workflow, with independent provenance, platform and licensing evidence.

The site publishes one bilingual discovery index with stable row anchors and downloadable metadata. It does not create thin project-detail pages for each unreviewed registry record. Canonical page counts, reviewed-project counts, paper counts and upstream-record counts remain separate.
