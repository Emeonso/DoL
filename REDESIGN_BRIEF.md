# Surface Redesign Brief

## 1. Purpose

This document defines a surface-level redesign for the current Degrees of Lewdity source workspace. The redesign preserves the existing assets, game logic, content breadth and core behaviour while changing the visible product identity and reorganising the source tree.

The intended result is a game that is not immediately recognisable through its interface, colour system, layout or repository structure, without requiring a full rewrite of the underlying systems.

## 2. Scope

### 2.1 Included

- New game name and visible branding.
- New browser title, favicon and build-facing identity.
- New colour scheme and design tokens.
- New typography and spacing system.
- New page silhouette and navigation layout.
- New button, link, panel, tab and overlay language.
- New presentation of status information, menus and major feature screens.
- New transitions and interaction feedback.
- Reorganisation and consolidation of source files.
- Preservation of existing image assets.
- Preservation of existing game logic and content unless a visible label or markup change is required for the redesign.

### 2.2 Excluded

- Replacement or redraw of the image library.
- Broad mechanical redesign.
- Rewriting the existing event and passage content.
- Replacing the renderer solely to achieve a new appearance.
- Save-data migration unless source moves or visible identity changes require it.
- Claims about legal separation. Technical distinctness and legal distinctness require separate assessment.

## 3. Design direction

The redesign should not be treated as a colour swap. Distinctiveness should come from a different visual grammar: the relationship between typography, spacing, navigation, controls, panels, status information and motion.

The existing game should be made to feel like a different kind of product. Possible directions include a survival dashboard, a case-file interface, a diary-like narrative system, a cold diagnostic console or a dense tactical application. One direction should be selected before detailed CSS work begins.

The design direction should define:

- neutral and accent colour relationships;
- typography hierarchy;
- page and navigation silhouette;
- control vocabulary;
- panel and overlay treatment;
- status-information density;
- image framing;
- animation behaviour;
- mobile layout behaviour.

## 4. Highest-impact surface changes

### 4.1 Global design tokens

The shared variables in `modules/css/theme.css` should become the central source of truth for the new visual system.

Candidate changes include:

- background and foreground hierarchy;
- greyscale balance;
- link and hover colours;
- danger, warning and success colours;
- tooltip backgrounds and borders;
- status colours;
- accent colour usage;
- border and focus colours;
- selection and disabled-state colours.

The new palette should change the relationship between neutral colours and accents, rather than only replacing individual colour values.

### 4.2 Typography

Typography is a high-impact, low-risk identity change.

Candidate changes include:

- body and heading font stacks;
- font sizes and line heights;
- heading weight and letter spacing;
- sentence case versus compact label treatment;
- paragraph width and reading density;
- link decoration;
- small-description styling;
- section headings, rules and markers.

The same prose can read as literary, editorial, technical, tactical or application-like depending on these choices.

### 4.3 Page silhouette

The persistent relationship between the sidebar, passage area and overlays should be changed.

Candidate layouts include:

- left sidebar to right sidebar;
- fixed sidebar to floating collapsible rail;
- sidebar to top navigation bar;
- sidebar to bottom navigation dock;
- open passage to framed application workspace;
- one large text column to a narrow reading column inside a shell;
- permanent HUD to compact expandable status strip.

Likely shared entry points are `modules/css/base.css`, `modules/css/main-passage-layout.css` and `game/base-system/caption.twee`.

### 4.4 Buttons and links

The existing link and button grammar should be replaced consistently across the game.

Candidate changes include:

- underlined text links to control-like buttons;
- flat links to framed choices;
- border radius and border thickness;
- filled, outlined and ghost button variants;
- hover, pressed, disabled and focus states;
- full-width versus inline choices;
- spacing and alignment of choice groups;
- icons, tags or secondary descriptions on important choices.

This change should establish a new control vocabulary rather than adding isolated button styles.

### 4.5 Panels, cards and foldouts

Repeated containers should share a new panel grammar.

Candidate changes include:

- square boxes to rounded cards;
- borders to shadows or inset borders;
- flat sections to layered panels;
- redesigned foldout headers;
- redesigned tabs;
- distinct save, settings and inventory rows;
- redesigned tooltips and confirmation boxes;
- consistent padding and internal hierarchy.

### 4.6 Status display

The status area is one of the strongest visual anchors in the game and should be treated as a redesigned information system.

Candidate changes include:

- reordering time, weather, money and condition information;
- labels versus icons;
- horizontal versus vertical status groups;
- raw numbers versus bars or segmented meters;
- compact chips versus descriptive rows;
- expanded statistics shown on demand;
- portrait, status and navigation separation;
- different treatment of primary and secondary information.

The underlying values can remain unchanged. The redesign changes how those values are read.

### 4.7 Image framing

Existing images can be retained while changing their visual role.

Candidate changes include:

- portrait and canvas frame shape;
- border, shadow and backdrop treatment;
- crop and scale;
- image alignment;
- image and prose relationship;
- dedicated visual panels;
- combat image framing;
- wardrobe preview framing;
- overlays and captions around images.

### 4.8 Start screen

The start screen should receive an independent composition pass because it establishes the new identity before gameplay begins.

Candidate changes include:

- title placement and treatment;
- menu orientation;
- button grouping;
- save and load prominence;
- settings placement;
- character preview placement;
- version and build display;
- introduction text width and alignment;
- background, framing and whitespace.

### 4.9 Overlays and dialogs

The overlay system should use a new modal language.

Candidate changes include:

- modal width and position;
- backdrop opacity;
- title bars;
- close controls;
- tab treatment;
- scroll behaviour;
- panel transitions;
- centred versus attached dialogs;
- fade, slide or scale transitions.

### 4.10 Major feature screens

Shared styling should be supported by focused presentation passes for the most visible feature areas:

- wardrobe;
- character creation;
- stats;
- journal;
- map;
- inventory;
- shops;
- combat;
- settings;
- save and load;
- school and work screens;
- social and relationship screens.

Each area may have a sublanguage while retaining the same global design tokens and control rules.

### 4.11 Icons and icon conventions

Without replacing the asset library, the interface can change its icon vocabulary.

Candidate changes include:

- icon selection;
- icon size and placement;
- icon-to-label ratio;
- monochrome versus status-coloured icons;
- icon containers such as circles, squares or badges;
- symbolic controls versus text-first controls;
- consistent use or deliberate removal of icons.

### 4.12 Spacing and density

Global spacing should be treated as an identity parameter.

Candidate changes include:

- page margins;
- paragraph spacing;
- section spacing;
- button padding;
- sidebar density;
- maximum passage width;
- line length;
- grid gaps;
- panel padding;
- whitespace around images;
- mobile breakpoints.

### 4.13 Motion and feedback

The redesign should select one consistent motion language.

Possible directions include:

- minimal motion and deliberate state changes;
- fast tactical transitions;
- slow soft fades;
- mechanical sliding panels;
- unstable or glitch-like interface feedback;
- subtle physical movement and bounce.

Potential targets include passage transitions, foldouts, tabs, tooltips, notifications, status updates and image presentation.

### 4.14 Mobile presentation

The mobile layout should be deliberately designed rather than treated as a collapsed desktop layout.

Candidate changes include:

- mobile header or bottom navigation;
- sidebar behaviour;
- button widths;
- portrait placement;
- compact status display;
- overlay height;
- touch-target shape;
- scroll behaviour;
- mobile wardrobe and combat layouts.

### 4.15 Visible terminology and branding

Internal variable names and passage names can remain unchanged during the first pass. Player-facing terminology should be changed where it contributes to identity.

Candidate targets include:

- game title;
- menu names;
- button labels;
- section headings;
- status labels;
- settings categories;
- location labels;
- notification headings;
- save metadata;
- version display;
- browser document title;
- favicon;
- loading and error-screen branding.

The favicon and document identity are controlled through `devTools/head.html` and related startup configuration.

## 5. Source-tree reorganisation

The source tree should be reorganised after the existing load and dependency relationships are mapped.

### 5.1 Desired structural changes

- Replace numbered folders with domain-oriented folders.
- Separate engine, core systems, presentation, content and data.
- Consolidate renderer files.
- Consolidate CSS by interface domain.
- Group shared helpers by responsibility.
- Replace generic filenames such as `base.js` and `base.css` with descriptive names.
- Replace development-history naming with product-oriented naming.
- Group content by player-facing feature where practical.
- Add an explicit load-order manifest or equivalent ordering convention.
- Remove obsolete folder numbering once the new structure is stable.

### 5.2 Main risks

- JavaScript execution order may change when files move.
- Widget registration order may change.
- CSS load order and specificity may change.
- Passages may depend on shared IDs and classes.
- Hard-coded paths may break.
- Startup code may depend on initialisation order.
- Build tooling may discover files in a different order.
- Save and load behaviour may be affected by renamed state or startup code.

File movement should therefore preserve contents initially. Behavioural and presentation changes should be isolated from the migration wherever possible.

## 6. Recommended implementation order

1. Record the current build, startup sequence and representative gameplay screens.
2. Create a new visual direction sheet covering palette, typography, spacing, controls, panels and navigation.
3. Change global design tokens and typography.
4. Redesign the page silhouette and persistent status area.
5. Redesign buttons, links, panels, tabs, tooltips and overlays.
6. Redesign the start screen and visible branding.
7. Apply focused passes to wardrobe, combat, stats, journal, map, inventory and settings.
8. Add motion and mobile-specific presentation.
9. Build a source dependency map.
10. Move and consolidate source files in small batches.
11. Compile and run focused smoke tests after each migration batch.
12. Run a full visual and functional regression pass.

The shared presentation layer should carry as much of the redesign as possible. Individual passage edits should be reserved for screens whose markup prevents a coherent result through shared CSS alone.

## 7. Surface-distinctiveness priority

| Priority | Area | Expected impact | Relative risk |
|---|---|---:|---:|
| 1 | Global design tokens | Very high | Low |
| 2 | Typography and spacing | Very high | Low |
| 3 | Page silhouette and navigation | Very high | Medium |
| 4 | Buttons, links and panels | Very high | Low to medium |
| 5 | Status display | High | Medium |
| 6 | Start screen and branding | High | Low |
| 7 | Overlays and dialogs | High | Low to medium |
| 8 | Feature-screen presentation | High | Medium |
| 9 | Image framing | Medium to high | Medium |
| 10 | Motion and mobile layout | Medium | Medium |
| 11 | Source-tree reorganisation | Not directly visible | High |

## 8. Completion criteria

The redesign is complete when:

- the game title and visible branding use the new identity;
- the start screen, main passage, persistent status display and major overlays use the new visual grammar;
- buttons, links, panels, tabs and tooltips are consistent with the new control language;
- representative wardrobe, combat, stats, journal, map, inventory, settings and save/load screens no longer present the original interface silhouette;
- desktop and mobile layouts have been checked separately;
- existing assets remain functional;
- the source tree follows the new taxonomy;
- the project compiles from the reorganised source tree;
- representative saves and gameplay routes still function;
- no UI change is being carried by an accidental CSS override that cannot be explained or maintained.

## 9. Implementation skeleton

The first implementation pass should establish the new visual system through shared files before making broad passage-specific edits. File responsibilities below are initial routing guidance and should be confirmed against the current source before each edit.

### 9.1 Identity and build surface

| File | Initial purpose | Suggested work |
|---|---|---|
| `devTools/head.html` | Document head, favicon and embedded head styles | Replace title-adjacent identity, favicon and any global head styling. Keep security policy and required engine configuration intact. |
| `game/01-config/versionInfo.twee` | Version and visible build information | Replace visible product name and version presentation where appropriate. |
| `game/01-config/start.twee` | Startup and initial presentation | Inspect startup labels, loading text and initial passage routing. |
| `game/03-JavaScript/theme.js` | Theme selection and theme-related behaviour | Preserve theme state and option logic while changing theme names or defaults. |
| `modules/css/theme.css` | Shared colour variables and palettes | Define the new neutral, accent, status, utility and tooltip palette. |

The first pass should avoid renaming persistent variables or save-state keys merely to change visible identity.

### 9.2 Global layout and controls

| File | Initial purpose | Suggested work |
|---|---|---|
| `modules/css/base.css` | Global elements, controls, dialogs, sidebar and common components | Establish the new base typography, buttons, links, panels, focus states, spacing and persistent chrome. |
| `modules/css/main-passage-layout.css` | Main passage visual and interaction layout | Choose and implement the new relationship between visual content and interaction content. |
| `game/base-system/caption.twee` | Sidebar, status display, navigation buttons and caption widgets | Reorder or regroup visible status and navigation markup where CSS alone cannot achieve the new silhouette. |
| `modules/css/defaults/*.css` | Shared layout utilities | Check grid, flex, details and utility rules for inherited assumptions that conflict with the new layout. |
| `modules/css/tooltip.css` | Tooltip-specific behaviour and presentation | Replace tooltip shape, spacing, backdrop and motion. |

The common control language should be defined here before feature screens receive individual styling.

### 9.3 Start screen and persistent menus

| File | Initial purpose | Suggested work |
|---|---|---|
| `modules/css/ui-start-menu.css` | Start-menu presentation | Replace the start screen composition, menu orientation, button grouping and title treatment. |
| `modules/css/ui-stats.css` | Stats display | Establish the new primary and secondary information hierarchy. |
| `modules/css/ui-journal.css` | Journal presentation | Apply the new panel, heading and navigation language to journal content. |
| `modules/css/settings.css` | Settings controls | Make settings rows, toggles, sliders and headings conform to the new control system. |
| `game/base-system/settings.twee` | Settings markup and labels | Edit only where existing markup prevents the intended structure or visible terminology. |
| `game/base-system/overlays/journal.twee` | Journal overlay markup | Adjust overlay-specific structure only when shared styling is insufficient. |

### 9.4 Wardrobe, shops and inventory

| File | Initial purpose | Suggested work |
|---|---|---|
| `modules/css/wardrobe.css` | Wardrobe layout and controls | Make wardrobe read as a distinct catalogue, fitting-room or equipment interface. |
| `modules/css/clothing-shop-v2.css` | Clothing shop presentation | Apply the new catalogue, filter, item-card and purchase-control language. |
| `modules/css/ui-hairstyles.css` | Hairstyle selection presentation | Align selector tabs, cards and preview framing with the new visual system. |
| `game/base-clothing/wardrobes.twee` | Shared wardrobe widgets and markup | Inspect shared widget boundaries before changing markup. Preserve preview state and apply behaviour. |
| `game/03-JavaScript/clothing-shop-v2.js` | Clothing-shop interaction and dynamic controls | Avoid logic changes. Update selectors only when markup has deliberately changed. |
| `modules/css/pills-inventory.css` | Pill inventory presentation | Replace item grouping, badges and quantity treatment where visible. |
| `modules/css/sextoys-inventory.css` | Specific inventory presentation | Bring specialised inventory screens into the same panel and control language. |

Wardrobe and shop screens should be tested after shared changes because they contain dense grids, dynamic replacement and preview rendering.

### 9.5 Combat and high-intensity screens

| File | Initial purpose | Suggested work |
|---|---|---|
| `modules/css/combat.css` | Combat layout and controls | Change combat framing, action grouping, target presentation and feedback states. |
| `modules/css/combat-layers.css` | Combat body and image layers | Change surrounding presentation, overlays and framing without altering layer identity or renderer logic. |
| `game/base-combat/widgets.twee` | Shared combat widgets | Inspect markup generated for action groups, status and combat controls. |
| `game/base-combat/actions*.twee` | Combat action content and controls | Change visible control wrappers only if shared CSS cannot establish the intended interaction pattern. |
| `game/03-JavaScript/05-renderer/*combat*` | Combat renderer and canvas support | Treat as a presentation dependency. Avoid changing renderer behaviour during the initial skin pass. |

Combat should receive a separate visual direction within the global system, but it should not become a second unrelated interface.

### 9.6 Image and canvas presentation

| File | Initial purpose | Suggested work |
|---|---|---|
| `modules/css/canvasmodel.css` | General canvas presentation | Change canvas frames, backgrounds, sizing and alignment. |
| `modules/css/characteristics.css` | Character and body presentation | Change layout and framing around existing character output. |
| `modules/css/colour-filters.css` | Image filter and time-of-day presentation | Check whether filters reinforce or undermine the new palette. Preserve image functionality. |
| `game/03-JavaScript/05-renderer/19-player-canvas-helper.js` | Player canvas support | Inspect only when CSS framing cannot handle the desired result. |
| `game/03-JavaScript/05-renderer/19-npc-canvas-helper.js` | NPC canvas support | Inspect only when CSS framing cannot handle the desired result. |

The asset files under `img/` remain unchanged. Distinctiveness comes from framing, scale, placement, backdrop and surrounding interface treatment.

## 10. Suggested first-pass changes

The first pass should be limited to changes with broad reach and low dependency cost.

1. Define one complete palette in `modules/css/theme.css`.
2. Define the new body, heading, label and small-description typography in `modules/css/base.css`.
3. Set the new global spacing, passage width, panel radius, border and shadow rules.
4. Replace the default link and button appearance.
5. Redesign the persistent sidebar or navigation silhouette.
6. Reorder the status display into primary, secondary and expandable information groups.
7. Redesign the start screen through `modules/css/ui-start-menu.css` and the relevant startup markup.
8. Redesign overlays, tabs, tooltips and save/load rows.
9. Apply the global system to wardrobe, combat, stats, journal, map, inventory and settings.
10. Add the new document title, favicon, loading identity and visible terminology.

The first pass should not move source files at the same time as the first visual experiment. The visual system needs a stable baseline so regressions can be attributed correctly.

## 11. Source reorganisation skeleton

The source migration should preserve file contents initially and change one structural group at a time. A possible destination taxonomy is:

```text
src/
  engine/
    framework/
    compatibility/
    startup/
    persistence/
  core/
    time/
    player/
    npc/
    events/
    state/
  systems/
    combat/
    clothing/
    relationships/
    pregnancy/
    shops/
    world/
  presentation/
    layout/
    overlays/
    widgets/
    renderer/
    themes/
  content/
    locations/
    characters/
    events/
    activities/
  data/
    constants/
    configuration/
    migrations/
```

This is a destination concept, not a request to create a second build root immediately. The existing Tweego input rules must be checked before adopting a new root structure.

### 11.1 Migration rules

- Preserve passage names and widget names during the first migration.
- Preserve JavaScript contents and global execution order until the moved build is proven equivalent.
- Move files in coherent groups rather than one large operation.
- Keep a source-to-destination manifest for every moved file.
- Add or preserve explicit ordering where the compiler relies on path order.
- Do not combine file movement with logic refactoring.
- Do not rename persistent state keys without a migration plan.
- Compile after each structural group.
- Run representative gameplay routes after each structural group.

### 11.2 Initial grouping candidates

- `game/00-framework-tools/` to `engine/framework/`.
- `game/01-config/` to `engine/startup/` and `data/configuration/`.
- `game/03-JavaScript/00-libs/` to `engine/compatibility/` or `engine/libraries/`.
- `game/03-JavaScript/02-Helpers/` to `core/helpers/`.
- `game/03-JavaScript/05-renderer/` to `presentation/renderer/`.
- `game/base-system/` to `systems/core/` and `presentation/widgets/`, after separating mixed files.
- `game/base-combat/` to `systems/combat/` and `content/combat/`.
- `game/base-clothing/` to `systems/clothing/` and `presentation/wardrobe/`.
- `overworld-town/`, `overworld-forest/`, `overworld-underground/` and `overworld-plains/` to `content/locations/`.
- `modules/css/` to `presentation/styles/`, grouped by global, feature and utility responsibility.

These are structural mappings only. The correct destination for mixed files should be determined from their actual definitions and call sites.

## 12. Verification matrix

The redesign should be checked through representative screens rather than only through compilation.

| Area | Minimum check |
|---|---|
| Startup | New title, loading state, favicon and start menu appear correctly. |
| Main passage | Passage width, navigation, headings, links and status display use the new system. |
| Status | Time, weather, money, condition and expandable statistics remain readable. |
| Overlay | Journal, settings, saves and dialogs open, close and scroll correctly. |
| Wardrobe | Categories, item selection, preview, apply and remove behaviour still work. |
| Shop | Filters, item cards, purchase controls and inventory updates remain functional. |
| Combat | Action controls, canvas framing, status feedback and transitions remain functional. |
| Mobile | Navigation, controls, overlays, status information and dense grids remain usable. |
| Save/load | Existing representative saves load and retain their state. |
| Build | The compiled HTML is generated from the reorganised source tree. |

Compilation is necessary but not sufficient. A visually successful change must also preserve the underlying state transition and the visible result that depends on it.
