import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";
import { promptEnhanceHandler, syncDimensionsNodeHandler, searchNodeHandler, APIKeyHandler, captionNodeHandler, mediaUUIDHandler, handleCustomErrors } from "./utils.js";
import { RUNWARE_NODE_TYPES, RUNWARE_NODE_PROPS, SEARCH_TERMS } from "./types.js";

const nodeInitList = [];
app.registerExtension({
	name: "runware.ai",
    async setup() {
        api.addEventListener('runwareError', handleCustomErrors);
        api.addEventListener('runwareImageCaption', captionNodeHandler);
        api.addEventListener('runwareMediaUUID', mediaUUIDHandler);
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
        } else if(nodeClass === RUNWARE_NODE_TYPES.IMAGECAPTION) {
            const captionInput = node.widgets[1].inputEl;
            captionInput.style.outline = "none";
            captionInput.readOnly = true;
            return;
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
                    node.callback = function(){};
                    searchNodeHandler(node, nodeWidget);
                    nodeInitList.push(node);
                }
            }
        }
    },
    loadedGraphNode(node) {
        if(nodeInitList.includes(node)) node.callback();
    }
})