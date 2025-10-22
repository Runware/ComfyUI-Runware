import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";
import { DEFAULT_DIMENSIONS_LIST, DEFAULT_MODELS_ARCH_LIST, DEFAULT_CONTROLNET_CONDITIONING_LIST,
    RUNWARE_NODE_TYPES, MODEL_TYPES_TERMS, MODEL_LIST_TERMS
} from "./types.js";

const TIMEOUT_RANGE = { min: 5, default: 90,  max: 99 };
const OUTPUT_QUALITY_RANGE = { min: 20, default: 95, max: 99 };
const CACHE_SIZE_RANGE = { min: 30, default: 150, max: 4096 };

let openDialog = false;
let lastTimeout = false;
let lastOutputFormat = false;
let lastOutputQuality = false;
let lastEnableImagesCaching = null;
let lastMinImageCacheSize = false;

async function queryLocalAPI(endpoint, data) {
    try {
        const resp = await api.fetchApi(`/${endpoint}`, {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        return await resp.json();
    } catch (err) {
        return false;
    }
}

const runwareLocalAPI = {
    enhancePrompt: (userPrompt) => queryLocalAPI('promptEnhance', { userPrompt }),
    setAPIKey: (apiKey) => queryLocalAPI('setAPIKey', { apiKey }),
    setTimeout: (maxTimeout) => queryLocalAPI('setMaxTimeout', { maxTimeout }),
    setOutputFormat: (outputFormat) => queryLocalAPI('setOutputFormat', { outputFormat }),
    setOutputQuality: (outputQuality) => queryLocalAPI('setOutputQuality', { outputQuality }),
    setEnableImagesCaching: (enableCaching) => queryLocalAPI('setEnableImagesCaching', { enableCaching }),
    setMinImageCacheSize: (minCacheSize) => queryLocalAPI('setMinImageCacheSize', { minCacheSize }),
    modelSearch: (modelQuery = "", modelArch = "all", modelType = "base", modelCat = "checkpoint", condtioning = "") => 
        queryLocalAPI('modelSearch', { modelQuery, modelArch, modelType, modelCat, condtioning })
};

function mediaUUIDHandler(msgEvent) {
    const mediaData = msgEvent.detail;
    const mediaUUID = mediaData.mediaUUID;
    const mediaNodeID = parseInt(mediaData.nodeID);
    
    if(mediaData.success) {
        const mediaNode = app.graph.getNodeById(mediaNodeID);
        if(mediaNode !== null && mediaNode !== undefined) {
            // Find the mediaUUID widget specifically
            const mediaUUIDWidget = mediaNode.widgets.find(widget => widget.name === "mediaUUID");
            if(mediaUUIDWidget && mediaUUIDWidget.inputEl) {
                mediaUUIDWidget.inputEl.value = mediaUUID;
            }
        }
    }
    return false;
}

function captionNodeHandler(msgEvent) {
    const captionData = msgEvent.detail;
    const captionText = captionData.captionText;
    const captionNodeID = parseInt(captionData.nodeID);
    
    if(captionData.success) {
        const captionNode = app.graph.getNodeById(captionNodeID);
        if(captionNode !== null && captionNode !== undefined) {
            // Find the imageCaption widget specifically
            const imageCaptionWidget = captionNode.widgets.find(widget => widget.name === "imageCaption");
            if(imageCaptionWidget && imageCaptionWidget.inputEl) {
                imageCaptionWidget.inputEl.value = captionText;
            }
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
        const enhanceResults = await runwareLocalAPI.enhancePrompt(userPrompt);
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
                }
                const setAPIKeyResults = await runwareLocalAPI.setAPIKey(apiKey);
                if(setAPIKeyResults.success) {
                    remNode(apiManagerNode);
                    notifyUser("API Key Set Successfully!", "success", "Runware API Manager");
                } else {
                    notifyUser(setAPIKeyResults.error, "error", "Runware API Manager");
                }
            });
        } else if(widget.name === "Max Timeout") {
            if(lastTimeout) widget.value = lastTimeout;
            appendWidgetCB(widget, async function(...args) {
                const maxTimeout = parseInt(args[0]);
                if(isNaN(maxTimeout) || maxTimeout < TIMEOUT_RANGE.min || maxTimeout > TIMEOUT_RANGE.max) {
                    notifyUser(`Invalid Timeout Value! Must be between ${TIMEOUT_RANGE.min} and ${TIMEOUT_RANGE.max} seconds.`, "error", "Runware API Manager");
                    widget.value = lastTimeout || TIMEOUT_RANGE.default;
                    return;
                }
                const setTimeoutResults = await runwareLocalAPI.setTimeout(maxTimeout);
                if(setTimeoutResults.success) {
                    notifyUser("Timeout Set Successfully!", "success", "Runware API Manager");
                    lastTimeout = maxTimeout;
                } else {
                    widget.value = lastTimeout || TIMEOUT_RANGE.default;
                    notifyUser(setTimeoutResults.error, "error", "Runware API Manager");
                }
            });
        } else if(widget.name === "Image Output Format") {
            if(lastOutputFormat) widget.value = lastOutputFormat;
            appendWidgetCB(widget, async function(...args) {
                const outputFormat = args[0].trim().toUpperCase();
                const setFormatResults = await runwareLocalAPI.setOutputFormat(outputFormat);
                if(setFormatResults.success) {
                    notifyUser("Default Image Output Format Set Successfully!", "success", "Runware API Manager");
                    lastOutputFormat = outputFormat;
                } else {
                    notifyUser(setFormatResults.error, "error", "Runware API Manager");
                }
            });
        } else if(widget.name === "Image Output Quality") {
            if(lastOutputQuality) widget.value = lastOutputQuality;
            appendWidgetCB(widget, async function(...args) {
                const outputQuality = parseInt(args[0]);
                if(isNaN(outputQuality) || outputQuality < OUTPUT_QUALITY_RANGE.min || outputQuality > OUTPUT_QUALITY_RANGE.max) {
                    notifyUser(`Invalid Quality Value! Must be between ${OUTPUT_QUALITY_RANGE.min} and ${OUTPUT_QUALITY_RANGE.max}.`, "error", "Runware API Manager");
                    widget.value = lastOutputQuality || OUTPUT_QUALITY_RANGE.default;
                    return;
                }
                const setQualityResults = await runwareLocalAPI.setOutputQuality(outputQuality);
                if(setQualityResults.success) {
                    notifyUser("Default Image Output Quality Set Successfully!", "success", "Runware API Manager");
                    lastOutputQuality = outputQuality;
                } else {
                    widget.value = lastOutputQuality || OUTPUT_QUALITY_RANGE.default;
                    notifyUser(setQualityResults.error, "error", "Runware API Manager");
                }
            });
        } else if(widget.name === "Enable Images Caching") {
            if(lastEnableImagesCaching !== null) widget.value = lastEnableImagesCaching;
            appendWidgetCB(widget, async function(...args) {
                const enableCaching = args[0];
                const setCachingResults = await runwareLocalAPI.setEnableImagesCaching(enableCaching);
                if(setCachingResults.success) {
                    notifyUser("Image Caching Setting Updated Successfully!", "success", "Runware API Manager");
                    lastEnableImagesCaching = enableCaching;
                } else {
                    widget.value = lastEnableImagesCaching;
                    notifyUser(setCachingResults.error, "error", "Runware API Manager");
                }
            });
        } else if(widget.name === "Min Image Cache Size") {
            if(lastMinImageCacheSize !== false) widget.value = lastMinImageCacheSize;
            appendWidgetCB(widget, async function(...args) {
                const minCacheSize = parseFloat(args[0]);
                if(isNaN(minCacheSize) || minCacheSize < CACHE_SIZE_RANGE.min || minCacheSize > CACHE_SIZE_RANGE.max) {
                    notifyUser(`Invalid cache size! Must be between ${CACHE_SIZE_RANGE.min} KB and ${CACHE_SIZE_RANGE.max} KB.`, "error", "Runware API Manager");
                    widget.value = lastMinImageCacheSize || CACHE_SIZE_RANGE.default;
                    return;
                }
                const setCacheSizeResults = await runwareLocalAPI.setMinImageCacheSize(minCacheSize);
                if(setCacheSizeResults.success) {
                    notifyUser("Minimum Image Cache Size Updated Successfully!", "success", "Runware API Manager");
                    lastMinImageCacheSize = minCacheSize;
                } else {
                    widget.value = lastMinImageCacheSize || CACHE_SIZE_RANGE.default;
                    notifyUser(setCacheSizeResults.error, "error", "Runware API Manager");
                }
            });
        }
    }
}

function addTriggerWords(prompt, triggerWords) {
    if (!triggerWords?.trim()) return prompt;
    const cleanedTriggerWords = triggerWords
        .trim()
        .replace(/,\s*$/, '')
        .split(',')
        .map(word => word.trim())
        .filter(word => word.length);
    if (!prompt?.trim()) return cleanedTriggerWords.join(', ');
    const wordsToAdd = cleanedTriggerWords.filter(word => 
        !new RegExp(`\\b${word}\\b`, 'i').test(prompt)
    );
    return wordsToAdd.length 
        ? `${prompt}${prompt.endsWith(',') ? ' ' : ', '}${wordsToAdd.join(', ')}`
        : prompt;
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
                runwareAPIForm.reportValidity();
                return;
                // notifyUser("Invalid API Key Set, Please Try Again!", "error", "Runware API Manager");
                // return;
            } else {
                const setAPIKeyResults = await runwareLocalAPI.setAPIKey(apiKey);
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
            oldNodeCB?.apply(this, args);
            newCB?.apply(this, args);
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

const shortenAirCode = input => !input || !input.startsWith('urn:air:') ? input : input.match(/urn:air:.*?:.*?(civitai:\d+@\d+)$/)?.[1] || input;

async function searchNodeHandler(searchNode, searchInputWidget) {
    const searchNodeWidgets = searchNode.widgets;
    let modelArchWidget = false, modelTypeWidget = false, modelListWidget = false,
    defaultWidgetValues = {}, triggerWordsList = {
        "civitai:58390@62833": "", "civitai:82098@87153": "", "civitai:122359@135867": "",
        "civitai:14171@16677": "mix4", "civitai:13941@16576": "", "civitai:25995@32988": "full body, chibi"
    }, embeddingTriggerWordsList = {
        "civitai:7808@9208": "easynegative", "civitai:4629@5637": "ng_deepnegative_v1_75t",
        "civitai:56519@60938": "negative_hand", "civitai:72437@77169": "BadDream",
        "civitai:11772@25820": "verybadimagenegative_v1.3", "civitai:71961@94057": "FastNegativeV2",
    };
    let isLora = false, isControlNet = false, isEmbedding = false, isVAE = false, modelTypeValue = false;
    if(searchNode.comfyClass === RUNWARE_NODE_TYPES.LORASEARCH) isLora = true;
    if(searchNode.comfyClass === RUNWARE_NODE_TYPES.CONTROLNET) isControlNet = true;
    if(searchNode.comfyClass === RUNWARE_NODE_TYPES.EMBEDDING) isEmbedding = true;
    if(searchNode.comfyClass === RUNWARE_NODE_TYPES.VAE) isVAE = true;

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

    async function searchModels(exactQuery = null, returnOutput = false) {
        let searchQuery;
        if(exactQuery) {
            searchQuery = exactQuery;
        } else {
            searchQuery = searchInputWidget.value.trim();
        }
        searchQuery = shortenAirCode(searchQuery);
        const modelArchValue = DEFAULT_MODELS_ARCH_LIST[modelArchWidget.value];
        if(isControlNet) {
            modelTypeValue = DEFAULT_CONTROLNET_CONDITIONING_LIST[modelTypeWidget.value];
        } else {
            if(isEmbedding) {
                modelTypeValue = "embeddings";
            } else if(isVAE) {
                modelTypeValue = "vae";
            } else {
                modelTypeValue = modelTypeWidget.value.toLowerCase().replace("model", "").trim();
            }
        }

        let modelSearchResults = null;
        if(isControlNet) {
            modelSearchResults = await runwareLocalAPI.modelSearch(searchQuery, modelArchValue, "", "controlnet", modelTypeValue);
        } else if(isLora || isEmbedding || isVAE) {
            modelSearchResults = await runwareLocalAPI.modelSearch(searchQuery, modelArchValue, "", modelTypeValue);
        } else {
            modelSearchResults = await runwareLocalAPI.modelSearch(searchQuery, modelArchValue, modelTypeValue);
        }

        if(modelSearchResults.success) {
            const modelListArray = [];
            modelSearchResults.modelList.forEach(modelObj => {
                if(isLora) triggerWordsList[modelObj.air] = modelObj.positiveTriggerWords?.trim() || false;
                if(isEmbedding) embeddingTriggerWordsList[modelObj.air] = modelObj.positiveTriggerWords?.trim() || false;
                modelListArray.push(`${modelObj.air} (${modelObj.name} ${modelObj.version})`);
            });

            if(exactQuery) {
                const extraSearch = await searchModels(null, true);
                if(extraSearch) {
                    const newModelList = [...new Set([...modelListArray, ...extraSearch])];
                    modelListWidget.options.values = newModelList;
                    return;
                }
            }

            if(returnOutput) return modelListArray;
            modelListWidget.options.values = modelListArray;
            modelListWidget.value = modelListArray[0];
        } else {
            if(returnOutput) return false;
            if(exactQuery) {
                notifyUser("Failed To Load Workflow's Model List Value!", "error", "Runware Search");
                return;
            }
            notifyUser(modelSearchResults.error, "error", "Runware Search");
        }
    }

    function findTargetWidget(currentNode, targetWidgetName, depth = 1) {
        try {
            if(depth < 0) return false;
            const nodeOutputs = currentNode.outputs;
            if(nodeOutputs.length === 0) return false;
            const outputLinks = nodeOutputs[0].links;
            if(outputLinks.length === 0) return false;
            for(const linkID of outputLinks) {
                const linkInfo = app.graph.links[linkID];
                const linkNodeID = linkInfo.target_id;
                if(!linkNodeID) continue;
                const targetNode = app.graph.getNodeById(linkNodeID);
                let widgetFound = false;
                if(targetNode.widgets !== undefined && targetNode.widgets.length > 0){
                    widgetFound = targetNode.widgets.find(widget => widget.name === targetWidgetName) || false;
                }
                if(widgetFound) {
                    return widgetFound;
                } else {
                    return findTargetWidget(targetNode, targetWidgetName, depth - 1);
                }
            }
        } catch(e) {
            return false;
        }
        return false;
    }

    if(isLora) {
        const runwareButton = document.createElement("button");
        runwareButton.textContent = "Add Lora To Prompt";
        runwareButton.style = "max-height: 50px; background-color: #333; color: #ccc;";
        searchNode.addDOMWidget("addLora", "custom", runwareButton, {
            selectOn: ['focus', 'click'],
        });

        runwareButton.addEventListener("click", async () => {
            const chosenLora = modelListWidget.value.split(" ")[0];
            if(!triggerWordsList.hasOwnProperty(chosenLora)) return;
            const triggerWords = triggerWordsList[chosenLora];
            if(triggerWords.length > 0) {
                const positivePromptWidget = findTargetWidget(searchNode, "positivePrompt");
                if(!positivePromptWidget) {
                    notifyUser("Lora Node Is Not Linked To Any Runware Inference Node!", "error", "Runware Lora Connector");
                    return;
                }
                const positivePromptWithTrigger = addTriggerWords(positivePromptWidget.value, triggerWords);
                if(positivePromptWidget.value === positivePromptWithTrigger) {
                    notifyUser("Trigger Words Already Exists", "info", "Runware Lora Connector");
                    return;
                }
                positivePromptWidget.value = positivePromptWithTrigger;
                notifyUser("Trigger Words Added Successfully!", "success", "Runware Lora Connector");
            } else {
                notifyUser("No Trigger Words Found For This Lora!", "warn", "Runware Lora Connector");
            }
        });
    } else if(isEmbedding) {
        const runwareButton = document.createElement("button");
        runwareButton.textContent = "Add Embedding To Negative Prompt";
        runwareButton.style = "max-height: 50px; background-color: #333; color: #ccc;";
        searchNode.addDOMWidget("addEmbedding", "custom", runwareButton, {
            selectOn: ['focus', 'click'],
        });

        runwareButton.addEventListener("click", async () => {
            const chosenEmbedding = modelListWidget.value.split(" ")[0];
            if (!embeddingTriggerWordsList.hasOwnProperty(chosenEmbedding)) return;
            const triggerWords = embeddingTriggerWordsList[chosenEmbedding];
            if(triggerWords.length > 0) {
                const negativePromptWidget = findTargetWidget(searchNode, "negativePrompt");
                if(!negativePromptWidget) {
                    notifyUser("Embedding Node Is Not Linked To Any Runware Inference Node!", "error", "Runware Embedding Connector");
                    return;
                }
                const negativePromptWithTrigger = addTriggerWords(negativePromptWidget.value, triggerWords);
                if(negativePromptWidget.value === negativePromptWithTrigger) {
                    notifyUser("Trigger Words Already Exists", "info", "Runware Embedding Connector");
                    return;
                }
                negativePromptWidget.value = negativePromptWithTrigger;
                notifyUser("Trigger Words Added Successfully!", "success", "Runware Embedding Connector");
            } else {
                notifyUser("No Trigger Words Found For This Embedding!", "warn", "Runware Embedding Connector");
            }
        });
    }

    appendWidgetCB(searchInputWidget, async function(...args) {
        let searchQuery = args[0].trim();
        const shortenSearchQuery = shortenAirCode(searchQuery);
        if(searchQuery !== shortenSearchQuery) {
            searchQuery = shortenSearchQuery;
            searchInputWidget.value = searchQuery;
        }
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

    if(!isVAE && !isEmbedding) {
        appendWidgetCB(modelTypeWidget, async function(...args) {
            await searchModels();
        });
    }

    appendWidgetCB(searchNode, async function(...args) {
        try {
            let modelListValues = modelListWidget.options.values;
            if(modelListValues.length <= 0) return;
            modelListValues = modelListValues.map(model => model.split(" ")[0]);
            const modelListCRValue = modelListWidget.value.split(" ")[0];
            if(!modelListValues.includes(modelListCRValue)) {
                searchModels(modelListCRValue);
            }
        } catch(e) {}
    });
}

export {
    notifyUser,
    promptEnhanceHandler,
    syncDimensionsNodeHandler,
    searchNodeHandler,
    mediaUUIDHandler,
    captionNodeHandler,
    handleCustomErrors,
    APIKeyHandler,
};