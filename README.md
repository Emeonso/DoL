# Degrees of Lewdity — Source Workspace

This repository is a working source tree for **Degrees of Lewdity**, a
SugarCube/Twee browser game, currently based on version `0.6.4`. It is set
up for local development, patching, and modding: editing the Twee/JavaScript
source, compiling it with Tweego, and validating changes before they're
built into the playable HTML file.

> **Content note:** Degrees of Lewdity is an adult (18+) game with explicit
> sexual content. This repository contains its full source, including
> content of that nature.

## Repository layout

- `game/` — game source, organized by responsibility rather than by screen:
  - `00-framework-tools/`, `01-config/`, `03-JavaScript/`, `04-Variables/` —
    engine setup, configuration, shared JS modules, and persistent state.
  - `base-system/`, `base-combat/`, `base-clothing/` — the core reusable
    game systems (widgets, combat, clothing).
  - `overworld-town/`, `overworld-forest/`, `overworld-underground/`,
    `overworld-plains/` — location-specific content and events.
- `modules/` — shared JavaScript/CSS modules used across the build.
- `devTools/` — the Tweego compiler, the head template, and Python source
  validators.
- `checkpoints/` — timestamped snapshots of files taken before larger edits,
  used to preserve prior state during iterative changes.
- `compile.bat` — builds the source into a single playable HTML file.
- `FILEMAP.md` — a generated inventory of source files (not the source of
  truth for implementation details).
- `AGENTS.md` — detailed conventions for editing `.twee`/JS source, the
  validation workflow, and editor tooling.
- `GAME_BRIEF.md` — a source-grounded write-up of the game's systems from
  the player's perspective, and the design direction for ongoing mods
  (currently focused on a consensual "haggle"/NPC-desire negotiation
  system).

## Building

The game is a [Twee](https://twinery.org/) project compiled with
[Tweego](https://www.motoslave.net/tweego/) into a single HTML file.

```bat
compile.bat
```

This compiles `game/` (with `modules/` as an additional module path) using
`devTools/head.html` as the head template, and writes the output HTML file
alongside `compile.bat`.

## Validating changes

Before compiling, run the source validators against changed files or the
relevant source tree:

```sh
python devTools/source_preflight.py
python devTools/twee_structure_check.py game
python devTools/macro_check.py <source files>
python devTools/widget_check.py game   # for widget-heavy changes
```

These catch malformed passage/macro structure and likely unknown or
misspelled SugarCube macros before they reach the compiler. See
`AGENTS.md` for the full editing and validation workflow, including editor
tooling and `.twee` conventions.

## Editing notes

- Edit source `.twee`/`.js`/`.css` files under `game/` and `modules/`; never
  patch the compiled output HTML directly.
- Preserve passage names, tags, and structure — see `AGENTS.md` for the
  detailed `.twee` conventions this project follows.
- Consider creating a checkpoint (see `checkpoints/`) before substantial
  source edits.
