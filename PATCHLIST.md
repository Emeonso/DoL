# 0.6.3.1 Patchlist

Running log of source changes made on the `0.6.3.1` branch. Entries are added as
work happens; each lists the files touched and what changed. Build/version
bookkeeping (version bump, compiled-output rename, build artifact housekeeping) is
kept separate from gameplay/UI changes for clarity.

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
