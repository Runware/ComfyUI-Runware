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

function save3DFilepathHandler(msgEvent) {
    const data = msgEvent.detail;
    const filepath = data.filepath;
    const nodeID = parseInt(data.nodeID, 10);
    if (Number.isNaN(nodeID)) return false;

    if(data.success && filepath) {
        const node = app.graph.getNodeById(nodeID);
        if(node !== null && node !== undefined) {
            const filepathWidget = node.widgets.find(widget => widget.name === "filepath");
            if(filepathWidget) {
                if(filepathWidget.value !== undefined) {
                    filepathWidget.value = filepath;
                }
                if(filepathWidget.inputEl) {
                    filepathWidget.inputEl.value = filepath;
                    filepathWidget.inputEl.dispatchEvent(new Event('input', { bubbles: true }));
                    filepathWidget.inputEl.dispatchEvent(new Event('change', { bubbles: true }));
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

function videoOutputsHandler(msgEvent) {
    const outputData = msgEvent.detail;
    const draftId = outputData.draftId || "";
    const videoId = outputData.videoId || "";
    const nodeID = outputData.nodeID;
    
    if(outputData.success && nodeID !== undefined && nodeID !== null) {
        const nodeIdInt = typeof nodeID === 'string' ? parseInt(nodeID) : nodeID;
        const outputNode = app.graph.getNodeById(nodeIdInt);
        
        if(outputNode !== null && outputNode !== undefined) {
            const draftIdWidget = outputNode.widgets.find(widget => widget.name === "draftId");
            const videoIdWidget = outputNode.widgets.find(widget => widget.name === "videoId");
            
            if(draftIdWidget) {
                if(draftIdWidget.value !== undefined) draftIdWidget.value = draftId;
                if(draftIdWidget.inputEl) {
                    draftIdWidget.inputEl.value = draftId;
                    draftIdWidget.inputEl.dispatchEvent(new Event('input', { bubbles: true }));
                    draftIdWidget.inputEl.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }
            
            if(videoIdWidget) {
                if(videoIdWidget.value !== undefined) videoIdWidget.value = videoId;
                if(videoIdWidget.inputEl) {
                    videoIdWidget.inputEl.value = videoId;
                    videoIdWidget.inputEl.dispatchEvent(new Event('input', { bubbles: true }));
                    videoIdWidget.inputEl.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }
            
            outputNode.setDirtyCanvas(true);
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
    const useStepsWidget = audioInferenceNode.widgets.find(w => w.name === "useSteps");
    const stepsWidget = audioInferenceNode.widgets.find(w => w.name === "steps");
    
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
    
    if (useStepsWidget && stepsWidget) {
        toggleWidgetState(useStepsWidget, stepsWidget, "steps");
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
    const useAudioWidget = bytedanceNode.widgets.find(w => w.name === "useAudio");
    const audioWidget = bytedanceNode.widgets.find(w => w.name === "audio");
    const useDraftWidget = bytedanceNode.widgets.find(w => w.name === "useDraft");
    const draftWidget = bytedanceNode.widgets.find(w => w.name === "draft");
    
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

    if (useAudioWidget && audioWidget) {
        toggleWidgetState(useAudioWidget, audioWidget, "audio");
    }

    if (useDraftWidget && draftWidget) {
        toggleWidgetState(useDraftWidget, draftWidget, "draft");
    }
}

function ultralyticsProviderSettingsToggleHandler(ultralyticsNode) {
    const useParamPairs = [
        ["useMaskBlur", "maskBlur"],
        ["useMaskPadding", "maskPadding"],
        ["useConfidence", "confidence"],
        ["usePositivePrompt", "positivePrompt"],
        ["useNegativePrompt", "negativePrompt"],
        ["useSteps", "steps"],
        ["useCFGScale", "CFGScale"],
        ["useStrength", "strength"],
    ];

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

            if (paramWidget.options && paramWidget.options.element) {
                paramWidget.options.element.disabled = !enabled;
                paramWidget.options.element.style.opacity = enabled ? "1" : "0.5";
                paramWidget.options.element.style.pointerEvents = enabled ? "auto" : "none";
            }

            if (!paramWidget.inputEl) {
                const nodeElement = ultralyticsNode.htmlElements?.widgetsContainer || ultralyticsNode.htmlElements;
                if (nodeElement) {
                    const input = nodeElement.querySelector(`input[name="${paramName}"], textarea[name="${paramName}"], select[name="${paramName}"]`);
                    if (input) {
                        input.disabled = !enabled;
                        input.style.opacity = enabled ? "1" : "0.5";
                        input.style.pointerEvents = enabled ? "auto" : "none";
                    }
                }
            }

            ultralyticsNode.setDirtyCanvas(true);
        }

        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });

        setTimeout(toggleEnabled, 100);
    }

    useParamPairs.forEach(([useName, paramName]) => {
        const useWidget = ultralyticsNode.widgets.find(w => w.name === useName);
        const paramWidget = ultralyticsNode.widgets.find(w => w.name === paramName);
        if (useWidget && paramWidget) {
            toggleWidgetState(useWidget, paramWidget, paramName);
        }
    });
}

function xaiProviderSettingsToggleHandler(xaiNode) {
    const useQualityWidget = xaiNode.widgets.find(w => w.name === "useQuality");
    const qualityWidget = xaiNode.widgets.find(w => w.name === "quality");

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

            if (paramWidget.options && paramWidget.options.element) {
                paramWidget.options.element.disabled = !enabled;
                paramWidget.options.element.style.opacity = enabled ? "1" : "0.5";
                paramWidget.options.element.style.pointerEvents = enabled ? "auto" : "none";
            }

            if (!paramWidget.inputEl) {
                const nodeElement = xaiNode.htmlElements?.widgetsContainer || xaiNode.htmlElements;
                if (nodeElement) {
                    const input = nodeElement.querySelector(`input[name="${paramName}"], textarea[name="${paramName}"], select[name="${paramName}"]`);
                    if (input) {
                        input.disabled = !enabled;
                        input.style.opacity = enabled ? "1" : "0.5";
                        input.style.pointerEvents = enabled ? "auto" : "none";
                    }
                }
            }

            xaiNode.setDirtyCanvas(true);
        }

        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });

        setTimeout(toggleEnabled, 100);
    }

    if (useQualityWidget && qualityWidget) {
        toggleWidgetState(useQualityWidget, qualityWidget, "quality");
    }
}

function viduProviderSettingsToggleHandler(viduNode) {
    const useAudioWidget = viduNode.widgets.find(w => w.name === "useAudio");
    const audioWidget = viduNode.widgets.find(w => w.name === "audio");
    const useBgmWidget = viduNode.widgets.find(w => w.name === "useBgm");
    const bgmWidget = viduNode.widgets.find(w => w.name === "bgm");
    const useStyleWidget = viduNode.widgets.find(w => w.name === "useStyle");
    const styleWidget = viduNode.widgets.find(w => w.name === "style");
    const useMovementAmplitudeWidget = viduNode.widgets.find(w => w.name === "useMovementAmplitude");
    const movementAmplitudeWidget = viduNode.widgets.find(w => w.name === "movementAmplitude");
    const useTemplateNameWidget = viduNode.widgets.find(w => w.name === "useTemplateName");
    const templateNameWidget = viduNode.widgets.find(w => w.name === "templateName");
    const useTemplateAreaWidget = viduNode.widgets.find(w => w.name === "useTemplateArea");
    const templateAreaWidget = viduNode.widgets.find(w => w.name === "templateArea");
    const useTemplateBeastWidget = viduNode.widgets.find(w => w.name === "useTemplateBeast");
    const templateBeastWidget = viduNode.widgets.find(w => w.name === "templateBeast");

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
                const nodeElement = viduNode.htmlElements?.widgetsContainer || viduNode.htmlElements;
                if (nodeElement) {
                    const input = nodeElement.querySelector(`input[name="${paramName}"], textarea[name="${paramName}"], select[name="${paramName}"]`);
                    if (input) {
                        input.disabled = !enabled;
                        input.style.opacity = enabled ? "1" : "0.5";
                        input.style.pointerEvents = enabled ? "auto" : "none";
                    }
                }
            }

            viduNode.setDirtyCanvas(true);
        }

        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });

        setTimeout(toggleEnabled, 100);
    }

    if (useAudioWidget && audioWidget) {
        toggleWidgetState(useAudioWidget, audioWidget, "audio");
    }
    if (useBgmWidget && bgmWidget) {
        toggleWidgetState(useBgmWidget, bgmWidget, "bgm");
    }
    if (useStyleWidget && styleWidget) {
        toggleWidgetState(useStyleWidget, styleWidget, "style");
    }
    if (useMovementAmplitudeWidget && movementAmplitudeWidget) {
        toggleWidgetState(useMovementAmplitudeWidget, movementAmplitudeWidget, "movementAmplitude");
    }
    if (useTemplateNameWidget && templateNameWidget) {
        toggleWidgetState(useTemplateNameWidget, templateNameWidget, "templateName");
    }
    if (useTemplateAreaWidget && templateAreaWidget) {
        toggleWidgetState(useTemplateAreaWidget, templateAreaWidget, "templateArea");
    }
    if (useTemplateBeastWidget && templateBeastWidget) {
        toggleWidgetState(useTemplateBeastWidget, templateBeastWidget, "templateBeast");
    }
}

function sourcefulProviderSettingsToggleHandler(sourcefulNode) {
    const useTransparencyWidget = sourcefulNode.widgets.find(w => w.name === "useTransparency");
    const transparencyWidget = sourcefulNode.widgets.find(w => w.name === "transparency");
    const useEnhancePromptWidget = sourcefulNode.widgets.find(w => w.name === "useEnhancePrompt");
    const enhancePromptWidget = sourcefulNode.widgets.find(w => w.name === "enhancePrompt");

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
                const nodeElement = sourcefulNode.htmlElements?.widgetsContainer || sourcefulNode.htmlElements;
                if (nodeElement) {
                    const input = nodeElement.querySelector(`input[name="${paramName}"], textarea[name="${paramName}"], select[name="${paramName}"]`);
                    if (input) {
                        input.disabled = !enabled;
                        input.style.opacity = enabled ? "1" : "0.5";
                        input.style.pointerEvents = enabled ? "auto" : "none";
                    }
                }
            }

            sourcefulNode.setDirtyCanvas(true);
        }

        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });

        setTimeout(toggleEnabled, 100);
    }

    if (useTransparencyWidget && transparencyWidget) {
        toggleWidgetState(useTransparencyWidget, transparencyWidget, "transparency");
    }
    if (useEnhancePromptWidget && enhancePromptWidget) {
        toggleWidgetState(useEnhancePromptWidget, enhancePromptWidget, "enhancePrompt");
    }
}

function sourcefulProviderSettingsFontsToggleHandler(fontsNode) {
    const useFont1Widget = fontsNode.widgets.find(w => w.name === "useFont1");
    const fontUrl1Widget = fontsNode.widgets.find(w => w.name === "fontUrl1");
    const text1Widget = fontsNode.widgets.find(w => w.name === "text1");
    const useFont2Widget = fontsNode.widgets.find(w => w.name === "useFont2");
    const fontUrl2Widget = fontsNode.widgets.find(w => w.name === "fontUrl2");
    const text2Widget = fontsNode.widgets.find(w => w.name === "text2");

    function toggleFontGroup(useWidget, fontUrlWidget, textWidget, fontParamName, textParamName) {
        if (!useWidget || !fontUrlWidget || !textWidget) return;

        function toggleEnabled() {
            const enabled = useWidget.value === true;

            [fontUrlWidget, textWidget].forEach(paramWidget => {
                if (paramWidget.inputEl) {
                    paramWidget.inputEl.disabled = !enabled;
                    paramWidget.inputEl.style.opacity = enabled ? "1" : "0.5";
                    paramWidget.inputEl.style.cursor = enabled ? "text" : "not-allowed";
                    paramWidget.inputEl.readOnly = !enabled;
                }
                paramWidget.disabled = !enabled;
            });

            const nodeElement = fontsNode.htmlElements?.widgetsContainer || fontsNode.htmlElements;
            if (nodeElement) {
                [fontParamName, textParamName].forEach(paramName => {
                    const input = nodeElement.querySelector(`input[name="${paramName}"], textarea[name="${paramName}"]`);
                    if (input) {
                        input.disabled = !enabled;
                        input.style.opacity = enabled ? "1" : "0.5";
                        input.style.pointerEvents = enabled ? "auto" : "none";
                    }
                });
            }

            fontsNode.setDirtyCanvas(true);
        }

        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });

        setTimeout(toggleEnabled, 100);
    }

    if (useFont1Widget && fontUrl1Widget && text1Widget) {
        toggleFontGroup(useFont1Widget, fontUrl1Widget, text1Widget, "fontUrl1", "text1");
    }
    if (useFont2Widget && fontUrl2Widget && text2Widget) {
        toggleFontGroup(useFont2Widget, fontUrl2Widget, text2Widget, "fontUrl2", "text2");
    }
}

function threeDInferenceToggleHandler(node) {
    const useOutputQualityWidget = node.widgets.find(w => w.name === "useOutputQuality");
    const outputQualityWidget = node.widgets.find(w => w.name === "outputQuality");
    if (!useOutputQualityWidget || !outputQualityWidget) return;
    function toggleEnabled() {
        const enabled = useOutputQualityWidget.value === true;
        if (outputQualityWidget.inputEl) {
            outputQualityWidget.inputEl.disabled = !enabled;
            outputQualityWidget.inputEl.style.opacity = enabled ? "1" : "0.5";
        }
        outputQualityWidget.disabled = !enabled;
        node.setDirtyCanvas(true);
    }
    appendWidgetCB(useOutputQualityWidget, () => setTimeout(toggleEnabled, 50));
    setTimeout(toggleEnabled, 100);
}

function threeDInferenceSettingsToggleHandler(node) {
    const pairs = [
        ["useTextureSize", "textureSize"],
        ["useDecimationTarget", "decimationTarget"],
        ["useRemesh", "remesh"],
        ["useResolution", "resolution"],
    ];
    pairs.forEach(([useName, paramName]) => {
        const useW = node.widgets.find(w => w.name === useName);
        const paramW = node.widgets.find(w => w.name === paramName);
        if (!useW || !paramW) return;
        function toggleEnabled() {
            const enabled = useW.value === true;
            if (paramW.inputEl) {
                paramW.inputEl.disabled = !enabled;
                paramW.inputEl.style.opacity = enabled ? "1" : "0.5";
            }
            paramW.disabled = !enabled;
            node.setDirtyCanvas(true);
        }
        appendWidgetCB(useW, () => setTimeout(toggleEnabled, 50));
        setTimeout(toggleEnabled, 100);
    });
}

function threeDInferenceSettingsLatToggleHandler(node) {
    const pairs = [
        ["useGuidanceStrength", "guidanceStrength"],
        ["useGuidanceRescale", "guidanceRescale"],
        ["useSteps", "steps"],
        ["useRescaleT", "rescaleT"],
    ];
    pairs.forEach(([useName, paramName]) => {
        const useW = node.widgets.find(w => w.name === useName);
        const paramW = node.widgets.find(w => w.name === paramName);
        if (!useW || !paramW) return;
        function toggleEnabled() {
            const enabled = useW.value === true;
            if (paramW.inputEl) {
                paramW.inputEl.disabled = !enabled;
                paramW.inputEl.style.opacity = enabled ? "1" : "0.5";
            }
            paramW.disabled = !enabled;
            node.setDirtyCanvas(true);
        }
        appendWidgetCB(useW, () => setTimeout(toggleEnabled, 50));
        setTimeout(toggleEnabled, 100);
    });
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

function pixverseProviderSettingsToggleHandler(pixverseNode) {
    // Find all "use" parameter widgets for Pixverse Provider Settings
    const useEffectWidget = pixverseNode.widgets.find(w => w.name === "useEffect");
    const effectWidget = pixverseNode.widgets.find(w => w.name === "effect");
    const useCameraMovementWidget = pixverseNode.widgets.find(w => w.name === "useCameraMovement");
    const cameraMovementWidget = pixverseNode.widgets.find(w => w.name === "cameraMovement");
    const useStyleWidget = pixverseNode.widgets.find(w => w.name === "useStyle");
    const styleWidget = pixverseNode.widgets.find(w => w.name === "style");
    const useMotionModeWidget = pixverseNode.widgets.find(w => w.name === "useMotionMode");
    const motionModeWidget = pixverseNode.widgets.find(w => w.name === "motionMode");
    const useSoundEffectSwitchWidget = pixverseNode.widgets.find(w => w.name === "useSoundEffectSwitch");
    const soundEffectSwitchWidget = pixverseNode.widgets.find(w => w.name === "soundEffectSwitch");
    const useSoundEffectContentWidget = pixverseNode.widgets.find(w => w.name === "useSoundEffectContent");
    const soundEffectContentWidget = pixverseNode.widgets.find(w => w.name === "soundEffectContent");
    const useAudioWidget = pixverseNode.widgets.find(w => w.name === "useAudio");
    const audioWidget = pixverseNode.widgets.find(w => w.name === "audio");
    const useMultiClipWidget = pixverseNode.widgets.find(w => w.name === "useMultiClip");
    const multiClipWidget = pixverseNode.widgets.find(w => w.name === "multiClip");
    const useThinkingWidget = pixverseNode.widgets.find(w => w.name === "useThinking");
    const thinkingWidget = pixverseNode.widgets.find(w => w.name === "thinking");
    
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
            
            // Handle dropdown widgets
            if (paramWidget.options && paramWidget.options.element) {
                paramWidget.options.element.disabled = !enabled;
                paramWidget.options.element.style.opacity = enabled ? "1" : "0.5";
                paramWidget.options.element.style.pointerEvents = enabled ? "auto" : "none";
            }
            
            paramWidget.disabled = !enabled;
            
            if (!paramWidget.inputEl) {
                const nodeElement = pixverseNode.htmlElements?.widgetsContainer || pixverseNode.htmlElements;
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
            
            pixverseNode.setDirtyCanvas(true);
        }
        
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        setTimeout(toggleEnabled, 100);
    }
    
    // Set up all toggle handlers
    if (useEffectWidget && effectWidget) {
        toggleWidgetState(useEffectWidget, effectWidget, "effect");
    }
    
    if (useCameraMovementWidget && cameraMovementWidget) {
        toggleWidgetState(useCameraMovementWidget, cameraMovementWidget, "cameraMovement");
    }
    
    if (useStyleWidget && styleWidget) {
        toggleWidgetState(useStyleWidget, styleWidget, "style");
    }
    
    if (useMotionModeWidget && motionModeWidget) {
        toggleWidgetState(useMotionModeWidget, motionModeWidget, "motionMode");
    }
    
    if (useSoundEffectSwitchWidget && soundEffectSwitchWidget) {
        toggleWidgetState(useSoundEffectSwitchWidget, soundEffectSwitchWidget, "soundEffectSwitch");
    }
    
    if (useSoundEffectContentWidget && soundEffectContentWidget) {
        toggleWidgetState(useSoundEffectContentWidget, soundEffectContentWidget, "soundEffectContent");
    }
    
    if (useAudioWidget && audioWidget) {
        toggleWidgetState(useAudioWidget, audioWidget, "audio");
    }
    
    if (useMultiClipWidget && multiClipWidget) {
        toggleWidgetState(useMultiClipWidget, multiClipWidget, "multiClip");
    }
    
    if (useThinkingWidget && thinkingWidget) {
        toggleWidgetState(useThinkingWidget, thinkingWidget, "thinking");
    }
}

function lightricksProviderSettingsToggleHandler(lightricksNode) {
    const useStartTimeWidget = lightricksNode.widgets.find(w => w.name === "useStartTime");
    const startTimeWidget = lightricksNode.widgets.find(w => w.name === "startTime");
    const useDurationWidget = lightricksNode.widgets.find(w => w.name === "useDuration");
    const durationWidget = lightricksNode.widgets.find(w => w.name === "duration");
    const useModeWidget = lightricksNode.widgets.find(w => w.name === "useMode");
    const modeWidget = lightricksNode.widgets.find(w => w.name === "mode");
    const useGenerateAudioWidget = lightricksNode.widgets.find(w => w.name === "useGenerateAudio");
    const generateAudioWidget = lightricksNode.widgets.find(w => w.name === "generateAudio");
    
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
            
            if (paramWidget.options && paramWidget.options.element) {
                paramWidget.options.element.disabled = !enabled;
                paramWidget.options.element.style.opacity = enabled ? "1" : "0.5";
                paramWidget.options.element.style.pointerEvents = enabled ? "auto" : "none";
            }
            
            paramWidget.disabled = !enabled;
            
            if (!paramWidget.inputEl) {
                const nodeElement = lightricksNode.htmlElements?.widgetsContainer || lightricksNode.htmlElements;
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
            
            lightricksNode.setDirtyCanvas(true);
        }
        
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        setTimeout(toggleEnabled, 100);
    }
    
    if (useStartTimeWidget && startTimeWidget) {
        toggleWidgetState(useStartTimeWidget, startTimeWidget, "startTime");
    }
    
    if (useDurationWidget && durationWidget) {
        toggleWidgetState(useDurationWidget, durationWidget, "duration");
    }
    
    if (useModeWidget && modeWidget) {
        toggleWidgetState(useModeWidget, modeWidget, "mode");
    }

    if (useGenerateAudioWidget && generateAudioWidget) {
        toggleWidgetState(useGenerateAudioWidget, generateAudioWidget, "generateAudio");
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
    const useResolutionWidget = imageInferenceNode.widgets.find(w => w.name === "useResolution");
    const resolutionWidget = imageInferenceNode.widgets.find(w => w.name === "resolution");
    const dimensionsWidget = imageInferenceNode.widgets.find(w => w.name === "dimensions");
    const widthWidget = imageInferenceNode.widgets.find(w => w.name === "width");
    const heightWidget = imageInferenceNode.widgets.find(w => w.name === "height");
    
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
    
    // Handle Resolution
    if (useResolutionWidget && resolutionWidget) {
        toggleWidgetState(useResolutionWidget, resolutionWidget, "resolution");
    }
    
    // Handle Dimensions - disable width/height when dimensions is "None"
    if (dimensionsWidget && widthWidget && heightWidget) {
        function toggleDimensionsState() {
            const dimensionsValue = dimensionsWidget.value;
            const enabled = dimensionsValue !== "None";
            
            // Toggle width widget
            if (widthWidget.inputEl) {
                widthWidget.inputEl.disabled = !enabled;
                widthWidget.inputEl.style.opacity = enabled ? "1" : "0.5";
                widthWidget.inputEl.style.cursor = enabled ? "text" : "not-allowed";
                widthWidget.inputEl.readOnly = !enabled;
            }
            widthWidget.disabled = !enabled;
            
            // Toggle height widget
            if (heightWidget.inputEl) {
                heightWidget.inputEl.disabled = !enabled;
                heightWidget.inputEl.style.opacity = enabled ? "1" : "0.5";
                heightWidget.inputEl.style.cursor = enabled ? "text" : "not-allowed";
                heightWidget.inputEl.readOnly = !enabled;
            }
            heightWidget.disabled = !enabled;
            
            // Fallback: try to find inputs via DOM if inputEl is not available
            if (!widthWidget.inputEl || !heightWidget.inputEl) {
                const nodeElement = imageInferenceNode.htmlElements?.widgetsContainer || imageInferenceNode.htmlElements;
                if (nodeElement) {
                    const widthInput = nodeElement.querySelector(`input[name="width"]`);
                    const heightInput = nodeElement.querySelector(`input[name="height"]`);
                    if (widthInput) {
                        widthInput.disabled = !enabled;
                        widthInput.style.opacity = enabled ? "1" : "0.5";
                        widthInput.style.cursor = enabled ? "text" : "not-allowed";
                        widthInput.readOnly = !enabled;
                    }
                    if (heightInput) {
                        heightInput.disabled = !enabled;
                        heightInput.style.opacity = enabled ? "1" : "0.5";
                        heightInput.style.cursor = enabled ? "text" : "not-allowed";
                        heightInput.readOnly = !enabled;
                    }
                }
            }
            
            imageInferenceNode.setDirtyCanvas(true);
        }
        
        appendWidgetCB(dimensionsWidget, () => {
            setTimeout(toggleDimensionsState, 50);
        });
        
        setTimeout(toggleDimensionsState, 100);
    }
}

function videoInferenceDimensionsHandler(videoInferenceNode) {
    // Find "use" parameter widgets for Video Inference
    const useDurationWidget = videoInferenceNode.widgets.find(w => w.name === "useDuration");
    const durationWidget = videoInferenceNode.widgets.find(w => w.name === "duration");
    const useFpsWidget = videoInferenceNode.widgets.find(w => w.name === "useFps");
    const fpsWidget = videoInferenceNode.widgets.find(w => w.name === "fps");
    const useSeedWidget = videoInferenceNode.widgets.find(w => w.name === "useSeed");
    const seedWidget = videoInferenceNode.widgets.find(w => w.name === "seed");
    const useStepsWidget = videoInferenceNode.widgets.find(w => w.name === "useSteps");
    const stepsWidget = videoInferenceNode.widgets.find(w => w.name === "steps");
    const useBatchSizeWidget = videoInferenceNode.widgets.find(w => w.name === "useBatchSize");
    const batchSizeWidget = videoInferenceNode.widgets.find(w => w.name === "batchSize");
    
    // Helper function to toggle widget enabled state
    function toggleWidgetState(useWidget, paramWidget, paramName) {
        if (!useWidget || !paramWidget) return;
        
        function toggleEnabled() {
            const enabled = useWidget.value === true;
            
            // Disable/enable widgets using inputEl if available
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
        
        // Set up callback
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        // Initial call to set initial state
        setTimeout(toggleEnabled, 100);
    }
    
    // Set up all toggle handlers for "use" parameters
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
    
    if (useBatchSizeWidget && batchSizeWidget) {
        toggleWidgetState(useBatchSizeWidget, batchSizeWidget, "batchSize");
    }
}

function videoModelSearchFilterHandler(videoModelSearchNode) {
    const modelArchWidget = videoModelSearchNode.widgets.find(w => w.name === "Model Architecture");
    const videoListWidget = videoModelSearchNode.widgets.find(w => w.name === "VideoList");
    const widthWidget = videoModelSearchNode.widgets.find(w => w.name === "Width");
    const heightWidget = videoModelSearchNode.widgets.find(w => w.name === "Height");
    const useCustomDimensionsWidget = videoModelSearchNode.widgets.find(w => w.name === "useCustomDimensions");
    const useResolutionWidget = videoModelSearchNode.widgets.find(w => w.name === "useResolution");
    const resolutionWidget = videoModelSearchNode.widgets.find(w => w.name === "resolution");
    
    if (!modelArchWidget || !videoListWidget) return;

    const VIDEO_MODELS = {
        "KlingAI": [
            "klingai:1@2 (KlingAI V1.0 Pro)", "klingai:1@1 (KlingAI V1 Standard)",
            "klingai:2@2 (KlingAI V1.5 Pro)", "klingai:2@1 (KlingAI V1.5 Standard)",
            "klingai:3@1 (KlingAI V1.6 Standard)", "klingai:3@2 (KlingAI V1.6 Pro)",
            "klingai:4@3 (KlingAI V2.1 Master)", "klingai:5@1 (KlingAI V2.1 Standard (I2V))",
            "klingai:5@2 (KlingAI V2.1 Pro (I2V))", "klingai:5@3 (KlingAI V2.0 Master)",
            "klingai:6@1 (KlingAI 2.5 Turbo Pro)",
            "klingai:7@1 (KlingAI Lip-Sync)",
            "klingai:kling@o1 (Kling VIDEO O1)",
            "klingai:kling-video@2.6-pro (Kling VIDEO 2.6 Pro)",
            "klingai:avatar@2.0-standard (KlingAI Avatar 2.0 Standard)",
            "klingai:avatar@2.0-pro (KlingAI Avatar 2.0 Pro)",
        ],
        "Veo": [
            "google:2@0 (Veo 2.0)", "google:3@0 (Veo 3.0)", "google:3@1 (Veo 3.0 Fast)",
            "google:3@2 (Veo 3.1)", "google:3@3 (Veo 3.1 Fast)",
        ],
        "Bytedance": [
            "bytedance:2@1 (Seedance 1.0 Pro)", "bytedance:1@1 (Seedance 1.0 Lite)",
            "bytedance:5@1 (OmniHuman 1)", "bytedance:5@2 (OmniHuman 1.5)",
            "bytedance:seedance@1.5-pro (Seedance 1.5 Pro)",
        ],
        "MiniMax": [
            "minimax:1@1 (MiniMax 01 Base)", "minimax:2@1 (MiniMax 01 Director)",
            "minimax:2@3 (MiniMax I2V 01 Live)", "minimax:3@1 (MiniMax 02 Hailuo)",
            "minimax:4@1 (MiniMax Hailuo 2.3)", "minimax:4@2 (MiniMax Hailuo 2.3 Fast)",
        ],
        "PixVerse": [
            "pixverse:1@1 (PixVerse v3.5)", "pixverse:1@2 (PixVerse v4)",
            "pixverse:1@3 (PixVerse v4.5)", "pixverse:1@5-fast (PixVerse v5 Fast)", "pixverse:1@6 (PixVerse v5.5)", "pixverse:1@7 (PixVerse v5.6)", "pixverse:lipsync@1 (PixVerse LipSync)",
        ],
        "Vidu": [
            "vidu:1@0 (Vidu Q1 Classic)", "vidu:1@1 (Vidu Q1)",
            "vidu:1@5 (Vidu 1.5)", "vidu:2@0 (Vidu 2.0)",
            "vidu:4@1 (Vidu Q3)",
            "vidu:4@2 (Vidu Q3 Turbo)",
        ],
        "Wan": [
            "runware:200@1 (Wan 2.1 1.3B)", "runware:200@2 (Wan 2.1 14B)",
            "runware:200@6 (Wan 2.2)",
            "runware:200@8 (Wan 2.2 A14B Animate)",
            "alibaba:wan@2.6 (Wan 2.6)",
            "alibaba:wan@2.6-flash (Wan 2.6 Flash)",
        ],
        "OpenAI": [
            "openai:3@1 (OpenAI Sora 3.1)", "openai:3@0 (OpenAI Sora 3.0)",
        ],
        "Lightricks": [
            "lightricks:2@0 (LTX Fast)", "lightricks:2@1 (LTX Pro)",
            "lightricks:3@1 (LTX-2 Retake)", "lightricks:ltx@2 (LTX-2)",
        ],
        "Ovi": [
            "runware:190@1 (Ovi)",
        ],
        "Runway": [
            "runway:2@1 (Runway Aleph)",
            "runway:1@1 (Runway Gen-4 Turbo)",
            "runway:1@2 (Runway Gen-4.5)",
        ],
        "Luma": [
            "lumaai:1@1 (Luma Ray 1.6)",
            "lumaai:2@1 (Luma Ray 2)",
            "lumaai:2@2 (Luma Ray 2 Flash)",
        ],
        "Sync": [
            "sync:lipsync-2@1 (Sync LipSync 2)",
            "sync:lipsync-2-pro@1 (Sync LipSync 2 Pro)",
            "sync:react-1@1 (Sync React-1)",
        ],
        "Bria": [
            "bria:60@1 (Bria Video Eraser)",
        ],
        "Creatify": [
            "creatify:aurora@fast (Creatify Aurora Avatar Model API (720p))",
            "creatify:aurora@0 (Creatify Aurora Avatar Model API (720p))",
        ],
        "Hunyuan": [
            "runware:hunyuanvideo@1.5 (HunyuanVideo-1.5)",
        ],
        "xAI": [
            "xai:grok-imagine@video (Grok Imagine Video)",
        ],
        "VEED": [
            "veed:fabric@1.0 (VEED Fabric 1.0)",
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
        "klingai:6@1": {"width": 1920, "height": 1080},
        "klingai:7@1": {"width": 0, "height": 0},
        "klingai:kling@o1": {"width": 1440, "height": 1440},
        "klingai:kling-video@2.6-pro": {"width": 1920, "height": 1080},
        "klingai:avatar@2.0-standard": {"width": 0, "height": 0},
        "klingai:avatar@2.0-pro": {"width": 0, "height": 0},
        "google:2@0": {"width": 1280, "height": 720},
        "google:3@0": {"width": 1280, "height": 720},
        "google:3@1": {"width": 1280, "height": 720},
        "google:3@2": {"width": 1280, "height": 720},
        "google:3@3": {"width": 1280, "height": 720},
        "bytedance:2@1": {"width": 864, "height": 480},
        "bytedance:1@1": {"width": 864, "height": 480},
        "bytedance:5@1": {"width": 1024, "height": 1024},
        "bytedance:5@2": {"width": 1024, "height": 1024},
        "bytedance:seedance@1.5-pro": {"width": 864, "height": 496},
        "minimax:1@1": {"width": 1366, "height": 768},
        "minimax:2@1": {"width": 1366, "height": 768},
        "minimax:2@3": {"width": 1366, "height": 768},
        "minimax:3@1": {"width": 1366, "height": 768},
        "minimax:4@1": {"width": 1366, "height": 768},
        "minimax:4@2": {"width": 1366, "height": 768},
        "pixverse:1@1": {"width": 640, "height": 360},
        "pixverse:1@2": {"width": 640, "height": 360},
        "pixverse:1@3": {"width": 640, "height": 360},
        "pixverse:1@6": {"width": 640, "height": 360},
        "pixverse:1@7": {"width": 640, "height": 360},
        "pixverse:lipsync@1": {"width": 640, "height": 360},
        "vidu:1@0": {"width": 1920, "height": 1080},
        "vidu:1@1": {"width": 1920, "height": 1080},
        "vidu:1@5": {"width": 1920, "height": 1080},
        "vidu:2@0": {"width": 1920, "height": 1080},
        "vidu:4@1": {"width": 1920, "height": 1080},
        "vidu:4@2": {"width": 1920, "height": 1080},
        "runware:200@1": {"width": 853, "height": 480},
        "runware:200@2": {"width": 853, "height": 480},
        "runware:200@6": {"width": 1280, "height": 720},
        "runware:200@8": {"width": 1104, "height": 832},
        "alibaba:wan@2.6": {"width": 1280, "height": 720},
        "alibaba:wan@2.6-flash": {"width": 1280, "height": 720},
        "openai:3@1": {"width": 1280, "height": 720},
        "openai:3@0": {"width": 1280, "height": 720},
        "lightricks:2@0": {"width": 1920, "height": 1080},
        "lightricks:2@1": {"width": 1920, "height": 1080},
        "lightricks:3@1": {"width": 0, "height": 0},
        "runware:190@1": {"width": 0, "height": 0},
        "runway:2@1": {"width": 1280, "height": 720},
        "runway:1@1": {"width": 1280, "height": 720},
        "runway:1@2": {"width": 1280, "height": 720},
        "lumaai:1@1": {"width": 1080, "height": 720},
        "lumaai:2@1": {"width": 1080, "height": 720},
        "lumaai:2@2": {"width": 1080, "height": 720},
        "sync:lipsync-2@1": {"width": 0, "height": 0},
        "sync:lipsync-2-pro@1": {"width": 0, "height": 0},
        "sync:react-1@1": {"width": 0, "height": 0},
        "bria:60@1": {"width": 1280, "height": 720},
        "creatify:aurora@fast": {"width": 1280, "height": 720},
        "creatify:aurora@0": {"width": 1280, "height": 720},
        "runware:hunyuanvideo@1.5": {"width": 848, "height": 480},
        "xai:grok-imagine@video": {"width": 480, "height": 480},
        "veed:fabric@1.0": {"width": 1280, "height": 720},
    };

    const MODEL_RESOLUTIONS = {
        "klingai:1@2": "720p",
        "klingai:1@1": "720p",
        "klingai:2@2": "1080p",
        "klingai:2@1": "720p",
        "klingai:3@1": "720p",
        "klingai:3@2": "1080p",
        "klingai:4@3": "720p",
        "klingai:5@1": "720p",
        "klingai:5@2": "1080p",
        "klingai:5@3": "1080p",
        "klingai:6@1": "1080p",
        "klingai:7@1": null,  // No resolution support
        "klingai:kling@o1": null,  // No standard resolution
        "klingai:kling-video@2.6-pro": "1080p",
        "klingai:avatar@2.0-standard": null,  // No resolution support
        "klingai:avatar@2.0-pro": null,  // No resolution support
        "google:2@0": "720p",
        "google:3@0": "720p",
        "google:3@1": "720p",
        "google:3@2": "720p",
        "google:3@3": "720p",
        "bytedance:2@1": "480p",
        "bytedance:1@1": "480p",
        "bytedance:5@1": null,  // No resolution support
        "bytedance:5@2": null,  // No resolution support
        "bytedance:seedance@1.5-pro": "480p",
        "minimax:1@1": "768p",
        "minimax:2@1": "768p",
        "minimax:2@3": "768p",
        "minimax:3@1": "768p",
        "minimax:4@1": "768p",
        "minimax:4@2": "768p",
        "pixverse:1@1": "360p",
        "pixverse:1@2": "360p",
        "pixverse:1@3": "360p",
        "pixverse:1@6": "360p",
        "pixverse:1@7": "360p",
        "pixverse:lipsync@1": "360p",
        "vidu:1@0": "1080p",
        "vidu:1@1": "1080p",
        "vidu:1@5": "1080p",
        "vidu:2@0": "1080p",
        "vidu:4@1": "1080p",
        "vidu:4@2": "1080p",
        "runware:200@1": "480p",
        "runware:200@2": "480p",
        "runware:200@6": "720p",
        "runware:200@8": "720p",
        "alibaba:wan@2.6": "720p",
        "alibaba:wan@2.6-flash": "720p",
        "openai:3@1": "720p",
        "openai:3@0": "720p",
        "lightricks:2@0": "1080p",
        "lightricks:2@1": "1080p",
        "lightricks:3@1": null,  // No resolution support
        "runware:190@1": null,  // No resolution support
        "runway:2@1": "720p",
        "runway:1@1": "720p",
        "runway:1@2": "720p",
        "lumaai:1@1": "720p",
        "lumaai:2@1": "720p",
        "lumaai:2@2": "720p",
        "sync:lipsync-2@1": "720p",
        "sync:lipsync-2-pro@1": "720p",
        "sync:react-1@1": "720p",
        "bria:60@1": "720p",
        "creatify:aurora@fast": "720p",
        "creatify:aurora@0": "720p",
        "runware:hunyuanvideo@1.5": "480p",
        "xai:grok-imagine@video": "480p",
        "veed:fabric@1.0": "720p",
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

        const useCustomDimensionsValue = useCustomDimensionsWidget ? useCustomDimensionsWidget.value : "Model Default";
        
        // Handle "Disabled" option - disable widgets and set to 0 (but Python will use None in dict)
        if (useCustomDimensionsValue === "Disabled") {
            setWidthHeightEnabled(false);
            if (widthWidget.callback) widthWidget.callback(0, "customSetOperation");
            widthWidget.value = 0;
            if (heightWidget.callback) heightWidget.callback(0, "customSetOperation");
            heightWidget.value = 0;
            videoModelSearchNode.setDirtyCanvas(true);
            return;
        }

        // Handle "Model Default" option - disable widgets and use model defaults
        if (useCustomDimensionsValue === "Model Default") {
            setWidthHeightEnabled(false);
        } else if (useCustomDimensionsValue === "Custom") {
            // Handle "Custom" option - enable widgets
        setWidthHeightEnabled(true);
        }

        const modelCode = selectedModel.split(" (")[0];
        const dims = MODEL_DIMENSIONS[modelCode] || DEFAULT_DIMENSIONS;

        // Only update dimensions if "Model Default" is selected (widgets are disabled but we show the values)
        if (useCustomDimensionsValue === "Model Default") {
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
        // For "Custom" mode, don't update - let user set their own values
        // For "Disabled" mode, already handled above (set to None and disabled)
        
        // Update resolution based on selected model
        if (resolutionWidget && useResolutionWidget) {
            const modelCode = selectedModel.split(" (")[0];
            const modelResolution = MODEL_RESOLUTIONS[modelCode];
            
            // If model supports resolution
            if (modelResolution !== null && modelResolution !== undefined) {
                // Enable useResolution checkbox
                if (useResolutionWidget.inputEl) {
                    useResolutionWidget.inputEl.disabled = false;
                    useResolutionWidget.inputEl.style.opacity = "1";
                }
                useResolutionWidget.disabled = false;
                
                // Only update resolution value if useResolution is enabled
                if (useResolutionWidget.value === true) {
                    // Set resolution value to model's default
                    if (resolutionWidget.callback) resolutionWidget.callback(modelResolution, "customSetOperation");
                    resolutionWidget.value = modelResolution;
                }
            } else {
                // Model doesn't support resolution, disable useResolution checkbox and resolution dropdown
                if (useResolutionWidget.callback) useResolutionWidget.callback(false, "customSetOperation");
                useResolutionWidget.value = false;
                
                // Disable useResolution checkbox
                if (useResolutionWidget.inputEl) {
                    useResolutionWidget.inputEl.disabled = true;
                    useResolutionWidget.inputEl.style.opacity = "0.5";
                }
                useResolutionWidget.disabled = true;
                
                // Disable resolution dropdown
                if (resolutionWidget.inputEl) {
                    resolutionWidget.inputEl.disabled = true;
                    resolutionWidget.inputEl.style.opacity = "0.5";
                    resolutionWidget.inputEl.style.cursor = "not-allowed";
                }
                resolutionWidget.disabled = true;
            }
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
    if (useCustomDimensionsWidget) {
        appendWidgetCB(useCustomDimensionsWidget, () => {
            updateDimensions();
        });
    }
    
    // Handle useResolution toggle
    if (useResolutionWidget && resolutionWidget) {
        function toggleResolutionState() {
            // Check if current model supports resolution
            const selectedModel = videoListWidget ? videoListWidget.value : null;
            if (!selectedModel) return;
            
            const modelCode = selectedModel.split(" (")[0];
            const modelResolution = MODEL_RESOLUTIONS[modelCode];
            
            // Only enable resolution if model supports it and useResolution is enabled
            const enabled = useResolutionWidget.value === true && modelResolution !== null && modelResolution !== undefined;
            
            if (resolutionWidget.inputEl) {
                resolutionWidget.inputEl.disabled = !enabled;
                resolutionWidget.inputEl.style.opacity = enabled ? "1" : "0.5";
                resolutionWidget.inputEl.style.cursor = enabled ? "text" : "not-allowed";
            }
            
            resolutionWidget.disabled = !enabled;
            
            // Fallback: try to find input via DOM if inputEl is not available
            if (!resolutionWidget.inputEl) {
                const nodeElement = videoModelSearchNode.htmlElements?.widgetsContainer || videoModelSearchNode.htmlElements;
                if (nodeElement) {
                    const input = nodeElement.querySelector(`select[name="resolution"]`);
                    if (input) {
                        input.disabled = !enabled;
                        input.style.opacity = enabled ? "1" : "0.5";
                        input.style.pointerEvents = enabled ? "auto" : "none";
                    }
                }
            }
            
            videoModelSearchNode.setDirtyCanvas(true);
        }
        
        appendWidgetCB(useResolutionWidget, () => {
            setTimeout(toggleResolutionState, 50);
        });
        
        // Also update when model changes
        if (videoListWidget) {
            appendWidgetCB(videoListWidget, () => {
                setTimeout(toggleResolutionState, 50);
            });
        }
        
        setTimeout(toggleResolutionState, 100);
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
        "Mirelo": [
            "mirelo:1@1 (Mirelo SFX 1.5)",
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
    const useKeepOriginalSoundWidget = klingNode.widgets.find(w => w.name === "useKeepOriginalSound");
    const keepOriginalSoundWidget = klingNode.widgets.find(w => w.name === "keepOriginalSound");
    const useSoundWidget = klingNode.widgets.find(w => w.name === "useSound");
    const soundWidget = klingNode.widgets.find(w => w.name === "sound");
    const useCharacterOrientationWidget = klingNode.widgets.find(w => w.name === "useCharacterOrientation");
    const characterOrientationWidget = klingNode.widgets.find(w => w.name === "characterOrientation");
    
    // Helper function to toggle widget enabled state (EXACT same pattern as imageInferenceToggleHandler)
    // Callers guard with if (useX && xWidget) before invoking
    function toggleWidgetState(useWidget, paramWidget, paramName) {
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
    
    if (useKeepOriginalSoundWidget && keepOriginalSoundWidget) {
        toggleWidgetState(useKeepOriginalSoundWidget, keepOriginalSoundWidget, "keepOriginalSound");
    }
    
    if (useSoundWidget && soundWidget) {
        toggleWidgetState(useSoundWidget, soundWidget, "sound");
    }
    
    if (useCharacterOrientationWidget && characterOrientationWidget) {
        toggleWidgetState(useCharacterOrientationWidget, characterOrientationWidget, "characterOrientation");
    }
}

function alibabaProviderSettingsToggleHandler(alibabaNode) {
    // Find all "use" parameter widgets for Alibaba Provider Settings
    const usePromptEnhancerWidget = alibabaNode.widgets.find(w => w.name === "usePromptEnhancer");
    const promptEnhancerWidget = alibabaNode.widgets.find(w => w.name === "promptEnhancer");
    const usePromptExtendWidget = alibabaNode.widgets.find(w => w.name === "usePromptExtend");
    const promptExtendWidget = alibabaNode.widgets.find(w => w.name === "promptExtend");
    const useAudioWidget = alibabaNode.widgets.find(w => w.name === "useAudio");
    const audioWidget = alibabaNode.widgets.find(w => w.name === "audio");
    const useShotTypeWidget = alibabaNode.widgets.find(w => w.name === "useShotType");
    const shotTypeWidget = alibabaNode.widgets.find(w => w.name === "shotType");
    
    // Helper function to toggle widget enabled state
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
                const nodeElement = alibabaNode.htmlElements?.widgetsContainer || alibabaNode.htmlElements;
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
            
            alibabaNode.setDirtyCanvas(true);
        }
        
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        setTimeout(toggleEnabled, 100);
    }
    
    // Special handler for shotType - depends on both usePromptExtend AND promptExtend being true
    function toggleShotTypeEnabled() {
        if (!useShotTypeWidget || !shotTypeWidget || !usePromptExtendWidget || !promptExtendWidget) return;
        
        const usePromptExtendEnabled = usePromptExtendWidget.value === true;
        const promptExtendValue = promptExtendWidget.value === true;
        const useShotTypeEnabled = useShotTypeWidget.value === true;
        
        // shotType is enabled only if: useShotType is enabled AND usePromptExtend is enabled AND promptExtend is true
        const enabled = useShotTypeEnabled && usePromptExtendEnabled && promptExtendValue;
        
        if (shotTypeWidget.inputEl) {
            shotTypeWidget.inputEl.disabled = !enabled;
            shotTypeWidget.inputEl.style.opacity = enabled ? "1" : "0.5";
            shotTypeWidget.inputEl.style.cursor = enabled ? "text" : "not-allowed";
            shotTypeWidget.inputEl.readOnly = !enabled;
        }
        
        shotTypeWidget.disabled = !enabled;
        
        if (!shotTypeWidget.inputEl) {
            const nodeElement = alibabaNode.htmlElements?.widgetsContainer || alibabaNode.htmlElements;
            if (nodeElement) {
                const input = nodeElement.querySelector(`input[name="shotType"], select[name="shotType"]`);
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
        
        alibabaNode.setDirtyCanvas(true);
    }
    
    // Set up toggle handlers
    if (usePromptEnhancerWidget && promptEnhancerWidget) {
        toggleWidgetState(usePromptEnhancerWidget, promptEnhancerWidget, "promptEnhancer");
    }
    
    if (usePromptExtendWidget && promptExtendWidget) {
        toggleWidgetState(usePromptExtendWidget, promptExtendWidget, "promptExtend");
        
        // Also listen to promptExtend value changes to update shotType
        appendWidgetCB(promptExtendWidget, () => {
            setTimeout(toggleShotTypeEnabled, 50);
        });
    }
    
    if (useAudioWidget && audioWidget) {
        toggleWidgetState(useAudioWidget, audioWidget, "audio");
    }
    
    if (useShotTypeWidget && shotTypeWidget) {
        // Listen to useShotType changes
        appendWidgetCB(useShotTypeWidget, () => {
            setTimeout(toggleShotTypeEnabled, 50);
        });
        
        // Also listen to usePromptExtend changes
        if (usePromptExtendWidget) {
            appendWidgetCB(usePromptExtendWidget, () => {
                setTimeout(toggleShotTypeEnabled, 50);
            });
        }
        
        // Initial state
        setTimeout(toggleShotTypeEnabled, 100);
    }
}

function mireloProviderSettingsToggleHandler(mireloNode) {
    // Find all "use" parameter widgets for Mirelo Provider Settings
    const useStartOffsetWidget = mireloNode.widgets.find(w => w.name === "useStartOffset");
    const startOffsetWidget = mireloNode.widgets.find(w => w.name === "startOffset");
    
    // Helper function to toggle widget enabled state
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
                const nodeElement = mireloNode.htmlElements?.widgetsContainer || mireloNode.htmlElements;
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
            
            mireloNode.setDirtyCanvas(true);
        }
        
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        setTimeout(toggleEnabled, 100);
    }
    
    // Set up toggle handler
    if (useStartOffsetWidget && startOffsetWidget) {
        toggleWidgetState(useStartOffsetWidget, startOffsetWidget, "startOffset");
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

function briaProviderSettingsToggleHandler(briaNode) {
    // Find all "use" parameter widgets for Bria Provider Settings
    const useMediumWidget = briaNode.widgets.find(w => w.name === "useMedium");
    const mediumWidget = briaNode.widgets.find(w => w.name === "medium");
    const usePromptEnhancementWidget = briaNode.widgets.find(w => w.name === "usePromptEnhancement");
    const promptEnhancementWidget = briaNode.widgets.find(w => w.name === "promptEnhancement");
    const useEnhanceImageWidget = briaNode.widgets.find(w => w.name === "useEnhanceImage");
    const enhanceImageWidget = briaNode.widgets.find(w => w.name === "enhanceImage");
    const usePromptContentModerationWidget = briaNode.widgets.find(w => w.name === "usePromptContentModeration");
    const promptContentModerationWidget = briaNode.widgets.find(w => w.name === "promptContentModeration");
    const useContentModerationWidget = briaNode.widgets.find(w => w.name === "useContentModeration");
    const contentModerationWidget = briaNode.widgets.find(w => w.name === "contentModeration");
    const useIpSignalWidget = briaNode.widgets.find(w => w.name === "useIpSignal");
    const ipSignalWidget = briaNode.widgets.find(w => w.name === "ipSignal");
    const usePreserveAlphaWidget = briaNode.widgets.find(w => w.name === "usePreserveAlpha");
    const preserveAlphaWidget = briaNode.widgets.find(w => w.name === "preserveAlpha");
    const useModeWidget = briaNode.widgets.find(w => w.name === "useMode");
    const modeWidget = briaNode.widgets.find(w => w.name === "mode");
    const useEnhanceReferenceImagesWidget = briaNode.widgets.find(w => w.name === "useEnhanceReferenceImages");
    const enhanceReferenceImagesWidget = briaNode.widgets.find(w => w.name === "enhanceReferenceImages");
    const useRefinePromptWidget = briaNode.widgets.find(w => w.name === "useRefinePrompt");
    const refinePromptWidget = briaNode.widgets.find(w => w.name === "refinePrompt");
    const useOriginalQualityWidget = briaNode.widgets.find(w => w.name === "useOriginalQuality");
    const originalQualityWidget = briaNode.widgets.find(w => w.name === "originalQuality");
    const useForceBackgroundDetectionWidget = briaNode.widgets.find(w => w.name === "useForceBackgroundDetection");
    const forceBackgroundDetectionWidget = briaNode.widgets.find(w => w.name === "forceBackgroundDetection");
    const useAutoTrimWidget = briaNode.widgets.find(w => w.name === "useAutoTrim");
    const autoTrimWidget = briaNode.widgets.find(w => w.name === "autoTrim");
    const usePreserveAudioWidget = briaNode.widgets.find(w => w.name === "usePreserveAudio");
    const preserveAudioWidget = briaNode.widgets.find(w => w.name === "preserveAudio");
    
    // Helper function to toggle widget enabled state (exact same pattern)
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
            
            // Handle dropdown widgets (for medium and mode)
            if (paramWidget.options && paramWidget.options.element) {
                paramWidget.options.element.disabled = !enabled;
                paramWidget.options.element.style.opacity = enabled ? "1" : "0.5";
                paramWidget.options.element.style.pointerEvents = enabled ? "auto" : "none";
            }
            
            // Also set widget property
            paramWidget.disabled = !enabled;
            
            // Fallback: try to find inputs via DOM if inputEl is not available
            if (!paramWidget.inputEl) {
                const nodeElement = briaNode.htmlElements?.widgetsContainer || briaNode.htmlElements;
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
            
            briaNode.setDirtyCanvas(true);
        }
        
        // Set up callback (exact same pattern)
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        // Initial call to set initial state
        setTimeout(toggleEnabled, 100);
    }
    
    // Set up all toggle handlers
    if (useMediumWidget && mediumWidget) {
        toggleWidgetState(useMediumWidget, mediumWidget, "medium");
    }
    
    if (usePromptEnhancementWidget && promptEnhancementWidget) {
        toggleWidgetState(usePromptEnhancementWidget, promptEnhancementWidget, "promptEnhancement");
    }
    
    if (useEnhanceImageWidget && enhanceImageWidget) {
        toggleWidgetState(useEnhanceImageWidget, enhanceImageWidget, "enhanceImage");
    }
    
    if (usePromptContentModerationWidget && promptContentModerationWidget) {
        toggleWidgetState(usePromptContentModerationWidget, promptContentModerationWidget, "promptContentModeration");
    }
    
    if (useContentModerationWidget && contentModerationWidget) {
        toggleWidgetState(useContentModerationWidget, contentModerationWidget, "contentModeration");
    }
    
    if (useIpSignalWidget && ipSignalWidget) {
        toggleWidgetState(useIpSignalWidget, ipSignalWidget, "ipSignal");
    }
    
    if (usePreserveAlphaWidget && preserveAlphaWidget) {
        toggleWidgetState(usePreserveAlphaWidget, preserveAlphaWidget, "preserveAlpha");
    }
    
    if (useModeWidget && modeWidget) {
        toggleWidgetState(useModeWidget, modeWidget, "mode");
    }
    
    if (useEnhanceReferenceImagesWidget && enhanceReferenceImagesWidget) {
        toggleWidgetState(useEnhanceReferenceImagesWidget, enhanceReferenceImagesWidget, "enhanceReferenceImages");
    }
    
    if (useRefinePromptWidget && refinePromptWidget) {
        toggleWidgetState(useRefinePromptWidget, refinePromptWidget, "refinePrompt");
    }
    
    if (useOriginalQualityWidget && originalQualityWidget) {
        toggleWidgetState(useOriginalQualityWidget, originalQualityWidget, "originalQuality");
    }
    
    if (useForceBackgroundDetectionWidget && forceBackgroundDetectionWidget) {
        toggleWidgetState(useForceBackgroundDetectionWidget, forceBackgroundDetectionWidget, "forceBackgroundDetection");
    }
    
    if (useAutoTrimWidget && autoTrimWidget) {
        toggleWidgetState(useAutoTrimWidget, autoTrimWidget, "autoTrim");
    }
    
    if (usePreserveAudioWidget && preserveAudioWidget) {
        toggleWidgetState(usePreserveAudioWidget, preserveAudioWidget, "preserveAudio");
    }
}

function audioInputToggleHandler(audioInputNode) {
    // Find "use" parameter widget and "id" widget for Audio Input
    const useIdWidget = audioInputNode.widgets.find(w => w.name === "useId");
    const idWidget = audioInputNode.widgets.find(w => w.name === "id");
    
    // Helper function to toggle widget enabled state
    function toggleWidgetState(useWidget, paramWidget, paramName) {
        if (!useWidget || !paramWidget) return;
        
        function toggleEnabled() {
            const enabled = useWidget.value === true;
            
            // Disable/enable widgets using inputEl if available
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
                const nodeElement = audioInputNode.htmlElements?.widgetsContainer || audioInputNode.htmlElements;
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
            
            audioInputNode.setDirtyCanvas(true);
        }
        
        // Set up callback
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        // Initial call to set initial state
        setTimeout(toggleEnabled, 100);
    }
    
    // Set up toggle handler for "useId" parameter
    if (useIdWidget && idWidget) {
        toggleWidgetState(useIdWidget, idWidget, "id");
    }
}

function speechInputToggleHandler(speechInputNode) {
    // Find "use" parameter widget and "id" widget for Speech Input
    const useIdWidget = speechInputNode.widgets.find(w => w.name === "useId");
    const idWidget = speechInputNode.widgets.find(w => w.name === "id");
    
    // Helper function to toggle widget enabled state
    function toggleWidgetState(useWidget, paramWidget, paramName) {
        if (!useWidget || !paramWidget) return;
        
        function toggleEnabled() {
            const enabled = useWidget.value === true;
            
            // Disable/enable widgets using inputEl if available
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
                const nodeElement = speechInputNode.htmlElements?.widgetsContainer || speechInputNode.htmlElements;
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
            
            speechInputNode.setDirtyCanvas(true);
        }
        
        // Set up callback
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        // Initial call to set initial state
        setTimeout(toggleEnabled, 100);
    }
    
    // Set up toggle handler for "useId" parameter
    if (useIdWidget && idWidget) {
        toggleWidgetState(useIdWidget, idWidget, "id");
    }
}

function briaProviderMaskToggleHandler(maskNode) {
    // Helper function to toggle widget enabled state for multiple widgets
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
                
                // Handle dropdown widgets (for Type fields)
                if (paramWidget.options && paramWidget.options.element) {
                    paramWidget.options.element.disabled = !enabled;
                    paramWidget.options.element.style.opacity = enabled ? "1" : "0.5";
                    paramWidget.options.element.style.pointerEvents = enabled ? "auto" : "none";
                }
                
                paramWidget.disabled = !enabled;
                
                // Fallback: try to find inputs via DOM if inputEl is not available
                if (!paramWidget.inputEl && paramNames[idx]) {
                    const nodeElement = maskNode.htmlElements?.widgetsContainer || maskNode.htmlElements;
                    if (nodeElement) {
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
            
            maskNode.setDirtyCanvas(true);
        }
        
        // Set up callback
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        // Initial call to set initial state
        setTimeout(toggleEnabled, 100);
    }
    
    // Set up toggle handlers for foreground, prompt, frameIndex
    const useForegroundWidget = maskNode.widgets.find(w => w.name === "useForeground");
    const foregroundWidget = maskNode.widgets.find(w => w.name === "foreground");
    if (useForegroundWidget && foregroundWidget) {
        toggleWidgetState(useForegroundWidget, [foregroundWidget], ["foreground"]);
    }
    
    const usePromptWidget = maskNode.widgets.find(w => w.name === "usePrompt");
    const promptWidget = maskNode.widgets.find(w => w.name === "prompt");
    if (usePromptWidget && promptWidget) {
        toggleWidgetState(usePromptWidget, [promptWidget], ["prompt"]);
    }
    
    const useFrameIndexWidget = maskNode.widgets.find(w => w.name === "useFrameIndex");
    const frameIndexWidget = maskNode.widgets.find(w => w.name === "frameIndex");
    if (useFrameIndexWidget && frameIndexWidget) {
        toggleWidgetState(useFrameIndexWidget, [frameIndexWidget], ["frameIndex"]);
    }
    
    // Set up toggle handlers for all 6 key points
    for (let i = 1; i <= 6; i++) {
        const useWidget = maskNode.widgets.find(w => w.name === `use_${i}`);
        const xWidget = maskNode.widgets.find(w => w.name === `X${i}`);
        const yWidget = maskNode.widgets.find(w => w.name === `Y${i}`);
        const typeWidget = maskNode.widgets.find(w => w.name === `Type${i}`);
        
        if (useWidget && xWidget && yWidget && typeWidget) {
            toggleWidgetState(useWidget, [xWidget, yWidget, typeWidget], [`X${i}`, `Y${i}`, `Type${i}`]);
        }
    }
}

function wanAnimateAdvancedFeatureSettingsToggleHandler(wanAnimateNode) {
    // Find widgets
    const useModeWidget = wanAnimateNode.widgets.find(w => w.name === "useMode");
    const modeWidget = wanAnimateNode.widgets.find(w => w.name === "mode");
    const useRetargetPoseWidget = wanAnimateNode.widgets.find(w => w.name === "useRetargetPose");
    const retargetPoseWidget = wanAnimateNode.widgets.find(w => w.name === "retargetPose");
    const usePrevSegCondFramesWidget = wanAnimateNode.widgets.find(w => w.name === "usePrevSegCondFrames");
    const prevSegCondFramesWidget = wanAnimateNode.widgets.find(w => w.name === "prevSegCondFrames");
    
    // Helper function to toggle widget enabled state
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
            
            // Handle dropdown widgets (for mode field)
            if (paramWidget.options && paramWidget.options.element) {
                paramWidget.options.element.disabled = !enabled;
                paramWidget.options.element.style.opacity = enabled ? "1" : "0.5";
                paramWidget.options.element.style.pointerEvents = enabled ? "auto" : "none";
            }
            
            paramWidget.disabled = !enabled;
            
            // Fallback: try to find inputs via DOM if inputEl is not available
            if (!paramWidget.inputEl && paramName) {
                const nodeElement = wanAnimateNode.htmlElements?.widgetsContainer || wanAnimateNode.htmlElements;
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
            
            wanAnimateNode.setDirtyCanvas(true);
        }
        
        // Set up callback
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        // Initial call to set initial state
        setTimeout(toggleEnabled, 100);
    }
    
    // Set up toggle handler for mode
    if (useModeWidget && modeWidget) {
        toggleWidgetState(useModeWidget, modeWidget, "mode");
    }
    
    // Set up toggle handler for retargetPose (with mode dependency)
    if (useRetargetPoseWidget && retargetPoseWidget) {
        function toggleRetargetPoseEnabled() {
            const useRetargetPoseEnabled = useRetargetPoseWidget.value === true;
            const modeValue = modeWidget ? modeWidget.value : "animate";
            // retargetPose is only supported for animate mode
            const enabled = useRetargetPoseEnabled && modeValue === "animate";
            
            if (retargetPoseWidget.inputEl) {
                retargetPoseWidget.inputEl.disabled = !enabled;
                retargetPoseWidget.inputEl.style.opacity = enabled ? "1" : "0.5";
                retargetPoseWidget.inputEl.style.cursor = enabled ? "text" : "not-allowed";
                retargetPoseWidget.inputEl.readOnly = !enabled;
            }
            
            retargetPoseWidget.disabled = !enabled;
            
            // Fallback: try to find inputs via DOM
            if (!retargetPoseWidget.inputEl) {
                const nodeElement = wanAnimateNode.htmlElements?.widgetsContainer || wanAnimateNode.htmlElements;
                if (nodeElement) {
                    const input = nodeElement.querySelector(`input[name="retargetPose"], textarea[name="retargetPose"], select[name="retargetPose"]`);
                    if (input) {
                        input.disabled = !enabled;
                        input.style.opacity = enabled ? "1" : "0.5";
                        input.style.cursor = enabled ? "text" : "not-allowed";
                        input.readOnly = !enabled;
                    }
                }
            }
            
            wanAnimateNode.setDirtyCanvas(true);
        }
        
        // Set up callback for useRetargetPose toggle
        appendWidgetCB(useRetargetPoseWidget, () => {
            setTimeout(toggleRetargetPoseEnabled, 50);
        });
        
        // Set up callback for mode change (to disable retargetPose when mode is "replace")
        if (modeWidget) {
            appendWidgetCB(modeWidget, () => {
                setTimeout(toggleRetargetPoseEnabled, 50);
            });
        }
        
        // Initial call to set initial state
        setTimeout(toggleRetargetPoseEnabled, 100);
    }
    
    // Set up toggle handler for prevSegCondFrames
    if (usePrevSegCondFramesWidget && prevSegCondFramesWidget) {
        toggleWidgetState(usePrevSegCondFramesWidget, prevSegCondFramesWidget, "prevSegCondFrames");
    }
}

function videoAdvancedFeatureInputsToggleHandler(advancedFeatureNode) {
    // Helper function to toggle widget enabled state
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
            
            // Fallback: try to find inputs via DOM if inputEl is not available
            if (!paramWidget.inputEl && paramName) {
                const nodeElement = advancedFeatureNode.htmlElements?.widgetsContainer || advancedFeatureNode.htmlElements;
                if (nodeElement) {
                    const input = nodeElement.querySelector(`input[name="${paramName}"], textarea[name="${paramName}"], select[name="${paramName}"]`);
                    if (input) {
                        input.disabled = !enabled;
                        input.style.opacity = enabled ? "1" : "0.5";
                        input.style.cursor = enabled ? "text" : "not-allowed";
                        input.readOnly = !enabled;
                    }
                }
            }
            
            advancedFeatureNode.setDirtyCanvas(true);
        }
        
        // Set up callback
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        // Initial call to set initial state
        setTimeout(toggleEnabled, 100);
    }
    
    // Set up toggle handlers for each parameter
    const useVideoCFGScaleWidget = advancedFeatureNode.widgets.find(w => w.name === "useVideoCFGScale");
    const videoCFGScaleWidget = advancedFeatureNode.widgets.find(w => w.name === "videoCFGScale");
    if (useVideoCFGScaleWidget && videoCFGScaleWidget) {
        toggleWidgetState(useVideoCFGScaleWidget, videoCFGScaleWidget, "videoCFGScale");
    }
    
    const useAudioCFGScaleWidget = advancedFeatureNode.widgets.find(w => w.name === "useAudioCFGScale");
    const audioCFGScaleWidget = advancedFeatureNode.widgets.find(w => w.name === "audioCFGScale");
    if (useAudioCFGScaleWidget && audioCFGScaleWidget) {
        toggleWidgetState(useAudioCFGScaleWidget, audioCFGScaleWidget, "audioCFGScale");
    }
    
    const useVideoNegativePromptWidget = advancedFeatureNode.widgets.find(w => w.name === "useVideoNegativePrompt");
    const videoNegativePromptWidget = advancedFeatureNode.widgets.find(w => w.name === "videoNegativePrompt");
    if (useVideoNegativePromptWidget && videoNegativePromptWidget) {
        toggleWidgetState(useVideoNegativePromptWidget, videoNegativePromptWidget, "videoNegativePrompt");
    }
    
    const useAudioNegativePromptWidget = advancedFeatureNode.widgets.find(w => w.name === "useAudioNegativePrompt");
    const audioNegativePromptWidget = advancedFeatureNode.widgets.find(w => w.name === "audioNegativePrompt");
    if (useAudioNegativePromptWidget && audioNegativePromptWidget) {
        toggleWidgetState(useAudioNegativePromptWidget, audioNegativePromptWidget, "audioNegativePrompt");
    }
    
    const useSlgLayerWidget = advancedFeatureNode.widgets.find(w => w.name === "useSlgLayer");
    const slgLayerWidget = advancedFeatureNode.widgets.find(w => w.name === "slgLayer");
    if (useSlgLayerWidget && slgLayerWidget) {
        toggleWidgetState(useSlgLayerWidget, slgLayerWidget, "slgLayer");
    }
}

function audioInferenceInputsToggleHandler(audioInputsNode) {
    // Find widgets
    const useVideoWidget = audioInputsNode.widgets.find(w => w.name === "useVideo");
    const videoWidget = audioInputsNode.widgets.find(w => w.name === "Video");
    const useVideosWidget = audioInputsNode.widgets.find(w => w.name === "useVideos");
    
    // Helper function to toggle widget enabled state
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
            
            // Fallback: try to find inputs via DOM if inputEl is not available
            if (!paramWidget.inputEl && paramName) {
                const nodeElement = audioInputsNode.htmlElements?.widgetsContainer || audioInputsNode.htmlElements;
                if (nodeElement) {
                    const input = nodeElement.querySelector(`input[name="${paramName}"], textarea[name="${paramName}"], select[name="${paramName}"]`);
                    if (input) {
                        input.disabled = !enabled;
                        input.style.opacity = enabled ? "1" : "0.5";
                        input.style.cursor = enabled ? "text" : "not-allowed";
                        input.readOnly = !enabled;
                    }
                }
            }
            
            audioInputsNode.setDirtyCanvas(true);
        }
        
        // Set up callback
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        // Initial call to set initial state
        setTimeout(toggleEnabled, 100);
    }
    
    // Set up toggle handler for single video
    if (useVideoWidget && videoWidget) {
        toggleWidgetState(useVideoWidget, videoWidget, "Video");
    }
    
    // Set up toggle handlers for multiple videos (Video1, Video2, Video3, Video4)
    if (useVideosWidget) {
        function toggleVideosEnabled() {
            const enabled = useVideosWidget.value === true;
            
            for (let i = 1; i <= 4; i++) {
                const videoWidget = audioInputsNode.widgets.find(w => w.name === `Video${i}`);
                if (videoWidget) {
                    if (videoWidget.inputEl) {
                        videoWidget.inputEl.disabled = !enabled;
                        videoWidget.inputEl.style.opacity = enabled ? "1" : "0.5";
                        videoWidget.inputEl.style.cursor = enabled ? "text" : "not-allowed";
                        videoWidget.inputEl.readOnly = !enabled;
                    }
                    
                    videoWidget.disabled = !enabled;
                    
                    // Fallback: try to find inputs via DOM
                    if (!videoWidget.inputEl) {
                        const nodeElement = audioInputsNode.htmlElements?.widgetsContainer || audioInputsNode.htmlElements;
                        if (nodeElement) {
                            const input = nodeElement.querySelector(`input[name="Video${i}"], textarea[name="Video${i}"], select[name="Video${i}"]`);
                            if (input) {
                                input.disabled = !enabled;
                                input.style.opacity = enabled ? "1" : "0.5";
                                input.style.cursor = enabled ? "text" : "not-allowed";
                                input.readOnly = !enabled;
                            }
                        }
                    }
                }
            }
            
            audioInputsNode.setDirtyCanvas(true);
        }
        
        // Set up callback
        appendWidgetCB(useVideosWidget, () => {
            setTimeout(toggleVideosEnabled, 50);
        });
        
        // Initial call to set initial state
        setTimeout(toggleVideosEnabled, 100);
    }
}

export {
    notifyUser,
    promptEnhanceHandler,
    syncDimensionsNodeHandler,
    searchNodeHandler,
    mediaUUIDHandler,
    save3DFilepathHandler,
    captionNodeHandler,
    videoTranscriptionHandler,
    videoOutputsHandler,
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
    xaiProviderSettingsToggleHandler,
    viduProviderSettingsToggleHandler,
    sourcefulProviderSettingsToggleHandler,
    sourcefulProviderSettingsFontsToggleHandler,
    threeDInferenceToggleHandler,
    threeDInferenceSettingsToggleHandler,
    threeDInferenceSettingsLatToggleHandler,
    ultralyticsProviderSettingsToggleHandler,
    openaiProviderSettingsToggleHandler,
    lightricksProviderSettingsToggleHandler,
    klingProviderSettingsToggleHandler,
    lumaProviderSettingsToggleHandler,
    briaProviderSettingsToggleHandler,
    pixverseProviderSettingsToggleHandler,
    alibabaProviderSettingsToggleHandler,
    mireloProviderSettingsToggleHandler,
    googleProviderSettingsToggleHandler,
    syncProviderSettingsToggleHandler,
    syncSegmentToggleHandler,
    settingsToggleHandler,
    audioInputToggleHandler,
    speechInputToggleHandler,
    briaProviderMaskToggleHandler,
    wanAnimateAdvancedFeatureSettingsToggleHandler,
    videoAdvancedFeatureInputsToggleHandler,
    audioInferenceInputsToggleHandler,
};

function googleProviderSettingsToggleHandler(googleNode) {
    // Find all "use" parameter widgets for Google Provider Settings
    const useGenerateAudioWidget = googleNode.widgets.find(w => w.name === "useGenerateAudio");
    const generateAudioWidget = googleNode.widgets.find(w => w.name === "generateAudio");
    const useEnhancePromptWidget = googleNode.widgets.find(w => w.name === "useEnhancePrompt");
    const enhancePromptWidget = googleNode.widgets.find(w => w.name === "enhancePrompt");
    const useSearchWidget = googleNode.widgets.find(w => w.name === "useSearch");
    const searchWidget = googleNode.widgets.find(w => w.name === "search");
    
    // Helper function to toggle widget enabled state
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
                const nodeElement = googleNode.htmlElements?.widgetsContainer || googleNode.htmlElements;
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
            
            googleNode.setDirtyCanvas(true);
        }
        
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        setTimeout(toggleEnabled, 100);
    }
    
    // Set up toggle handlers
    if (useGenerateAudioWidget && generateAudioWidget) {
        toggleWidgetState(useGenerateAudioWidget, generateAudioWidget, "generateAudio");
    }
    if (useEnhancePromptWidget && enhancePromptWidget) {
        toggleWidgetState(useEnhancePromptWidget, enhancePromptWidget, "enhancePrompt");
    }
    if (useSearchWidget && searchWidget) {
        toggleWidgetState(useSearchWidget, searchWidget, "search");
    }
}

function settingsToggleHandler(settingsNode) {
    // Find all "use" parameter widgets for Settings
    const useTemperatureWidget = settingsNode.widgets.find(w => w.name === "useTemperature");
    const temperatureWidget = settingsNode.widgets.find(w => w.name === "temperature");
    const useSystemPromptWidget = settingsNode.widgets.find(w => w.name === "useSystemPrompt");
    const systemPromptWidget = settingsNode.widgets.find(w => w.name === "systemPrompt");
    const useTopPWidget = settingsNode.widgets.find(w => w.name === "useTopP");
    const topPWidget = settingsNode.widgets.find(w => w.name === "topP");
    const useLayersWidget = settingsNode.widgets.find(w => w.name === "useLayers");
    const layersWidget = settingsNode.widgets.find(w => w.name === "layers");
    const useTrueCFGScaleWidget = settingsNode.widgets.find(w => w.name === "useTrueCFGScale");
    const trueCFGScaleWidget = settingsNode.widgets.find(w => w.name === "trueCFGScale");
    const useQualityWidget = settingsNode.widgets.find(w => w.name === "useQuality");
    const qualityWidget = settingsNode.widgets.find(w => w.name === "quality");
    
    // Helper function to toggle widget enabled state
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
                const nodeElement = settingsNode.htmlElements?.widgetsContainer || settingsNode.htmlElements;
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
            
            settingsNode.setDirtyCanvas(true);
        }
        
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        setTimeout(toggleEnabled, 100);
    }
    
    // Set up toggle handlers
    if (useTemperatureWidget && temperatureWidget) {
        toggleWidgetState(useTemperatureWidget, temperatureWidget, "temperature");
    }
    if (useSystemPromptWidget && systemPromptWidget) {
        toggleWidgetState(useSystemPromptWidget, systemPromptWidget, "systemPrompt");
    }
    if (useTopPWidget && topPWidget) {
        toggleWidgetState(useTopPWidget, topPWidget, "topP");
    }
    if (useLayersWidget && layersWidget) {
        toggleWidgetState(useLayersWidget, layersWidget, "layers");
    }
    if (useTrueCFGScaleWidget && trueCFGScaleWidget) {
        toggleWidgetState(useTrueCFGScaleWidget, trueCFGScaleWidget, "trueCFGScale");
    }
    if (useQualityWidget && qualityWidget) {
        toggleWidgetState(useQualityWidget, qualityWidget, "quality");
    }
}

function syncProviderSettingsToggleHandler(syncNode) {
    // Find all "use" parameter widgets for Sync Provider Settings
    const useEditRegionWidget = syncNode.widgets.find(w => w.name === "useEditRegion");
    const editRegionWidget = syncNode.widgets.find(w => w.name === "editRegion");
    const useEmotionPromptWidget = syncNode.widgets.find(w => w.name === "useEmotionPrompt");
    const emotionPromptWidget = syncNode.widgets.find(w => w.name === "emotionPrompt");
    const useTemperatureWidget = syncNode.widgets.find(w => w.name === "useTemperature");
    const temperatureWidget = syncNode.widgets.find(w => w.name === "temperature");
    const useActiveSpeakerDetectionWidget = syncNode.widgets.find(w => w.name === "useActiveSpeakerDetection");
    const activeSpeakerDetectionWidget = syncNode.widgets.find(w => w.name === "activeSpeakerDetection");
    const useOcclusionDetectionEnabledWidget = syncNode.widgets.find(w => w.name === "useOcclusionDetectionEnabled");
    const occlusionDetectionEnabledWidget = syncNode.widgets.find(w => w.name === "occlusionDetectionEnabled");
    
    // Helper function to toggle widget enabled state
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
                const nodeElement = syncNode.htmlElements?.widgetsContainer || syncNode.htmlElements;
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
            
            syncNode.setDirtyCanvas(true);
        }
        
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        setTimeout(toggleEnabled, 100);
    }
    
    // Set up toggle handlers
    if (useEditRegionWidget && editRegionWidget) {
        toggleWidgetState(useEditRegionWidget, editRegionWidget, "editRegion");
    }
    if (useEmotionPromptWidget && emotionPromptWidget) {
        toggleWidgetState(useEmotionPromptWidget, emotionPromptWidget, "emotionPrompt");
    }
    if (useTemperatureWidget && temperatureWidget) {
        toggleWidgetState(useTemperatureWidget, temperatureWidget, "temperature");
    }
    if (useActiveSpeakerDetectionWidget && activeSpeakerDetectionWidget) {
        toggleWidgetState(useActiveSpeakerDetectionWidget, activeSpeakerDetectionWidget, "activeSpeakerDetection");
    }
    if (useOcclusionDetectionEnabledWidget && occlusionDetectionEnabledWidget) {
        toggleWidgetState(useOcclusionDetectionEnabledWidget, occlusionDetectionEnabledWidget, "occlusionDetectionEnabled");
    }
}

function syncSegmentToggleHandler(syncSegmentNode) {
    // Find all "use" parameter widgets for Sync Segment
    const useAudioStartTimeWidget = syncSegmentNode.widgets.find(w => w.name === "useAudioStartTime");
    const audioStartTimeWidget = syncSegmentNode.widgets.find(w => w.name === "audioStartTime");
    const useAudioEndTimeWidget = syncSegmentNode.widgets.find(w => w.name === "useAudioEndTime");
    const audioEndTimeWidget = syncSegmentNode.widgets.find(w => w.name === "audioEndTime");
    
    // Helper function to toggle widget enabled state
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
                const nodeElement = syncSegmentNode.htmlElements?.widgetsContainer || syncSegmentNode.htmlElements;
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
            
            syncSegmentNode.setDirtyCanvas(true);
        }
        
        appendWidgetCB(useWidget, () => {
            setTimeout(toggleEnabled, 50);
        });
        
        setTimeout(toggleEnabled, 100);
    }
    
    // Set up toggle handlers
    if (useAudioStartTimeWidget && audioStartTimeWidget) {
        toggleWidgetState(useAudioStartTimeWidget, audioStartTimeWidget, "audioStartTime");
    }
    if (useAudioEndTimeWidget && audioEndTimeWidget) {
        toggleWidgetState(useAudioEndTimeWidget, audioEndTimeWidget, "audioEndTime");
    }
}