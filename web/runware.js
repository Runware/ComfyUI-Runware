import { app } from "../../scripts/app.js";

// ----------------------------------------------------------------- API key setting

function pushKey(value) {
    fetch("/runware/set_key", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ key: value || "" }),
    }).catch(() => {});
}

app.registerExtension({
    name: "Runware.Settings",
    settings: [
        {
            id: "Runware.APIKey",
            name: "Runware API key",
            type: "text",
            defaultValue: "",
            tooltip: "Used by all Runware nodes. The RUNWARE_API_KEY environment variable takes precedence if set.",
            onChange: (value) => pushKey(value),
        },
    ],
    async setup() {
        let value = "";
        try {
            value =
                app.extensionManager?.setting?.get?.("Runware.APIKey") ??
                app.ui?.settings?.getSettingValue?.("Runware.APIKey", "") ??
                "";
        } catch (_e) {
            value = "";
        }
        if (value) pushKey(value);
    },
});

// ----------------------------------------------------------------- model picker

// Builder nodes whose `model` widget gets a catalog search, with the filter that scopes
// each one. The catalog's `category` is single-valued, so a slot that spans more than one
// (LoRA lives under both `lora` and `lycoris`) lists them in `categories`.
//
// ControlNet and IP-Adapter are intentionally absent: their compatible models depend on the
// base model's architecture, which a standalone builder node can't know, so a catalog name
// search would just surface incompatible models. Those fields stay a plain editable AIR.
const PICKER = {
    RunwareBuild_lora: { categories: ["lora", "lycoris"] },
    RunwareBuild_embeddings: { category: "embeddings" },
    RunwareBuild_refiner: { category: "checkpoint", type: "refiner" },
};

async function searchOne(params) {
    const resp = await fetch("/runware/model_search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(params),
    });
    if (!resp.ok) {
        const err = await resp.json().catch(() => ({}));
        throw new Error(err.error || `search failed (${resp.status})`);
    }
    return (await resp.json()).models || [];
}

// One catalog search, or several when the slot spans multiple categories: the per-category
// searches run in parallel and interleave into a single deduped list so each is represented.
async function searchModels(filter, search) {
    const { categories, ...rest } = filter || {};
    const base = { ...rest, search, limit: 40 };
    if (!Array.isArray(categories) || !categories.length) return searchOne(base);

    const batches = await Promise.all(categories.map((c) => searchOne({ ...base, category: c })));
    const seen = new Set(), merged = [];
    for (let i = 0; batches.some((b) => i < b.length); i++) {
        for (const b of batches) {
            const m = b[i];
            if (m && !seen.has(m.air)) { seen.add(m.air); merged.push(m); }
        }
    }
    return merged;
}

let _rwPickerStyled = false;
function rwInjectPickerCSS() {
    if (_rwPickerStyled) return;
    _rwPickerStyled = true;
    const style = document.createElement("style");
    style.textContent = `
    .rw-search { position:fixed; z-index:2147483000; display:flex; flex-direction:column;
      width:340px; max-width:90vw; background:var(--comfy-menu-bg,#2b2b2b);
      border:1px solid var(--border-color,#4e4e4e); border-radius:10px;
      box-shadow:0 10px 30px rgba(0,0,0,.5); overflow:hidden; }
    .rw-search-input { box-sizing:border-box; width:100%; height:30px; padding:0 9px;
      background:var(--comfy-input-bg,#222); color:var(--input-text,#ddd);
      border:none; border-bottom:1px solid var(--border-color,#4e4e4e); font-size:13px; outline:none; }
    .rw-search-input::placeholder { color:#777; }
    .rw-search-list { max-height:280px; overflow-y:auto; padding:4px; font-size:12px; }
    .rw-search-row { display:flex; flex-direction:column; gap:1px; padding:6px 8px;
      border-radius:6px; cursor:pointer; }
    .rw-search-row.active { background:var(--p-primary-color,#3a6df0); }
    .rw-search-row.active .rw-air { color:#dfe7ff; }
    .rw-name { color:var(--input-text,#eee); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
    .rw-air { color:#8b8b8b; font-family:monospace; font-size:11px;
      white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
    .rw-search-note { padding:9px 10px; color:#9a9a9a; }`;
    document.head.appendChild(style);
}

// Open a floating catalog search anchored near the click. The panel holds its OWN input, so
// the focused element lives inside it: with `data-capture-wheel` that is the one arrangement
// ComfyUI honours to let the results list scroll natively instead of zooming the canvas.
function rwOpenSearch(node, modelWidget, filter, event) {
    rwInjectPickerCSS();
    if (document._rwSearchClose) document._rwSearchClose();

    const panel = document.createElement("div");
    panel.className = "rw-search";
    panel.setAttribute("data-capture-wheel", "true");

    const input = document.createElement("input");
    input.type = "text";
    input.className = "rw-search-input";
    input.placeholder = "Search Runware models…";
    input.autocomplete = "off";
    input.spellcheck = false;
    input.value = modelWidget.value || "";

    const list = document.createElement("div");
    list.className = "rw-search-list";
    panel.append(input, list);
    document.body.appendChild(panel);

    // anchor at the click, then nudge back inside the viewport
    const px = event?.clientX ?? window.innerWidth / 2;
    const py = event?.clientY ?? window.innerHeight / 2;
    panel.style.left = `${Math.min(px, window.innerWidth - 350)}px`;
    panel.style.top = `${Math.min(py, window.innerHeight - 320)}px`;

    let items = [], active = -1, seq = 0, debounce = null;
    const paint = () => [...list.children].forEach((c, i) => c.classList.toggle("active", i === active));
    const scrollActive = () => { const el = list.children[active]; if (el?.scrollIntoView) el.scrollIntoView({ block: "nearest" }); };

    function close() {
        document.removeEventListener("pointerdown", onDocPointer, true);
        document.removeEventListener("keydown", onKey, true);
        panel.remove();
        if (document._rwSearchClose === close) document._rwSearchClose = null;
    }
    document._rwSearchClose = close;

    function note(text) {
        list.replaceChildren();
        const d = document.createElement("div");
        d.className = "rw-search-note";
        d.textContent = text;
        list.appendChild(d);
    }
    function pick(m) {
        modelWidget.value = m.air;
        if (modelWidget.callback) modelWidget.callback(m.air);
        node.setDirtyCanvas(true, true);
        close();
    }
    function render() {
        list.replaceChildren();
        items.forEach((m, i) => {
            const row = document.createElement("div");
            row.className = "rw-search-row" + (i === active ? " active" : "");
            const name = document.createElement("span");
            name.className = "rw-name";
            name.textContent = m.name;
            const air = document.createElement("span");
            air.className = "rw-air";
            air.textContent = m.air;
            row.append(name, air);
            row.addEventListener("pointerdown", (e) => { e.preventDefault(); pick(m); });
            row.addEventListener("mouseenter", () => { active = i; paint(); });
            list.appendChild(row);
        });
    }
    async function query() {
        const term = input.value.trim();
        const my = ++seq;
        note("Searching…");
        try {
            const models = await searchModels(filter, term);
            if (my !== seq) return;  // a newer query superseded this one
            items = models;
            active = models.length ? 0 : -1;
            if (!models.length) return note(`No models found${term ? ` for "${term}"` : ""}.`);
            render();
        } catch (err) {
            if (my !== seq) return;
            note(`Search error: ${err.message}`);
        }
    }

    const onKey = (e) => {
        if (e.key === "ArrowDown") { active = Math.min(active + 1, items.length - 1); paint(); scrollActive(); e.preventDefault(); }
        else if (e.key === "ArrowUp") { active = Math.max(active - 1, 0); paint(); scrollActive(); e.preventDefault(); }
        else if (e.key === "Enter") { if (items[active]) { pick(items[active]); e.preventDefault(); } }
        else if (e.key === "Escape") { close(); e.preventDefault(); }
    };
    // close only on a click outside the panel, so clicking the list or its scrollbar keeps it open
    const onDocPointer = (e) => { if (!panel.contains(e.target)) close(); };

    input.addEventListener("input", () => { clearTimeout(debounce); debounce = setTimeout(query, 250); });
    document.addEventListener("keydown", onKey, true);
    document.addEventListener("pointerdown", onDocPointer, true);
    input.focus();
    query();
}

// Give a node's `model` widget a catalog search: the field stays editable (paste an AIR
// directly), and a button right beneath it opens the search panel scoped to this node.
function rwAttachModelSearch(node, filter) {
    const modelWidget = node.widgets?.find((w) => w.name === "model");
    if (!modelWidget || node._rwSearchBtn) return;
    node._rwSearchBtn = true;

    const btn = node.addWidget("button", "🔍 search catalog", null, (_v, _canvas, n, _pos, event) => {
        rwOpenSearch(n || node, modelWidget, filter, event);
    });
    btn.serialize = false;

    // move the button to sit immediately under the model field, not at the node's bottom
    const bi = node.widgets.indexOf(btn);
    if (bi !== -1) node.widgets.splice(bi, 1);
    const mi = node.widgets.indexOf(modelWidget);
    node.widgets.splice(mi + 1, 0, btn);
}

app.registerExtension({
    name: "Runware.ModelPicker",
    beforeRegisterNodeDef(nodeType, nodeData) {
        // Architecture nodes carry their search scope on the `model` widget (the arch id),
        // read from the node definition since ComfyUI drops custom widget options at runtime.
        const defs = { ...(nodeData.input?.required || {}), ...(nodeData.input?.optional || {}) };
        const opts = Array.isArray(defs.model) ? defs.model[1] : null;
        if (opts && opts.rw_model_picker) {
            nodeType.prototype._rwPickerFilter = { category: "checkpoint", architecture: opts.rw_model_picker };
        }
    },
    nodeCreated(node) {
        const filter = PICKER[node.comfyClass || node.type] || node._rwPickerFilter;
        if (!filter) return;
        rwAttachModelSearch(node, filter);
    },
});

// ----------------------------------------------------------------- socket model scope

// ControlNet/IP-Adapter models are model-specific: each base model (or architecture) pins the
// set it accepts, carried on its socket as `rw_socket_models`. Those builders are stackable, so
// only the last one touches the model node directly; the rest chain into another builder. So we
// walk a builder's output forward through the chain to the terminal model/architecture node, and
// scope the builder's `model` field to that node's list (a dropdown), or leave it a free text
// field when nothing downstream constrains it.

// Builders whose fields (and per-field dropdowns) can vary by the wired model. Array builders
// (ControlNet/IP-Adapter add advanced params per architecture; LoRA's `transformer` is video-only)
// are stackable and get field-scoping; ControlNet/IP-Adapter also carry a scoped `model` list. The
// Speech builder is a single-object union: its fields differ per model and its `voice`/`language`
// dropdowns are model-specific, so it also carries per-field enum lists on the socket.
const RW_SOCKET_BUILDER = {
    RunwareBuild_controlNet: "controlNet", RunwareBuild_ipAdapters: "ipAdapters",
    RunwareBuild_lora: "lora", RunwareBuild_embeddings: "embeddings",
    RunwareBuild_speech: "speech",
    RunwareBuild_referenceImages: "referenceImages", RunwareBuild_referenceVideos: "referenceVideos",
    RunwareBuild_referenceVoices: "referenceVoices",
    RunwareBuild_acceleratorOptions: "acceleratorOptions", RunwareBuild_outpaint: "outpaint",
};
const RW_SOCKET_SLOTS = ["controlNet", "ipAdapters", "lora", "embeddings", "speech",
    "referenceImages", "referenceVideos", "referenceVoices", "acceleratorOptions", "outpaint"];

// Builders whose per-field dropdowns are model-specific: Speech `voice`/`language`, and reference-
// group `role`/`type` (try-on roles vs SkyReels grid/image differ per model). When wired, each
// supported field's widget becomes the host's list, a free text field when the host takes an open
// value, or is hidden by rwSync when unsupported. (Widget hiding only — IMAGE input sockets like a
// reference group's `image`/`images` are not hidden, so both can still show; the model node strips
// whichever it doesn't accept from the request.)
const RW_ENUM_SCOPED_BUILDERS = new Set([
    "RunwareBuild_speech",
    "RunwareBuild_referenceImages", "RunwareBuild_referenceVideos", "RunwareBuild_referenceVoices",
]);

function rwGraphNodes(graph) {
    return (graph && (graph._nodes || graph.nodes)) || [];
}

// Follow the builder's `slot` output through any same-kind builders to the model/architecture
// node it ultimately feeds; return that host's {models, fields} for the slot (its allowed model
// list and the item fields it accepts), or null when nothing downstream constrains it.
function rwTerminalHost(builder, slot) {
    const graph = builder.graph;
    if (!graph) return null;
    let node = builder;
    const seen = new Set();
    while (node && !seen.has(node.id)) {
        seen.add(node.id);
        const out = node.outputs?.find((o) => o.name === slot);
        const links = out && out.links;
        if (!links || !links.length) return null;
        const link = graph.links?.[links[0]];
        if (!link) return null;
        const target = graph.getNodeById(link.target_id);
        if (!target) return null;
        const models = target._rwSocketModels?.[slot];
        const fields = target._rwSocketFields?.[slot];
        const enums = target._rwSocketEnums?.[slot];
        if (Array.isArray(models) || Array.isArray(fields) || (enums && typeof enums === "object")) {
            return { models: models ?? null, fields: fields ?? null, enums: enums ?? null };
        }
        if (RW_SOCKET_BUILDER[target.comfyClass || target.type] === slot) { node = target; continue; }
        return null;  // reached a host that does not pin this slot, or a dead end
    }
    return null;
}

// Swap a named widget between a scoped dropdown and a free text field, preserving the current
// value. `keepOffList` keeps a value that isn't in the new list selectable (so loading never drops
// a saved free-form AIR) — correct for a builder's `model` field. Speech's `voice`/`language` pass
// it false: a value from another model is never valid here, so the stale one is dropped instead of
// leaking into the new model's list as an extra option.
function rwSetComboWidget(node, name, values, keepOffList = true) {
    const idx = node.widgets ? node.widgets.findIndex((w) => w.name === name) : -1;
    if (idx < 0) return;
    const old = node.widgets[idx];
    const cur = old.value == null ? "" : String(old.value);
    const move = (w) => {
        const at = node.widgets.indexOf(w);
        if (at !== -1) node.widgets.splice(at, 1);
        node.widgets.splice(idx, 1, w);
        node.setDirtyCanvas(true, true);
    };
    if (Array.isArray(values) && values.length) {
        const vals = keepOffList && cur && !values.includes(cur) ? [cur, ...values] : values.slice();
        if (old.type === "combo" && String(old.options?.values) === String(vals)) return;  // unchanged
        move(node.addWidget("combo", name, vals.includes(cur) ? cur : vals[0], () => {}, { values: vals }));
    } else if (old.type === "combo") {
        move(node.addWidget("text", name, cur, () => {}));
    }
}

const rwSetModelWidget = (node, values) => rwSetComboWidget(node, "model", values);

function rwRescopeSockets(graph) {
    for (const node of rwGraphNodes(graph)) {
        const slot = RW_SOCKET_BUILDER[node.comfyClass || node.type];
        if (!slot) continue;
        try {
            const host = rwTerminalHost(node, slot);
            rwSetModelWidget(node, host?.models ?? null);
            // the fields the wired host accepts drive widget visibility; rwSync (below) reads
            // this and hides the rest, so it never fights the gate/size visibility it also owns
            const hostFields = Array.isArray(host?.fields) ? new Set(host.fields) : null;
            // object-feature builders (Speech): each supported field's dropdown becomes the host's
            // list, or a free text field when the host supports it without one (rwSetComboWidget is a
            // no-op on non-combo widgets like text/speed). Gated so array builders are untouched.
            if (RW_ENUM_SCOPED_BUILDERS.has(node.comfyClass || node.type) && hostFields) {
                const hostEnums = host?.enums || {};
                for (const f of hostFields) rwSetComboWidget(node, f, hostEnums[f] || null, false);
            }
            node._rwHostFields = hostFields;
            rwSync(node);
        } catch (e) { console.error("[Runware] socket scope", e); }
    }
}

app.registerExtension({
    name: "Runware.SocketModelScope",
    beforeRegisterNodeDef(nodeType, nodeData) {
        const name = nodeData?.name || "";
        const isBuilder = name in RW_SOCKET_BUILDER;
        const isHost = name.startsWith("Runware_") || name.startsWith("RunwareArch_");
        if (!isBuilder && !isHost) return;

        // Host nodes (models + architectures) publish their allowed lists off the socket options,
        // read from the definition since ComfyUI drops custom options off the live input.
        if (isHost) {
            const defs = { ...(nodeData.input?.required || {}), ...(nodeData.input?.optional || {}) };
            const models = {}, fields = {}, enums = {};
            for (const slot of RW_SOCKET_SLOTS) {
                const opts = Array.isArray(defs[slot]) ? defs[slot][1] : null;
                if (opts && Array.isArray(opts.rw_socket_models)) models[slot] = opts.rw_socket_models;
                if (opts && Array.isArray(opts.rw_socket_fields)) fields[slot] = opts.rw_socket_fields;
                if (opts && opts.rw_socket_enums && typeof opts.rw_socket_enums === "object") enums[slot] = opts.rw_socket_enums;
            }
            if (Object.keys(models).length) nodeType.prototype._rwSocketModels = models;
            if (Object.keys(fields).length) nodeType.prototype._rwSocketFields = fields;
            if (Object.keys(enums).length) nodeType.prototype._rwSocketEnums = enums;
        }

        // Any connection anywhere in a chain can change a builder's terminal, and upstream
        // builders never get their own event, so re-scope the whole graph's socket builders.
        const prev = nodeType.prototype.onConnectionsChange;
        nodeType.prototype.onConnectionsChange = function () {
            const r = prev?.apply(this, arguments);
            try { rwRescopeSockets(this.graph); } catch (e) { /* graph not ready */ }
            return r;
        };
    },
});

// ----------------------------------------------------------------- run info badge

// After a run, model / architecture / custom nodes report a short line (cost + whether the
// safety check flagged the result) in the execution message. Paint it along the title bar,
// so it stays visible even when the node body is filled with widgets or a preview.
app.registerExtension({
    name: "Runware.RunInfo",
    beforeRegisterNodeDef(nodeType, nodeData) {
        const name = nodeData?.name || "";
        if (!(name.startsWith("Runware_") || name.startsWith("RunwareArch_") || name === "RunwareCustom")) return;

        const onExecuted = nodeType.prototype.onExecuted;
        nodeType.prototype.onExecuted = function (message) {
            onExecuted?.apply(this, arguments);
            const info = message?.runware_info?.[0];
            if (info) {
                this._rwInfo = info;
                this.setDirtyCanvas(true, true);
            }
        };

        const onDraw = nodeType.prototype.onDrawForeground;
        nodeType.prototype.onDrawForeground = function (ctx) {
            onDraw?.apply(this, arguments);
            if (this.flags?.collapsed || !this._rwInfo) return;
            const th = LiteGraph.NODE_TITLE_HEIGHT;
            ctx.save();
            ctx.font = "600 11px sans-serif";
            ctx.fillStyle = "#7ec98f";  // soft green, reads on the dark title bar
            ctx.textAlign = "right";
            ctx.textBaseline = "middle";
            ctx.fillText(this._rwInfo, this.size[0] - 10, -th * 0.5);
            ctx.restore();
        };
    },
});

// ----------------------------------------------------------------- node layout

// Pure UI polish over the Python plan: draw section headers between widget groups,
// and turn no-default numeric params into reveal toggles (a "set X" checkbox that
// shows its value field only when on). The request itself is built server-side from
// the widget values, so generation is correct even if any of this is skipped.

const RW_HIDDEN = "rw_hidden";

// The <textarea> behind a multiline STRING widget, if this widget is one. Number / combo / boolean
// widgets in newer frontends also carry an `.element`, but ComfyUI manages their layout — toggling
// their display leaves a stale width that overflows the node, so touch ONLY a real textarea.
function rwTextarea(widget) {
    const el = widget.inputEl || widget.element;
    if (!el) return null;
    if (el.tagName === "TEXTAREA") return el;
    return el.querySelector ? el.querySelector("textarea") : null;
}

function rwHide(widget) {
    if (widget.hidden) return;
    widget.hidden = true;
    widget._rwType = widget.type;
    widget._rwCompute = widget.computeSize;
    widget.type = RW_HIDDEN;
    widget.computeSize = () => [0, -4];
    const ta = rwTextarea(widget);
    if (ta) { widget._rwDisplay = ta.style.display; ta.style.display = "none"; }
}

function rwShow(widget) {
    if (!widget.hidden) return;
    widget.hidden = false;
    widget.type = widget._rwType;
    widget.computeSize = widget._rwCompute;
    // litegraph draws a widget at `widget.width || node_width`; a widget hidden at node creation can
    // keep a stale cached `.width` and then draw past the node edge. Clear it so it uses node width.
    widget.width = undefined;
    const ta = rwTextarea(widget);
    if (ta) ta.style.display = widget._rwDisplay ?? "";
}

function rwResize(node) {
    const size = node.computeSize();
    node.setSize([Math.max(node.size[0], size[0]), size[1]]);
    node.setDirtyCanvas(true, true);
}

// A gate's value widget, found via the metadata hint or the "<name>_value"
// convention, so it works even if ComfyUI drops the custom widget option.
function rwGateValue(w, byName) {
    const key = w.options?.rw_gates || (byName[w.name + "_value"] ? w.name + "_value" : null);
    return key ? byName[key] : null;
}

// Visibility for every widget: a gate's value field is hidden when its toggle is off,
// and any field is hidden when a real on/off boolean it belongs to (by name prefix,
// e.g. teaCache -> teaCacheDistance) is off. A "real" boolean is a toggle with no
// `_value` sibling, which distinguishes it from a reveal gate.
function rwSync(node) {
    if (!node.widgets) return;
    const byName = {};
    for (const w of node.widgets) byName[w.name] = w;
    const offParents = node.widgets
        .filter((w) => w.type === "toggle" && !byName[w.name + "_value"] && !w.value)
        .map((w) => w.name);
    // A `size` dropdown set to a resolution tier sends that instead of width/height, so
    // hide the (now ignored) dimension widgets on the free-dimension models that keep them.
    const size = byName["size"];
    const sizeHidesDims = size && typeof size.value === "string" && size.value.endsWith("(from input)");
    for (const w of node.widgets) {
        if (w.type === "rw_header") continue;
        let hidden = offParents.some((p) => w.name !== p && w.name.startsWith(p));
        if (!hidden && sizeHidesDims && (w.name === "width" || w.name === "height")) hidden = true;
        if (!hidden && w.name.endsWith("_value")) {
            const toggle = byName[w.name.slice(0, -"_value".length)];
            if (toggle && !toggle.value) hidden = true;
        }
        // a socket builder wired to a host that doesn't declare this item field hides it (the
        // host also strips it from the request, so this is purely visual). `button` is the LoRA
        // search affordance, not an item field, so it is never scoped away.
        if (!hidden && node._rwHostFields && w.type !== "button") {
            const base = w.name.endsWith("_value") ? w.name.slice(0, -"_value".length) : w.name;
            if (!node._rwHostFields.has(base)) hidden = true;
        }
        if (hidden) rwHide(w); else rwShow(w);
    }
    rwResize(node);
}

// Relabel gate widgets ("set X" toggle, "X" value) and hook every toggle to re-sync.
function rwSetupGates(node) {
    if (!node.widgets) return;
    const byName = {};
    for (const w of node.widgets) byName[w.name] = w;
    for (const w of node.widgets) {
        const value = rwGateValue(w, byName);
        if (value) {
            value.label = w.name;
            w.label = "set " + w.name;
        }
        if ((w.type === "toggle" || w.name === "size") && !w._rwHooked) {  // toggles + the size combo re-sync
            w._rwHooked = true;
            const prev = w.callback;
            w.callback = function () {
                const r = prev ? prev.apply(this, arguments) : undefined;
                rwSync(node);
                return r;
            };
        }
    }
}

function rwHeader(label) {
    return {
        name: "rw_header_" + label,
        type: "rw_header",
        value: undefined,
        options: { serialize: false },
        serialize: false,
        computeSize: () => [0, 22],
        draw(ctx, node, width, y) {
            const text = label.toUpperCase();
            // Derive the right edge from the node's own width (authoritative in widget-draw
            // coords) and match LiteGraph's 15px widget margin, so the rule never overshoots
            // the node however the passed `width` is measured.
            const margin = 15;
            const right = (node?.size?.[0] ?? width) - margin;
            ctx.save();
            ctx.font = "600 10px sans-serif";
            ctx.fillStyle = "#9a9a9a";
            ctx.fillText(text, margin, y + 15);
            const tw = ctx.measureText(text).width;
            ctx.strokeStyle = "rgba(150,150,150,0.25)";
            ctx.beginPath();
            ctx.moveTo(margin + tw + 8, y + 11);
            ctx.lineTo(Math.max(margin + tw + 8, right), y + 11);
            ctx.stroke();
            ctx.restore();
        },
    };
}

// Insert a header before the first widget of each section. Idempotent. The section
// map comes from the node definition (node._rwCats), since ComfyUI drops the custom
// rw_cat option from the live widget.
function rwAddSections(node) {
    if (!node.widgets || !node._rwCats) return;
    const widgets = node.widgets.filter((w) => w.type !== "rw_header");
    const out = [];
    let last = null;
    for (const w of widgets) {
        const cat = node._rwCats[w.name];
        if (cat && cat !== last) {
            out.push(rwHeader(cat));
            last = cat;
        }
        out.push(w);
    }
    node.widgets = out;
}

app.registerExtension({
    name: "Runware.NodeLayout",
    beforeRegisterNodeDef(nodeType, nodeData) {
        const name = nodeData?.name || "";
        const isModel = name.startsWith("Runware_");
        const isBuilder = name.startsWith("RunwareBuild_");
        if (!isModel && !isBuilder) return;

        // ComfyUI drops custom widget options at runtime, so read the section labels
        // from the node definition (which keeps them) and stash a name -> section map.
        const cats = {};
        const defs = { ...(nodeData.input?.required || {}), ...(nodeData.input?.optional || {}) };
        for (const key in defs) {
            const opts = Array.isArray(defs[key]) ? defs[key][1] : null;
            if (opts && opts.rw_cat) cats[key] = opts.rw_cat;
        }
        nodeType.prototype._rwCats = cats;

        const onCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            const r = onCreated?.apply(this, arguments);
            try {
                rwSetupGates(this);
                rwAddSections(this);  // no-op unless widgets carry rw_cat (models always, grouped builders)
                rwSync(this);
            } catch (e) {
                console.error("[Runware] layout error", e);
            }
            return r;
        };

        const onConfigure = nodeType.prototype.onConfigure;
        nodeType.prototype.onConfigure = function () {
            const r = onConfigure?.apply(this, arguments);
            try { rwSync(this); } catch (e) { console.error("[Runware] layout error", e); }
            return r;
        };
    },
});
