import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";
import { promptEnhanceHandler, syncDimensionsNodeHandler, searchNodeHandler, APIKeyHandler, captionNodeHandler, mediaUUIDHandler, save3DFilepathHandler, videoTranscriptionHandler, videoOutputsHandler, handleCustomErrors, videoInferenceDimensionsHandler, videoModelSearchFilterHandler, audioModelSearchFilterHandler, useParameterToggleHandler, imageInferenceToggleHandler, upscalerToggleHandler, videoUpscalerToggleHandler, audioInferenceToggleHandler, audioInferenceSpeechToggleHandler, audioSettingsToggleHandler, acceleratorOptionsToggleHandler, bytedanceProviderSettingsToggleHandler, xaiProviderSettingsToggleHandler, viduProviderSettingsToggleHandler, sourcefulProviderSettingsToggleHandler, sourcefulProviderSettingsFontsToggleHandler, threeDInferenceToggleHandler, threeDInferenceSettingsToggleHandler, threeDInferenceSettingsLatToggleHandler, ultralyticsProviderSettingsToggleHandler, openaiProviderSettingsToggleHandler, lightricksProviderSettingsToggleHandler, klingProviderSettingsToggleHandler, lumaProviderSettingsToggleHandler, briaProviderSettingsToggleHandler, pixverseProviderSettingsToggleHandler, alibabaProviderSettingsToggleHandler, mireloProviderSettingsToggleHandler, googleProviderSettingsToggleHandler, syncProviderSettingsToggleHandler, syncSegmentToggleHandler, settingsToggleHandler, audioInputToggleHandler, speechInputToggleHandler, briaProviderMaskToggleHandler, wanAnimateAdvancedFeatureSettingsToggleHandler, videoAdvancedFeatureInputsToggleHandler, audioInferenceInputsToggleHandler } from "./utils.js";
import { RUNWARE_NODE_TYPES, RUNWARE_NODE_PROPS, SEARCH_TERMS } from "./types.js";

const nodeInitList = [];
app.registerExtension({
	name: "runware.ai",
    async setup() {
        api.addEventListener('runwareError', handleCustomErrors);
        api.addEventListener('runwareImageCaption', captionNodeHandler);
        api.addEventListener('runwareMediaUUID', mediaUUIDHandler);
        api.addEventListener('runwareSave3DFilepath', save3DFilepathHandler);
        api.addEventListener('runwareVideoTranscription', videoTranscriptionHandler);
        api.addEventListener('runwareVideoOutputs', videoOutputsHandler);
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
        } else if(nodeClass === RUNWARE_NODE_TYPES.MEDIAUPLOAD) {
            // Style the mediaUUID widget to show full UUID
            const mediaUUIDWidget = node.widgets.find(widget => widget.name === "mediaUUID");
            if(mediaUUIDWidget && mediaUUIDWidget.inputEl) {
                mediaUUIDWidget.inputEl.style.width = "100%";
                mediaUUIDWidget.inputEl.style.minWidth = "300px";
                mediaUUIDWidget.inputEl.style.fontSize = "11px";
                mediaUUIDWidget.inputEl.style.fontFamily = "monospace";
            }
        } else if(nodeClass === RUNWARE_NODE_TYPES.VIDEOINFERENCEOUTPUTS) {
            // Style draftId and videoId widgets to show full IDs (like Media Upload)
            const draftIdWidget = node.widgets.find(widget => widget.name === "draftId");
            const videoIdWidget = node.widgets.find(widget => widget.name === "videoId");
            for(const w of [draftIdWidget, videoIdWidget]) {
                if(w && w.inputEl) {
                    w.inputEl.style.width = "100%";
                    w.inputEl.style.minWidth = "300px";
                    w.inputEl.style.fontSize = "11px";
                    w.inputEl.style.fontFamily = "monospace";
                }
            }
        } else if(nodeClass === RUNWARE_NODE_TYPES.SAVE3D) {
            // Style the filepath widget to show full path (like Media Upload mediaUUID)
            const filepathWidget = node.widgets.find(widget => widget.name === "filepath");
            if(filepathWidget && filepathWidget.inputEl) {
                filepathWidget.inputEl.style.width = "100%";
                filepathWidget.inputEl.style.minWidth = "300px";
                filepathWidget.inputEl.style.fontSize = "11px";
                filepathWidget.inputEl.style.fontFamily = "monospace";
            }
        }

        const nodeWidgets = node.widgets;
        
        // Handle node-specific handlers first - each node has its own dedicated handler
        // These must be called BEFORE the colorModeOnly check
        if(nodeClass === RUNWARE_NODE_TYPES.IMAGEINFERENCE) {
            imageInferenceToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.VIDEOINFERENCE) {
            videoInferenceDimensionsHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.UPSCALER) {
            upscalerToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.VIDEOUPSCALER) {
            videoUpscalerToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.AUDIOINFERENCE) {
            audioInferenceToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.AUDIOINFERENCESPEECH) {
            audioInferenceSpeechToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.AUDIOSETTINGS) {
            audioSettingsToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.ACCELERATOROPTIONS) {
            acceleratorOptionsToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.BYTEDANCEPROVIDERSETTINGS) {
            bytedanceProviderSettingsToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.XAIPROVIDERSETTINGS) {
            xaiProviderSettingsToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.ULTRALYTICSINPUTS) {
            ultralyticsProviderSettingsToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.OPENAIPROVIDERSETTINGS) {
            openaiProviderSettingsToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.LIGHTRICKSPROVIDERSETTINGS) {
            lightricksProviderSettingsToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.KLINGPROVIDERSETTINGS) {
            klingProviderSettingsToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.LUMAPROVIDERSETTINGS) {
            lumaProviderSettingsToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.BRIAPROVIDERSETTINGS) {
            briaProviderSettingsToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.PIXVERSEPROVIDERSETTINGS) {
            pixverseProviderSettingsToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.ALIBABAPROVIDERSETTINGS) {
            alibabaProviderSettingsToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.MIRELOPROVIDERSETTINGS) {
            mireloProviderSettingsToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.GOOGLEPROVIDERSETTINGS) {
            googleProviderSettingsToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.SYNCPROVIDERSETTINGS) {
            syncProviderSettingsToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.SYNCSEGMENT) {
            syncSegmentToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.VIDUPROVIDERSETTINGS) {
            viduProviderSettingsToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.SOURCEFULPROVIDERSETTINGS) {
            sourcefulProviderSettingsToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.SOURCEFULPROVIDERSETTINGSFONTS) {
            sourcefulProviderSettingsFontsToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.SETTINGS) {
            settingsToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.AUDIOINPUT) {
            audioInputToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.SPEECHINPUT) {
            speechInputToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.BRIAPROVIDERMASK) {
            briaProviderMaskToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.WANANIMATEADVANCEDFEATURESETTINGS) {
            wanAnimateAdvancedFeatureSettingsToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.VIDEOADVANCEDFEATUREINPUTS) {
            videoAdvancedFeatureInputsToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.AUDIOINFERENCEINPUTS) {
            audioInferenceInputsToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.THREEDINFERENCE) {
            threeDInferenceToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.THREEDINFERENCESETTINGS) {
            threeDInferenceSettingsToggleHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.THREEDINFERENCESETTINGSSPARSESTRUCTURE ||
                  nodeClass === RUNWARE_NODE_TYPES.THREEDINFERENCESETTINGSSHAPESLAT ||
                  nodeClass === RUNWARE_NODE_TYPES.THREEDINFERENCESETTINGSTEXSLAT) {
            threeDInferenceSettingsLatToggleHandler(node);
        }

        if(crNodeProps.colorModeOnly === true) return;
        if(nodeWidgets.length <= 0) return;

        if(nodeClass === RUNWARE_NODE_TYPES.VIDEOMODELSEARCH) {
            videoModelSearchFilterHandler(node);
        } else if(nodeClass === RUNWARE_NODE_TYPES.AUDIOMODELSEARCH) {
            audioModelSearchFilterHandler(node);
        }

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