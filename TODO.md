# 0.6.3.1 TODO / Backlog

Future work queued up for this branch, not yet implemented. See `PATCHLIST.md`
for what's actually been done.

## Wardrobe: clean up the bottom action-button row

The row of controls at the bottom of the wardrobe screen — "Reset",
"No changes to apply"/"Apply changes (N minutes)", "Strip" — rendered by the
`wardrobeApplyChanges` widget (`game/base-clothing/wardrobes.twee`, ~line 1328).
Needs a pass to tidy layout/spacing and general polish. No design decided yet.

## Wardrobe: add custom outfit buttons

Let the player create/save custom-named outfit quick-select buttons, similar
to a favourites row. Existing outfit-set infrastructure to build on:

- `<<widget "listoutfits">>` (`game/base-clothing/clothing-sets.twee`) — renders
  the current saved-outfit buttons and the "Create new set from current
  clothing" / "Edit all sets" controls.
- `<<widget "wardrobeNewOutfit">>` (`game/base-clothing/wardrobes.twee`, ~line
  1691) — the existing "save current outfit as a new set" flow this would
  extend or reuse.
- `<<widget "wardrobePreviewOutfit">>` (`game/base-clothing/wardrobes.twee`,
  ~line 769) — how an existing saved outfit gets applied via preview.

No design decided yet — needs a plan pass before implementation.
