from .utils import runwareUtils as rwUtils

class bgremoval:
    RUNWARE_RMBG_MODELS = {
        "RemBG 1.4": "runware:109@1",
        "Bria RMBG 2.0": "runware:110@1",
        "Bria RMBG v2.0": "bria:2@1",
        "BiRefNet v1 Base": "runware:112@1",
        "BiRefNet v1 Base - COD": "runware:112@2",
        "BiRefNet Dis": "runware:112@3",
        "BiRefNet General": "runware:112@5",
        "BiRefNet General RES 512x512": "runware:112@6",
        "BiRefNet HRSOD DHU": "runware:112@7",
        "BiRefNet Massive TR DIS5K TES": "runware:112@8",
        "BiRefNet Matting": "runware:112@9",
        "BiRefNet Portrait": "runware:112@10"
    }

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Image": ("IMAGE", {
                        "tooltip": "Specifies the input image to be processed."
                }),
                "Model": (list(cls.RUNWARE_RMBG_MODELS.keys()), {
                    "tooltip": "Select the background removal model to use. Different models have varying strengths depending on image content and complexity.",
                    "default": "RemBG 1.4",
                }),
            },
            "optional": {
                "Post Process Mask": ("BOOLEAN", {
                    "tooltip": "Controls whether the mask should undergo additional post-processing. This step can improve the accuracy and quality of the background removal mask.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "Return Only Mask": ("BOOLEAN", {
                    "tooltip": "Whether to return only the mask. The mask is the opposite of the image background removal.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "Alpha Matting": ("BOOLEAN", {
                    "tooltip": "Alpha matting is a post-processing technique that enhances the quality of the output by refining the edges of the foreground object.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "Alpha Matting Foreground Threshold": ("INT", {
                    "tooltip": "Threshold value used in alpha matting to distinguish the foreground from the background. Adjusting this parameter affects the sharpness and accuracy of the foreground object edges.",
                    "default": 240,
                    "min": 1,
                    "max": 255,
                }),
                "Alpha Matting Background Threshold": ("INT", {
                    "tooltip": "Threshold value used in alpha matting to refine the background areas. It influences how aggressively the algorithm removes the background while preserving image details. The higher the value, the more computation is needed and therefore the more expensive the operation is.",
                    "default": 10,
                    "min": 1,
                    "max": 255,
                }),
                "Alpha Matting Erode Size": ("INT", {
                    "tooltip": "Specifies the size of the erosion operation used in alpha matting. Erosion helps in smoothing the edges of the foreground object for a cleaner removal of the background.",
                    "default": 10,
                    "min": 1,
                    "max": 255,
                }),
                "safetyInputs": ("RUNWARESAFETYINPUTS", {
                    "tooltip": "Connect Runware Safety Inputs node to configure safety and content moderation settings.",
                }),
                "Accelerator": ("RUNWAREACCELERATOR", {
                    "tooltip": "Connect a Runware Accelerator Options Node to configure caching and acceleration settings.",
                }),
                "providerSettings": ("RUNWAREPROVIDERSETTINGS", {
                    "tooltip": "Connect a Runware Provider Settings node to configure provider-specific parameters.",
                }),
                **rwUtils.RUNWARE_REMBG_OUTPUT_FORMATS,
            }
        }

    DESCRIPTION = "Remove backgrounds from images effortlessly using Runware's low-cost image editing Inference."
    FUNCTION = "rembg"
    RETURN_TYPES = ("IMAGE",)
    CATEGORY = "Runware"

    def rembg(self, **kwargs):
        image = kwargs.get("Image")
        modelName = kwargs.get("Model", "RemBG 1.4")
        postProcessMask = kwargs.get("Post Process Mask", False)
        returnOnlyMask = kwargs.get("Return Only Mask", False)
        alphaMatting = kwargs.get("Alpha Matting", False)
        alphaMattingForegroundThreshold = kwargs.get("Alpha Matting Foreground Threshold", 240)
        alphaMattingBackgroundThreshold = kwargs.get("Alpha Matting Background Threshold", 10)
        alphaMattingErodeSize = kwargs.get("Alpha Matting Erode Size", 10)
        outputFormat = kwargs.get("outputFormat", "WEBP")
        safetyInputs = kwargs.get("safetyInputs", None)
        runwareAccelerator = kwargs.get("Accelerator", None)
        providerSettings = kwargs.get("providerSettings", None)
        modelAIR = self.RUNWARE_RMBG_MODELS.get(modelName, "runware:109@1")
        includeExtraSettings = postProcessMask or returnOnlyMask or alphaMatting

        if modelAIR != "runware:109@1" and includeExtraSettings:
            raise ValueError(
                f"Oops! The selected model '{modelName}' does not support additional settings!\n"
                "Please switch to 'RemBG 1.4' if you wish to use these features."
            )

        genConfig = {
            "taskType": "imageBackgroundRemoval",
            "taskUUID": rwUtils.genRandUUID(),
            "inputImage": rwUtils.convertTensor2IMG(image),
            "model": modelAIR,
            "outputFormat": outputFormat,
            "outputQuality": rwUtils.OUTPUT_QUALITY,
            "outputType": "base64Data",
        }

        if includeExtraSettings:
            settings = {
                "postProcessMask": postProcessMask,
                "returnOnlyMask": returnOnlyMask,
                "alphaMatting": alphaMatting,
            }
            if alphaMatting:
                settings["alphaMattingForegroundThreshold"] = alphaMattingForegroundThreshold
                settings["alphaMattingBackgroundThreshold"] = alphaMattingBackgroundThreshold
                settings["alphaMattingErodeSize"] = alphaMattingErodeSize
            genConfig["settings"] = settings
        
        # Add safety inputs if provided
        if safetyInputs is not None and isinstance(safetyInputs, dict) and len(safetyInputs) > 0:
            genConfig["safety"] = safetyInputs
        
        # Add accelerator options if provided
        if runwareAccelerator is not None and isinstance(runwareAccelerator, dict) and len(runwareAccelerator) > 0:
            genConfig["acceleratorOptions"] = runwareAccelerator
        
        # Handle providerSettings - extract provider name from model and merge with custom settings
        if providerSettings is not None:
            # Extract provider name from model (e.g., "bria:2@1" -> "bria", "runware:109@1" -> "runware")
            provider_name = modelAIR.split(":")[0] if ":" in modelAIR else "runware"
            
            # If providerSettings is a dictionary, create the correct API format
            if isinstance(providerSettings, dict):
                # Create the providerSettings object with provider name as key
                final_provider_settings = {
                    provider_name: providerSettings
                }
                genConfig["providerSettings"] = final_provider_settings
                print(f"[Debugging] Provider settings: {final_provider_settings}")
            else:
                # If it's just a string, use it directly
                genConfig["providerSettings"] = providerSettings

        # Debug: Print the request being sent
        print(f"[DEBUG] Sending Background Removal Request:", flush=True)
        print(f"[DEBUG] Request Payload: {rwUtils.safe_json_dumps([genConfig], indent=2)}", flush=True)
        
        try:
            genResult = rwUtils.inferenecRequest([genConfig])
            
            # Debug: Print the response received
            print(f"[DEBUG] Received Background Removal Response:", flush=True)
            print(f"[DEBUG] Response: {rwUtils.safe_json_dumps(genResult, indent=2)}", flush=True)
        except Exception as e:
            print(f"[DEBUG] Error in Background Removal Request: {str(e)}", flush=True)
            raise
        
        images = rwUtils.convertImageB64List(genResult)
        return (images, )