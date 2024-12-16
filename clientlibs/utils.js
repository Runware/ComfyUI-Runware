import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";
import { DEFAULT_DIMENSIONS_LIST, DEFAULT_MODELS_ARCH_LIST, DEFAULT_CONTROLNET_CONDITIONING_LIST,
    RUNWARE_NODE_TYPES, MODEL_TYPES_TERMS, MODEL_LIST_TERMS
} from "./types.js";

let openDialog = false;
let lastTimeout = false;

async function enhancePrompt(userPrompt) {
    const resp = await api.fetchApi('/promptEnhance', {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            userPrompt: userPrompt
        })
    });
    const enhancePromptResults = await resp.json();
    return enhancePromptResults;
}

async function setAPIKey(apiKey) {
    const resp = await api.fetchApi('/setAPIKey', {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            apiKey: apiKey
        })
    });
    const setAPIKeyResults = await resp.json();
    return setAPIKeyResults;
}

async function setTimeout(maxTimeout) {
    const resp = await api.fetchApi('/setMaxTimeout', {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            maxTimeout: maxTimeout
        })
    });
    const setTimeoutResults = await resp.json();
    return setTimeoutResults;
}

async function modelSearch(modelQuery = "", modelArch = "all", modelType = "base", modelCat = "checkpoint", condtioning = "") {
    const resp = await api.fetchApi('/modelSearch', {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            modelQuery: modelQuery,
            modelArch: modelArch,
            modelType: modelType,
            modelCat: modelCat,
            condtioning: condtioning
        })
    });
    const modelSearchResults = await resp.json();
    return modelSearchResults;
}

function captionNodeHandler(msgEvent) {
    const captionData = msgEvent.detail;
    const captionText = captionData.captionText;
    const captionNodeID = parseInt(captionData.nodeID);
    if(captionData.success) {
        const captionNode = app.graph.getNodeById(captionNodeID);
        if(captionNode !== null || captionNode !== undefined) {
            const captionInput = captionNode.widgets[1].inputEl;
            captionInput.value = captionText;
        }
    }
    return false;
}

function notifyUser(message, type="info", title = "Runware", life = 4.5) {
    app.extensionManager.toast.add({
        severity: type, // 'info', 'success', 'warn', 'error' \\
        summary: title,
        detail: message,
        life: Math.floor(life * 1000)
    });
}

async function promptEnhanceHandler(e) {
    if(e.ctrlKey && e.altKey && e.key.toLowerCase() === 'e') {
        const userPrompt = e.target.value.trim();
        if(userPrompt.length <= 1) {
            notifyUser("Prompt Is Too Short!", "error", "Runware Prompt Enhancer");
            return;
        } else if(userPrompt.length > 300) {
            notifyUser("Prompt Must Not Exceed 300 Characters!", "error", "Runware Prompt Enhancer");
            return;
        }
        const enhanceResults = await enhancePrompt(userPrompt);
        if(enhanceResults.success) {
            e.target.value = enhanceResults.enhancedPrompt;
        } else {
            notifyUser(enhanceResults.error, "error", "Runware Prompt Enhancer");
        }
    }
}

function remNode(node) {
    app.graph.remove(node);
    app.graph.setDirtyCanvas(true,true);
}

async function APIKeyHandler(apiManagerNode) {
    const widgets = apiManagerNode.widgets;
    for(const widget of widgets) {
        if(widget.name === "API Key") {
            appendWidgetCB(widget, async function(...args) {
                if(openDialog) return;
                const apiKey = args[0].trim();
                if(apiKey.length < 30) {
                    notifyUser("Invalid API Key Set, Please Try Again!", "error", "Runware API Manager");
                    return;
                } else {
                    const setAPIKeyResults = await setAPIKey(apiKey);
                    if(setAPIKeyResults.success) {
                        remNode(apiManagerNode);
                        notifyUser("API Key Set Successfully!", "success", "Runware API Manager");
                    } else {
                        notifyUser(setAPIKeyResults.error, "error", "Runware API Manager");
                    }
                }
            });
        } else if(widget.name === "Max Timeout") {
            if(lastTimeout) widget.value = lastTimeout;
            appendWidgetCB(widget, async function(...args) {
                const maxTimeout = args[0];
                if(maxTimeout < 5 || maxTimeout > 99) {
                    notifyUser("Invalid Timeout Value, Timeout must be between 5 and 99 seconds!", "error", "Runware API Manager");
                    return;
                } else {
                    const setTimeoutResults = await setTimeout(maxTimeout);
                    if(setTimeoutResults.success) {
                        remNode(apiManagerNode);
                        notifyUser("Timeout Set Successfully!", "success", "Runware API Manager");
                        lastTimeout = maxTimeout;
                    } else {
                        notifyUser(setTimeoutResults.error, "error", "Runware API Manager");
                    }
                }
            });
        }
    }
}

function handleCustomErrors(errObj) {
    const errData = errObj.detail;
    const errCode = errData.errorCode;
    if(errCode === 401 && !openDialog) {
        const dialog = new comfyAPI.asyncDialog.ComfyAsyncDialog();
        const htmlContent = `
                <center>
                    <div style="padding: auto 200px; text-align: center;">
                        <h2>Runware Inference Error</h2>
                        <h4>Your API Key is Invalid Or Undefined. You Need To Update It.</h4>
                        <form method="POST" id="runwareAPIKey">
                            <input 
                                id="apiKey" 
                                type="text" 
                                placeholder="Enter Your API Key ..." minlength="30" maxlength="48"
                                style="padding: 5px; min-width: 300px; text-align: center; margin-top: 10px;" required>

                            <div style="margin-top: 15px; display: flex; justify-content: center; gap: 10px;">
                                <button id="setAPIKeyBTN" style="padding: 8px 15px; background-color: #6c5ce7; color: #ccc;">Set Your API Key</button>
                                <button  id="getAPIKeyBTN" style="padding: 8px 15px; background-color: #dfe6e9; color: #000;">Create New API Key</button>
                            </div>
                        </form>
                    </div>
                </center>
    `;
        dialog.showModal(htmlContent).then(() => {
            openDialog = false;
        });
        openDialog = true;
        dialog.element.addEventListener('close', () => {
            openDialog = false;
        });
        const runwareAPIForm = document.getElementById("runwareAPIKey");
        const apiKeyInput = document.getElementById("apiKey");
        const getAPIKeyBTN = document.getElementById("getAPIKeyBTN");
        const setAPIKeyBTN = document.getElementById("setAPIKeyBTN");

        getAPIKeyBTN.onclick = (e) => {
            e.preventDefault();
            window.open("https://my.runware.ai/keys?utm_source=comfyui&utm_medium=referral&utm_campaign=comfyui_api_key_creation", "_blank");
        };

        async function authUser(e) {
            e.preventDefault();
            e.stopPropagation();
            const apiKey = apiKeyInput.value.trim();
            if(apiKey.length < 30) {
                notifyUser("Invalid API Key Set, Please Try Again!", "error", "Runware API Manager");
                return;
            } else {
                const setAPIKeyResults = await setAPIKey(apiKey);
                if(setAPIKeyResults.success) {
                    dialog.close();
                    openDialog = false;
                    notifyUser("API Key Set Successfully!", "success", "Runware API Manager");
                } else {
                    notifyUser(setAPIKeyResults.error, "error", "Runware API Manager");
                }
            }
        };

        setAPIKeyBTN.onclick = async (e) => {
            authUser(e);
        };

        runwareAPIForm.onsubmit = async (e) => {
            authUser(e);
        };
    }
}

function appendWidgetCB(node, newCB) {
    const oldNodeCB = node.callback;
    if(typeof oldNodeCB === "function") {
        node.callback = function(...args) {
            newCB?.apply(this, args);
            oldNodeCB?.apply(this, args);
        }
    } else {
        node.callback = newCB;
    }
}

async function syncDimensionsNodeHandler(node, dimensionsWidget) {
    const nodeWidgets = node.widgets;
    let widthWidget = false, heightWidget = false;
    for(const nodeWidget of nodeWidgets) {
        const widgetName = nodeWidget.name;
        const widgetType = nodeWidget.type;
        if(widgetName === "width" && widgetType === "number") widthWidget = nodeWidget;
        if(widgetName === "height" && widgetType === "number") heightWidget = nodeWidget;
    }

    appendWidgetCB(dimensionsWidget, function(...args) {
        const chosenDimension = args[0];
        if(chosenDimension === "Custom") return;
        const dimensionValue = DEFAULT_DIMENSIONS_LIST[chosenDimension];
        const [width, height] = dimensionValue.split("x");
        widthWidget.callback(width, "customSetOperation");
        heightWidget.callback(height, "customSetOperation");
    });

    if(widthWidget !== false) {
        appendWidgetCB(widthWidget, function(...args) {
            if(args[1] === "customSetOperation") return;
            dimensionsWidget.value = "Custom";
        });
    }

    if(heightWidget !== false) {
        appendWidgetCB(heightWidget, function(...args) {
            if(args[1] === "customSetOperation") return;
            dimensionsWidget.value = "Custom";
        });
    }
}

async function searchNodeHandler(searchNode, searchInputWidget) {
    const searchNodeWidgets = searchNode.widgets;
    let modelArchWidget = false, modelTypeWidget = false, modelListWidget = false, defaultWidgetValues = {};
    let isLora = false, isControlNet = false, modelTypeValue;
    if(searchNode.comfyClass === RUNWARE_NODE_TYPES.LORASEARCH) isLora = true;
    if(searchNode.comfyClass === RUNWARE_NODE_TYPES.CONTROLNET) isControlNet = true;
    for(const searchWidget of searchNodeWidgets) {
        const widgetName = searchWidget.name;
        const widgetType = searchWidget.type;
        if(widgetName === "Model Architecture" && widgetType === "combo") {
            modelArchWidget = searchWidget;
            defaultWidgetValues["modelArch"] = searchWidget.options.values;
        }
        if(MODEL_TYPES_TERMS.includes(widgetName) && widgetType === "combo") {
            modelTypeWidget = searchWidget;
            defaultWidgetValues["modelType"] = searchWidget.options.values;
        }
        if(MODEL_LIST_TERMS.includes(widgetName) && widgetType === "combo") {
            modelListWidget = searchWidget;
            defaultWidgetValues["modelList"] = searchWidget.options.values;
        }
    }

    function resetValues() {
        if(modelArchWidget) {
            modelArchWidget.options.values = defaultWidgetValues["modelArch"];
            modelArchWidget.value = defaultWidgetValues["modelArch"][0];
        }
        if(modelTypeWidget) {
            modelTypeWidget.options.values = defaultWidgetValues["modelType"];
            modelTypeWidget.value = defaultWidgetValues["modelType"][0];
        }
        if(modelListWidget) {
            modelListWidget.options.values = defaultWidgetValues["modelList"];
            modelListWidget.value = defaultWidgetValues["modelList"][0];
        }
    }

    async function searchModels() {
        const searchQuery = searchInputWidget.value.trim();
        const modelArchValue = DEFAULT_MODELS_ARCH_LIST[modelArchWidget.value];
        if(isControlNet) {
            modelTypeValue = DEFAULT_CONTROLNET_CONDITIONING_LIST[modelTypeWidget.value];
        } else {
            modelTypeValue = modelTypeWidget.value.toLowerCase().replace("model", "").trim();
        }

        let modelSearchResults = null;
        if(isControlNet) {
            modelSearchResults = await modelSearch(searchQuery, modelArchValue, "", "controlnet", modelTypeValue);
        } else if(isLora) {
            modelSearchResults = await modelSearch(searchQuery, modelArchValue, "", modelTypeValue);
        } else {
            modelSearchResults = await modelSearch(searchQuery, modelArchValue, modelTypeValue);
        }

        if(modelSearchResults.success) {
            const modelListArray = [];
            modelSearchResults.modelList.forEach(modelObj => {
                modelListArray.push(`${modelObj.air} (${modelObj.name} ${modelObj.version})`);
            });
            modelListWidget.options.values = modelListArray;
            modelListWidget.value = modelListArray[0];
        } else {
            notifyUser(modelSearchResults.error, "error", "Runware Search");
        }
    }

    appendWidgetCB(searchInputWidget, async function(...args) {
        const searchQuery = args[0].trim();
        if(searchQuery.length === 0) {
            resetValues();
        } else if(searchQuery.length < 2 || searchQuery.length > 32) {
            notifyUser("Invalid Search Value, Search Query must be between 2 and 32 characters!", "error", "Runware Search");
            return;
        } else {
            await searchModels();
        }
    });

    appendWidgetCB(modelArchWidget, async function(...args) {
        await searchModels();
    });

    if(!isLora){
        appendWidgetCB(modelTypeWidget, async function(...args) {     
            await searchModels();
        });
    }
}

export {
    enhancePrompt,
    modelSearch,
    notifyUser,
    promptEnhanceHandler,
    syncDimensionsNodeHandler,
    searchNodeHandler,
    captionNodeHandler,
    handleCustomErrors,
    APIKeyHandler
};