# Patchlist: Desire System Upgrade (Folding the Bolt-On Into the Action Controller)

Branch: `desire-action-controller-fold` (based on `0.6.3.2`)
Plan: `GAME_BRIEF.md`-adjacent design doc, implemented per the 8-step plan (see conversation/plan file for full rationale).

6 commits, 6 files changed, 176 insertions / 29 deletions.

---

## Files changed

### `game/03-JavaScript/ingame.js` (+165 / -6)
Core logic file. All additions live in the `combatDynamics*` region.

- **New: weighted-target seeding (Step 1)**
  - `combatDynamicsBodyPositionConfig` — new frozen config: `spread` (0.6), `jitterMin`/`jitterMax` (0.85/1.15), and `targetPositions` (8 body-part targets mapped to a 0.00–1.00 least→most-sexual spectrum: `feet`, `hands`, `thighs`, `chest`, `buttocks`, `mouth`, `vagina`/`penis`, `anus`).
  - `combatDynamicsBodyPosition(bodyIndex, bodyCount)` — new function; converts an NPC's body-description index into a 0–1 position on that gradient.
  - `combatDynamicsTargetWeight(target, position)` — new function; triangular falloff weight for a given target at a given body position, with bounded random jitter.
  - `combatDynamicsSeedCandidates(npc, bodyIndex, bodyCount)` — new function; wraps `combatDynamicsCandidates` and multiplies each candidate's flat score by its target's weight.

- **Changed: `combatDynamicsPreferredRoll` activated (Step 2)**
  - Was a no-op passthrough (`return nativeRoll`). Now takes a third `target` argument, looks up that target's relative candidate weight via new helper `combatDynamicsPreferredRollWeight(index, target)`, and returns `nativeRoll` skewed by up to `combatDynamicsConfig.rngSkewMax` (new config field, `15`) toward the preferred target. Clamped to `[0, 99]`.
  - `combatDynamicsPreferredRollWeight` is new — normalizes a target's candidate score against the NPC's own highest-scoring candidate; returns `0.5` (neutral) whenever the system is ineligible/uninitialized/target unmatched.

- **Changed: `combatDynamicsProfile` (Step 3)**
  - Now checks for cached `npc.desireBodyIndex`/`npc.desireBodyCount` (set at generation time — see `npc-generation.twee` below) and calls `combatDynamicsSeedCandidates` instead of the flat `combatDynamicsCandidates` when present. Falls back to the old flat-score path when absent (older saves, non-generation-path NPCs).

- **Changed: `combatDynamicsIsEligible` (Step 4)**
  - Removed the `V.consensual === 1` requirement. Eligibility is now `V.combat === 1 && V.enemytype === "man" && !V.npcSub && !V.gloryhole && Array.isArray(V.NPCList) && V.enemyno > 0`. The separate `combatAgency*` "ask"/"direct" layer's own independent `V.consensual !== 1` checks (multiple call sites, unchanged) still gate player-initiated propositions to consensual encounters only.

- **Changed: `combatDynamicsDebugSnapshot` (Step 7)**
  - Each NPC entry in the snapshot now includes a `desire` block: `bodyIndex`, `bodyCount`, `bodyPosition`, `targetWeights` (per target, reusing the stable seeded score — not re-jittered on every render), and `rngSkew` (the actual skew each target would currently produce). Top-level snapshot also now reports `rngSkewMax`.

- **No changes** to `combatAgencySuccessChance`, satisfaction-band thresholds/deltas, or any other existing scoring formula.

### `game/base-combat/npc-generation.twee` (+5 / -0)
- In the shared NPC-generation widget, immediately after `$NPCList[_n].description` is set from the body-description array (`$_desc[_i]`), two new lines cache `$NPCList[_n].desireBodyIndex` (`_i`) and `$NPCList[_n].desireBodyCount` (`$_desc.length`) on the NPC object. Runs unconditionally for every generated NPC (teen/adult × male/female-appearing), immediately after the array is guaranteed set.

### `game/base-combat/man-combat.twee` (+4 / -2, 2 lines changed)
- `penisinit` widget (`:5900`): `combatDynamicsPreferredRoll(_n, $rng)` → `combatDynamicsPreferredRoll(_n, $rng, "penis")`.
- `vaginainit` widget (`:6336`): `combatDynamicsPreferredRoll(_n, $rng)` → `combatDynamicsPreferredRoll(_n, $rng, "vagina")`.

### `game/base-combat/init.twee` (1 line changed)
- Encounter-init widget: `<<combatDynamicsInit>>` (widget call) → `<<run combatDynamicsInit()>>` (direct JS call), following the wrapper-widget removal below.

### `game/base-combat/actions.twee` (1 line changed)
- `actionsman` widget, per-turn: `<<combatDynamicsFinishTurn>><<combatDynamicsBeginTurn>>` → `<<run combatDynamicsFinishTurn()>><<run combatDynamicsBeginTurn()>>`.

### `game/base-combat/effects.twee` (+27 / -13 net)
- **Removed** three widget definitions that were pure one-line `<<run fn()>>` passthroughs: `combatDynamicsInit`, `combatDynamicsBeginTurn`, `combatDynamicsFinishTurn`. (Their call sites now call the JS directly — see `init.twee`/`actions.twee` above.) `combatAgency*` widgets, which contain real Twee/SugarCube macro logic, are untouched.
- **Added** a new row to the `combatDynamicsDebugPanel` widget ("Body-type seed") displaying the current NPC's cached body index/count, position on the gradient, per-target weights, and per-target RNG skew, plus an updated "Encounter" row noting eligibility no longer requires consensual.

---

## Behavior changes vs. structural-only changes

| Change | Type |
|---|---|
| Weighted-target candidate seeding (Step 1/3) | Structural + tuning input — candidate scores now vary by NPC body type instead of a flat `20` |
| `combatDynamicsPreferredRoll` activation (Step 2) | **Deliberate behavior change** — native RNG rolls are now skewed by desire, bounded by `rngSkewMax` |
| Non-consensual eligibility (Step 4) | **Deliberate behavior change** — desire's state-reset nudge and RNG skew now also apply during non-consensual (rape) encounters with unnamed NPCs; player-ask layer (`combatAgency*`) unaffected |
| Widget wrapper collapse (Step 5) | Pure structural — identical runtime behavior, fewer indirection layers |
| Debug panel additions (Step 7) | Tooling only — no gameplay effect |

## Validation performed
`source_preflight.py`, `twee_structure_check.py`, `widget_check.py` (3 pre-existing unrelated findings, unchanged baseline), `node -c` on `ingame.js`, and a full Tweego compile — all clean. Not yet manually playtested in-game.
