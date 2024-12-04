import { app } from "../../scripts/app.js";
import { promptEnhanceHandler, syncDimensionsNodeHandler, searchNodeHandler, APIKeyHandler } from "./utils.js";
import { RUNWARE_NODE_TYPES, RUNWARE_NODE_PROPS, SEARCH_TERMS } from "./types.js";

app.registerExtension({
	name: "runware.ai",
    async setup() {
        // pass
    },

    async nodeCreated(node) {
        const nodeClass = node.comfyClass;
        let crNodeProps = false;
        if(typeof nodeClass === "string" && Object.values(RUNWARE_NODE_TYPES).includes(nodeClass)) {
            crNodeProps = RUNWARE_NODE_PROPS[nodeClass];
        } else {
            return;
        }

        node.bgcolor = crNodeProps.bgColor;
        if(nodeClass === RUNWARE_NODE_TYPES.APIMANAGER) {
            APIKeyHandler(node);
        }

        if(crNodeProps.colorModeOnly === true) return;
        const nodeWidgets = node.widgets;
        if(nodeWidgets.length <= 0) return;

        for(const nodeWidget of nodeWidgets) {
            const widgetName = nodeWidget.name;
            const widgetType = nodeWidget.type;

            if(crNodeProps.promptEnhancer === true && widgetType === "customtext") {
                if (widgetName === "positivePrompt" || widgetName === "negativePrompt") {
                    nodeWidget.inputEl.addEventListener('keydown', promptEnhanceHandler);
                }
            } else if(crNodeProps.liveDimensions === true && widgetType === "combo" && widgetName === "dimensions") {
                syncDimensionsNodeHandler(node, nodeWidget);
            }

            if(crNodeProps.liveSearch === true) {
                if(widgetType === "text" && SEARCH_TERMS.includes(widgetName)) {
                    searchNodeHandler(node, nodeWidget);
                }
            }
        }
    }
})