# Sprite Workbench

This folder is a safe demo area for deterministic sprite creation. The workbench reads existing images as references when a recipe requests them, but all generated composites, exported sprites, recipes, previews, and reports stay inside this folder.

The main operator is the AI. The normal loop is:

```text
edit a recipe
→ run snapshot
→ inspect the rendered outputs
→ revise the recipe
→ repeat
```

No game asset is edited in place.

## Structure

```text
devTools/
├─ sprite_workbench.py       Workbench command-line tool
└─ sprite-workbench-demo/
   ├─ README.md              This guide
   ├─ *.json                 Sprite recipes
   └─ output/                Composites, exports, previews, grids, reports
```

Recipes use paths relative to their own location. A recipe in this folder can read `../../img/...` as a source reference, while its output paths must remain inside the demo folder. The workbench rejects output paths that escape the recipe directory.

## Requirements

Python and Pillow are required.

```powershell
python -m pip install Pillow
```

## Commands

Run commands from the repository root.

### Inspect one image

```powershell
python -B devTools/sprite_workbench.py inspect img/hair/fringe/default/short.png
```

This reports the file format, colour mode, dimensions, non-transparent bounds, alpha values, palette transparency, and common colours.

### Render a recipe

```powershell
python -B devTools/sprite_workbench.py run devTools/sprite-workbench-demo/angel_wings_sol_v2.json
```

This writes the recipe's composite, preview, and declared layer exports.

### Create an inspection snapshot

```powershell
python -B devTools/sprite_workbench.py snapshot devTools/sprite-workbench-demo/angel_wings_sol_v2.json
```

Snapshot output includes:

- `composite.png`, the final assembled canvas;
- `composite-8x.png`, a nearest-neighbour enlarged preview;
- `layers-contact-sheet.png`, the composite and every layer in order;
- `*-pixel-grid.txt`, a coordinate-labelled text representation;
- `report.json`, machine-readable dimensions, bounds, layers, and edit counts;
- any files declared under `exports`.

The snapshot command is the normal AI inspection command.

### Watch a recipe

```powershell
python -B devTools/sprite_workbench.py run devTools/sprite-workbench-demo/angel_wings_sol_v2.json --watch
```

The command reruns when the recipe or one of its declared source layers changes. This is useful when an external editor changes a source reference, but recipe editing followed by `snapshot` is the preferred workflow for new procedural sprites.

### Optional coordinate editor

```powershell
python devTools/sprite_workbench.py edit devTools/sprite-workbench-demo/angel_wings_sol_v2.json
```

This opens a Tkinter editor that records clicks as pixel or erase operations. It is an optional fallback. The intended operator workflow is non-interactive recipe editing and rendered-output inspection.

## Recipe structure

A recipe contains a canvas, ordered layers, edits, outputs, and inspection settings.

```json
{
  "canvas": {"width": 256, "height": 128},
  "layers": [
    {"name": "new-sprite", "new": true, "size": [256, 128]},
    {"name": "reference-layer", "path": "../../img/body/base-classic.png"}
  ],
  "edits": [],
  "output": "output/composite.png",
  "inspection_dir": "output/inspection",
  "exports": [
    {"layer": "new-sprite", "path": "output/new-sprite.png", "mode": "RGBA"}
  ]
}
```

Layers are composited in listed order. Later layers appear over earlier layers. A source layer is read-only. A `new` layer starts as a transparent canvas unless `fill` is provided.

### Copy and edit

Use an existing image as a read-only base and export the edited layer under a new path.

```json
{
  "name": "custom-fringe",
  "path": "../../img/hair/fringe/default/short.png"
}
```

```json
{
  "exports": [
    {
      "layer": "custom-fringe",
      "path": "output/custom-fringe.png",
      "mode": "preserve_palette"
    }
  ]
}
```

When `preserve_palette` is used, the source layer's indexed palette and transparency are used where possible.

### New sprite

Start with no image source.

```json
{
  "name": "fresh-sprite",
  "new": true,
  "size": [256, 128],
  "fill": "#00000000"
}
```

New sprites normally export as RGBA. A manually defined palette export can be added later if the target format requires indexed output.

## Edit operations

Every edit names its target layer.

| Operation | Purpose | Main fields |
|---|---|---|
| `pixel` | Set one pixel | `x`, `y`, `colour` |
| `erase` | Make one pixel transparent | `x`, `y` |
| `replace` | Replace one exact RGBA colour | `from`, `to` |
| `rect` | Fill or outline a rectangle | `box`, `colour`, `fill` |
| `polygon` | Draw a hard-edged polygon | `points`, `colour` |
| `line` | Draw a pixel-aligned line | `points`, `colour`, `width` |
| `ellipse` | Draw an ellipse | `box`, `colour`, `fill`, `outline` |
| `shift` | Move a rectangular region | `box`, `dx`, `dy` |
| `copy` | Copy a rectangular region | `box`, `target_x`, `target_y` |
| `mirror` | Mirror a rectangular region horizontally | `box`, `target_x` |
| `feather` | Rasterise a curved tapered feather | `root`, `control`, `tip`, widths, colours |

The `feather` operation follows a quadratic curve from `root` through `control` to `tip`. It creates an outlined tapered shape with a fill and central highlight. Multiple feather operations can be layered to construct a wing or other organic sprite.

## Inspection practice

For every meaningful revision, inspect the enlarged composite and the contact sheet. Use the pixel grid when a silhouette, gap, isolated pixel, or alignment point needs exact coordinates.

Check:

- the final silhouette and its alignment with the intended body anchor;
- layer order and unwanted occlusion;
- transparent bounds and canvas dimensions;
- isolated pixels and accidental holes;
- palette size and alpha behaviour;
- whether both static frame cells match when a two-cell asset is required.

The workbench reports what it rendered. It does not prove that a new asset has been registered by the game or that every runtime mask and colour filter matches the game renderer.

## Safety rules

- Keep recipes and generated files under `devTools/sprite-workbench-demo/`.
- Treat `img/` and all other game asset locations as read-only.
- Export new filenames rather than replacing source files.
- Use `python -B` during normal runs to avoid creating Python bytecode beside the tool.
- Do not compile the game for sprite-only experiments.

## Current examples

- `angel_wings_fresh_no_inputs.json` demonstrates a completely procedural sprite with a procedural body guide.
- `angel_wings_sol_v1.json` records the first curved-feather attempt.
- `angel_wings_sol_v2.json` records the revised bent-wing construction using real body layers only for preview alignment.
- `sprite_workbench_demo.json` demonstrates copy-and-edit export from an existing hair layer.
- `sprite_workbench_new_sprite.json` demonstrates a new transparent layer and RGBA export.
