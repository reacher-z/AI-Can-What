# AI-built software: examples and development evidence

[Website version](https://aicanwhat.com/guides/ai-built-software/) · 2026-10-16

Find games, websites and native apps with first-party AI-development statements, then distinguish code, demos and limited interaction evidence.

Start with the artifact and its creator’s development account. A public demo shows an available interface; source code shows an implementation; neither alone proves who wrote it. The projects below have explicit author evidence, with the contribution scope and practical limits preserved.

## Games and interactive toys

Compare an original demo, a reconstruction and a work with human-produced assets. Their creation claims cover different components.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [Tic Tac Toe — Imperium Edition](https://aicanwhat.com/projects/gpt5-tic-tac-toe-game/) · [Source](https://github.com/openai/gpt-5-coding-examples/tree/main/apps/tic-tac-toe-game) | Inspect a published generating prompt, single-file game and one recorded two-player round. | The computer opponent uses game logic including minimax, not an LLM service. This showcase has no benchmark protocol. A separate browser observation covers one local two-player win; opponent strategy and other modes were not tested. Repository code is MIT. |
| [Three.js Quake](https://aicanwhat.com/projects/threejs-quake/) · [Source](https://github.com/mrdoob/three-quake) | Study an AI-assisted browser port while preserving the original game’s authorship and separate data rights. | The AI-development claim concerns the port; id Software created the original game. The repository includes Episode 1 shareware data and requires a registered game's data for full-game content. |
| [Firewood Splitting Simulator](https://aicanwhat.com/projects/firewood-splitting-simulator/) · [Source](https://screen.toys/firewood/) | See how generated implementation can work with an artist’s scans, animation and sound. | This entry covers the browser version. The creator supplied and edited physical scans, animation and sound; no public source repository or code-reuse license was identified. |

## Websites and browser tools

These examples connect a concrete use to a traceable maker account. A hosted interface does not establish backend correctness or a reuse license.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [Aldi Prices](https://aicanwhat.com/projects/aldi-prices/) · [Source](https://aldi-prices.lawruk.com/) | Inspect a data-driven site and the separately recorded search-to-history interaction. | The creator describes this as a personal price log. Its CSV is not a comprehensive or live retailer price feed; coverage and freshness depend on the recorded observations. A source-code reuse license was not identified in the reviewed repository. |
| [Social Media Card Cropper](https://aicanwhat.com/projects/social-media-card-cropper/) · [Source](https://tools.simonwillison.net/social-media-cropper) | Follow an openly documented implementation history for an image-cropping browser tool. | The tool uses third-party browser libraries and may load image-encoder code from a CDN. Export support and speed depend on the browser; no image was uploaded or processed in this review. Repository code is Apache-2.0 licensed; external libraries retain their own terms. |

## Desktop and mobile software

Check the application’s actual distribution target. A browser client, a native bundle and a command-line layer have different installation and provenance boundaries.

| Project and evidence | Use it to study | Setup and limits |
| --- | --- | --- |
| [Context](https://aicanwhat.com/projects/context-mcp/) · [Source](https://github.com/indragiek/Context) | Inspect a native macOS MCP client with creator development evidence and published code. | Requires macOS 15+. The reviewed README lists protocol features still unsupported or in progress; prebuilt releases enable Sentry crash reporting. Source code is MIT-licensed. |
| [Davit](https://aicanwhat.com/projects/davit/) · [Source](https://davit.app/) | Inspect a native Mac interface that manages Linux containers; the target and managed runtime differ. | Requires an Apple Silicon Mac and macOS 15+ plus Apple's container platform. The macOS tag describes the desktop application; the containers it manages run Linux. Source code is MIT-licensed. |
| [A9 Voice](https://aicanwhat.com/projects/a9-voice/) · [Source](https://a9voice.com/) | Compare a packaged Windows application with a public release history but proprietary source. | Requires 64-bit Windows 10/11. Dictation is free; Notes has a trial then a paid license. Selected cloud providers receive the configured audio/text, and license checks require network access. |
| [RhoUnpacker](https://aicanwhat.com/projects/rhounpacker/) · [Source](https://github.com/w1426421352/RhoUnpacker) | Examine an AI-generated Windows CLI layer around a separately authored library. | The AI-generated part is the command-line layer; the core KartLibrary unpacking library is human-authored. The documented Native AOT target is Windows x64, and the project is GPLv3. |
| [Shelly](https://aicanwhat.com/projects/shelly-android/) · [Source](https://github.com/RYOITABASHI/Shelly) | Inspect an Android terminal application with a documented prerelease distribution. | The maintainer calls it prerelease software and limits unattended-cycle verification to one Galaxy Z Fold6 observation. The rolling android-latest release is the documented APK source; its reviewed manifest identifies version 8.1.1. Repository code is GPLv3. |

## Selection questions

### Does “AI-built” mean every asset and dependency was generated?

No. Read the attributed contribution scope. A generated interface can use a human-written library; a generated game can contain human-made models, music and an original game design.

### Where can I find more examples for a particular platform?

Use the app-platform indexes and select Software made with AI. The broader category also contains environment and dataset resources, whose platform tags have a different meaning.

### Which examples have actual interaction notes?

The Tic Tac Toe and Aldi Prices notes record a specific browser flow with dated steps and screenshots. They do not certify the full application, computer-opponent strategy or price-data accuracy.

## Continue exploring

- [All software examples](https://aicanwhat.com/?kind=ai-generated-output)
- [Windows examples](https://aicanwhat.com/apps/windows/?kind=ai-generated-output)
- [macOS examples](https://aicanwhat.com/apps/macos/?kind=ai-generated-output)
- [iOS examples](https://aicanwhat.com/apps/ios/?kind=ai-generated-output)
- [Android examples](https://aicanwhat.com/apps/android/?kind=ai-generated-output)

Compiled from catalog primary sources with AI-assisted research and writing. Groups are not rankings; experiments and complete runtime behavior have not been independently verified.

[Review method](https://aicanwhat.com/about/)
