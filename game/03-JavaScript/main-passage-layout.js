// @ts-check

/**
 * Moves explicitly marked main-passage visuals into a separate column when the
 * player has selected the split layout. The sidebar is intentionally outside
 * this pass and is never queried or modified here.
 */
const MainPassageLayout = (() => {
	const visualSelector = "[data-main-passage-visual]";
	const layoutState = new WeakMap();

	function setWideMainPassage(enabled) {
		for (const selector of ["#story", "#passages"]) {
			document.querySelector(selector)?.classList.toggle("main-passage-layout-wide", enabled);
		}
	}

	function restorePassage(passage) {
		const state = layoutState.get(passage);
		if (state == null) return;

		for (const [placeholder, visual] of state.placeholders) placeholder.replaceWith(visual);

		state.layout.replaceWith(...Array.from(state.interaction.childNodes));
		passage.classList.remove("main-passage-layout-split");
		setWideMainPassage(false);
		layoutState.delete(passage);
	}

	function refresh(content) {
		const passage = $(content)[0];
		if (!(passage instanceof HTMLElement)) return;

		if (V.options?.mainPassageVisualLayout !== "split") {
			restorePassage(passage);
			setWideMainPassage(false);
			return;
		}
		if (layoutState.has(passage)) return;

		const visualNodes = Array.from(passage.querySelectorAll(visualSelector)).filter(element => element.parentElement?.closest(visualSelector) == null);
		if (visualNodes.length === 0) {
			setWideMainPassage(false);
			return;
		}

		const layout = document.createElement("div");
		layout.className = "main-passage-layout";

		const visuals = document.createElement("div");
		visuals.className = "main-passage-visuals";

		const interaction = document.createElement("div");
		interaction.className = "main-passage-interaction";
		const placeholders = new Map();

		visualNodes.forEach((node, index) => {
			const placeholder = document.createComment(`main-passage-visual-${index}`);
			placeholders.set(placeholder, node);
			node.replaceWith(placeholder);
		});

		for (const node of Array.from(passage.childNodes)) {
			interaction.append(node);
		}
		visuals.append(...visualNodes);

		layout.append(visuals, interaction);
		passage.append(layout);
		passage.classList.add("main-passage-layout-split");
		setWideMainPassage(true);
		layoutState.set(passage, { layout, interaction, placeholders });
	}

	return Object.freeze({ refresh, restorePassage });
})();

$(document).on(":passagerender", event => {
	MainPassageLayout.refresh(event.content);
});
