# Degrees of Lewdity source workspace

**IMPORTANT SHELL ACCESS: IF THE RESTRICTED SHELL FAILS WITH `HELPER_UNKNOWN_ERROR`, RUN THE COMMAND WITH `sandbox_permissions: "require_escalated"` AND INCLUDE A SHORT USER-FACING `justification` QUESTION, SUCH AS `MAY I RUN THIS READ-ONLY INSPECTION COMMAND?` OR `MAY I WRITE THIS TEMPORARY TEST FILE?` THIS ACCESS-JUSTIFICATION COMBINATION WAS REQUIRED TO GET THE SHELL WORKING IN THIS WORKSPACE.**

## Source and build layout

- The editable source is at this workspace root.
- Game source files are under `game/`.
- Shared JavaScript and CSS modules are under `modules/`.
- The source-tree inventory is recorded in `FILEMAP.md` at this workspace root.
- Run `compile.bat` to compile the source with Tweego.
- The compiler uses `devTools/head.html` as the head template and writes compiled output beside `compile.bat`.

## Game source structure

The game is a SugarCube/Twee project. The source is divided by responsibility rather than being organised as one file per screen.

- Passages define content and game transitions. They use `:: Passage Name` headers and are primarily under `game/`, with story and location passages grouped in `overworld-*` and `special-*` directories.
- Widgets are reusable Twee logic modules. They are defined in `.twee` files with `<<widget>>` and invoked as SugarCube macros. Core widgets are concentrated in `base-system/`, `base-combat/`, `base-clothing/`, and the relevant feature directories.
- JavaScript modules provide shared calculations, state management, helpers, UI behaviour, rendering, and larger subsystems. They live mainly under `game/03-JavaScript/`, with framework and version support in `game/00-framework-tools/`.
- Configuration and initial variables live under `game/01-config/` and `game/04-Variables/`. These areas define startup behaviour, constants, save variables, version migrations, and persistent game state.
- CSS controls presentation. Feature-specific styles live beside their systems under `game/`, while shared styles and fonts live under `modules/css/`.
- `base-system/`, `base-combat/`, and `base-clothing/` contain the main reusable game systems. `overworld-town/`, `overworld-forest/`, `overworld-underground/`, and `overworld-plains/` contain location-specific content and events.
- `devTools/` contains the Tweego compiler, source validators, and development utilities. `FILEMAP.md` is an inventory, not the source of truth for implementation.

## File safety

- Edit source files under `game/` and `modules/`, then recompile when updated output is required.
- Preserve existing user changes and create a named checkpoint before substantial source edits.

## Validation

- Keep the source version and compiled output filename aligned.
- Before delivery, verify the intended source files changed and that the compile output was generated from the source tree rather than manually edited.
- Before compiling, run the three source validators below against the changed files or relevant source tree:
  - `python devTools/source_preflight.py` checks universal high-confidence source hazards, including malformed backtick link terminators that can swallow later widget registrations.
  - `python devTools/twee_structure_check.py game` checks `.twee` passage boundaries, malformed closing macros, unclosed structures, and mismatched `else`/`case` branches.
  - `python devTools/macro_check.py <source files>` looks for likely unknown or misspelled SugarCube macros by collecting widget and JavaScript macro definitions before checking usage. It is heuristic and should be treated as an additional warning pass.
- `python devTools/widget_check.py game` performs the more detailed widget-definition, passage-tag, duplicate, nesting, and unresolved-call audit. Use it when changing widget-heavy code; it complements rather than replaces the three preflight checks.
- `devTools/widget_runtime_probe.js` is a browser-console/runtime audit. It checks supplied expected widget names against `SugarCube.Macro`, and can execute supplied test calls such as `<<wardrobeHairRenderCategoryTiles>>` to catch widget-body macro parsing failures. After startup, SugarCube may discard tagged widget passage source, so the probe must receive an expected-name list when source text is unavailable.
- A failed validator must be investigated before running `compile.bat`; validation tools are read-only.

## Editor tooling

The following VS Code extensions are installed in the local development environment:

- `cyrusfirheir.twee3-language-tools` (`.twee`/Twee syntax highlighting and editing support).
- `dbaeumer.vscode-eslint` (JavaScript lint integration).
- `eamodio.gitlens` (Git history and review UI; useful only where Git metadata/history is available).
- `editorconfig.editorconfig` (EditorConfig formatting rules).
- `stylelint.vscode-stylelint` (CSS lint integration).
- `streetsidesoftware.code-spell-checker` (optional spelling assistance; expect false positives from SugarCube macros, game terminology, names, and adult vocabulary).

The downloaded source materials include JavaScript/CSS tooling configuration under `Other/`:

- `Other/package.json` and `Other/package-lock.json` define the ESLint and Stylelint dependencies.
- `Other/.eslintrc.cjs` configures ESLint for the JavaScript source style and SugarCube globals.
- `Other/stylelint.config.cjs` configures Stylelint for CSS and browser-compatibility warnings.
- `Other/.editorconfig` specifies tabs, LF endings, and final newlines.

These configs are currently under `Other/`, not at the active workspace root, so they are reference/tooling material unless a command is run from `Other/` or an explicit config path is supplied. They do not replace the source preflight, Twee structure check, macro check, or Tweego compile. The editor extensions are convenience tools; only the Python validators and `compile.bat` are part of the authoritative DoL build workflow.

When using the archived JavaScript/CSS tooling, run it from `Other/` after installing its locked dependencies with `npm install`; do not run the `Other/package.json` lint command as a substitute for validation of `game/` `.twee` files.
## General `.twee` guidelines

- Treat `.twee` files as Twee/Twine source. Preserve passage headers, tags, indentation, and the existing local style.
- Edit the source `.twee` file under `game/`; do not patch compiled output.
- Preserve passage names and IDs where they already exist. Do not create duplicate passage names unless the project explicitly requires them.
- Keep every passage as a complete top-level unit. Do not insert content inside another passage or split a passage boundary accidentally.
- Preserve the surrounding passage structure, including `:: Passage Name`, optional tags, `<<widget>>` definitions, and SugarCube macro closers such as `<</if>>` and `<</link>>`.
- Keep SugarCube macro syntax separate from JavaScript syntax. Use `<<run>>` only for JavaScript; invoke SugarCube macros using their macro form.
- Avoid putting complex dynamic HTML attributes or conditional macro branches inside link bodies unless the existing project pattern clearly supports it. Prefer established project macros and button patterns.
- Keep raw `.twee` source unencoded and compile it directly.
- For focused edits, use unique nearby anchors and verify the expected replacement count. Avoid broad replacements across unrelated passages.
- After editing, compile with `compile.bat`

## SugarCube Language

<NotepadPlus>
	<UserLang name="Sugarcube4" ext="twee tw" udlVersion="2.1">
		<Settings>
			<Global caseIgnored="no" allowFoldOfComments="no" foldCompact="yes" forcePureLC="0" decimalSeparator="0" />
			<Prefix Keywords1="yes" Keywords2="no" Keywords3="no" Keywords4="no" Keywords5="no" Keywords6="no" Keywords7="no" Keywords8="no" />
		</Settings>
		<KeywordLists>
			<Keywords name="Comments">00 01 02 03/% 03/* 03&lt;!-- 04%/ 04*/ 04--&gt;</Keywords>
			<Keywords name="Numbers, prefix1"></Keywords>
			<Keywords name="Numbers, prefix2"></Keywords>
			<Keywords name="Numbers, extras1"></Keywords>
			<Keywords name="Numbers, extras2"></Keywords>
			<Keywords name="Numbers, suffix1"></Keywords>
			<Keywords name="Numbers, suffix2"></Keywords>
			<Keywords name="Numbers, range"></Keywords>
			<Keywords name="Operators1">+ - * / = += -= *= /= ++ -- == != === !== &gt; &lt; &gt;= &lt;= ! &amp;&amp; || &amp; | ( )</Keywords>
			<Keywords name="Operators2"></Keywords>
			<Keywords name="Folders in code1, open">&lt;&lt;if</Keywords>
			<Keywords name="Folders in code1, middle"></Keywords>
			<Keywords name="Folders in code1, close">&lt;&lt;/if&gt;&gt;</Keywords>
			<Keywords name="Folders in code2, open"></Keywords>
			<Keywords name="Folders in code2, middle"></Keywords>
			<Keywords name="Folders in code2, close"></Keywords>
			<Keywords name="Folders in comment, open"></Keywords>
			<Keywords name="Folders in comment, middle"></Keywords>
			<Keywords name="Folders in comment, close"></Keywords>
			<Keywords name="Keywords1">$ _</Keywords>
			<Keywords name="Keywords2"></Keywords>
			<Keywords name="Keywords3"></Keywords>
			<Keywords name="Keywords4"></Keywords>
			<Keywords name="Keywords5"></Keywords>
			<Keywords name="Keywords6"></Keywords>
			<Keywords name="Keywords7"></Keywords>
			<Keywords name="Keywords8"></Keywords>
			<Keywords name="Delimiters">00:: 01 02((EOL)) 03&lt;&lt; 04 05&gt;&gt; 06[[ 07 08]] 09&lt; 10 11&gt; 12&apos;&apos; 13 14&apos;&apos; 15// 16 17// 18@@ 19 20@@ 21[img[ 22 23]]</Keywords>
		</KeywordLists>
		<Styles>
			<WordsStyle name="DEFAULT" fgColor="000000" bgColor="FFFFFF" fontName="" fontStyle="0" nesting="0" />
			<WordsStyle name="COMMENTS" fgColor="808080" bgColor="FFFFFF" fontName="" fontStyle="2" nesting="0" />
			<WordsStyle name="LINE COMMENTS" fgColor="000000" bgColor="FFFFFF" fontName="" fontStyle="0" nesting="0" />
			<WordsStyle name="NUMBERS" fgColor="000000" bgColor="FFFFFF" fontName="" fontStyle="0" nesting="0" />
			<WordsStyle name="KEYWORDS1" fgColor="004080" bgColor="FFFFFF" fontName="" fontStyle="1" nesting="0" />
			<WordsStyle name="KEYWORDS2" fgColor="8080C0" bgColor="FFFFFF" fontName="" fontStyle="0" nesting="0" />
			<WordsStyle name="KEYWORDS3" fgColor="000000" bgColor="FFFFFF" fontName="" fontStyle="0" nesting="0" />
			<WordsStyle name="KEYWORDS4" fgColor="000000" bgColor="FFFFFF" fontName="" fontStyle="0" nesting="0" />
			<WordsStyle name="KEYWORDS5" fgColor="000000" bgColor="FFFFFF" fontName="" fontStyle="0" nesting="0" />
			<WordsStyle name="KEYWORDS6" fgColor="000000" bgColor="FFFFFF" fontName="" fontStyle="0" nesting="0" />
			<WordsStyle name="KEYWORDS7" fgColor="000000" bgColor="FFFFFF" fontName="" fontStyle="0" nesting="0" />
			<WordsStyle name="KEYWORDS8" fgColor="000000" bgColor="FFFFFF" fontName="" fontStyle="0" nesting="0" />
			<WordsStyle name="OPERATORS" fgColor="800040" bgColor="FFFFFF" fontName="" fontStyle="1" nesting="0" />
			<WordsStyle name="FOLDER IN CODE1" fgColor="000000" bgColor="FFFFFF" fontName="" fontStyle="1" nesting="0" />
			<WordsStyle name="FOLDER IN CODE2" fgColor="000000" bgColor="FFFFFF" fontName="" fontStyle="0" nesting="0" />
			<WordsStyle name="FOLDER IN COMMENT" fgColor="000000" bgColor="FFFFFF" fontName="" fontStyle="0" nesting="0" />
			<WordsStyle name="DELIMITERS1" fgColor="000000" bgColor="FFFFFF" fontName="" fontStyle="5" fontSize="12" nesting="0" />
			<WordsStyle name="DELIMITERS2" fgColor="800080" bgColor="FFFFFF" fontName="" fontStyle="1" nesting="50334724" />
			<WordsStyle name="DELIMITERS3" fgColor="0000FF" bgColor="FFFFFF" fontName="" fontStyle="1" nesting="1024" />
			<WordsStyle name="DELIMITERS4" fgColor="0000FF" bgColor="FFFFFF" fontName="" fontStyle="0" nesting="0" />
			<WordsStyle name="DELIMITERS5" fgColor="000000" bgColor="FFFFFF" fontName="" fontStyle="1" nesting="32" />
			<WordsStyle name="DELIMITERS6" fgColor="000000" bgColor="FFFFFF" fontName="" fontStyle="2" nesting="16" />
			<WordsStyle name="DELIMITERS7" fgColor="008000" bgColor="FFFFFF" fontName="" fontStyle="0" nesting="0" />
			<WordsStyle name="DELIMITERS8" fgColor="8080FF" bgColor="FFFFFF" fontName="" fontStyle="1" nesting="0" />
		</Styles>
	</UserLang>
</NotepadPlus>
