(() => {
	"use strict";

	function getSlotFromRow(row) {
		const id = row.querySelector(":scope > .saveGroup > .saveId")?.textContent.trim();
		if (id === "A") return 0;
		const slot = Number.parseInt(id, 10);
		return Number.isInteger(slot) ? slot : null;
	}

	function createGameTimeColumn(saveObj, isHeader = false) {
		const column = document.createElement("div");
		column.className = "saveGameTime";
		if (isHeader) {
			const header = document.createElement("span");
			header.className = "saveGameTimeHeader";
			header.innerText = "In-game Date/Time";
			column.appendChild(header);
			return column;
		}

		const gameTime = saveObj ? getSavedGameTime({ state: saveObj }) : null;
		if (!gameTime) return column;

		const date = document.createElement("span");
		date.innerText = `${getShortFormattedDate(gameTime.date)} ${gameTime.date.year}`;
		const time = document.createElement("span");
		time.innerText = ampm(gameTime.date.hour, gameTime.date.minute);
		const days = document.createElement("span");
		days.className = "saveDays";
		days.innerText = `Day ${gameTime.days}`;
		column.append(date, time, days);
		return column;
	}

	function addHeaderDeleteSpacer(row) {
		if (row.querySelector(":scope > .deleteButton")) return;
		const spacer = document.createElement("button");
		spacer.className = "deleteButton right saveMenuButton";
		spacer.type = "button";
		spacer.innerText = "Delete";
		spacer.disabled = true;
		spacer.style.visibility = "hidden";
		row.appendChild(spacer);
	}

	async function decorateIndexedDbSaveList(container) {
		if (container.dataset.gameTimeReady === "true" || !window.idb?.getAllSaves) return;
		container.dataset.gameTimeReady = "pending";
		try {
			const saves = await idb.getAllSaves();
			const saveBySlot = new Map(saves.map(save => [Number(save.slot), save.data]));
			const rows = container.querySelectorAll(":scope > .savesListRow");
			rows.forEach((row, index) => {
				const group = row.querySelector(":scope > .saveGroup");
				if (!group || group.querySelector(":scope > .saveGameTime")) return;
				const slot = getSlotFromRow(row);
				group.appendChild(index === 0 ? createGameTimeColumn(null, true) : createGameTimeColumn(saveBySlot.get(slot)));
				if (index === 0) addHeaderDeleteSpacer(row);
			});
			container.dataset.gameTimeReady = "true";
		} catch {
			delete container.dataset.gameTimeReady;
		}
	}

	const observer = new MutationObserver(() => {
		const container = document.getElementById("saves-list-container");
		if (container) setTimeout(() => decorateIndexedDbSaveList(container));
	});

	function startObserver() {
		if (document.body) {
			observer.observe(document.body, { childList: true, subtree: true });
			const container = document.getElementById("saves-list-container");
			if (container) decorateIndexedDbSaveList(container);
			setInterval(() => {
				const currentContainer = document.getElementById("saves-list-container");
				if (currentContainer) decorateIndexedDbSaveList(currentContainer);
			}, 500);
		} else {
			setTimeout(startObserver, 0);
		}
	}

	startObserver();
})();
