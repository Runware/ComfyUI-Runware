from .utils import runwareUtils as rwUtils

class upscaler:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Image": ("IMAGE", {
                        "tooltip": "Specifies the input image to be upscaled."
                }),
                "upscaleFactor": ("FLOAT", {
                    "tooltip": "Each level will increase the size of the image by the corresponding factor.",
                    "default": 2.0,
                    "min": 1.0,
                    "max": 8.0,
                    "step": 0.1,
                }),
            },
            "optional": {
                "model": ("STRING", {
                    "tooltip": "Model AIR ID (runware:500@1, runware:501@1, runware:502@1, runware:503@1, runware:504@1, bria:52@1)",
                    "default": "",
                }),
                # Common parameters toggles
                "useSteps": ("BOOLEAN", {
                    "tooltip": "Enable quality steps parameter",
                    "default": False,
                }),
                "steps": ("INT", {
                    "tooltip": "Quality steps (4-60 depending on model)",
                    "default": 20,
                    "min": 1,
                    "max": 100,
                }),
                "useSeed": ("BOOLEAN", {
                    "tooltip": "Enable seed for reproducibility",
                    "default": False,
                }),
                "seed": ("INT", {
                    "tooltip": "Reproducibility toggle",
                    "default": 0,
                    "min": 0,
                }),
                "useCFGScale": ("BOOLEAN", {
                    "tooltip": "Enable CFG Scale parameter",
                    "default": False,
                }),
                "CFGScale": ("FLOAT", {
                    "tooltip": "Guidance CFG (3-20 depending on model)",
                    "default": 7.0,
                    "min": 1.0,
                    "max": 30.0,
                    "step": 0.1,
                }),
                "usePrompts": ("BOOLEAN", {
                    "tooltip": "Enable positive and negative prompts",
                    "default": False,
                }),
                "positivePrompt": ("STRING", {
                    "tooltip": "Positive prompt for upscaling",
                    "multiline": True,
                    "default": "",
                }),
                "negativePrompt": ("STRING", {
                    "tooltip": "Negative prompt for upscaling",
                    "multiline": True,
                    "default": "",
                }),
                # Clarity upscaler specific toggles
                "useClarityParams": ("BOOLEAN", {
                    "tooltip": "Enable Clarity upscaler specific parameters",
                    "default": False,
                }),
                "controlNetWeight": ("FLOAT", {
                    "tooltip": "Style preservation/Resemblance (0-1) - Clarity upscaler specific",
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
                "strength": ("FLOAT", {
                    "tooltip": "Creativity (0-1) - Clarity upscaler specific",
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
                "scheduler": ("STRING", {
                    "tooltip": "Controls noise addition/removal - Clarity upscaler specific",
                    "default": "DPM++ 2M Karras",
                }),
                # CCSR and Latent upscaler specific toggles
                "useCCSRParams": ("BOOLEAN", {
                    "tooltip": "Enable CCSR and Latent upscaler specific parameters",
                    "default": False,
                }),
                "colorFix": ("BOOLEAN", {
                    "tooltip": "Color correction (ADAIN/NOFIX) - CCSR and Latent upscaler specific",
                    "default": False,
                }),
                "tileDiffusion": ("BOOLEAN", {
                    "tooltip": "Tile diffusion for large images - CCSR and Latent upscaler specific",
                    "default": False,
                }),
                # Latent upscaler specific toggle
                "useLatentParams": ("BOOLEAN", {
                    "tooltip": "Enable Latent upscaler specific parameters",
                    "default": False,
                }),
                "clipSkip": ("INT", {
                    "tooltip": "Skip CLIP layers during guidance (0-2) - Latent upscaler specific",
                    "default": 0,
                    "min": 0,
                    "max": 2,
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
            },
        }

    DESCRIPTION = "Enhance the resolution and quality of your images using Runware's advanced upscaling API. Transform low-resolution images into sharp, high-definition visuals."
    FUNCTION = "upscale"
    RETURN_TYPES = ("IMAGE",)
    CATEGORY = "Runware"

    def upscale(self, **kwargs):
        image = kwargs.get("Image")
        upscaleFactor = kwargs.get("upscaleFactor", 2.0)
        
        # Get toggle parameters
        useSteps = kwargs.get("useSteps", False)
        useSeed = kwargs.get("useSeed", False)
        useCFGScale = kwargs.get("useCFGScale", False)
        usePrompts = kwargs.get("usePrompts", False)
        useClarityParams = kwargs.get("useClarityParams", False)
        useCCSRParams = kwargs.get("useCCSRParams", False)
        useLatentParams = kwargs.get("useLatentParams", False)
        
        # Get optional parameters
        model = kwargs.get("model", "")
        steps = kwargs.get("steps", 20)
        seed = kwargs.get("seed", 0)
        CFGScale = kwargs.get("CFGScale", 7.0)
        positivePrompt = kwargs.get("positivePrompt", "")
        negativePrompt = kwargs.get("negativePrompt", "")
        controlNetWeight = kwargs.get("controlNetWeight", 0.5)
        strength = kwargs.get("strength", 0.5)
        scheduler = kwargs.get("scheduler", "DPM++ 2M Karras")
        colorFix = kwargs.get("colorFix", False)
        tileDiffusion = kwargs.get("tileDiffusion", False)
        clipSkip = kwargs.get("clipSkip", 0)
        safetyInputs = kwargs.get("safetyInputs", None)
        runwareAccelerator = kwargs.get("Accelerator", None)
        providerSettings = kwargs.get("providerSettings", None)

        # Build the base configuration
        genConfig = {
            "taskType": "imageUpscale",
            "taskUUID": rwUtils.genRandUUID(),
            "inputImage": rwUtils.convertTensor2IMG(image),
            "upscaleFactor": upscaleFactor,
            "outputFormat": rwUtils.OUTPUT_FORMAT,
            "outputQuality": rwUtils.OUTPUT_QUALITY,
            "outputType": "base64Data",
        }
        
        # Add model if specified
        if model:
            genConfig["model"] = model
            
        # Build settings object for advanced parameters
        settings = {}
        
        # Common parameters - only add if their toggle is enabled
        if useSteps:
            settings["steps"] = steps
        if useSeed:
            settings["seed"] = seed
        if useCFGScale:
            settings["CFGScale"] = CFGScale
        if usePrompts:
            if positivePrompt:
                settings["positivePrompt"] = positivePrompt
            if negativePrompt:
                settings["negativePrompt"] = negativePrompt
                
        # Clarity upscaler specific parameters
        if useClarityParams:
            settings["controlNetWeight"] = controlNetWeight
            settings["strength"] = strength
            settings["scheduler"] = scheduler
            
        # CCSR and Latent upscaler specific parameters
        if useCCSRParams:
            settings["colorFix"] = colorFix
            settings["tileDiffusion"] = tileDiffusion
            
        # Latent upscaler specific parameters
        if useLatentParams:
            settings["clipSkip"] = clipSkip
            
        # Add settings to config if any settings were specified
        if settings:
            genConfig["settings"] = settings
        
        # Add safety inputs if provided
        if safetyInputs is not None and isinstance(safetyInputs, dict) and len(safetyInputs) > 0:
            genConfig["safety"] = safetyInputs
        
        # Add accelerator options if provided
        if runwareAccelerator is not None and isinstance(runwareAccelerator, dict) and len(runwareAccelerator) > 0:
            genConfig["acceleratorOptions"] = runwareAccelerator
        
        # Handle providerSettings - extract provider name from model and merge with custom settings
        if providerSettings is not None:
            # Extract provider name from model (e.g., "runware:500@1" -> "runware")
            provider_name = model.split(":")[0] if ":" in model and model else "runware"
            
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
        print(f"[DEBUG] Sending Image Upscale Request:", flush=True)
        print(f"[DEBUG] Request Payload: {rwUtils.safe_json_dumps([genConfig], indent=2)}", flush=True)
        
        try:
            genResult = rwUtils.inferenecRequest([genConfig])
            
            # Debug: Print the response received
            print(f"[DEBUG] Received Image Upscale Response:", flush=True)
            print(f"[DEBUG] Response: {rwUtils.safe_json_dumps(genResult, indent=2)}", flush=True)
        except Exception as e:
            print(f"[DEBUG] Error in Image Upscale Request: {str(e)}", flush=True)
            raise
        
        images = rwUtils.convertImageB64List(genResult)
        return (images, )