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

## Build / version bookkeeping
- Version bumped to `0.6.3.1` (`game/01-config/sugarcubeConfig.js`, `README.md`,
  `compile.bat`); compiled output renamed to `Degrees of Lewdity 0.6.3.1.html`.
- Restored the `img/` asset tree (18,433 files) that was missing from the branch.
- Marked `devTools/tweego/tweego_linux64` executable (needed for compiling in this
  Linux dev environment).
- Recompiled `Degrees of Lewdity 0.6.3.1.html` after each source change above.
