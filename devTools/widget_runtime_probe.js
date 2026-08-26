/*
 * SugarCube widget registration probe.
 *
 * Run this file's contents in the browser developer console after the game has
 * loaded. By default it audits the "Widgets Wardrobe" passage. To inspect a
 * different widget passage afterwards, call:
 *
 *   widgetRuntimeProbe("Passage Name")
 */
(function installWidgetRuntimeProbe() {
	"use strict";

	window.widgetRuntimeProbe = function widgetRuntimeProbe(
		passageName = "Widgets Wardrobe",
		expectedWidgetNames = window.widgetRuntimeProbeExpectedWidgets,
		testCalls = [],
	) {
		// SugarCube 2.36 exposes these through SugarCube. Older builds may expose
		// the legacy globals directly, so retain the fallback for compatibility.
		const sugarCube = window.SugarCube;
		const story = sugarCube?.Story || window.Story;
		const macro = sugarCube?.Macro || window.Macro;
		if (!story || !macro) {
			throw new Error("SugarCube is not available. Run the probe after the game has loaded.");
		}

		let passage;
		try {
			// Tagged widget passages may be retrievable with get() even when has()
			// excludes them from the ordinary passage lookup index.
			passage = story.get(passageName);
		} catch (error) {
			throw new Error(`Passage ${JSON.stringify(passageName)} does not exist: ${error.message}`);
		}
		if (!passage || typeof passage.text !== "string") {
			throw new Error(`Passage ${JSON.stringify(passageName)} does not contain readable source text.`);
		}

		const source = passage.text;
		const sourceIsErrorPlaceholder = passage.title === "Error" || source.includes("does not exist");
		if (sourceIsErrorPlaceholder && !Array.isArray(expectedWidgetNames)) {
			throw new Error(
				`SugarCube no longer exposes the source for ${JSON.stringify(passageName)} after startup. `
				+ "Pass an array of expected widget names as the second argument, "
				+ "or set window.widgetRuntimeProbeExpectedWidgets before running the probe.",
			);
		}

		const definitionPattern = /<<widget\s+(["'])([A-Za-z][\w-]*)\1/g;
		const definitions = [];
		let match;

		if (Array.isArray(expectedWidgetNames)) {
			expectedWidgetNames.forEach((name, index) => {
				definitions.push({
					index: index + 1,
					name,
					line: null,
					registered: macro.has(name),
				});
			});
		} else {
			while ((match = definitionPattern.exec(source)) !== null) {
				const before = source.slice(0, match.index);
				definitions.push({
					index: definitions.length + 1,
					name: match[2],
					line: before.split("\n").length,
					registered: macro.has(match[2]),
				});
			}
		}

		const firstMissingIndex = definitions.findIndex(definition => !definition.registered);
		const firstMissing = firstMissingIndex === -1 ? null : definitions[firstMissingIndex];
		const lastRegisteredBeforeFailure = firstMissingIndex <= 0
			? null
			: definitions.slice(0, firstMissingIndex).reverse().find(definition => definition.registered) || null;
		const registeredAfterFailure = firstMissingIndex === -1
			? []
			: definitions.slice(firstMissingIndex + 1).filter(definition => definition.registered);
		const executionTests = Array.isArray(testCalls)
			? testCalls.map(sourceText => {
				const fragment = document.createDocumentFragment();
				try {
					new (sugarCube.Wikifier || window.Wikifier)(fragment, sourceText);
					const renderedText = fragment.textContent || "";
					const hasErrorView = Boolean(fragment.querySelector?.(".error, .error-view"));
					return {
						source: sourceText,
						ok: !hasErrorView && !renderedText.includes("unable to parse macro"),
						error: hasErrorView || renderedText.includes("unable to parse macro")
							? renderedText.trim()
							: null,
					};
				} catch (error) {
					return { source: sourceText, ok: false, error: error.message };
				}
			})
			: [];

		const report = {
			passage: passageName,
			definitionCount: definitions.length,
			registeredCount: definitions.filter(definition => definition.registered).length,
			missingCount: definitions.filter(definition => !definition.registered).length,
			lastRegisteredBeforeFailure,
			firstMissing,
			registeredAfterFailure,
			executionTests,
			definitions,
		};

		console.group(`Widget runtime probe: ${passageName}`);
		console.table(definitions);
		if (firstMissing) {
			console.error("First missing widget:", firstMissing);
			console.log("Last registered widget before it:", lastRegisteredBeforeFailure);
			if (registeredAfterFailure.length) {
				console.warn("Registration resumes later; this is not a simple passage-abort boundary.", registeredAfterFailure);
			} else {
				console.warn("No later widgets registered; processing probably stopped at or before the first missing widget.");
			}
		} else {
			console.log("Every widget found in the passage source is registered.");
		}
		if (executionTests.length) {
			console.table(executionTests);
			if (executionTests.some(test => !test.ok)) {
				console.error("One or more widget execution tests failed.");
			} else {
				console.log("All widget execution tests passed.");
			}
		}
		console.groupEnd();

		return report;
	};

	try {
		window.widgetRuntimeProbe();
	} catch (error) {
		console.error(`Widget runtime probe could not inspect the default passage: ${error.message}`);
	}
})();
