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
            
            if(mediaUUIDWidget) {
                // Update both widget.value and inputEl.value for STRING widgets
                if(mediaUUIDWidget.value !== undefined) {
                    mediaUUIDWidget.value = mediaUUID;
                }
                
                if(mediaUUIDWidget.inputEl) {
                    mediaUUIDWidget.inputEl.value = mediaUUID;
                    // Trigger change events to update the UI
                    mediaUUIDWidget.inputEl.dispatchEvent(new Event('input', { bubbles: true }));
                    mediaUUIDWidget.inputEl.dispatchEvent(new Event('change', { bubbles: true }));
                }
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

function videoTranscriptionHandler(msgEvent) {
    const transcriptionData = msgEvent.detail;
    const transcriptionText = transcriptionData.transcriptionText;
    const transcriptionNodeID = parseInt(transcriptionData.nodeID);
    
    if(transcriptionData.success) {
        const transcriptionNode = app.graph.getNodeById(transcriptionNodeID);
        if(transcriptionNode !== null && transcriptionNode !== undefined) {
            // Find the prompt widget (where transcription is displayed)
            const promptWidget = transcriptionNode.widgets.find(widget => widget.name === "prompt");
            if(promptWidget && promptWidget.inputEl) {
                promptWidget.inputEl.value = transcriptionText;
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

function toggleWidgetEnabled(widget, enabled, node) {
    if (!widget || !widget.name) return;
    
    // Use the same simple approach as videoInferenceDimensionsHandler
    // Set widget disabled property
    widget.disabled = !enabled;
    
    // Disable/enable widgets using inputEl if available (same pattern as videoInferenceDimensionsHandler)
    if (widget.inputEl) {
        widget.inputEl.disabled = !enabled;
        widget.inputEl.style.opacity = enabled ? "1" : "0.5";
        widget.inputEl.style.cursor = enabled ? "text" : "not-allowed";
        widget.inputEl.readOnly = !enabled;
    }
    
    // For combo/dropdown widgets, also try to disable the options element
    if (widget.options && widget.options.element) {
        widget.options.element.disabled = !enabled;
        widget.options.element.style.opacity = enabled ? "1" : "0.5";
        widget.options.element.style.pointerEvents = enabled ? "auto" : "none";
    }
    
    // Fallback: try to find inputs via DOM if inputEl is not available (same as videoInferenceDimensionsHandler)
    if (!widget.inputEl && node) {
        const nodeElement = node.htmlElements?.widgetsContainer || node.htmlElements;
        if (nodeElement) {
            const input = nodeElement.querySelector(`input[name="${widget.name}"], textarea[name="${widget.name}"], select[name="${widget.name}"]`);
            if (input) {
                input.disabled = !enabled;
                input.style.opacity = enabled ? "1" : "0.5";
                input.style.cursor = enabled ? "text" : "not-allowed";
                input.readOnly = !enabled;
                if (input.tagName === "SELECT") {
                    input.style.pointerEvents = enabled ? "auto" : "none";
                }
            }
        }
    }
}

function videoUpscalerToggleHandler(videoUpscalerNode) {
    if (!videoUpscalerNode?.widgets) return;

    const useUpscaleFactorWidget = videoUpscalerNode.widgets.find(w => w && w.name === "useUpscaleFactor");
    const upscaleFactorWidget = videoUpscalerNode.widgets.find(w => w && w.name === "upscaleFactor");

    if (!useUpscaleFactorWidget || !upscaleFactorWidget) return;

    function applyToggleState() {
        const enabled = useUpscaleFactorWidget.value === true;
        toggleWidgetEnabled(upscaleFactorWidget, enabled, videoUpscalerNode);
        videoUpscalerNode.setDirtyCanvas(true);
    }

    // Initialize state once widgets are rendered
    setTimeout(applyToggleState, 100);

    appendWidgetCB(useUpscaleFactorWidget, () => {
        setTimeout(applyToggleState, 50);
    });
}

function useParameterToggleHandler(node) {
    // Prevent double registration
    if (node._useParameterToggleHandlerRegistered) return;
    node._useParameterToggleHandlerRegistered = true;
    
    // Define explicit mappings: "useParameterName" -> ["parameter1", "parameter2", ...]
    const parameterMappings = {
        // Image Inference
        "useSteps": ["steps"],
        "useSeed": ["seed"],
        "useCFGScale": ["cfgScale"], // Image inference uses lowercase cfgScale
        "useScheduler": ["scheduler"],
        "useClipSkip": ["clipSkip"],
        
        // Video Inference
        "useCustomDimensions": ["width", "height"], // Note: Also handled separately in videoInferenceDimensionsHandler
        "useDuration": ["duration"],
        "useFps": ["fps"],
        // useSteps and useSeed are same as image inference, handled by fallback
        
        // Upscaler specific mappings (override for nodes that have CFGScale with capital C)
        "usePrompts": ["positivePrompt", "negativePrompt"],
        "useClarityParams": ["controlNetWeight", "strength", "scheduler"],
        "useCCSRParams": ["colorFix", "tileDiffusion"],
        "useLatentParams": ["clipSkip"],
        
        // Audio Inference
        "usePositivePrompt": ["positivePrompt"],
        
        // Accelerator Options
        "useCacheDistance": ["cacheDistance"],
        "useTeaCacheDistance": ["teaCacheDistance"],
        "useDeepCacheOptions": ["deepCacheInterval", "deepCacheBranchId"],
        "useCacheSteps": ["cacheStartStep", "cacheEndStep"],
        "useCachePercentageSteps": ["cacheStartStepPercentage", "cacheEndStepPercentage"],
        "useCacheMaxConsecutiveSteps": ["cacheMaxConsecutiveSteps"],
        
        // Bytedance Provider Settings
        "useCameraFixed": ["cameraFixed"],
        "useMaxSequentialImages": ["maxSequentialImages"],
        "useFastMode": ["fastMode"],
        
        // OpenAI Provider Settings (these are dropdowns, not booleans, but handle them anyway)
        "useBackground": ["background"],
        "useStyle": ["style"],
        
        // Mask Margin
        "Mask Margin": ["maskMargin"],
    };
    
    // Node-specific overrides for parameters that have different names in different nodes
    // Format: nodeClass -> { "useParam": ["param1", "param2"] }
    const nodeSpecificMappings = {
        // Upscaler uses CFGScale (capital C) instead of cfgScale
        [RUNWARE_NODE_TYPES.UPSCALER]: {
            "useCFGScale": ["CFGScale"],
        },
    };
    
    // Wait for widgets to be ready
    function initializeHandler() {
        if (!node.widgets || node.widgets.length === 0) {
            setTimeout(initializeHandler, 100);
            return;
        }
        
        // Find all "use" widgets and their corresponding parameter widgets upfront (like videoInferenceDimensionsHandler does)
        const togglePairs = [];
        
        // Find all "use" widgets
        node.widgets.forEach(widget => {
            if (!widget || !widget.name) return;
            
            const isUseWidget = widget.name.startsWith("use") && (widget.type === "BOOLEAN" || widget.type === "COMBO");
            const isMaskMargin = widget.name === "Mask Margin" && widget.type === "BOOLEAN";
            
            if (!isUseWidget && !isMaskMargin) return;
            
            const useParamName = widget.name;
            
            // Get corresponding parameters - check node-specific mappings first, then general mappings
            let paramNames = [];
            const nodeClass = node.comfyClass;
            if (nodeClass && nodeSpecificMappings[nodeClass] && nodeSpecificMappings[nodeClass][useParamName]) {
                paramNames = nodeSpecificMappings[nodeClass][useParamName];
            } else {
                paramNames = parameterMappings[useParamName] || [];
            }
            
            // Handle special case: remove "use" prefix and lowercase first letter
            if (paramNames.length === 0) {
                const paramName = useParamName.replace(/^use/, "").replace(/^[A-Z]/, (match) => match.toLowerCase());
                paramNames = [paramName];
            }
            
            // Find the actual parameter widgets
            const paramWidgets = [];
            paramNames.forEach(paramName => {
                const paramWidget = node.widgets.find(w => w && w.name === paramName);
                if (paramWidget) {
                    paramWidgets.push(paramWidget);
                } else {
                    // If mapped parameter doesn't exist, try fallback auto-detection
                    const fallbackParamName = useParamName.replace(/^use/, "").replace(/^[A-Z]/, (match) => match.toLowerCase());
                    if (fallbackParamName !== paramName) {
                        const fallbackWidget = node.widgets.find(w => w && w.name === fallbackParamName);
                        if (fallbackWidget) {
                            paramWidgets.push(fallbackWidget);
                        }
                    }
                }
            });
            
            if (paramWidgets.length > 0) {
                togglePairs.push({
                    useWidget: widget,
                    paramWidgets: paramWidgets
                });
            }
        });
        
        // Create toggle functions for each pair (like toggleDimensionsEnabled in videoInferenceDimensionsHandler)
        togglePairs.forEach(pair => {
            const { useWidget, paramWidgets } = pair;
            
            function toggleEnabled() {
                // Determine if enabled based on widget type
                let enabled = false;
                if (useWidget.type === "BOOLEAN") {
                    enabled = useWidget.value === true;
                } else if (useWidget.type === "COMBO") {
                    enabled = useWidget.value === "enable" || useWidget.value === "Enable";
                }
                
                // Apply to each parameter widget (exactly like toggleDimensionsEnabled does)
                paramWidgets.forEach(paramWidget => {
                    if (paramWidget.inputEl) {
                        paramWidget.inputEl.disabled = !enabled;
                        paramWidget.inputEl.style.opacity = enabled ? "1" : "0.5";
                        paramWidget.inputEl.style.cursor = enabled ? "text" : "not-allowed";
                        paramWidget.inputEl.readOnly = !enabled;
                    }
                    paramWidget.disabled = !enabled;
                    
                    // Fallback: try to find inputs via DOM if inputEl is not available
                    if (!paramWidget.inputEl) {
                        const nodeElement = node.htmlElements?.widgetsContainer || node.htmlElements;
                        if (nodeElement) {
                            const input = nodeElement.querySelector(`input[name="${paramWidget.name}"], textarea[name="${paramWidget.name}"], select[name="${paramWidget.name}"]`);
                            if (input) {
                                input.disabled = !enabled;
                                input.style.opacity = enabled ? "1" : "0.5";
                                input.style.cursor = enabled ? "text" : "not-allowed";
                                input.readOnly = !enabled;
                                if (input.tagName === "SELECT") {
                                    input.style.pointerEvents = enabled ? "auto" : "none";
                                }
                            }
                        }
                    }
                });
                
                node.setDirtyCanvas(true);
            }
            
            // Set up callback (exactly like videoInferenceDimensionsHandler does)
            appendWidgetCB(useWidget, () => {
                setTimeout(toggleEnabled, 50);
            });
            
            // Initial call to set initial state
            setTimeout(toggleEnabled, 50);
        });
    }
    
    // Start initialization
    setTimeout(initializeHandler, 200);
}

function upscalerToggleHandler(upscalerNode) {
    // Find all "use" parameter widgets for Upscaler
    const useStepsWidget = upscalerNode.widgets.find(w => w.name === "useSteps");
    const stepsWidget = upscalerNode.widgets.find(w => w.name === "steps");
    const useSeedWidget = upscalerNode.widgets.find(w => w.name === "useSeed");
    const seedWidget = upscalerNode.widgets.find(w => w.name === "seed");
    const useCFGScaleWidget = upscalerNode.widgets.find(w => w.name === "useCFGScale");
    const cfgScaleWidget = upscalerNode.widgets.find(w => w.name === "CFGScale");
    const usePromptsWidget = upscalerNode.widgets.find(w => w.name === "usePrompts");
    const positivePromptWidget = upscalerNode.widgets.find(w => w.name === "positivePrompt");
    const negativePromptWidget = upscalerNode.widgets.find(w => w.name === "negativePrompt");
    const useClarityParamsWidget = upscalerNode.widgets.find(w => w.name === "useClarityParams");
    const controlNetWeightWidget = upscalerNode.widgets.find(w => w.name === "controlNetWeight");
    const strengthWidget = upscalerNode.widgets.find(w => w.name === "strength");
    const schedulerWidget = upscalerNode.widgets.find(w => w.name === "scheduler");
    const useCCSRParamsWidget = upscalerNode.widgets.find(w => w.name === "useCCSRParams");
    const colorFixWidget = upscalerNode.widgets.find(w => w.name === "colorFix");
    const tileDiffusionWidget = upscalerNode.widgets.find(w => w.name === "tileDiffusion");
    const useLatentParamsWidget = upscalerNode.widgets.find(w => w.name === "useLatentParams");
    const clipSkipWidget = upscalerNode.widgets.find(w => w.name === "clipSkip");
    
    // Helper function to toggle widget enabled state (exact same pattern)
    function toggleWidgetState(useWidget, paramWidgets, paramNames) {
        if (!useWidget || !paramWidgets || paramWidgets.length === 0) return;
        
        function toggleEnabled() {
            const enabled = useWidget.value === true;
            
            // Apply to each parameter widget
            paramWidgets.forEach((paramWidget, idx) => {
                if (!paramWidget) return;
                
                if (paramWidget.inputEl) {
                    paramWidget.inputEl.disabled = !enabled;
                    paramWidget.inputEl.style.opacity = enabled ? "1" : "0.5";
                    paramWidget.inputEl.style.cursor = enabled ? "text" : "not-allowed";
                    paramWidget.inputEl.readOnly = !enabled;
                }
                paramWidget.disabled = !enabled;
                
                // Fallback: try to find inputs via DOM if inputEl is not available
                if (!paramWidget.inputEl) {
                    const nodeElement = upscalerNode.htmlElements?.widgetsContainer || upscalerNode.htmlElements;
                    if (nodeElement && paramNames[idx]) {
                        const input = nodeElement.querySelector(`input[name="${paramNames[idx]}"], textarea[name="${paramNames[idx]}"], select[name="${paramNames[idx]}"]`);
                        if (input) {
                            input.disabled = !enabled;
                            input.style.opacity = enabled ? "1" : "0.5";
                            input.style.cursor = enabled ? "text" : "not-allowed";
                            input.readOnly = !enabled;
                            if (input.tagName === "SELECT") {
                                input.style.pointerEvents = enabled ? "auto" : "none";
                            }
                        }
                    }
                }
            });
            
            upscalerNode.setDirtyCanvas(true);
        }
        
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        setTimeout(toggleEnabled, 100);
    }
    
    // Set up all toggle handlers
    if (useStepsWidget && stepsWidget) {
        toggleWidgetState(useStepsWidget, [stepsWidget], ["steps"]);
    }
    
    if (useSeedWidget && seedWidget) {
        toggleWidgetState(useSeedWidget, [seedWidget], ["seed"]);
    }
    
    if (useCFGScaleWidget && cfgScaleWidget) {
        toggleWidgetState(useCFGScaleWidget, [cfgScaleWidget], ["CFGScale"]);
    }
    
    if (usePromptsWidget && positivePromptWidget && negativePromptWidget) {
        toggleWidgetState(usePromptsWidget, [positivePromptWidget, negativePromptWidget], ["positivePrompt", "negativePrompt"]);
    }
    
    if (useClarityParamsWidget && controlNetWeightWidget && strengthWidget && schedulerWidget) {
        toggleWidgetState(useClarityParamsWidget, [controlNetWeightWidget, strengthWidget, schedulerWidget], ["controlNetWeight", "strength", "scheduler"]);
    }
    
    if (useCCSRParamsWidget && colorFixWidget && tileDiffusionWidget) {
        toggleWidgetState(useCCSRParamsWidget, [colorFixWidget, tileDiffusionWidget], ["colorFix", "tileDiffusion"]);
    }
    
    if (useLatentParamsWidget && clipSkipWidget) {
        toggleWidgetState(useLatentParamsWidget, [clipSkipWidget], ["clipSkip"]);
    }
}

function audioInferenceToggleHandler(audioInferenceNode) {
    // Find all "use" parameter widgets for Audio Inference
    const usePositivePromptWidget = audioInferenceNode.widgets.find(w => w.name === "usePositivePrompt");
    const positivePromptWidget = audioInferenceNode.widgets.find(w => w.name === "positivePrompt");
    const useDurationWidget = audioInferenceNode.widgets.find(w => w.name === "useDuration");
    const durationWidget = audioInferenceNode.widgets.find(w => w.name === "duration");
    const useSampleRateWidget = audioInferenceNode.widgets.find(w => w.name === "useSampleRate");
    const sampleRateWidget = audioInferenceNode.widgets.find(w => w.name === "sampleRate");
    const useBitrateWidget = audioInferenceNode.widgets.find(w => w.name === "useBitrate");
    const bitrateWidget = audioInferenceNode.widgets.find(w => w.name === "bitrate");
    
    // Helper function to toggle widget enabled state (exact same pattern)
    function toggleWidgetState(useWidget, paramWidget, paramName) {
        if (!useWidget || !paramWidget) return;
        
        function toggleEnabled() {
            const enabled = useWidget.value === true;
            
            if (paramWidget.inputEl) {
                paramWidget.inputEl.disabled = !enabled;
                paramWidget.inputEl.style.opacity = enabled ? "1" : "0.5";
                paramWidget.inputEl.style.cursor = enabled ? "text" : "not-allowed";
                paramWidget.inputEl.readOnly = !enabled;
            }
            paramWidget.disabled = !enabled;
            
            if (!paramWidget.inputEl) {
                const nodeElement = audioInferenceNode.htmlElements?.widgetsContainer || audioInferenceNode.htmlElements;
                if (nodeElement) {
                    const input = nodeElement.querySelector(`input[name="${paramName}"], textarea[name="${paramName}"], select[name="${paramName}"]`);
                    if (input) {
                        input.disabled = !enabled;
                        input.style.opacity = enabled ? "1" : "0.5";
                        input.style.cursor = enabled ? "text" : "not-allowed";
                        input.readOnly = !enabled;
                        if (input.tagName === "SELECT") {
                            input.style.pointerEvents = enabled ? "auto" : "none";
                        }
                    }
                }
            }
            
            audioInferenceNode.setDirtyCanvas(true);
        }
        
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        setTimeout(toggleEnabled, 100);
    }
    
    // Set up all toggle handlers
    if (usePositivePromptWidget && positivePromptWidget) {
        toggleWidgetState(usePositivePromptWidget, positivePromptWidget, "positivePrompt");
    }
    
    if (useDurationWidget && durationWidget) {
        toggleWidgetState(useDurationWidget, durationWidget, "duration");
    }
    
    if (useSampleRateWidget && sampleRateWidget) {
        toggleWidgetState(useSampleRateWidget, sampleRateWidget, "sampleRate");
    }
    
    if (useBitrateWidget && bitrateWidget) {
        toggleWidgetState(useBitrateWidget, bitrateWidget, "bitrate");
    }
}

function acceleratorOptionsToggleHandler(acceleratorNode) {
    // Find all "use" parameter widgets for Accelerator Options
    const useCacheDistanceWidget = acceleratorNode.widgets.find(w => w.name === "useCacheDistance");
    const cacheDistanceWidget = acceleratorNode.widgets.find(w => w.name === "cacheDistance");
    const useTeaCacheDistanceWidget = acceleratorNode.widgets.find(w => w.name === "useTeaCacheDistance");
    const teaCacheDistanceWidget = acceleratorNode.widgets.find(w => w.name === "teaCacheDistance");
    const useDeepCacheOptionsWidget = acceleratorNode.widgets.find(w => w.name === "useDeepCacheOptions");
    const deepCacheIntervalWidget = acceleratorNode.widgets.find(w => w.name === "deepCacheInterval");
    const deepCacheBranchIdWidget = acceleratorNode.widgets.find(w => w.name === "deepCacheBranchId");
    const useCacheStepsWidget = acceleratorNode.widgets.find(w => w.name === "useCacheSteps");
    const cacheStartStepWidget = acceleratorNode.widgets.find(w => w.name === "cacheStartStep");
    const cacheEndStepWidget = acceleratorNode.widgets.find(w => w.name === "cacheEndStep");
    const useCachePercentageStepsWidget = acceleratorNode.widgets.find(w => w.name === "useCachePercentageSteps");
    const cacheStartStepPercentageWidget = acceleratorNode.widgets.find(w => w.name === "cacheStartStepPercentage");
    const cacheEndStepPercentageWidget = acceleratorNode.widgets.find(w => w.name === "cacheEndStepPercentage");
    const useCacheMaxConsecutiveStepsWidget = acceleratorNode.widgets.find(w => w.name === "useCacheMaxConsecutiveSteps");
    const cacheMaxConsecutiveStepsWidget = acceleratorNode.widgets.find(w => w.name === "cacheMaxConsecutiveSteps");
    
    // Helper function to toggle widget enabled state (exact same pattern)
    function toggleWidgetState(useWidget, paramWidgets, paramNames) {
        if (!useWidget || !paramWidgets || paramWidgets.length === 0) return;
        
        function toggleEnabled() {
            const enabled = useWidget.value === true;
            
            paramWidgets.forEach((paramWidget, idx) => {
                if (!paramWidget) return;
                
                if (paramWidget.inputEl) {
                    paramWidget.inputEl.disabled = !enabled;
                    paramWidget.inputEl.style.opacity = enabled ? "1" : "0.5";
                    paramWidget.inputEl.style.cursor = enabled ? "text" : "not-allowed";
                    paramWidget.inputEl.readOnly = !enabled;
                }
                paramWidget.disabled = !enabled;
                
                if (!paramWidget.inputEl) {
                    const nodeElement = acceleratorNode.htmlElements?.widgetsContainer || acceleratorNode.htmlElements;
                    if (nodeElement && paramNames[idx]) {
                        const input = nodeElement.querySelector(`input[name="${paramNames[idx]}"], textarea[name="${paramNames[idx]}"], select[name="${paramNames[idx]}"]`);
                        if (input) {
                            input.disabled = !enabled;
                            input.style.opacity = enabled ? "1" : "0.5";
                            input.style.cursor = enabled ? "text" : "not-allowed";
                            input.readOnly = !enabled;
                            if (input.tagName === "SELECT") {
                                input.style.pointerEvents = enabled ? "auto" : "none";
                            }
                        }
                    }
                }
            });
            
            acceleratorNode.setDirtyCanvas(true);
        }
        
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        setTimeout(toggleEnabled, 100);
    }
    
    // Set up all toggle handlers
    if (useCacheDistanceWidget && cacheDistanceWidget) {
        toggleWidgetState(useCacheDistanceWidget, [cacheDistanceWidget], ["cacheDistance"]);
    }
    
    if (useTeaCacheDistanceWidget && teaCacheDistanceWidget) {
        toggleWidgetState(useTeaCacheDistanceWidget, [teaCacheDistanceWidget], ["teaCacheDistance"]);
    }
    
    if (useDeepCacheOptionsWidget && deepCacheIntervalWidget && deepCacheBranchIdWidget) {
        toggleWidgetState(useDeepCacheOptionsWidget, [deepCacheIntervalWidget, deepCacheBranchIdWidget], ["deepCacheInterval", "deepCacheBranchId"]);
    }
    
    if (useCacheStepsWidget && cacheStartStepWidget && cacheEndStepWidget) {
        toggleWidgetState(useCacheStepsWidget, [cacheStartStepWidget, cacheEndStepWidget], ["cacheStartStep", "cacheEndStep"]);
    }
    
    if (useCachePercentageStepsWidget && cacheStartStepPercentageWidget && cacheEndStepPercentageWidget) {
        toggleWidgetState(useCachePercentageStepsWidget, [cacheStartStepPercentageWidget, cacheEndStepPercentageWidget], ["cacheStartStepPercentage", "cacheEndStepPercentage"]);
    }
    
    if (useCacheMaxConsecutiveStepsWidget && cacheMaxConsecutiveStepsWidget) {
        toggleWidgetState(useCacheMaxConsecutiveStepsWidget, [cacheMaxConsecutiveStepsWidget], ["cacheMaxConsecutiveSteps"]);
    }
}

function bytedanceProviderSettingsToggleHandler(bytedanceNode) {
    // Find all "use" parameter widgets for Bytedance Provider Settings
    const useCameraFixedWidget = bytedanceNode.widgets.find(w => w.name === "useCameraFixed");
    const cameraFixedWidget = bytedanceNode.widgets.find(w => w.name === "cameraFixed");
    const useMaxSequentialImagesWidget = bytedanceNode.widgets.find(w => w.name === "useMaxSequentialImages");
    const maxSequentialImagesWidget = bytedanceNode.widgets.find(w => w.name === "maxSequentialImages");
    const useFastModeWidget = bytedanceNode.widgets.find(w => w.name === "useFastMode");
    const fastModeWidget = bytedanceNode.widgets.find(w => w.name === "fastMode");
    
    // Helper function to toggle widget enabled state (exact same pattern)
    function toggleWidgetState(useWidget, paramWidget, paramName) {
        if (!useWidget || !paramWidget) return;
        
        function toggleEnabled() {
            const enabled = useWidget.value === true;
            
            if (paramWidget.inputEl) {
                paramWidget.inputEl.disabled = !enabled;
                paramWidget.inputEl.style.opacity = enabled ? "1" : "0.5";
                paramWidget.inputEl.style.cursor = enabled ? "text" : "not-allowed";
                paramWidget.inputEl.readOnly = !enabled;
            }
            paramWidget.disabled = !enabled;
            
            if (!paramWidget.inputEl) {
                const nodeElement = bytedanceNode.htmlElements?.widgetsContainer || bytedanceNode.htmlElements;
                if (nodeElement) {
                    const input = nodeElement.querySelector(`input[name="${paramName}"], textarea[name="${paramName}"], select[name="${paramName}"]`);
                    if (input) {
                        input.disabled = !enabled;
                        input.style.opacity = enabled ? "1" : "0.5";
                        input.style.cursor = enabled ? "text" : "not-allowed";
                        input.readOnly = !enabled;
                        if (input.tagName === "SELECT") {
                            input.style.pointerEvents = enabled ? "auto" : "none";
                        }
                    }
                }
            }
            
            bytedanceNode.setDirtyCanvas(true);
        }
        
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        setTimeout(toggleEnabled, 100);
    }
    
    // Set up all toggle handlers
    if (useCameraFixedWidget && cameraFixedWidget) {
        toggleWidgetState(useCameraFixedWidget, cameraFixedWidget, "cameraFixed");
    }
    
    if (useMaxSequentialImagesWidget && maxSequentialImagesWidget) {
        toggleWidgetState(useMaxSequentialImagesWidget, maxSequentialImagesWidget, "maxSequentialImages");
    }
    
    if (useFastModeWidget && fastModeWidget) {
        toggleWidgetState(useFastModeWidget, fastModeWidget, "fastMode");
    }
}

function openaiProviderSettingsToggleHandler(openaiNode) {
    // Find all "use" parameter widgets for OpenAI Provider Settings (these are COMBO widgets)
    const useBackgroundWidget = openaiNode.widgets.find(w => w.name === "useBackground");
    const backgroundWidget = openaiNode.widgets.find(w => w.name === "background");
    const useStyleWidget = openaiNode.widgets.find(w => w.name === "useStyle");
    const styleWidget = openaiNode.widgets.find(w => w.name === "style");
    
    // Helper function to toggle widget enabled state (exact same pattern, but handles COMBO)
    function toggleWidgetState(useWidget, paramWidget, paramName) {
        if (!useWidget || !paramWidget) return;
        
        function toggleEnabled() {
            // For COMBO widgets, check if value is "enable"
            const enabled = useWidget.value === "enable" || useWidget.value === "Enable";
            
            if (paramWidget.inputEl) {
                paramWidget.inputEl.disabled = !enabled;
                paramWidget.inputEl.style.opacity = enabled ? "1" : "0.5";
                paramWidget.inputEl.style.cursor = enabled ? "text" : "not-allowed";
                paramWidget.inputEl.readOnly = !enabled;
            }
            
            // Handle dropdown widgets
            if (paramWidget.options && paramWidget.options.element) {
                paramWidget.options.element.disabled = !enabled;
                paramWidget.options.element.style.opacity = enabled ? "1" : "0.5";
                paramWidget.options.element.style.pointerEvents = enabled ? "auto" : "none";
            }
            
            paramWidget.disabled = !enabled;
            
            if (!paramWidget.inputEl) {
                const nodeElement = openaiNode.htmlElements?.widgetsContainer || openaiNode.htmlElements;
                if (nodeElement) {
                    const input = nodeElement.querySelector(`input[name="${paramName}"], textarea[name="${paramName}"], select[name="${paramName}"]`);
                    if (input) {
                        input.disabled = !enabled;
                        input.style.opacity = enabled ? "1" : "0.5";
                        input.style.cursor = enabled ? "text" : "not-allowed";
                        input.readOnly = !enabled;
                        if (input.tagName === "SELECT") {
                            input.style.pointerEvents = enabled ? "auto" : "none";
                        }
                    }
                }
            }
            
            openaiNode.setDirtyCanvas(true);
        }
        
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        setTimeout(toggleEnabled, 100);
    }
    
    // Set up all toggle handlers
    if (useBackgroundWidget && backgroundWidget) {
        toggleWidgetState(useBackgroundWidget, backgroundWidget, "background");
    }
    
    if (useStyleWidget && styleWidget) {
        toggleWidgetState(useStyleWidget, styleWidget, "style");
    }
}

function imageInferenceToggleHandler(imageInferenceNode) {
    // Find all "use" parameter widgets for Image Inference
    const useStepsWidget = imageInferenceNode.widgets.find(w => w.name === "useSteps");
    const stepsWidget = imageInferenceNode.widgets.find(w => w.name === "steps");
    const useSeedWidget = imageInferenceNode.widgets.find(w => w.name === "useSeed");
    const seedWidget = imageInferenceNode.widgets.find(w => w.name === "seed");
    const useCFGScaleWidget = imageInferenceNode.widgets.find(w => w.name === "useCFGScale");
    const cfgScaleWidget = imageInferenceNode.widgets.find(w => w.name === "cfgScale");
    const useSchedulerWidget = imageInferenceNode.widgets.find(w => w.name === "useScheduler");
    const schedulerWidget = imageInferenceNode.widgets.find(w => w.name === "scheduler");
    const useClipSkipWidget = imageInferenceNode.widgets.find(w => w.name === "useClipSkip");
    const clipSkipWidget = imageInferenceNode.widgets.find(w => w.name === "clipSkip");
    const maskMarginWidget = imageInferenceNode.widgets.find(w => w.name === "Mask Margin");
    const maskMarginValueWidget = imageInferenceNode.widgets.find(w => w.name === "maskMargin");
    
    // Helper function to toggle widget enabled state (exact same pattern as videoInferenceDimensionsHandler)
    function toggleWidgetState(useWidget, paramWidget, paramName) {
        if (!useWidget || !paramWidget) return;
        
        function toggleEnabled() {
            const enabled = useWidget.value === true;
            
            // Disable/enable widgets using inputEl if available (exact same pattern)
            if (paramWidget.inputEl) {
                paramWidget.inputEl.disabled = !enabled;
                paramWidget.inputEl.style.opacity = enabled ? "1" : "0.5";
                paramWidget.inputEl.style.cursor = enabled ? "text" : "not-allowed";
                paramWidget.inputEl.readOnly = !enabled;
            }
            // Also set widget property
            paramWidget.disabled = !enabled;
            
            // Fallback: try to find inputs via DOM if inputEl is not available
            if (!paramWidget.inputEl) {
                const nodeElement = imageInferenceNode.htmlElements?.widgetsContainer || imageInferenceNode.htmlElements;
                if (nodeElement) {
                    const input = nodeElement.querySelector(`input[name="${paramName}"], textarea[name="${paramName}"], select[name="${paramName}"]`);
                    if (input) {
                        input.disabled = !enabled;
                        input.style.opacity = enabled ? "1" : "0.5";
                        input.style.cursor = enabled ? "text" : "not-allowed";
                        input.readOnly = !enabled;
                        if (input.tagName === "SELECT") {
                            input.style.pointerEvents = enabled ? "auto" : "none";
                        }
                    }
                }
            }
            
            imageInferenceNode.setDirtyCanvas(true);
        }
        
        // Set up callback (exact same pattern as useCustomDimensions)
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        // Initial call to set initial state
        setTimeout(toggleEnabled, 100);
    }
    
    // Set up all toggle handlers
    if (useStepsWidget && stepsWidget) {
        toggleWidgetState(useStepsWidget, stepsWidget, "steps");
    }
    
    if (useSeedWidget && seedWidget) {
        toggleWidgetState(useSeedWidget, seedWidget, "seed");
    }
    
    if (useCFGScaleWidget && cfgScaleWidget) {
        toggleWidgetState(useCFGScaleWidget, cfgScaleWidget, "cfgScale");
    }
    
    if (useSchedulerWidget && schedulerWidget) {
        toggleWidgetState(useSchedulerWidget, schedulerWidget, "scheduler");
    }
    
    if (useClipSkipWidget && clipSkipWidget) {
        toggleWidgetState(useClipSkipWidget, clipSkipWidget, "clipSkip");
    }
    
    // Handle Mask Margin (BOOLEAN widget)
    if (maskMarginWidget && maskMarginValueWidget) {
        toggleWidgetState(maskMarginWidget, maskMarginValueWidget, "maskMargin");
    }
}

function videoInferenceDimensionsHandler(videoInferenceNode) {
    const widthWidget = videoInferenceNode.widgets.find(w => w.name === "width");
    const heightWidget = videoInferenceNode.widgets.find(w => w.name === "height");
    const useCustomDimensionsWidget = videoInferenceNode.widgets.find(w => w.name === "useCustomDimensions");
    
    if (!widthWidget || !heightWidget || !useCustomDimensionsWidget) return;

    const MODEL_DIMENSIONS = {
        "klingai:1@2": {width: 1280, height: 720}, "klingai:1@1": {width: 1280, height: 720},
        "klingai:2@2": {width: 1920, height: 1080}, "klingai:2@1": {width: 1280, height: 720},
        "klingai:3@1": {width: 1280, height: 720}, "klingai:3@2": {width: 1920, height: 1080},
        "klingai:4@3": {width: 1280, height: 720}, "klingai:5@1": {width: 1280, height: 720},
        "klingai:5@2": {width: 1920, height: 1080}, "klingai:5@3": {width: 1920, height: 1080},
        "klingai:7@1": {width: 0, height: 0},
        "google:2@0": {width: 1280, height: 720}, "google:3@0": {width: 1280, height: 720},
        "google:3@1": {width: 1280, height: 720}, "google:3@2": {width: 1280, height: 720},
        "google:3@3": {width: 1280, height: 720},
        "bytedance:2@1": {width: 864, height: 480}, "bytedance:1@1": {width: 864, height: 480},
        "bytedance:5@1": {width: 1024, height: 1024}, "bytedance:5@2": {width: 1024, height: 1024},
        "minimax:1@1": {width: 1366, height: 768}, "minimax:2@1": {width: 1366, height: 768},
        "minimax:2@3": {width: 1366, height: 768}, "minimax:3@1": {width: 1366, height: 768},
        "minimax:4@1": {width: 1366, height: 768}, "minimax:4@2": {width: 1366, height: 768},
        "pixverse:1@1": {width: 640, height: 360}, "pixverse:1@2": {width: 640, height: 360},
        "pixverse:1@3": {width: 640, height: 360}, "pixverse:lipsync@1": {width: 640, height: 360},
        "vidu:1@0": {width: 1920, height: 1080}, "vidu:1@1": {width: 1920, height: 1080},
        "vidu:1@5": {width: 1920, height: 1080}, "vidu:2@0": {width: 1920, height: 1080},
        "runware:200@1": {width: 853, height: 480}, "runware:200@2": {width: 853, height: 480},
        "runware:200@6": {width: 1280, height: 720},
        "openai:3@1": {width: 1280, height: 720}, "openai:3@0": {width: 1280, height: 720},
        "lightricks:2@0": {width: 1920, height: 1080}, "lightricks:2@1": {width: 1920, height: 1080},
        "runware:190@1": {width: 0, height: 0},
    };

    // Find other "use" parameter widgets for Video Inference
    const useDurationWidget = videoInferenceNode.widgets.find(w => w.name === "useDuration");
    const durationWidget = videoInferenceNode.widgets.find(w => w.name === "duration");
    const useFpsWidget = videoInferenceNode.widgets.find(w => w.name === "useFps");
    const fpsWidget = videoInferenceNode.widgets.find(w => w.name === "fps");
    const useSeedWidget = videoInferenceNode.widgets.find(w => w.name === "useSeed");
    const seedWidget = videoInferenceNode.widgets.find(w => w.name === "seed");
    const useStepsWidget = videoInferenceNode.widgets.find(w => w.name === "useSteps");
    const stepsWidget = videoInferenceNode.widgets.find(w => w.name === "steps");
    
    // Helper function to toggle widget enabled state (exact same pattern as toggleDimensionsEnabled)
    function toggleWidgetState(useWidget, paramWidget, paramName) {
        if (!useWidget || !paramWidget) return;
        
        function toggleEnabled() {
            const enabled = useWidget.value === true;
            
            // Disable/enable widgets using inputEl if available (exact same pattern)
            if (paramWidget.inputEl) {
                paramWidget.inputEl.disabled = !enabled;
                paramWidget.inputEl.style.opacity = enabled ? "1" : "0.5";
                paramWidget.inputEl.style.cursor = enabled ? "text" : "not-allowed";
                paramWidget.inputEl.readOnly = !enabled;
            }
            // Also set widget property
            paramWidget.disabled = !enabled;
            
            // Fallback: try to find inputs via DOM if inputEl is not available
            if (!paramWidget.inputEl) {
                const nodeElement = videoInferenceNode.htmlElements?.widgetsContainer || videoInferenceNode.htmlElements;
                if (nodeElement) {
                    const input = nodeElement.querySelector(`input[name="${paramName}"], textarea[name="${paramName}"], select[name="${paramName}"]`);
                    if (input) {
                        input.disabled = !enabled;
                        input.style.opacity = enabled ? "1" : "0.5";
                        input.style.cursor = enabled ? "text" : "not-allowed";
                        input.readOnly = !enabled;
                        if (input.tagName === "SELECT") {
                            input.style.pointerEvents = enabled ? "auto" : "none";
                        }
                    }
                }
            }
            
            videoInferenceNode.setDirtyCanvas(true);
        }
        
        // Set up callback (exact same pattern as useCustomDimensions)
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        // Initial call to set initial state
        setTimeout(toggleEnabled, 100);
    }
    
    function toggleDimensionsEnabled() {
        const isCustom = useCustomDimensionsWidget.value === true;
        
        // Disable/enable widgets using inputEl if available
        if (widthWidget) {
            if (widthWidget.inputEl) {
                widthWidget.inputEl.disabled = !isCustom;
                widthWidget.inputEl.style.opacity = isCustom ? "1" : "0.5";
                widthWidget.inputEl.style.cursor = isCustom ? "text" : "not-allowed";
                widthWidget.inputEl.readOnly = !isCustom;
            }
            // Also set widget property
            widthWidget.disabled = !isCustom;
        }
        
        if (heightWidget) {
            if (heightWidget.inputEl) {
                heightWidget.inputEl.disabled = !isCustom;
                heightWidget.inputEl.style.opacity = isCustom ? "1" : "0.5";
                heightWidget.inputEl.style.cursor = isCustom ? "text" : "not-allowed";
                heightWidget.inputEl.readOnly = !isCustom;
            }
            // Also set widget property
            heightWidget.disabled = !isCustom;
        }
        
        // Fallback: try to find inputs via DOM if inputEl is not available
        if (!widthWidget.inputEl || !heightWidget.inputEl) {
            const nodeElement = videoInferenceNode.htmlElements?.widgetsContainer || videoInferenceNode.htmlElements;
            if (nodeElement) {
                const widthInput = nodeElement.querySelector(`input[name="width"]`);
                const heightInput = nodeElement.querySelector(`input[name="height"]`);
                
                if (widthInput) {
                    widthInput.disabled = !isCustom;
                    widthInput.style.opacity = isCustom ? "1" : "0.5";
                    widthInput.style.cursor = isCustom ? "text" : "not-allowed";
                    widthInput.readOnly = !isCustom;
                }
                
                if (heightInput) {
                    heightInput.disabled = !isCustom;
                    heightInput.style.opacity = isCustom ? "1" : "0.5";
                    heightInput.style.cursor = isCustom ? "text" : "not-allowed";
                    heightInput.readOnly = !isCustom;
                }
            }
        }
        
        videoInferenceNode.setDirtyCanvas(true);
    }
    
    // Set up all toggle handlers for "use" parameters (useCustomDimensions is handled separately below)
    if (useDurationWidget && durationWidget) {
        toggleWidgetState(useDurationWidget, durationWidget, "duration");
    }
    
    if (useFpsWidget && fpsWidget) {
        toggleWidgetState(useFpsWidget, fpsWidget, "fps");
    }
    
    if (useSeedWidget && seedWidget) {
        toggleWidgetState(useSeedWidget, seedWidget, "seed");
    }
    
    if (useStepsWidget && stepsWidget) {
        toggleWidgetState(useStepsWidget, stepsWidget, "steps");
    }

    function updateDimensions() {
        if (useCustomDimensionsWidget.value === true) return;

        const modelInput = videoInferenceNode.inputs.find(input => input.name === "Model");
        let model = null;

        if (modelInput && modelInput.link) {
            const link = app.graph.links[modelInput.link];
            if (link) {
                const sourceNode = app.graph.getNodeById(link.origin_id);
                if (sourceNode && sourceNode.imgs && sourceNode.imgs.length > 0) {
                    const modelValue = sourceNode.imgs[0];
                    model = typeof modelValue === "object" && modelValue.model ? modelValue.model : modelValue;
                }
            }
        }

        if (!model) {
            const modelWidget = videoInferenceNode.widgets.find(w => w.name === "Model");
            if (modelWidget && modelWidget.value) {
                const modelValue = modelWidget.value;
                model = typeof modelValue === "object" && modelValue.model ? modelValue.model : modelValue;
            }
        }

        if (model && MODEL_DIMENSIONS[model]) {
            const dims = MODEL_DIMENSIONS[model];
            if (dims.width !== 0 && dims.height !== 0) {
                if (widthWidget.callback) widthWidget.callback(dims.width, "customSetOperation");
                if (heightWidget.callback) heightWidget.callback(dims.height, "customSetOperation");
                videoInferenceNode.setDirtyCanvas(true);
            }
        }
    }

    const originalOnConnect = videoInferenceNode.onConnect;
    videoInferenceNode.onConnect = function(...args) {
        if (originalOnConnect) originalOnConnect.apply(this, args);
        setTimeout(() => {
            updateDimensions();
            toggleDimensionsEnabled();
        }, 100);
    };

    if (useCustomDimensionsWidget) {
        appendWidgetCB(useCustomDimensionsWidget, () => {
            setTimeout(() => {
                updateDimensions();
                toggleDimensionsEnabled();
            }, 100);
        });
    }

    // Initial setup
    setTimeout(() => {
        updateDimensions();
        toggleDimensionsEnabled();
    }, 200);
}

function videoModelSearchFilterHandler(videoModelSearchNode) {
    const modelArchWidget = videoModelSearchNode.widgets.find(w => w.name === "Model Architecture");
    const videoListWidget = videoModelSearchNode.widgets.find(w => w.name === "VideoList");
    const widthWidget = videoModelSearchNode.widgets.find(w => w.name === "Width");
    const heightWidget = videoModelSearchNode.widgets.find(w => w.name === "Height");
    const useResolutionWidget = videoModelSearchNode.widgets.find(w => w.name === "useResolution");
    
    if (!modelArchWidget || !videoListWidget) return;

    const VIDEO_MODELS = {
        "KlingAI": [
            "klingai:1@2 (KlingAI V1.0 Pro)", "klingai:1@1 (KlingAI V1 Standard)",
            "klingai:2@2 (KlingAI V1.5 Pro)", "klingai:2@1 (KlingAI V1.5 Standard)",
            "klingai:3@1 (KlingAI V1.6 Standard)", "klingai:3@2 (KlingAI V1.6 Pro)",
            "klingai:4@3 (KlingAI V2.1 Master)", "klingai:5@1 (KlingAI V2.1 Standard (I2V))",
            "klingai:5@2 (KlingAI V2.1 Pro (I2V))", "klingai:5@3 (KlingAI V2.0 Master)",
            "klingai:7@1 (KlingAI Lip-Sync)",
        ],
        "Veo": [
            "google:2@0 (Veo 2.0)", "google:3@0 (Veo 3.0)", "google:3@1 (Veo 3.0 Fast)",
            "google:3@2 (Veo 3.1)", "google:3@3 (Veo 3.1 Fast)",
        ],
        "Bytedance": [
            "bytedance:2@1 (Seedance 1.0 Pro)", "bytedance:1@1 (Seedance 1.0 Lite)",
            "bytedance:5@1 (OmniHuman 1)", "bytedance:5@2 (OmniHuman 1.5)",
        ],
        "MiniMax": [
            "minimax:1@1 (MiniMax 01 Base)", "minimax:2@1 (MiniMax 01 Director)",
            "minimax:2@3 (MiniMax I2V 01 Live)", "minimax:3@1 (MiniMax 02 Hailuo)",
            "minimax:4@1 (MiniMax Hailuo 2.3)", "minimax:4@2 (MiniMax Hailuo 2.3 Fast)",
        ],
        "PixVerse": [
            "pixverse:1@1 (PixVerse v3.5)", "pixverse:1@2 (PixVerse v4)",
            "pixverse:1@3 (PixVerse v4.5)", "pixverse:lipsync@1 (PixVerse LipSync)",
        ],
        "Vidu": [
            "vidu:1@0 (Vidu Q1 Classic)", "vidu:1@1 (Vidu Q1)",
            "vidu:1@5 (Vidu 1.5)", "vidu:2@0 (Vidu 2.0)",
        ],
        "Wan": [
            "runware:200@1 (Wan 2.1 1.3B)", "runware:200@2 (Wan 2.1 14B)",
            "runware:200@6 (Wan 2.2)",
        ],
        "OpenAI": [
            "openai:3@1 (OpenAI Sora 3.1)", "openai:3@0 (OpenAI Sora 3.0)",
        ],
        "Lightricks": [
            "lightricks:2@0 (LTX Fast)", "lightricks:2@1 (LTX Pro)",
        ],
        "Ovi": [
            "runware:190@1 (Ovi)",
        ],
        "Runway": [
            "runway:2@1 (Runway Aleph)",
            "runway:1@1 (Runway Gen-4 Turbo)",
        ],
        "Luma": [
            "lumaai:1@1 (Luma Ray 1.6)",
            "lumaai:2@1 (Luma Ray 2)",
            "lumaai:2@2 (Luma Ray 2 Flash)",
        ],
    };

    const MODEL_DIMENSIONS = {
        "klingai:1@2": {"width": 1280, "height": 720},
        "klingai:1@1": {"width": 1280, "height": 720},
        "klingai:2@2": {"width": 1920, "height": 1080},
        "klingai:2@1": {"width": 1280, "height": 720},
        "klingai:3@1": {"width": 1280, "height": 720},
        "klingai:3@2": {"width": 1920, "height": 1080},
        "klingai:4@3": {"width": 1280, "height": 720},
        "klingai:5@1": {"width": 1280, "height": 720},
        "klingai:5@2": {"width": 1920, "height": 1080},
        "klingai:5@3": {"width": 1920, "height": 1080},
        "klingai:7@1": {"width": 0, "height": 0},
        "google:2@0": {"width": 1280, "height": 720},
        "google:3@0": {"width": 1280, "height": 720},
        "google:3@1": {"width": 1280, "height": 720},
        "google:3@2": {"width": 1280, "height": 720},
        "google:3@3": {"width": 1280, "height": 720},
        "bytedance:2@1": {"width": 864, "height": 480},
        "bytedance:1@1": {"width": 864, "height": 480},
        "bytedance:5@1": {"width": 1024, "height": 1024},
        "bytedance:5@2": {"width": 1024, "height": 1024},
        "minimax:1@1": {"width": 1366, "height": 768},
        "minimax:2@1": {"width": 1366, "height": 768},
        "minimax:2@3": {"width": 1366, "height": 768},
        "minimax:3@1": {"width": 1366, "height": 768},
        "minimax:4@1": {"width": 1366, "height": 768},
        "minimax:4@2": {"width": 1366, "height": 768},
        "pixverse:1@1": {"width": 640, "height": 360},
        "pixverse:1@2": {"width": 640, "height": 360},
        "pixverse:1@3": {"width": 640, "height": 360},
        "pixverse:lipsync@1": {"width": 640, "height": 360},
        "vidu:1@0": {"width": 1920, "height": 1080},
        "vidu:1@1": {"width": 1920, "height": 1080},
        "vidu:1@5": {"width": 1920, "height": 1080},
        "vidu:2@0": {"width": 1920, "height": 1080},
        "runware:200@1": {"width": 853, "height": 480},
        "runware:200@2": {"width": 853, "height": 480},
        "runware:200@6": {"width": 1280, "height": 720},
        "openai:3@1": {"width": 1280, "height": 720},
        "openai:3@0": {"width": 1280, "height": 720},
        "lightricks:2@0": {"width": 1920, "height": 1080},
        "lightricks:2@1": {"width": 1920, "height": 1080},
        "runware:190@1": {"width": 0, "height": 0},
        "runway:2@1": {"width": 1280, "height": 720},
        "runway:1@1": {"width": 1280, "height": 720},
        "lumaai:1@1": {"width": 1080, "height": 720},
        "lumaai:2@1": {"width": 1080, "height": 720},
        "lumaai:2@2": {"width": 1080, "height": 720},
    };

    const DEFAULT_DIMENSIONS = {"width": 1024, "height": 576};

    function setWidthHeightEnabled(enabled) {
        if (!widthWidget || !heightWidget) return;
        [widthWidget, heightWidget].forEach(widget => {
            widget.disabled = !enabled;
            if (widget.inputEl) {
                widget.inputEl.disabled = !enabled;
                widget.inputEl.style.opacity = enabled ? "1" : "0.5";
                widget.inputEl.style.cursor = enabled ? "text" : "not-allowed";
                widget.inputEl.readOnly = !enabled;
            }
        });
    }

    function updateDimensions() {
        if (!widthWidget || !heightWidget || !videoListWidget) return;

        const selectedModel = videoListWidget.value;
        if (!selectedModel) return;

        if (useResolutionWidget && !useResolutionWidget.value) {
            setWidthHeightEnabled(false);
            if (widthWidget.callback) widthWidget.callback(0, "customSetOperation");
            widthWidget.value = 0;
            if (heightWidget.callback) heightWidget.callback(0, "customSetOperation");
            heightWidget.value = 0;
            videoModelSearchNode.setDirtyCanvas(true);
            return;
        }

        setWidthHeightEnabled(true);

        const modelCode = selectedModel.split(" (")[0];
        const dims = MODEL_DIMENSIONS[modelCode] || DEFAULT_DIMENSIONS;

        if (dims.width === 0 && dims.height === 0) {
            // Set to None when dimensions are 0,0
            if (widthWidget.callback) widthWidget.callback(null, "customSetOperation");
            if (heightWidget.callback) heightWidget.callback(null, "customSetOperation");
            videoModelSearchNode.setDirtyCanvas(true);
        } else if (dims.width !== 0 && dims.height !== 0) {
            if (widthWidget.callback) widthWidget.callback(dims.width, "customSetOperation");
            if (heightWidget.callback) heightWidget.callback(dims.height, "customSetOperation");
            videoModelSearchNode.setDirtyCanvas(true);
        }
    }

    function filterModelList() {
        const selectedArch = modelArchWidget.value;
        let filteredModels = [];

        if (selectedArch === "All") {
            Object.values(VIDEO_MODELS).forEach(models => filteredModels.push(...models));
        } else if (VIDEO_MODELS[selectedArch]) {
            filteredModels = VIDEO_MODELS[selectedArch];
        }

        if (filteredModels.length > 0) {
            const currentValue = videoListWidget.value;
            videoListWidget.options.values = filteredModels;
            
            if (!filteredModels.includes(currentValue)) {
                videoListWidget.value = filteredModels[0];
            }
            
            updateDimensions();
            videoModelSearchNode.setDirtyCanvas(true);
        }
    }

    appendWidgetCB(modelArchWidget, filterModelList);
    if (videoListWidget) {
        appendWidgetCB(videoListWidget, updateDimensions);
    }
    if (useResolutionWidget) {
        appendWidgetCB(useResolutionWidget, () => {
            updateDimensions();
        });
    }
    filterModelList();
    updateDimensions();
}

function audioModelSearchFilterHandler(audioModelSearchNode) {
    const modelProviderWidget = audioModelSearchNode.widgets.find(w => w.name === "Model Provider");
    const audioListWidget = audioModelSearchNode.widgets.find(w => w.name === "AudioList");
    
    if (!modelProviderWidget || !audioListWidget) return;

    const AUDIO_MODELS = {
        "ElevenLabs": [
            "elevenlabs:1@1 (ElevenLabs Multilingual v2)",
            "elevenlabs:2@1 (ElevenLabs Multilingual v2 Turbo)",
            "elevenlabs:3@1 (ElevenLabs Monolingual v1)",
        ],
        "KlingAI": [
            "klingai:8@1 (KlingAI Audio)",
        ],
    };

    function filterModelList() {
        const selectedProvider = modelProviderWidget.value;
        let filteredModels = [];

        if (selectedProvider === "All") {
            Object.values(AUDIO_MODELS).forEach(models => filteredModels.push(...models));
        } else if (AUDIO_MODELS[selectedProvider]) {
            filteredModels = AUDIO_MODELS[selectedProvider];
        }

        if (filteredModels.length > 0) {
            const currentValue = audioListWidget.value;
            audioListWidget.options.values = filteredModels;
            
            if (!filteredModels.includes(currentValue)) {
                audioListWidget.value = filteredModels[0];
            }
            
            audioModelSearchNode.setDirtyCanvas(true);
        }
    }

    appendWidgetCB(modelProviderWidget, filterModelList);
    filterModelList();
}

function klingProviderSettingsToggleHandler(klingNode) {
    // Find all "use" parameter widgets for KlingAI Provider Settings (EXACT same pattern as imageInferenceToggleHandler)
    const useCameraControlWidget = klingNode.widgets.find(w => w.name === "useCameraControl");
    const cameraControlWidget = klingNode.widgets.find(w => w.name === "cameraControl");
    const useSoundVolumeWidget = klingNode.widgets.find(w => w.name === "useSoundVolume");
    const soundVolumeWidget = klingNode.widgets.find(w => w.name === "soundVolume");
    const useOriginalAudioVolumeWidget = klingNode.widgets.find(w => w.name === "useOriginalAudioVolume");
    const originalAudioVolumeWidget = klingNode.widgets.find(w => w.name === "originalAudioVolume");
    const useSoundEffectPromptWidget = klingNode.widgets.find(w => w.name === "useSoundEffectPrompt");
    const soundEffectPromptWidget = klingNode.widgets.find(w => w.name === "soundEffectPrompt");
    const useBgmPromptWidget = klingNode.widgets.find(w => w.name === "useBgmPrompt");
    const bgmPromptWidget = klingNode.widgets.find(w => w.name === "bgmPrompt");
    const useAsmrModeWidget = klingNode.widgets.find(w => w.name === "useAsmrMode");
    const asmrModeWidget = klingNode.widgets.find(w => w.name === "asmrMode");
    
    // Helper function to toggle widget enabled state (EXACT same pattern as imageInferenceToggleHandler)
    function toggleWidgetState(useWidget, paramWidget, paramName) {
        if (!useWidget || !paramWidget) return;
        
        function toggleEnabled() {
            const enabled = useWidget.value === true;
            
            // Disable/enable widgets using inputEl if available (exact same pattern)
            if (paramWidget.inputEl) {
                paramWidget.inputEl.disabled = !enabled;
                paramWidget.inputEl.style.opacity = enabled ? "1" : "0.5";
                paramWidget.inputEl.style.cursor = enabled ? "text" : "not-allowed";
                paramWidget.inputEl.readOnly = !enabled;
            }
            // Also set widget property
            paramWidget.disabled = !enabled;
            
            // Fallback: try to find inputs via DOM if inputEl is not available
            if (!paramWidget.inputEl) {
                const nodeElement = klingNode.htmlElements?.widgetsContainer || klingNode.htmlElements;
                if (nodeElement) {
                    const input = nodeElement.querySelector(`input[name="${paramName}"], textarea[name="${paramName}"], select[name="${paramName}"]`);
                    if (input) {
                        input.disabled = !enabled;
                        input.style.opacity = enabled ? "1" : "0.5";
                        input.style.cursor = enabled ? "text" : "not-allowed";
                        input.readOnly = !enabled;
                        if (input.tagName === "SELECT") {
                            input.style.pointerEvents = enabled ? "auto" : "none";
                        }
                    }
                }
            }
            
            klingNode.setDirtyCanvas(true);
        }
        
        // Set up callback (exact same pattern as imageInferenceToggleHandler)
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        // Initial call to set initial state (exact same pattern)
        setTimeout(toggleEnabled, 100);
    }
    
    // Set up all toggle handlers (exact same pattern as imageInferenceToggleHandler)
    if (useCameraControlWidget && cameraControlWidget) {
        toggleWidgetState(useCameraControlWidget, cameraControlWidget, "cameraControl");
    }
    
    if (useSoundVolumeWidget && soundVolumeWidget) {
        toggleWidgetState(useSoundVolumeWidget, soundVolumeWidget, "soundVolume");
    }
    
    if (useOriginalAudioVolumeWidget && originalAudioVolumeWidget) {
        toggleWidgetState(useOriginalAudioVolumeWidget, originalAudioVolumeWidget, "originalAudioVolume");
    }
    
    if (useSoundEffectPromptWidget && soundEffectPromptWidget) {
        toggleWidgetState(useSoundEffectPromptWidget, soundEffectPromptWidget, "soundEffectPrompt");
    }
    
    if (useBgmPromptWidget && bgmPromptWidget) {
        toggleWidgetState(useBgmPromptWidget, bgmPromptWidget, "bgmPrompt");
    }
    
    if (useAsmrModeWidget && asmrModeWidget) {
        toggleWidgetState(useAsmrModeWidget, asmrModeWidget, "asmrMode");
    }
}

function lumaProviderSettingsToggleHandler(lumaNode) {
    // Find all "use" parameter widgets for Luma Provider Settings
    const useLoopWidget = lumaNode.widgets.find(w => w.name === "useLoop");
    const loopWidget = lumaNode.widgets.find(w => w.name === "loop");
    const useConcept1Widget = lumaNode.widgets.find(w => w.name === "useConcept1");
    const concept1Widget = lumaNode.widgets.find(w => w.name === "concept1");
    const useConcept2Widget = lumaNode.widgets.find(w => w.name === "useConcept2");
    const concept2Widget = lumaNode.widgets.find(w => w.name === "concept2");
    const useConcept3Widget = lumaNode.widgets.find(w => w.name === "useConcept3");
    const concept3Widget = lumaNode.widgets.find(w => w.name === "concept3");
    const useConcept4Widget = lumaNode.widgets.find(w => w.name === "useConcept4");
    const concept4Widget = lumaNode.widgets.find(w => w.name === "concept4");

    function toggleWidgetState(useWidget, paramWidget, paramName) {
        if (!useWidget || !paramWidget) return;

        function toggleEnabled() {
            const enabled = useWidget.value === true;

            if (paramWidget.inputEl) {
                paramWidget.inputEl.disabled = !enabled;
                paramWidget.inputEl.style.opacity = enabled ? "1" : "0.5";
                paramWidget.inputEl.style.cursor = enabled ? "text" : "not-allowed";
                paramWidget.inputEl.readOnly = !enabled;
            }
            paramWidget.disabled = !enabled;

            if (!paramWidget.inputEl) {
                const nodeElement = lumaNode.htmlElements?.widgetsContainer || lumaNode.htmlElements;
                if (nodeElement) {
                    const input = nodeElement.querySelector(`input[name="${paramName}"], textarea[name="${paramName}"], select[name="${paramName}"]`);
                    if (input) {
                        input.disabled = !enabled;
                        input.style.opacity = enabled ? "1" : "0.5";
                        input.style.cursor = enabled ? "text" : "not-allowed";
                        input.readOnly = !enabled;
                        if (input.tagName === "SELECT") {
                            input.style.pointerEvents = enabled ? "auto" : "none";
                        }
                    }
                }
            }

            lumaNode.setDirtyCanvas(true);
        }

        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });

        setTimeout(toggleEnabled, 100);
    }

    if (useLoopWidget && loopWidget) {
        toggleWidgetState(useLoopWidget, loopWidget, "loop");
    }

    if (useConcept1Widget && concept1Widget) {
        toggleWidgetState(useConcept1Widget, concept1Widget, "concept1");
    }

    if (useConcept2Widget && concept2Widget) {
        toggleWidgetState(useConcept2Widget, concept2Widget, "concept2");
    }

    if (useConcept3Widget && concept3Widget) {
        toggleWidgetState(useConcept3Widget, concept3Widget, "concept3");
    }

    if (useConcept4Widget && concept4Widget) {
        toggleWidgetState(useConcept4Widget, concept4Widget, "concept4");
    }
}

export {
    notifyUser,
    promptEnhanceHandler,
    syncDimensionsNodeHandler,
    searchNodeHandler,
    mediaUUIDHandler,
    captionNodeHandler,
    videoTranscriptionHandler,
    handleCustomErrors,
    APIKeyHandler,
    videoInferenceDimensionsHandler,
    videoModelSearchFilterHandler,
    audioModelSearchFilterHandler,
    useParameterToggleHandler,
    imageInferenceToggleHandler,
    upscalerToggleHandler,
    videoUpscalerToggleHandler,
    audioInferenceToggleHandler,
    acceleratorOptionsToggleHandler,
    bytedanceProviderSettingsToggleHandler,
    openaiProviderSettingsToggleHandler,
    klingProviderSettingsToggleHandler,
    lumaProviderSettingsToggleHandler,
};