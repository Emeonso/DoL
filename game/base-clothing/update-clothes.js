/**
 * Used for making clothes colour customisable.
 * Structured in such a way that primary and accessory colours
 * can be updated separately without affecting the other, if applicable.
 * This function should be updated whenever a new clothing item
 * is made colour customisable with the clothing item in question.
 * Colours should be specifically chosen based on whatever best matches the original.
 *
 * @param {object} item clothes item object
 * @param {object} itemRef item prototype from setup
 */
function updateClothingColours(item, itemRef) {
	switch (item.name) {
		case "swimming goggles":
			if (!item.accessory_colour || item.accessory_colour === 0) item.accessory_colour = "white";
			break;
		case "winter jacket":
			if (item.colour === 0) item.colour = "black";
			if (!item.accessory_colour || item.accessory_colour === 0) item.accessory_colour = "tan";
			break;
		// eslint-disable-next-line no-fallthrough
		case "long leather gloves":
		case "leather dress":
		case "round shades":
		case "witch shoes":
		case "mesh shirt":
		case "fishnet stockings":
		case "fishnet tights":
		case "combat boots":
			if (!item.colour || item.colour === 0) item.colour = "black";
			break;
		case "square shades":
		case "shield shades":
		case "punk shades":
			if (!item.colour || item.colour === 0) item.colour = "black";
			if (!item.accessory_colour || item.accessory_colour === 0) item.accessory_colour = "black";
			break;
		case "aviators":
			if (!item.colour || item.colour === 0) item.colour = "grey";
			if (!item.accessory_colour || item.accessory_colour === 0 || item.accessory_colour === "original") item.accessory_colour = "black";
			break;
		case "glasses":
			if (!item.colour || item.colour === 0) item.colour = "silver";
			break;
		case "checkered shirt":
			if (!item.colour || item.colour === 0) item.colour = "russet";
			break;
		case "lace choker":
			if (!item.colour || item.colour === 0) item.colour = "black";
			break;
		case "school shirt":
			if (!item.accessory_colour || item.accessory_colour === 0) {
				item.accessory_colour = "light blue";
				item.accessory_colour_combat = "light blue";
			}
			break;
		case "brown leather jacket":
			if (!item.colour || item.colour === 0) item.colour = "brown";
			break;
		case "love locket":
			if (!item.colour || item.colour === 0) item.colour = "bronze";
			break;
		case "black leather jacket":
			if (!item.colour || item.colour === 0) item.colour = "black";
			if (!item.accessory_colour || item.accessory_colour === 0) item.accessory_colour = "silver";
			break;
		case "overall bottoms":
		case "overalls":
			if (!item.colour || item.colour === 0 || item.colour === "original") item.colour = "denim";
			if (!item.accessory_colour || item.accessory_colour === 0) item.accessory_colour = "gold";
			break;
		case "jean miniskirt":
		case "booty jorts":
		case "denim shorts":
		case "jeans":
			if (!item.colour || item.colour === 0 || item.colour === "original") item.colour = "denim";
			break;
		case "loose socks":
			if (!item.colour || item.colour === 0) item.colour = "white";
			break;
		case "cowboy hat":
			if (item.colour === 0) item.colour = "sand";
			if (!item.accessory_colour || item.accessory_colour === 0) item.accessory_colour = "black";
			break;
		case "ballgown":
		case "ballgown skirt":
		case "short ballgown":
		case "short ballgown skirt":
		case "school swim shorts":
		case "futuristic bodysuit":
		case "argyle sweater vest":
		case "diving suit":
			if (!item.accessory_colour || item.accessory_colour === 0) item.accessory_colour = item.colour;
			if (item.colourCustom) item.accessory_colourCustom = item.colourCustom;
			break;
		case "karate jacket":
			if (!item.colour || item.colour === 0) item.colour = "white";
			if (!item.accessory_colour || item.accessory_colour === 0) item.accessory_colour = "red";
			break;
		case "karate trousers":
			if (!item.colour || item.colour === 0) item.colour = "white";
			break;
		case "gingham dress":
		case "gingham skirt":
		case "patterned dress":
		case "patterned skirt":
			if (!item.pattern || item.pattern === 0) item.pattern = "gingham";
			if (!item.accessory_colour || item.accessory_colour === 0) {
				item.accessory_colour = item.colour;
				item.colour = "white";
			}
			break;
		case "animal slippers":
		case "bunny slippers":
			if (!item.pattern || item.pattern === 0) item.pattern = "bunny";
			break;
		case "plastic nurse skirt":
		case "plastic nurse dress":
		case "plastic nurse hat":
		case "pink nurse skirt":
		case "pink nurse dress":
		case "pink nurse hat":
		case "nurse skirt":
		case "nurse dress":
		case "nurse hat":
		case "nurse socks":
			if (!item.accessory_colour || item.accessory_colour === 0) item.accessory_colour = "red";
			if (!item.colour || item.colour === 0) item.colour = item.name === "nurse socks" ? "red" : "hospital pink";
			if ((!item.pattern || item.pattern === 0) && ["upper", "lower"].includes(itemRef.slot)) item.pattern = "zipper";
			break;
		case "witch hat":
			if (!item.pattern || item.pattern === 0) item.pattern = "buckle";
			break;
		case "evening gown":
		case "evening gown skirt":
			if (!item.pattern || item.pattern === 0) item.pattern = "ombre";
			if (!item.accessory_colour || item.accessory_colour === 0) item.accessory_colour = item.colour;
			break;
		case "bunny collar":
			if (!item.accessory_colour || item.accessory_colour === 0) item.accessory_colour = "red";
			if (!item.colour || item.colour === 0) item.colour = "white";
			break;
		case "cat bell collar":
			if (!item.accessory_colour || item.accessory_colour === 0) item.accessory_colour = "gold";
			if (!item.colour || item.colour === 0) item.colour = "black";
			break;
		case "cow bell":
			if (!item.accessory_colour || item.accessory_colour === 0) item.accessory_colour = "gold";
			if (!item.colour || item.colour === 0) item.colour = "black";
			break;
		case "cow onesie":
		case "cow onesie hood":
		case "cow onesie bottoms":
		case "cow sleeves":
		case "cow socks":
		case "cow panties":
		case "cow bra":
			if (!item.accessory_colour || item.accessory_colour === 0) item.accessory_colour = "black";
			break;
		case "heart choker":
			if (!item.accessory_colour || item.accessory_colour === 0) item.accessory_colour = "red";
			if (!item.colour || item.colour === 0) item.colour = "black";
			break;
		case "sexy nun's ornate veil":
		case "cargo pants":
			if (!item.accessory_colour || item.accessory_colour === 0) item.accessory_colour = "silver";
			break;
		case "racing helmet":
			if (!item.accessory_colour || item.accessory_colour === 0) item.accessory_colour = item.colour;
			if (!item.pattern || item.pattern === 0) item.pattern = "goggles";
			break;
		case "riding helmet":
			if (!item.colour || item.colour === 0) item.colour = "black";
			if (!item.accessory_colour || item.accessory_colour === 0) item.accessory_colour = "black";
			if (!item.pattern || item.pattern === 0) item.pattern = "strap";
			break;
		case "classic gothic gown":
		case "classic gothic skirt":
			if (!item.accessory_colour || item.accessory_colour === 0) item.accessory_colour = item.colour;
			break;
		case "shadbelly coat":
			if (!item.colour || item.colour === 0) item.colour = "black";
			if (!item.accessory_colour || item.accessory_colour === 0) item.accessory_colour = "yellow";
			if (!item.pattern || item.pattern === 0) item.pattern = "shirt";
			break;
		case "cheerleading top":
		case "cheerleading skirt":
		case "gym bloomers":
		case "cheerleader gloves":
		case "pom poms":
			if (!item.accessory_colour || item.accessory_colour === 0) item.accessory_colour = "white";
			break;
		case "tam o' shanter":
			if (!item.colour || item.colour === 0) item.colour = "green";
			if (!item.accessory_colour || item.accessory_colour === 0) item.accessory_colour = "red";
			if (!item.pattern || item.pattern === 0) item.pattern = "pompom";
			break;
		case "cowboy chaps":
		case "cowboy print chaps":
			if (!item.colour || item.colour === 0) item.colour = "denim";
			break;
		case "hairpin":
			if (!item.colour || item.colour === 0) item.colour = "white";
			if (!item.accessory_colour || item.accessory_colour === 0) item.accessory_colour = "white";
			break;
		default:
			if ((item.colour === 0 || !item.colour) && itemRef.colour_options?.length) item.colour = itemRef.colour_options[0];
			if ((item.pattern === 0 || !item.pattern) && itemRef.pattern_options?.length) item.pattern = itemRef.pattern_options[0];
			if ((item.accessory_colour === 0 || !item.accessory_colour) && itemRef.accessory_colour_options?.length)
				item.accessory_colour = itemRef.accessory_colour_options[0];
	}
}

// these constants should be available within the scope of these next 2 functions
const skip = [
	"integrity",
	"integrity_max",
	"colour",
	"accessory_colour",
	"pattern",
	"exposed",
	"vagina_exposed",
	"anus_exposed",
	"anal_shield",
	"one_piece",
	"skirt_down",
	"state",
	"state_top",
	"name_cap",
	"iconFile",
	"accIcon",
	"notuck",
	"skirt",
	"description",
	"colour_options",
	"accessory_colour_options",
	"pattern_options",
	"fabric_strength",
	"integrity_max",
	"bustresize",
	"sleeve_img",
	"breast_img",
	"exposed_base",
	"vagina_exposed_base",
	"anus_exposed_base",
	"state_top_base",
	"state_base",
	"word",
	"femininity",
	"strap",
	"cost",
	"shop",
	"cursed",
	"collared",
	"location",
];
const remapColours = {
	"light-pink": "light pink",
	"blue-steel": "blue steel",
};
// .variable must be the same across all outfit pieces, correct wrongly assigned props here
const remapVariables = {
	vintageskirt: "vintageskirtsuit",
	vintagepants: "vintagepantsuit",
	"chain tunic skirt": "chain tunic",
};

/**
 * Updates a single clothes object
 *
 * @param {string} slot equip slot
 * @param {object} item clothes item object
 * @param {boolean} debug print old and new object to the console
 */
/* Handheld bookbag inventory. State belongs to each clothing instance so it
   follows the item through worn, carried, wardrobe, store, and save state. */
/* Location-backed carried-item inventory. The location store is authoritative
   for migrated consumables; legacy scalar fields are compatibility mirrors only. */
const LOCATION_INVENTORY_VERSION = 1;
function locationInventoryEnsure() {
    if (!V.locationInventory || typeof V.locationInventory !== "object") V.locationInventory = { version: LOCATION_INVENTORY_VERSION, locations: {} };
    if (V.locationInventory.version !== LOCATION_INVENTORY_VERSION) V.locationInventory.version = LOCATION_INVENTORY_VERSION;
    if (!V.locationInventory.locations || typeof V.locationInventory.locations !== "object") V.locationInventory.locations = {};
    const ensure = key => {
        if (!V.locationInventory.locations[key] || typeof V.locationInventory.locations[key] !== "object") V.locationInventory.locations[key] = { items: [], forcedOverflow: [] };
        if (!Array.isArray(V.locationInventory.locations[key].items)) V.locationInventory.locations[key].items = [];
        if (!Array.isArray(V.locationInventory.locations[key].forcedOverflow)) V.locationInventory.locations[key].forcedOverflow = [];
        return V.locationInventory.locations[key];
    };
    ensure("home");
    ensure(V.location || "home");
    return V.locationInventory;
}
window.locationInventoryEnsure = locationInventoryEnsure;

function locationInventoryCurrentKey() { return V.location || "home"; }
function locationInventoryBucket(key = locationInventoryCurrentKey()) { return locationInventoryEnsure().locations[key] || locationInventoryEnsure().locations.home; }
function locationInventoryEntry(key, label, quantity = 1, data = {}) {
    return { key, name: label, label, quantity: Math.max(0, Number(quantity) || 0), data: clone(data), source: locationInventoryCurrentKey() };
}
function locationInventoryFind(list, key, predicate) {
    return list.find(entry => entry && entry.key === key && (!predicate || predicate(entry)));
}
function locationInventoryMerge(list, entry) {
    const existing = locationInventoryFind(list, entry.key, candidate => JSON.stringify(candidate.data || {}) === JSON.stringify(entry.data || {}));
    if (existing && Number.isFinite(existing.quantity) && Number.isFinite(entry.quantity)) existing.quantity += entry.quantity;
    else list.push(clone(entry));
    return existing || list[list.length - 1];
}
function locationInventoryActiveBackpack() { return window.handheldInventoryActive ? window.handheldInventoryActive() : null; }
function locationInventoryActiveSlots() {
    const bag = locationInventoryActiveBackpack();
    return bag && window.ensureHandheldInventory ? window.ensureHandheldInventory(bag) : null;
}
function locationInventoryActiveEntry(key, predicate) {
    const inventory = locationInventoryActiveSlots();
    if (!inventory) return null;
    return inventory.slots.find(entry => entry && entry.key === key && (!predicate || predicate(entry)));
}
function locationInventoryActiveQuantity(key, predicate) {
    const inventory = locationInventoryActiveSlots();
    if (!inventory) return 0;
    return inventory.slots.reduce((total, entry) => total + (entry && entry.key === key && (!predicate || predicate(entry)) ? Number(entry.quantity) || 0 : 0), 0);
}
window.locationInventoryActiveQuantity = locationInventoryActiveQuantity;

function locationInventoryCanAdd(key, quantity = 1, predicate) {
    const inventory = locationInventoryActiveSlots();
    if (!inventory || quantity <= 0) return false;
    if (locationInventoryActiveEntry(key, predicate)) return true;
    return inventory.slots.some(entry => entry == null);
}
function locationInventoryAddBackpack(entry) {
    const bag = locationInventoryActiveBackpack();
    const inventory = locationInventoryActiveSlots();
    if (!bag || !inventory || !entry) return false;
    const existing = locationInventoryActiveEntry(entry.key, candidate => JSON.stringify(candidate.data || {}) === JSON.stringify(entry.data || {}));
    if (existing && Number.isFinite(existing.quantity) && Number.isFinite(entry.quantity)) { existing.quantity += entry.quantity; return true; }
    return window.handheldInventoryAdd(bag, entry);
}
function locationInventoryAddOrdinary(entry, locationKey = locationInventoryCurrentKey()) {
    locationInventoryMerge(locationInventoryBucket(locationKey).items, entry);
    return true;
}
function locationInventoryAddForced(entry, locationKey = locationInventoryCurrentKey()) {
    const bucket = locationInventoryBucket(locationKey);
    entry.source = locationKey;
    locationInventoryMerge(bucket.forcedOverflow, entry);
    return true;
}
function locationInventoryAcquire(entry, forced = false) {
    if (!entry || !entry.key) return false;
    if (locationInventoryAddBackpack(entry)) return true;
    return forced ? locationInventoryAddForced(entry) : false;
}
function locationInventoryTake(locationKey, index, forced = false) {
    const bucket = locationInventoryBucket(locationKey);
    const list = forced ? bucket.forcedOverflow : bucket.items;
    const entry = list[index];
    if (!entry || !locationInventoryAddBackpack(entry)) return false;
    list.splice(index, 1);
    if (entry.key === "pill" && V.sexStats?.pills?.pills?.[entry.data?.pillType]) V.sexStats.pills.pills[entry.data.pillType].owned = Number(entry.quantity) || 0;
    return true;
}
function syncPillBackpackMirrors() {
    const records = V.sexStats?.pills?.pills || {};
    Object.entries(records).forEach(([type, record]) => {
        const entry = locationInventoryActiveEntry("pill", candidate => candidate.data?.pillType === type);
        if (!entry) { if (record) record.owned = 0; return; }
        if (Number(record?.owned) !== Number(entry.quantity)) entry.quantity = Math.max(0, Number(record?.owned) || 0);
        record.owned = Number(entry.quantity) || 0;
    });
}
function locationInventoryConsume(key, quantity = 1, predicate) {
    let remaining = Math.max(0, Number(quantity) || 0);
    const inventory = locationInventoryActiveSlots();
    if (!inventory || !remaining) return false;
    for (const entry of inventory.slots) {
        if (!entry || entry.key !== key || (predicate && !predicate(entry))) continue;
        const available = Number(entry.quantity) || 0;
        const used = Math.min(available, remaining);
        entry.quantity -= used;
        remaining -= used;
        if (entry.quantity <= 0) inventory.slots[inventory.slots.indexOf(entry)] = null;
        if (!remaining) return true;
    }
    return false;
}
function locationInventoryLabel(entry) {
    if (!entry) return "Stored item";
    const quantity = Number(entry.quantity);
    const label = entry.name || entry.label || entry.key || "Stored item";
    return Number.isFinite(quantity) && quantity > 1 ? `${label} (${quantity})` : label;
}
window.locationInventoryLabel = locationInventoryLabel;
window.locationInventoryCanAdd = locationInventoryCanAdd;
window.locationInventoryAcquire = locationInventoryAcquire;
window.locationInventoryTake = locationInventoryTake;
window.locationInventoryConsume = locationInventoryConsume;

function migrateLegacyLocationInventory() {
    const store = locationInventoryEnsure();
    if (V.locationInventory.migrationVersion >= 1) return;
    const quarantine = V.locationInventory.quarantine || [];
    const addLegacy = (key, label, quantity, data = {}) => {
        if (quantity === undefined || quantity === null) return;
        const numeric = Number(quantity);
        if (!Number.isFinite(numeric) || numeric < 0) { quarantine.push({ key, value: clone(quantity) }); return; }
        if (numeric > 0) locationInventoryMerge(store.locations.home.items, locationInventoryEntry(key, label, numeric, data));
    };
    addLegacy("condoms", "condoms", V.condoms);
    if (Number(V.spraymax) > 0 || Number(V.spray) > 0) addLegacy("pepper_spray", "pepper spray", 1, { charges: Math.max(0, Number(V.spray) || 0), maxCharges: Math.max(0, Number(V.spraymax) || 0), canister: true });
    addLegacy("pregnancy_test", "pregnancy test", V.pregnancyTest);
    V.locationInventory.quarantine = quarantine;
    V.locationInventory.migrationVersion = 1;
    V.condoms = 0;
    V.spray = 0;
    V.spraymax = 0;
    V.pregnancyTest = 0;
}
function migratePillState() {
    const store = locationInventoryEnsure();
    if (V.locationInventory.pillMigrationVersion >= 1 || !V.sexStats?.pills?.pills) return;
    Object.entries(V.sexStats.pills.pills).forEach(([type, record]) => {
        const quantity = Number(record?.owned) || 0;
        if (quantity > 0) locationInventoryMerge(store.locations.home.items, locationInventoryEntry("pill", record.name || type, quantity, { pillType: type }));
        if (record && typeof record === "object") record.owned = 0;
    });
    V.locationInventory.pillMigrationVersion = 1;
}
function syncLegacyInventoryMirrors() {
    const condoms = locationInventoryActiveEntry("condoms");
    const spray = locationInventoryActiveEntry("pepper_spray");
    const pregnancy = locationInventoryActiveEntry("pregnancy_test");
    V.condoms = condoms ? Math.max(0, Number(condoms.quantity) || 0) : 0;
    V.spray = spray ? Math.max(0, Number(spray.data?.charges) || 0) : 0;
    V.spraymax = spray ? Math.max(0, Number(spray.data?.maxCharges) || 0) : 0;
    V.pregnancyTest = pregnancy ? Math.max(0, Number(pregnancy.quantity) || 0) : 0;
}
function locationInventoryUpdate() {
    locationInventoryEnsure();
    migrateLegacyLocationInventory();
    migratePillState();
    if (window.handheldInventoryUpdate) window.handheldInventoryUpdate();
    syncPillBackpackMirrors();
    syncLegacyInventoryMirrors();
}
window.locationInventoryUpdate = locationInventoryUpdate;

function inventoryCondomChange(amount, forced = true) {
    const numeric = Number(amount) || 0;
    if (numeric > 0) locationInventoryAcquire(locationInventoryEntry("condoms", "condoms", numeric), forced);
    else if (numeric < 0) locationInventoryConsume("condoms", -numeric);
    syncLegacyInventoryMirrors();
}
window.inventoryCondomChange = inventoryCondomChange;

function inventoryPepperSprayAdjust(amount, forced = true) {
    const numeric = Number(amount) || 0;
    let entry = locationInventoryActiveEntry("pepper_spray");
    if (!entry && numeric > 0) {
        entry = { key: "pepper_spray", name: "pepper spray", label: "pepper spray", quantity: 1, data: { charges: 0, maxCharges: 0, canister: true }, source: locationInventoryCurrentKey() };
        if (!locationInventoryAcquire(entry, forced)) return false;
        entry = locationInventoryActiveEntry("pepper_spray") || locationInventoryBucket().forcedOverflow.find(candidate => candidate.key === "pepper_spray");
    }
    if (!entry) return false;
    entry.data = entry.data || { charges: 0, maxCharges: 0, canister: true };
    entry.data.charges = Math.clamp((Number(entry.data.charges) || 0) + numeric, 0, Number(entry.data.maxCharges) || 0);
    syncLegacyInventoryMirrors();
    return true;
}
function inventoryPepperSprayCapacity(amount, forced = true) {
    const numeric = Math.max(0, Number(amount) || 0);
    let entry = locationInventoryActiveEntry("pepper_spray");
    if (!entry) {
        entry = { key: "pepper_spray", name: "pepper spray", label: "pepper spray", quantity: 1, data: { charges: 0, maxCharges: 0, canister: true }, source: locationInventoryCurrentKey() };
        if (!locationInventoryAcquire(entry, forced)) return false;
        entry = locationInventoryActiveEntry("pepper_spray") || locationInventoryBucket().forcedOverflow.find(candidate => candidate.key === "pepper_spray");
    }
    entry.data = entry.data || { charges: 0, maxCharges: 0, canister: true };
    entry.data.maxCharges = Math.max(0, Number(entry.data.maxCharges) || 0) + numeric;
    entry.data.charges = Math.min(Number(entry.data.maxCharges), Number(entry.data.charges) || 0);
    syncLegacyInventoryMirrors();
    return true;
}
window.inventoryPepperSprayAdjust = inventoryPepperSprayAdjust;
window.inventoryPepperSprayCapacity = inventoryPepperSprayCapacity;

function inventoryPillAcquire(type, amount = 14, forced = false) {
    const record = V.sexStats?.pills?.pills?.[type];
    if (!record) return false;
    const entry = locationInventoryEntry("pill", record.name || type, amount, { pillType: type });
    if (!locationInventoryAcquire(entry, forced)) return false;
    const active = locationInventoryActiveEntry("pill", item => item.data?.pillType === type);
    record.owned = Number(active?.quantity) || 0;
    return true;
}
window.inventoryPillAcquire = inventoryPillAcquire;

function inventorySexToyCanBuy() { return !!locationInventoryActiveSlots()?.slots.some(entry => entry == null); }
window.inventorySexToyCanBuy = inventorySexToyCanBuy;

const handheldInventoryDefinitions = Object.freeze({
    purse: { slots: 2 },
    heartpurse: { slots: 2 },
    messengerbag: { slots: 3 },
    backpack: { slots: 5 },
    gymbag: { slots: 4 },
    "clock purse": { slots: 2 },
    "cloud purse": { slots: 2 },
    "teddy backpack": { slots: 4 },
    "star purse": { slots: 2 },
    totebag: { slots: 5 },
    luggage: { slots: 6 },
    "vintage suitcase": { slots: 6 },
});

function handheldInventoryDefinition(item) {
    if (!item || item.slot !== "handheld" || !item.type?.includes("bookbag")) return null;
    const key = item.variable || item.name;
    return handheldInventoryDefinitions[key] || { slots: 4 };
}
window.handheldInventoryDefinition = handheldInventoryDefinition;

function ensureHandheldInventory(item) {
    const definition = handheldInventoryDefinition(item);
    if (!definition) return null;
    let inventory = item.backpackInventory;
    if (Array.isArray(inventory)) {
        inventory = { version: 1, slots: inventory, overflow: [] };
        item.backpackInventory = inventory;
    }
    if (!inventory || typeof inventory !== "object" || !Array.isArray(inventory.slots)) {
        inventory = { version: 1, slots: [], overflow: [] };
        item.backpackInventory = inventory;
    }
    inventory.version = 1;
    if (!Array.isArray(inventory.overflow)) inventory.overflow = [];
    if (inventory.slots.length > definition.slots) {
        inventory.overflow.push(...inventory.slots.splice(definition.slots).filter(entry => entry != null));
    }
    while (inventory.slots.length < definition.slots) inventory.slots.push(null);
    return inventory;
}
window.ensureHandheldInventory = ensureHandheldInventory;

function handheldInventoryUpdate() {
    const visited = new Set();
    const visit = item => {
        if (!item || typeof item !== "object" || visited.has(item)) return;
        visited.add(item);
        ensureHandheldInventory(item);
    };
    const visitArray = items => {
        if (Array.isArray(items)) items.forEach(visit);
    };
    visit(V.worn?.handheld);
    visit(V.carried?.handheld);
    visitArray(V.wardrobe?.handheld);
    visitArray(V.store?.handheld);
    Object.values(V.wardrobes || {}).forEach(wardrobe => visitArray(wardrobe?.handheld));
    visit(V.tryOn?.ownedStored?.handheld);
    visit(V.tryOn?.tryingOn?.handheld);
}
window.handheldInventoryUpdate = handheldInventoryUpdate;

function handheldInventoryActive() {
    const item = V.worn?.handheld;
    return handheldInventoryDefinition(item) ? item : null;
}
window.handheldInventoryActive = handheldInventoryActive;

function handheldInventoryAdd(item, entry, slot) {
    const inventory = ensureHandheldInventory(item);
    if (!inventory || entry == null) return false;
    const target = Number.isInteger(slot) ? slot : inventory.slots.findIndex(value => value == null);
    if (target < 0 || target >= inventory.slots.length || inventory.slots[target] != null) return false;
    inventory.slots[target] = clone(typeof entry === "string" ? { name: entry } : entry);
    return true;
}
window.handheldInventoryAdd = handheldInventoryAdd;

function handheldInventoryRemove(item, slot) {
    const inventory = ensureHandheldInventory(item);
    if (!inventory || !Number.isInteger(slot) || slot < 0 || slot >= inventory.slots.length) return null;
    const entry = inventory.slots[slot];
    inventory.slots[slot] = null;
    return entry;
}
window.handheldInventoryRemove = handheldInventoryRemove;

function handheldInventoryRecover(item, overflowIndex) {
    const inventory = ensureHandheldInventory(item);
    if (!inventory || !Number.isInteger(overflowIndex) || overflowIndex < 0 || overflowIndex >= inventory.overflow.length) return false;
    const slot = inventory.slots.findIndex(value => value == null);
    if (slot < 0) return false;
    inventory.slots[slot] = inventory.overflow.splice(overflowIndex, 1)[0];
    return true;
}
window.handheldInventoryRecover = handheldInventoryRecover;

function handheldInventoryItemLabel(entry) {
    return entry?.name || entry?.label || entry?.item || "Stored item";
}
window.handheldInventoryItemLabel = handheldInventoryItemLabel;
function updateClothesItem(slot, item, debug) {
	if (!item) return; // might be old save that didn't have a new slot
	if (item.temp) return; // temp items are not meant to be proper clothes
	if (Object.keys(remapVariables).includes(item.variable)) item.variable = remapVariables[item.variable];
	const itemOld = clone(item);
	// transfer new properties from itemRef to the item
	const itemRef = setup.clothes[slot][clothesIndex(slot, item)];
	for (const key in itemRef) {
		// don't clone skipped keys onto the item
		if (skip.includes(key)) continue;
		// migrate some properties only if they are not already on the item
		if (["hoodposition", "altposition"].includes(key) && item[key]) continue;
		if (key === "outfitPrimary") {
			if (itemRef.outfitPrimary !== undefined) {
				if (item.outfitPrimary === undefined) item.outfitPrimary = clone(itemRef.outfitPrimary);
				for (const k in itemRef.outfitPrimary) {
					// if one_piece is broken, everything is broken
					if (item.one_piece === "broken" || item.one_piece === "split") item.outfitPrimary[k] = item.one_piece;
					else if (k === "head" && item.hoodposition === "down") delete item.outfitPrimary[k];
					// if an item is still in one piece, it's safe to regenerate it's value from itemRef
					else if (item.outfitPrimary[k] !== "broken" && item.outfitPrimary[k] !== "split") item.outfitPrimary[k] = clone(itemRef.outfitPrimary[k]);
				}
			}
			continue;
		}
		if (key === "outfitSecondary") {
			if (itemRef[key] !== undefined) {
				if (item[key] === undefined) item[key] = clone(itemRef[key]);
				if (item.one_piece === "broken" || item.one_piece === "split") item[key][1] = item.one_piece;
				// Fix both items in outfitSecondary array being "split" or "broken" when key index 0 should still be the slot of the matched item
				if (["broken", "split"].includes(item[key][0]) && item[key][0] === item[key][1]) item[key][0] = clone(itemRef[key][0]);
			}
			continue;
		}
		if (item.variable === "schoolcardigan" && item.name !== itemRef.name) {
			const colour = item.colour;
			item.name = itemRef.name;
			item.name_cap = itemRef.name_cap;
			item.colour = item.accessory_colour;
			item.accessory_colour = colour;
		}
		item[key] = clone(itemRef[key]);
	}
	item.index = itemRef.index;
	item.colour = remapColours[item.colour] || item.colour;
	item.accessory_colour = remapColours[item.accessory_colour] || item.accessory_colour;
	item.pattern = remapColours[item.pattern] || item.pattern;
	if (
		((!item.colour || item.colour === 0 || item.colour === "original") && itemRef.colour_options.length > 0) ||
		((!item.accessory_colour || item.accessory_colour === 0) && itemRef.accessory_colour_options?.length > 0) ||
		((!item.pattern || item.pattern === 0) && itemRef.pattern_options?.length > 0)
	) {
		updateClothingColours(item, itemRef);
	}

	// one_piece fix for items that shouldn't have it set
	if (["school pinafore", "plaid school pinafore"].includes(item.name) && item.one_piece === 1) item.one_piece = 0;

	// one_piece fix for items that should have it set
	if ((item.outfitPrimary || item.outfitSecondary) && item.one_piece === 0) item.one_piece = 1;

	// Clothing warmth
	if (item.warmth !== itemRef.warmth) item.warmth = itemRef.warmth;

	// Fix for 0.2.21.x issue
	if (item.colour_combat !== undefined && itemRef.colour_options.length === 0) item.colour = 0;
	if (item.accessory_colour_combat !== undefined && itemRef.colour_options.length === 0) item.accessory_colour = 0;
	// end of fix
	if (slot === "genitals") return;
	if (slot === "handheld") ensureHandheldInventory(item);

	// put renamed clothes and updated types here
	if (item.type.includes("covered")) {
		switch (item.slot) {
			case "under_upper":
				item.type.splice(item.type.indexOf("covered"), 1, "torso_covering");
				break;
			case "under_lower":
				item.type.splice(item.type.indexOf("covered"), 1, "lower_covering");
				break;
			case "lower":
				item.type.splice(item.type.indexOf("covered"), 1, "overalls");
				break;
			case "face":
				item.type.splice(item.type.indexOf("covered"), 1, "face_covering");
				break;
		}
	}

	switch (item.name) {
		case "Crop top":
			item.name = "crop top";
			break;
		case "overalls":
			if (slot === "lower") item.name = "overall bottoms";
			else if (item.outfitPrimary.lower === "overalls") item.outfitPrimary.lower = "overall bottoms";
			break;
		case "sleeveless jingle-bell dress":
			if (item.outfitPrimary.lower === "jingle-bell skirt") item.outfitPrimary.lower = "sleeveless jingle-bell skirt";
			break;
		case "Rib-knit ankle socks":
			item.name = "rib-knit ankle socks";
			break;
		case "Striped kneehighs":
			item.name = "striped kneehighs";
			break;
		case "brown leather jacket":
			item.name = "leather jacket";
			item.name_cap = "Leather jacket";
			break;
		case "black leather jacket":
			item.name = "punk leather jacket";
			item.name_cap = "Punk leather jacket";
			break;
		case "swim shirt":
			item.type = ["swim", "school", "chest_bind", "constricting", "torso_covering"];
			break;
		case "undershirt":
		case "long johns":
			item.type = ["normal", "lower_covering"];
			break;
		case "unitard bottom":
		case "leotard bottom":
		case "unitard":
		case "leotard":
		case "turtleneck leotard":
		case "skimpy leotard":
			item.type = ["dance", "torso_covering"];
			break;
		case "turtleneck leotard bottom":
		case "skimpy leotard bottom":
			item.type = ["dance"];
			break;
		case "sports bra":
			item.type = ["normal", "athletic", "torso_covering"];
			break;
		case "witch dress":
		case "scarecrow shirt":
		case "rag skirt":
		case "skeleton outfit":
		case "pom poms":
		case "futuristic bodysuit":
		case "witch skirt":
		case "scarecrow skirt":
		case "futuristic bodysuit pants":
		case "skeleton bottoms":
		case "cheerleader gloves":
			item.type = ["costume"];
			break;
		case "rag top":
		case "vampire jacket":
			item.type = ["costume", "bellyShow"];
			break;
		case "classy vampire jacket":
			item.type = ["costume", "formal"];
			break;
		case "skeleton mask":
			item.type = ["costume", "mask"];
			break;
		case "riding helmet":
		case "racing helmet":
			item.type = ["costume", "riding"];
			break;
		case "scout shorts":
		case "baseball cap":
			item.type = ["normal"];
			break;
		case "purse":
		case "backpack":
		case "messenger bag":
		case "heart purse":
			item.type = ["school", "bookbag"];
			break;
		case "boy's gym socks":
		case "girl's gym socks":
			item.type = ["school", "athletic"];
			break;
		case "padded football shirt":
			item.name = "foreign football shirt";
			item.name_cap = "Foreign football shirt";
			break;
		case "football shorts":
			item.name = item.index === 53 ? "foreign football shorts" : "football shorts";
			item.name_cap = item.index === 53 ? "Foreign football shorts" : "Football shorts";
			break;
		case "football helmet":
			item.name = "foreign football helmet";
			item.name_cap = "Foreign football helmet";
			item.type = ["costume"];
			break;
		case "soccer shorts":
			item.name = "football shorts";
			item.name_cap = "Football shorts";
			break;
		case "soccer shirt":
			item.name = "football shirt";
			item.name_cap = "Football shirt";
			break;
		case "kittycat hat":
			item.name_cap = "Kittycat hat";
			break;
		case "doggy muzzle":
			item.name_cap = "Doggy muzzle";
			break;
		case "gingham dress":
			item.name = "patterned dress";
			item.name_cap = "Patterned dress";
			break;
		case "gingham skirt":
			item.name = "patterned skirt";
			item.name_cap = "Patterned skirt";
			break;
		case "sarong":
			item.type = ["naked"];
			break;
		case "pencil skirt":
			item.name = "pencil miniskirt";
			item.name_cap = "Pencil miniskirt";
			break;
		case "bunny slippers":
			item.name = "animal slippers";
			item.name_cap = "Animal slippers";
			break;
		case "pink nurse dress":
			item.name = "nurse dress";
			item.name_cap = "Nurse dress";
			break;
		case "pink nurse skirt":
			item.name = "nurse skirt";
			item.name_cap = "Nurse skirt";
			break;
		case "pink nurse hat":
			item.name = "nurse hat";
			item.name_cap = "Nurse hat";
			break;
		case "leather miniskirt":
			item.one_piece = 0;
			item.type.pushUnique("waterproof");
			break;
		case "school skirt":
			if (item.variable === "schoolskirt2") {
				item.name = "simple school skirt";
				item.name_cap = "Simple school skirt";
			}
			break;
		case "catsuit":
		case "catsuit bottoms":
		case "cropped leather jacket":
		case "leather crop top":
		case "leather dress":
		case "leather jacket":
		case "leather leggings":
		case "leather pants":
		case "leather shorts":
		case "leather skirt":
		case "leather top":
		case "lederhosen bottoms":
		case "plastic nurse dress":
		case "plastic nurse skirt":
		case "puffer jacket":
		case "punk leather jacket":
		case "zipped leather crop top":
		case "zipped leather top":
			item.type.pushUnique("waterproof");
			break;
		case "starry witch hat":
			item.accessory = 0;
			break;
		case "slacks":
			item.type = ["formal", "school"];
	}

	if (debug) console.log("updateClothesItem:", slot, itemOld, clone(item));
}

function updateClothes() {
	for (const slot of setup.clothes_all_slots) {
		/* === $worn section === */
		const worn = V.worn[slot];
		updateClothesItem(slot, worn);

		/* === $carried section === */
		const carried = V.carried[slot];
		updateClothesItem(slot, carried);

		/* === $wardrobes section === */

		// Check for empty wardrobe items - and remove them
		Object.keys(V.wardrobe).forEach(key => {
			if (Array.isArray(V.wardrobe[key])) {
				V.wardrobe[key] = V.wardrobe[key].filter(item => item !== undefined && item !== null && item !== "");
			}
		});

		if (V.wardrobe[slot]) {
			for (const item of V.wardrobe[slot]) updateClothesItem(slot, item);
		}
		if (V.wardrobes !== undefined) {
			for (const wardrobe in V.wardrobes) {
				if (wardrobe === "wardrobe" || wardrobe === "shopReturn" || !V.wardrobes[wardrobe][slot]) continue;
				for (const item of V.wardrobes[wardrobe][slot]) updateClothesItem(slot, item);
			}
		}

		/* === $store section === */
		if (V.store !== undefined && V.store[slot]) {
			for (const item of V.store[slot]) updateClothesItem(slot, item);
		}

		/* === $outfit section === */
		for (const outfit of V.outfit) {
			switch (outfit[slot]) {
				case "Crop top":
					outfit[slot] = "crop top";
					break;
				case "overalls":
					if (slot === "lower") outfit[slot] = "overall bottoms";
					break;
				case "sleeveless jingle-bell dress":
					if (slot === "lower") outfit[slot] = "sleeveless jingle-bell skirt";
					break;
				case "pink nurse hat":
					outfit[slot] = "nurse hat";
					break;
			}
		}
	}
}
DefineMacro("updateClothes", updateClothes);

function wardrobesUpdate() {
	/* default wardrobe object */
	const defWardrobe = {
		face: [],
		feet: [],
		hands: [],
		handheld: [],
		head: [],
		legs: [],
		lower: [],
		neck: [],
		over_head: [],
		over_lower: [],
		over_upper: [],
		genitals: [],
		under_lower: [],
		under_upper: [],
		upper: [],
		unlocked: false,
		shopSend: false, // whether to allow sending or transferring clothes to location. the wardrobe MUST be isolated!!
		transfer: true, // whether to allow transfering clothes from location
		isolated: false, // whether the wardrobe has separate inventory from the default wardrobe
		locationRequirement: [],
		space: 5,
	};
	/* initialise multiple wardrobes. works for both old saves and new games */
	if (V.wardrobes === undefined) {
		V.wardrobes = {
			shopReturn: "wardrobe",
			wardrobe: {
				NOTE: "DO NOT USE THIS OBJECT TO STORE CLOTHES",
				unlocked: true,
				shopSend: true,
				transfer: true,
				name: "Orphanage",
			},
			changingRoom: clone(defWardrobe),
			edensCabin: clone(defWardrobe),
			asylum: clone(defWardrobe),
			alexFarm: clone(defWardrobe),
			stripClub: clone(defWardrobe),
			brothel: clone(defWardrobe),
			schoolBoys: clone(defWardrobe),
			schoolGirls: clone(defWardrobe),
			prison: clone(defWardrobe),
			avery_mansion: clone(defWardrobe),
		};
		/* beach */
		V.wardrobes.changingRoom.name = "Beach changing room";
		V.wardrobes.changingRoom.unlocked = true;
		/* eden's */
		V.wardrobes.edensCabin.name = "Eden's Cabin";
		V.wardrobes.edensCabin.isolated = true;
		V.wardrobes.edensCabin.space = 10;
		// allow sending clothes to the cabin when pc can leave for a day
		V.wardrobes.edensCabin.shopSend = V.edenfreedom >= 1;
		// allow transferring clothes from the cabin when pc can leave for a week
		V.wardrobes.edensCabin.transfer = V.edenfreedom >= 2;
		if (V.syndromeeden) V.wardrobes.edensCabin.unlocked = true;
		/* asylum */
		V.wardrobes.asylum.locationRequirement.push("asylum");
		V.wardrobes.asylum.name = "Asylum";
		V.wardrobes.asylum.transfer = false;
		V.wardrobes.asylum.isolated = true;
		/* alex's */
		V.wardrobes.alexFarm.name = "Alex's Farm";
		V.wardrobes.alexFarm.shopSend = true;
		V.wardrobes.alexFarm.isolated = true;
		V.wardrobes.alexFarm.space = 40;
		if (V.farm_stage >= 7) V.wardrobes.alexFarm.unlocked = true;
		/* strip club */
		V.wardrobes.stripClub.name = "Strip Club";
		V.wardrobes.stripClub.space = 10;
		if (V.stripclubdancingintro) V.wardrobes.stripClub.unlocked = true;
		/* brothel */
		V.wardrobes.brothel.name = "Brothel";
		V.wardrobes.brothel.space = 10;
		if (V.brotheljob) V.wardrobes.brothel.unlocked = true;
		/* school pool boys */
		V.wardrobes.schoolBoys.name = "Schools boy's locker";
		V.wardrobes.schoolBoys.unlocked = true;
		V.wardrobes.schoolBoys.under_lower.push(clone(setup.clothes.under_lower[7]));
		V.wardrobes.schoolBoys.under_lower.last().colour = "blue";
		/* school pool girls */
		V.wardrobes.schoolGirls.name = "Schools girl's locker";
		V.wardrobes.schoolGirls.unlocked = true;
		V.wardrobes.schoolGirls.under_lower.push(clone(setup.clothes.under_lower[6]));
		V.wardrobes.schoolGirls.under_lower.last().colour = "blue";
		V.wardrobes.schoolGirls.under_upper.push(clone(setup.clothes.under_upper[2]));
		V.wardrobes.schoolGirls.under_upper.last().colour = "blue";
		/* prison */
		V.wardrobes.prison.name = "Prison locker";
		V.wardrobes.prison.transfer = false;
		V.wardrobes.prison.isolated = true;
		/* mansion */
		V.wardrobes.avery_mansion.name = "Mansion Wardrobe";
		V.wardrobes.avery_mansion.transfer = true;
		V.wardrobes.avery_mansion.isolated = true;
		V.wardrobes.avery_mansion.shopSend = true;
		V.wardrobes.avery_mansion.space = 80;
		if (V.avery_mansion) V.wardrobes.avery_mansion.unlocked = true;
		V.wardrobes.avery_mansion.locationRequirement.push("avery_mansion", "alley");
		/* add .lastTaken prop to everything */
		if (V.worn !== undefined) Object.keys(V.worn).forEach(s => (V.worn[s].lastTaken = "wardrobe"));
		if (V.carried !== undefined) Object.keys(V.carried).forEach(s => (V.carried[s].lastTaken = "wardrobe"));
		if (V.store !== undefined) Object.keys(V.store).forEach(s => V.store[s].forEach(i => (i.lastTaken = "wardrobe")));
	}
	/* fix prison wardrobe name */
	if (V.wardrobes.prison.name === "Prison Locker") V.wardrobes.prison.name = "Prison locker";
	/* very old saves */
	if (V.objectVersion.wardrobes < 2) {
		for (const slot in setup.clothes_all_slots) {
			/* skip slots that didn't exist in old saves */
			if (V.wardrobe[slot] === undefined) continue;
			/* remove all temporary items */
			for (let j = V.wardrobe[slot].length - 1; j >= 0; j--) {
				if (V.wardrobe[slot][j].temp) V.wardrobe[slot].deleteAt(j);
			}
			for (let j = V.wardrobes.prison[slot].length - 1; j >= 0; j--) {
				if (V.wardrobes.prison[slot][j].temp) V.wardrobes.prison[slot].deleteAt(j);
			}
			for (let j = V.wardrobes.asylum[slot].length - 1; j >= 0; j--) {
				if (V.wardrobes.asylum[slot][j].temp) V.wardrobes.asylum[slot].deleteAt(j);
			}
		}
	}
	/* less old saves */
	if (V.objectVersion.wardrobes < 4) {
		/* remove unnecessary vars */
		window.clothesDataTrimmerLoop();
		/* add a slot for genitals to all wardrobes */
		if (V.wardrobe.genitals === undefined) V.wardrobe.genitals = [];
		for (const w in V.wardrobes) {
			if (w !== "wardrobe" && V.wardrobes[w].unlocked !== undefined && V.wardrobes[w].genitals === undefined) V.wardrobes[w].genitals = [];
		}
	}
	if (!V.wardrobes.temple) {
		V.wardrobes.temple = clone(defWardrobe);
		V.wardrobes.temple.unlocked = V.temple_rank === "monk";
		V.wardrobes.temple.space = 20;
	}
	if (!V.wardrobes.temple.name) {
		V.wardrobes.temple.name = "Temple";
	}
	if (!V.wardrobes.pirate) {
		V.wardrobes.pirate = clone(defWardrobe);
		V.wardrobes.pirate.unlocked = V.pirate_rank >= 0;
		V.wardrobes.pirate.space = 5;
	}
	if (!V.wardrobes.pirate.name) {
		V.wardrobes.pirate.name = "Pirate Ship";
	}
	if (V.objectVersion.wardrobes < 7) {
		Object.values(V.wardrobes).forEach(wardrobe => {
			if (wardrobe && Array.isArray(wardrobe.upper) && !wardrobe.handheld) wardrobe.handheld = [];
		});
	}

	if (!V.wardrobes.officeBuilding) {
		V.wardrobes.officeBuilding = clone(defWardrobe);
		V.wardrobes.officeBuilding.name = "Office agency changing room";
		V.wardrobes.officeBuilding.unlocked = V.officejobintro === 1;
		V.wardrobes.officeBuilding.space = 5;
	}

	if (!V.wardrobes.birdTower) {
		/* Great Hawk's tower */
		V.wardrobes.birdTower = clone(defWardrobe);
		V.wardrobes.birdTower.name = "Great Hawk's Tower";
		V.wardrobes.birdTower.unlocked = false;
		V.wardrobes.birdTower.isolated = true;
		V.wardrobes.birdTower.space = 15;
	}
	if (!V.wardrobes.birdTower.locationRequirement?.length) {
		V.wardrobes.birdTower.locationRequirement = ["tower", "moor"];
	}

	if (!V.wardrobes.prison.locationRequirement?.length) {
		V.wardrobes.prison.locationRequirement = ["prison"];
	}

	if (!V.wardrobes.avery_mansion) {
		V.wardrobes.avery_mansion = clone(defWardrobe);
		V.wardrobes.avery_mansion.name = "Mansion Wardrobe";
		V.wardrobes.avery_mansion.transfer = true;
		V.wardrobes.avery_mansion.isolated = true;
		V.wardrobes.avery_mansion.shopSend = true;
		V.wardrobes.avery_mansion.space = 80;
		V.wardrobes.avery_mansion.locationRequirement.push("avery_mansion");
	}
	if (V.avery_mansion) V.wardrobes.avery_mansion.unlocked = true;
	if (V.objectVersion.wardrobes < 16) {
		V.wardrobes.alexFarm.isolated = true;
		V.wardrobes.edensCabin.isolated = true;
		V.wardrobes.edensCabin.shopSend = V.edenfreedom >= 1;
		V.wardrobes.edensCabin.transfer = V.edenfreedom >= 2;
		V.wardrobes.wardrobe.transfer = true;
	}
	if (V.objectVersion.wardrobes < 17) {
		V.wardrobes.avery_mansion.locationRequirement.pushUnique("alley");
		/* remove broken temporary clothes creeped into main wardrobe */
		V.wardrobe.lower = V.wardrobe.lower.filter(s => !s.temp);
	}
}
DefineMacro("wardrobesUpdate", wardrobesUpdate);
