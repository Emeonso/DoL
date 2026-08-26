# Widget checker follow-ups

These are unresolved macro calls reported by `widget_check.py` on 2026-08-24.
They are deliberately logged without changing the game source.

## OverTopShop

- Calls: `game/overworld-town/loc-adultshop/shop.twee:54` and
  `game/overworld-forest/loc-forestshop/shop.twee:44`
- Current status: no active Twee widget or JavaScript macro registration found;
  SugarCube runtime reports `Macro.has("OverTopShop") === false`.
- Investigate whether the shop widget was renamed, removed, or needs restoring.

## actionsfencingtease

- Call: `game/base-combat/effects.twee:6272`
- Current status: no active registration found; SugarCube runtime reports
  `Macro.has("actionsfencingtease") === false`.
- `Other/t3lt.twee-config.yml` contains the name, so check whether the source
  definition was removed or whether the call is stale.

## passeif

- Call: `game/overworld-town/loc-beach/phallus-project.twee:928`
- Current status: no active registration or runtime macro found.
- Investigate whether this is an omitted custom macro or a typo for an existing
  passage/control-flow macro.

