# Patchlist

Running log of source changes made on this branch. Entries are added as work
happens; each lists the files touched and what changed. Build/version bookkeeping
(version bump, compiled-output rename, build artifact housekeeping) is kept
separate from gameplay/UI changes for clarity.

# 0.6.4

Bug and optimisation sweep. Findings came from `widget_check.py` (3 unresolved
macros, now 0), a filtered `macro_check.py` pass, and a review of the branch's own
recent changes.

## Content and correctness fixes

### Repair the corrupted `Beach Phallus Prude` passage
- `game/overworld-town/loc-beach/phallus-project.twee` — the passage, reachable in
  normal play from `loc-beach/widgets.twee` ("Ask to measure ..." behind
  `<<promiscuous3>>`), carried three separate defects. `<<passeif $molestationstart
  is 1>>` was merge damage that fused `<<pass 15>>` and `<<if>>`, so SugarCube
  rendered an unknown-macro error in the passage body. Following it was a block of
  unrelated combat boilerplate (`<<controlloss>>`, `<<molested>>`, `<<maninit>>`,
  `<<man>>`, `<<actionsman>>`) linking to `Chalets Work One Sex` — a different
  scene entirely — inside an `<<if>>` that was never opened or closed. And the
  `<<beachicon>>` "Stop" exit that every sibling passage has was missing. Restored
  to match its siblings `Beach Phallus Birdwatcher Decline` and
  `Beach Phallus Old`.

### Attach the "New warmth" tooltip to the preview marker
- `game/03-JavaScript/clothing-shop-v2.js` — `updatewarmthscale()`. In the
  `newWarmth !== null` branch the second `.tooltip()` call targeted `indicator`,
  the *current* warmth marker, instead of `indicatorNew`. Hovering the current
  marker reported the previewed warmth and the preview marker had no tooltip at
  all. Pre-existing; affects the wardrobe and all six clothing-shop screens.

### Stop dropping the warmth preview for clothing index 0
- `game/03-JavaScript/clothing-shop-v2.js` — the guard was
  `V.clothes_choice && T.realSlot && T.realIndex`. `T.realIndex` comes from
  `_temp_choice.index`, and index `0` is a real entry (the `naked` item in
  `clothing-upper.js`), so a truthiness test silently skipped the preview for it.
  Now an explicit `!= null` check on both fields.

### Remove the vestigial `fencingtease` branch
- `game/base-combat/effects.twee` — the `$penisaction is "fencingtease"` branch
  called `<<actionsfencingtease>>`, which does not exist. This was leftover rather
  than disconnected content: the menu builder `actionspenisPenisFencing`
  (`actions-penis.twee`) never offers it, so `$penisaction` can never take that
  value; no prose widget for it exists in `actions-text.twee` alongside its three
  siblings; and `ingame.js`'s agency classification lists do not mention it.
  Writing the widget would mean authoring new content plus a new menu option, so
  the dead branch was removed instead.

### Add the missing `OverTopShop` category widget
- `game/overworld-town/loc-shop/clothingCategories-v2.twee` — the category widgets
  follow a strict slot/filter pattern (`OutfitShop` = upper/outfits, `TopShop` =
  upper/non-outfits, `OverOutfitShop` = over_upper/outfits), and the
  over_upper/non-outfits member was never written. As a result non-outfit
  over-upper stock was unreachable by category in every shop, and the live caller
  in `loc-adultshop/shop.twee` (behind `$debug is 1`) errored. Added by mirroring
  `OverOutfitShop` with the filter changed to `"non-outfits"`.
- The commented-out over-clothing links in `overworld-forest/loc-forestshop/shop.twee`
  were left as they are: no over-clothing item lists `"forest"` in its `shop` array,
  so those links would open empty pages, and `AllShop` reaches any stock anyway.

## Options persistence

Root cause of "settings don't save": `updateOptions()` calls `State.restore(true)`,
whose soft restore does `_active = clone(_history[_activeIndex])`. `V` then points
at a clone detached from the history frame, so the following `V.options =
optionsData` never reaches `_history`. SugarCube marshals the session from
`_history` in a `beforeunload` handler and never from `_active`, so changing
options and refreshing before navigating a passage lost them.

### Write options into every session frame
- `game/03-JavaScript/ui.js` — `updateOptions()` patched only
  `session.history[sessionIndex]`. Now iterates every frame before
  `State.setSessionState()`, matching the save-count idiom in `save.js`, so the
  history back/forward controls no longer step onto stale options.

### Drop the browser-global option cache
- `game/01-config/sugarcubeConfig.js`, `game/03-JavaScript/ui.js`,
  `game/base-system/overlays/options.twee` — the `dolSessionOptions` localStorage
  cache was merged into every history frame of any save being loaded. That hook
  (`Save.onLoad`) fires on slot loads and imports but not on F5 restore, so it was
  not what made refresh work — it just meant loading save B after playing save A
  gave B the options from A, and importing someone else's save rewrote theirs.
  Removed the merge in `onLoad()`, the `:passagestart` restore and capture-phase
  `change` listener in `ui.js`, and the write in the `onInputChanged` callback. A
  one-time `removeItem` clears the retired key for existing players.

### Make "Save Current As Default" cover the options it should
- `game/03-JavaScript/save.js` — added `globalDefaultGeneralOptionKeys()`,
  `globalDefaultThemeOptionKeys()` and `applyGlobalDefaultOptions()`. The general
  allowlist is now derived from the existing `settingsObjects("general").options`
  registry (minus debug tooling, per-save state, and theme-owned keys) rather than
  hand-listed, so a newly added option is covered automatically. It grew from 15
  keys to 50 — `images`, `silhouetteEnabled`, `combatControls`, `maxStates`,
  `mainPassageVisualLayout` and many others previously had no defaults path at all.
- `game/base-system/overlays/options.twee` — both "Save Current As Default"
  buttons guarded each field with `<<if $options.X>>`, so a `false` was never
  stored, and a theme line-height or font-size of `0` (which means "use default")
  could not be stored either. Both now test `isnot undefined`.
- `game/04-Variables/variables-start.twee` — the read side used
  `_globalGeneralDefaults.X or Y`; SugarCube `or` is `||`, so even a correctly
  stored `false` resolved back to the built-in default. The inline fallbacks are
  gone; the literal holds plain defaults and a single validated pass applies the
  stored ones, checked against the registry via `validateValue` so a stale or
  corrupt value is ignored rather than written in.

## Optimisations

### Gate the save-list decorator to the saves overlay
- `game/03-JavaScript/save-list-idb.js` — the module ran a `MutationObserver` on
  `document.body` with `subtree: true` plus a `setInterval(..., 500)` for the whole
  session, to decorate an overlay that is open rarely. The observer fired on
  essentially every DOM mutation the game makes. `#saves-list-container` is
  rendered by the bundled `idb-backend` plugin in the story format, so there is no
  render hook to call, but the watch can be scoped: one attribute-filtered observer
  on `#customOverlay` starts a `#customOverlayContent` observer when `data-overlay`
  becomes `"saves"` and `:oncloseoverlay` stops it. The interval is gone. Also
  fixed the reentrancy guard, which set `dataset.gameTimeReady = "pending"` but
  only tested for `"true"`, letting overlapping calls both hit IndexedDB.

### Replace the deferred `linkifyDivs` calls with event delegation
- `game/03-JavaScript/clothing-shop-v2.js` plus 13 `.twee` files — `linkifyDivs()`
  bound click handlers to whichever `.div-link` elements existed at call time, so
  every call site needed its own `setTimeout(..., 0)` to run after the markup
  reached the live DOM, and any new markup that forgot one silently did nothing.
  Replaced with two handlers delegated from `document` (`.div-link a` for
  propagation, `.div-link` for forwarding), bound once at load. Nesting behaves as
  before, since jQuery builds its delegated queue from the target outward and
  honours `isPropagationStopped()` between levels. All 23 call sites removed;
  `linkifyDivs()` is retained as a no-op shim for compatibility.

### Unify the save-list date format
- `game/base-system/overlays/saves.twee` — the Twee path printed
  `getFormattedDate()` ("the 4th of September", no year) while the IndexedDB path
  in `save-list-idb.js` printed the short form plus year ("4th Sep 2022"), so the
  same column read differently depending on the player's storage backend. Both now
  use the short form plus year.

### Remove the dead version-check module
- Deleted `game/03-JavaScript/new-version-check.js` and its orphaned
  `#new-version-notification` CSS block in `modules/css/base.css`, plus the
  commented-out debug stub in `options.twee` that was its only caller. The module
  early-returned on `!window.testCheckNewVersion` so none of it ran; it also called
  a `<<newversionnotification>>` widget that does not exist and compared versions
  with `>` on strings, so `"0.6.10" > "0.6.4"` was `false`. `$notifyUpdate` and its
  entry in the save-compression dictionary were left alone, since that list is
  index-ordered and changing it would break existing saves.

## Build
- Recompiled `Degrees of Lewdity 0.6.4.html` from source with Tweego.

---

# 0.6.3.1

## Gameplay / UI changes

### Wardrobe: show outside temperature on the Warmth header row
- `game/base-clothing/wardrobes.twee` — `wardrobeRightSummary` widget now prints the
  current outside temperature (e.g. "21°C") right-aligned on the same row as the
  "Warmth:" label, instead of only inside the paragraph text below.
- `modules/css/wardrobe.css` — added `.wardrobe-warmth-header` flex row style to lay
  out the label and temperature reading on opposite ends of the row.

### Warmth guidance: fix "stay indoors" showing on comfortable days
- `game/base-clothing/wardrobes.twee` — `warmth_description` widget. The min/max
  warmth branch logic used `<<if $_minWarmth and $_maxWarmth>>`, which treats a
  legitimate `0` result (no clothing warmth needed) as falsy, identically to `null`
  (no valid answer). A genuinely comfortable day (min=0, max=null) fell through every
  branch to "to stay indoors" instead of reporting the real "comfortable regardless
  of what you wear" result. Rewrote the branches to explicit `is null`/value checks
  so every combination of 0/null/real-number on both sides gets its own correct
  wording (restored the original "at most"/"at least" phrasing for the common
  hot/cold-only cases, which a first-pass fix had regressed to "between 0 and X").

### Warmth bar revamp: visual comfort dividers instead of raw numbers
Replaces the raw-number paragraph ("Your clothing warmth is currently 9", "you'll
need a clothing warmth between 0 and 13") with a purely visual/descriptive design.
Affects every screen that renders the shared `warmthscale`/`warmth_description`
widgets: the wardrobe and all 6 clothing shop screens (main/legacy clothing shop,
school shop, forest shop, adult shop, beach stall).
- `game/overworld-town/loc-shop/clothing-v2.twee` — `warmthscale` widget markup: adds
  two static divider elements to the bar.
- `modules/css/clothing-shop-v2.css` — `.warmth-scale-comfort-divider` (+ `-min`/`-max`
  modifiers): fixed-position tick marks at 41.67%/58.33% on the bar (the 36.5°C/37.5°C
  comfort band on the indicator's existing 34–40°C domain), so the comfortable zone
  reads visually instead of numerically.
- `game/03-JavaScript/weather/01-setup/weather-descriptions.js` — new
  `warmthComfort()`/`warmthGapText()` functions: compare current warmth against
  `getTargetWarmth(36.5)`/`getTargetWarmth(37.5)` and grade the gap into prose
  ("You're feeling a bit chilly." → "You feel comfortable in what you're wearing." →
  "You're feeling a bit hot." → ...) instead of printing the threshold numbers.
- `game/base-clothing/wardrobes.twee` — `warmth_description` widget now just prints
  `setup.WeatherDescriptions.warmthComfort()`, dropping the ambient-temperature line,
  the raw warmth number, and the min/max branch block entirely.
- The bar indicator's existing hover tooltip (exact warmth number, e.g. "Warmth: 10")
  is untouched, by design, for players who want the precise value.

### Fix warmth indicator desync during wardrobe preview + colour the feeling text
- `game/03-JavaScript/clothing-shop-v2.js` — `updatewarmthscale()`. Root cause: the
  wardrobe preview system briefly swaps `$worn` to the draft outfit for one
  synchronous render, then restores it (`wardrobePreviewProjectCurrent`/
  `wardrobePreviewRestoreProjection` in `wardrobes.twee`). This macro read
  `$worn`-derived warmth values *inside* its deferred `$(() => {...})` callback,
  which only runs on a later tick — by then `$worn` had already been restored to
  the real (pre-preview) value, so the bar's indicator silently kept showing the
  old outfit's position while the prose (evaluated synchronously) correctly showed
  the new one. Fixed by computing warmth/resting-point values synchronously at
  macro-call time and only deferring the actual DOM writes (still needed, since the
  freshly-rendered `#warmthIndicator` element doesn't exist in the DOM yet at call
  time).
- `game/03-JavaScript/weather/01-setup/weather-descriptions.js` —
  `warmthGapText()` now colours each band using the game's existing hot/cold text
  convention (green = comfortable, teal/blue = cold side, orange/red = hot side),
  matching `setup.WeatherDescriptions.shop()`/`extremeTemperature()`.

### Fix clothing shop icon buttons (colour swatches, filters, etc.) not responding to clicks
- `game/overworld-town/loc-shop/clothing-v2.twee` — all 10 `<<run linkifyDivs(...)>>`
  call sites. Pre-existing bug (predates this branch, traced to the original repo
  import commit). `linkifyDivs()` (`game/03-JavaScript/clothing-shop-v2.js`) binds
  click handlers to whichever `.div-link` elements are selectable *at call time*.
  Every call in this file ran synchronously as part of SugarCube's widget/passage
  expansion, which builds the entire output as a string *before* it's inserted into
  the live DOM — so the selector always found nothing, and the elements (colour
  swatches, filter/options buttons, the mannequin panel, etc.) never got their click
  handlers wired up. Clicking them looked like a normal button (no console error,
  no visible failure) but silently did nothing. `wardrobes.twee` already had the
  correct fix for this exact utility (wrap the call in
  `setTimeout(() => ..., 0)` so it runs after the new DOM actually exists) — applied
  the same pattern to every call site in this file.
- Swept the rest of the codebase for the same unwrapped-`linkifyDivs` pattern and
  applied the identical fix to every remaining bare call site: `game/base-clothing/school-shop.twee`,
  `game/overworld-forest/loc-forestshop/shop.twee`, `game/overworld-town/loc-adultshop/shop.twee`,
  `game/overworld-town/loc-beach/balloon.twee`, `game/overworld-town/loc-shop/clothing.twee`
  (legacy shop), `game/overworld-town/loc-shop/clothingCategories-v2.twee`,
  `game/base-system/pregnancy/children.twee`, `game/base-debug/scene-viewer.twee`.
  `game/overworld-plains/loc-estate/cards_widgets.twee`'s call was already correctly
  deferred via jQuery's `$(() => {...})` ready-shorthand (same effective behaviour
  as `setTimeout(..., 0)` once the document has loaded), so it was left as-is.

### False alarm: "clothing shop buttons still don't work" report
Investigated a follow-up report that the clothing shop was still totally
unresponsive after the `linkifyDivs` fix above, even the Back button. A full
multi-step headless repro (enter shop → View All → open item → click a colour
swatch → Try On → Back) found no errors, no stuck overlay, and every
interaction working correctly, repeatedly. User confirmed it was a stale
uploaded/cached build on their end, not a regression — no code change needed.
See `TODO.md` for queued-up future work.

### New "Outfits" panel: relocate Clothing Sets, restyle its controls, visual outfit cards
Both `TODO.md` backlog items ("wardrobe cleanup bottom buttons" — turned out to mean
these controls, not the bottom action-button row — and "add custom outfit buttons")
landed together, since the second turned into "give the existing outfit-set system its
own panel."
- `game/base-clothing/wardrobes.twee` — added an "Outfits" button next to Hair/Makeup
  (`.wardrobe-paperdoll-controls`), opening a right-panel sub-view via the same generic
  `wardrobeStylePanel`/`wardrobePreviewRenderStylePanel`/`wardrobePreviewRefresh`
  mechanism already used for Hair/Makeup/the clothing-slot panel. Removed the old
  inline "Clothing sets" heading/section from the main wardrobe body (moved into the
  new `wardrobePreviewRenderOutfitsPanel` widget). Fixed a pre-existing gap in
  `updatewardrobe` that called `<<wardrobePreviewRefresh>>` without forwarding
  `_args[0]`, which would have kicked the player back to the summary panel after
  saving a new outfit while the Outfits panel was open.
- `game/base-clothing/clothing-sets.twee` — `listoutfits` widget: restyled the
  "Create new set from current clothing" / "Edit all sets" links and the
  "Wear / Delete / Overwrite" radio row into bordered flex rows
  (`.wardrobe-outfits-panel-controls`, `.wardrobe-outfits-mode-row`), matching the
  Hair/Makeup button convention instead of the old plain pipe-separated links. Each
  saved outfit is now a visual card (image, divider, name) instead of a plain text
  button, showing an actual composited render of what the player would look like
  wearing it — reuses the existing `wearoutfit` equip-resolution widget and the
  wardrobe preview sandbox (`wardrobePreviewProjectCurrent`/
  `wardrobePreviewRestoreProjection`) to resolve each outfit's worn/hair state
  without touching real player state, same as the live paperdoll preview already does.
  Clicking a card still calls `wardrobePreviewOutfit` to preview/wear it, unchanged.
- `game/03-JavaScript/base-clothing.js` — added `wardrobeRenderOutfitCardQueue()`.
  Firing several independent full-body `CanvasModel` renders in the same tick corrupts
  each other's output (some cards would render only a hair/face bust, missing
  body/clothing layers) — the renderer's layer-loading pipeline isn't safe to run
  concurrently across model instances. Each card's render options are resolved
  synchronously up front (cheap, no rendering), then rendered strictly one at a time,
  chained via the renderer's own `renderingDone` completion callback rather than a
  guessed delay (an earlier `setTimeout`-staggered attempt remained randomly unreliable
  even at very long delays). The queue itself is kicked off via a deferred
  `setTimeout(..., 0)`, since the panel's HTML can still be an unattached fragment
  (built by `new Wikifier(null, ...)`) at the moment the widget finishes — the queue's
  first entry would otherwise run before the elements exist in `document` and silently
  fail to find its target.
- `modules/css/wardrobe.css` — new `.wardrobe-outfit-card`/`-viewport`/`-divider`/
  `-title`/`-action` rules for the card grid, and `.wardrobe-outfits-panel-controls`/
  `.wardrobe-outfits-mode-row` for the restyled controls row.
- `modules/css/base.css` — removed the old `.outfitContainer button` rules, superseded
  by the new card styling in `wardrobe.css`.
- `TODO.md` — both backlog items completed and removed.

## Build / version bookkeeping
- Version bumped to `0.6.3.1` (`game/01-config/sugarcubeConfig.js`, `README.md`,
  `compile.bat`); compiled output renamed to `Degrees of Lewdity 0.6.3.1.html`.
- Restored the `img/` asset tree (18,433 files) that was missing from the branch.
- Marked `devTools/tweego/tweego_linux64` executable (needed for compiling in this
  Linux dev environment).
- Recompiled `Degrees of Lewdity 0.6.3.1.html` after each source change above.
