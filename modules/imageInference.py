from .utils import runwareUtils as rwUtils


class txt2img:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "positivePrompt": ("STRING", {
                    "multiline": True,
                    "placeholder": "Positive Prompt: a text instruction to guide the model on generating the image. It is usually a sentence or a paragraph that provides positive guidance for the task. This parameter is essential to shape the desired results.\n\nYou Can Press (Ctrl + Alt + E) To Enhance The Prompt!",
                    "tooltip": "Positive Prompt: a text instruction to guide the model on generating the image. You Can Also Press (Ctrl + Alt + E) To Enhance The Prompt!"
                }),
                "negativePrompt": ("STRING", {
                    "multiline": True,
                    "placeholder": "Negative Prompt: a text instruction to guide the model on generating the image. It is usually a sentence or a paragraph that provides negative guidance for the task. This parameter helps to avoid certain undesired results.",
                    "tooltip": "Negative Prompt: a text instruction to guide the model on generating the image."
                }),
                "Model": ("RUNWAREMODEL", {
                    "tooltip": "Connect a Runware Model From Runware Model Node.",
                }),
                "Multi Inference Mode": ("BOOLEAN", {
                    "tooltip": "If Enabled the node will skip the image generation process and will only return the Runware Task Object to be used in the Multi Inference Node.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "Prompt Weighting": (["Disabled", "sdEmbeds", "Compel"], {
                    "default": "Disabled",
                    "tooltip": "Prompt weighting allows you to adjust how strongly different parts of your prompt influence the generated image.\n\nChoose between \"compel\" notation with advanced weighting operations or \"sdEmbeds\" for simple emphasis adjustments.\n\nCompel Example: \"small+ dog, pixar style\"\n\nsdEmbeds Example: \"(small:2.5) dog, pixar style\"",
                }),
                "dimensions": ([
                    "None", "Square (512x512)", "Square HD (1024x1024)", "Portrait 3:4 (768x1024)",
                    "Portrait 9:16 (576x1024)", "Landscape 4:3 (1024x768)",
                    "Landscape 16:9 (1024x576)",
                    "Custom"
                ], {
                    "default": "Square (512x512)",
                    "tooltip": "Adjust the dimensions of the generated image by specifying its width and height in pixels, or select from the predefined options. Image dimensions must be multiples of 64 (e.g., 512x512, 1024x768). Select 'None' to let the model determine dimensions automatically.",
                }),
                "width": ("INT", {
                    "tooltip": "The Width of the image in pixels.",
                    "default": 512,
                    "min": 128,
                    "max": 6048,
                    "step": 1,
                }),
                "height": ("INT", {
                    "tooltip": "The Height of the image in pixels.",
                    "default": 512,
                    "min": 128,
                    "max": 6048,
                    "step": 1,
                }),
                "useSteps": ("BOOLEAN", {
                    "tooltip": "Enable to include steps parameter in API request. Disable if your model doesn't support steps (like nano banana).",
                    "default": True,
                }),
                "steps": ("INT", {
                    "tooltip": "The number of steps is the number of iterations the model will perform to generate the image. Only used when 'Use Steps' is enabled.",
                    "default": 4,
                    "min": 1,
                    "max": 100,
                }),
                "useScheduler": ("BOOLEAN", {
                    "tooltip": "Enable to include scheduler parameter in API request. Disable if your model doesn't support scheduler.",
                    "default": True,
                }),
                "scheduler": (['Default', 'DDIM', 'DDIMScheduler', 'DDPMScheduler', 'DEISMultistepScheduler', 'DPMSolverSinglestepScheduler', 'DPMSolverMultistepScheduler', 'DPMSolverMultistepInverse', 'DPM++', 'DPM++ Karras', 'DPM++ 2M', 'DPM++ 2M Karras', 'DPM++ 2M SDE Karras', 'DPM++ 2M SDE', 'DPM++ 3M', 'DPM++ 3M Karras', 'DPM++ SDE Karras', 'DPM++ SDE', 'EDMEulerScheduler', 'EDMDPMSolverMultistepScheduler', 'Euler', 'EulerDiscreteScheduler', 'Euler Karras', 'Euler a', 'EulerAncestralDiscreteScheduler', 'FlowMatchEulerDiscreteScheduler', 'Heun', 'HeunDiscreteScheduler', 'Heun Karras', 'IPNDMScheduler', 'KDPM2DiscreteScheduler', 'KDPM2AncestralDiscreteScheduler', 'LCM', 'LCMScheduler', 'LMS', 'LMSDiscreteScheduler', 'LMS Karras', 'PNDMScheduler', 'TCDScheduler', 'UniPC', 'UniPCMultistepScheduler', 'UniPC Karras', 'UniPC 2M', 'UniPC 2M Karras', 'UniPC 3M', 'UniPC 3M Karras'], {
                    "tooltip": "An scheduler is a component that manages the inference process. Different schedulers can be used to achieve different results like more detailed images, faster inference, or more accurate results.",
                    "default": "Default",
                }),
                "useCFGScale": ("BOOLEAN", {
                    "tooltip": "Enable to include CFG scale parameter in API request. Disable if your model doesn't support CFG scale (like nano banana).",
                    "default": True,
                }),
                "cfgScale": ("FLOAT", {
                    "tooltip": "Guidance scale represents how closely the images will resemble the prompt or how much freedom the AI model has. Only used when 'Use CFG Scale' is enabled.",
                    "default": 6.5,
                    "min": 1.0,
                    "max": 50.0,
                    "step": 0.5,
                }),
                "useSeed": ("BOOLEAN", {
                    "tooltip": "Enable to include seed parameter in API request. Disable if your model doesn't support seed.",
                    "default": True,
                }),
                "seed": ("INT", {
                    "tooltip": "A value used to randomize the image generation. If you want to make images reproducible (generate the same image multiple times), you can use the same seed value. Set to 0 to auto-generate a random seed.",
                    "default": 1,
                    "min": 0,
                    "max": 4294967295,
                }),
                "useClipSkip": ("BOOLEAN", {
                    "tooltip": "Enable to include clipSkip parameter in API request. Disable if your model doesn't support clipSkip.",
                    "default": True,
                }),
                "clipSkip": ("INT", {
                    "tooltip": "Enables skipping layers of the CLIP embedding process, leading to quicker and more varied image generation. Only used when 'Use Clip Skip' is enabled.",
                    "default": 0,
                    "min": 0,
                    "max": 2,
                }),
                "strength": ("FLOAT", {
                    "tooltip": "When doing Image-to-Image or Inpainting, this parameter is used to determine the influence of the seedImage image in the generated output. A lower value results in more influence from the original image, while a higher value allows more creative deviation.",
                    "default": 0.8,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
                "Mask Margin": ("BOOLEAN", {
                    "tooltip": "Enables Or Disables Mask Margin Feature.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "maskMargin": ("INT", {
                    "tooltip": "Adds extra context pixels around the masked region during inpainting. When this parameter is present, the model will zoom into the masked area, considering these additional pixels to create more coherent and well-integrated details.",
                    "default": 32,
                    "min": 32,
                    "max": 128,
                }),
                "outputFormat": (["WEBP", "PNG", "JPEG", "SVG"], {
                    "tooltip": "Choose the output image format.",
                    "default": "WEBP",
                }),
                "batchSize": ("INT", {
                    "tooltip": "The number of images to generate in a single request.",
                    "default": 1,
                    "min": 1,
                    "max": 10,
                }),
                "acceleration": (["none", "low", "medium", "high"], {
                    "tooltip": "Applies optimized acceleration presets that automatically configure multiple generation parameters for the best speed and quality balance. This parameter serves as an abstraction layer that intelligently adjusts acceleratorOptions, steps, scheduler, and other underlying settings.\n\nAvailable values:\n- none: No acceleration applied, uses default parameter values.\n- low: Minimal acceleration with optimized settings for lowest quality loss.\n- medium: Balanced acceleration preset with moderate speed improvements.\n- high: Maximum acceleration with caching and aggressive optimizations for fastest generation.",
                    "default": "none",
                }),
            },
            "optional": {
                "Accelerator": ("RUNWAREACCELERATOR", {
                    "tooltip": "Connect a Runware Accelerator Options Node to configure caching and acceleration settings.",
                }),
                "Lora": ("RUNWARELORA", {
                    "tooltip": "Connect a Runware Lora From Lora Search Node Or Lora Combine For Multiple Lora's Together.",
                }),
                "Outpainting": ("RUNWAREOUTPAINT", {
                    "tooltip": "Connect a Runware Outpainting Node to extend the image boundaries in different directions.",
                }),
                "IPAdapters": ("RUNWAREIPAdapter", {
                    "tooltip": "Connect a Runware IP Adapter node or IP Adapter Combine node to use reference images for guiding the generation.",
                }),
                "ControlNet": ("RUNWARECONTROLNET", {
                    "tooltip": "Connect a Runware ControlNet Guidance Node to help the model generate images that align with the desired structure.",
                }),
                "Refiner": ("RUNWAREREFINER", {
                    "tooltip": "Connect a Runware Refiner Node to help create higher quality image outputs by incorporating specialized models designed to enhance image details and overall coherence.",
                }),
                "seedImage": ("IMAGE", {
                    "tooltip": "Specifies the seed image to be used for the diffusion process, when doing Image-to-Image, Inpainting or Outpainting, this parameter is required.",
                }),
                "maskImage": ("MASK", {
                    "tooltip": "Specifies the mask image to be used for the inpainting process, when doing Inpainting, this parameter is required.",
                }),
                "Embeddings": ("RUNWAREEMBEDDING", {
                    "tooltip": "Connect a Runware Embedding Node to help the model generate images that align with the desired structure.",
                }),
                "VAE": ("RUNWAREVAE", {
                    "tooltip": "Connect a Runware VAE Node to help the model generate images that align with the desired structure.",
                }),
                "referenceImages": ("RUNWAREREFERENCEIMAGES", {
                    "tooltip": "Connect a Runware Reference Images Node to provide visual guidance for image generation.",
                }),
                "inputs": ("RUNWAREIMAGEINFERENCEINPUTS", {
                    "tooltip": "Connect a Runware Image Inference Inputs Node to provide custom inputs like references for the inference process.",
                }),
                "providerSettings": ("RUNWAREPROVIDERSETTINGS", {
                    "tooltip": "Connect a Runware Provider Settings Node to configure provider-specific parameters.",
                }),
                "safetyInputs": ("RUNWARESAFETYINPUTS", {
                    "tooltip": "Connect Runware Safety Inputs node to configure safety and content moderation settings.",
                }),
            }
        }

    DESCRIPTION = "Generates Images Lightning Fast With Runware Image Inference Sonic Engine."
    FUNCTION = "generateImage"
    RETURN_TYPES = ("IMAGE", "RUNWARETASK")
    RETURN_NAMES = ("IMAGE", "RW-Task")
    CATEGORY = "Runware"

    @classmethod
    def VALIDATE_INPUTS(cls, **kwargs):
        positivePrompt = kwargs.get("positivePrompt", "")
        negativePrompt = kwargs.get("negativePrompt", "")
        
        # Only validate positivePrompt length if it's provided
        if positivePrompt and len(positivePrompt) > 2000:
            return "Positive Prompt is too long. Maximum length is 2000 characters."
        
        if negativePrompt and len(negativePrompt) > 2000:
            return "Negative Prompt is too long. Maximum length is 2000 characters."
        
        return True

    def generateImage(self, **kwargs):
        runwareModel = kwargs.get("Model")
        positivePrompt = kwargs.get("positivePrompt")
        negativePrompt = kwargs.get("negativePrompt", None)
        multiInferenceMode = kwargs.get("Multi Inference Mode", False)
        promptWeighting = kwargs.get("Prompt Weighting", "Disabled")
        runwareControlNet = kwargs.get("ControlNet", None)
        runwareAccelerator = kwargs.get("Accelerator", None)
        runwareLora = kwargs.get("Lora", None)
        runwareOutpainting = kwargs.get("Outpainting", None)
        runwareIPAdapters = kwargs.get("IPAdapters", None)
        runwareRefiner = kwargs.get("Refiner", None)
        runwareEmbedding = kwargs.get("Embeddings", None)
        runwareVAE = kwargs.get("VAE", None)
        referenceImages = kwargs.get("referenceImages", None)
        inputs = kwargs.get("inputs", None)
        providerSettings = kwargs.get("providerSettings", None)
        safetyInputs = kwargs.get("safetyInputs", None)
        seedImage = kwargs.get("seedImage", None)
        seedImageStrength = kwargs.get("strength", 0.8)
        maskImage = kwargs.get("maskImage", None)
        enableMaskMargin = kwargs.get("Mask Margin", False)
        maskImageMargin = kwargs.get("maskMargin", 32)
        clipSkip = kwargs.get("clipSkip", 0)
        height = kwargs.get("height", 512)
        width = kwargs.get("width", 512)
        steps = kwargs.get("steps", 4)
        useSteps = kwargs.get("useSteps", True)
        scheduler = kwargs.get("scheduler", "Default")
        useScheduler = kwargs.get("useScheduler", True)
        cfgScale = kwargs.get("cfgScale", 6.5)
        useCFGScale = kwargs.get("useCFGScale", True)
        seed = kwargs.get("seed")
        useSeed = kwargs.get("useSeed", True)
        useClipSkip = kwargs.get("useClipSkip", True)
        dimensions = kwargs.get("dimensions", "Square (512x512)")
        outputFormat = kwargs.get("outputFormat", "WEBP")
        batchSize = kwargs.get("batchSize", 1)
        acceleration = kwargs.get("acceleration", "none")
        
        if (maskImage is not None and seedImage is None):
            raise Exception("Mask Image Requires Seed Image To Be Provided!")

        genConfig = [
            {
                "taskType": "imageInference",
                "taskUUID": rwUtils.genRandUUID(),
                "model": runwareModel,
                "outputType": "base64Data",
                "outputFormat": outputFormat,
                "outputQuality": rwUtils.OUTPUT_QUALITY,
                "numberResults": batchSize,
            }
        ]
        
        # Add positivePrompt only if provided
        if positivePrompt is not None and positivePrompt != "":
            genConfig[0]["positivePrompt"] = positivePrompt
        

        # For Debugging Purposes Only
        print(f"[Debugging] Task UUID: {genConfig[0]['taskUUID']}")

        # Add steps, CFGScale, seed, scheduler, clipSkip, and dimensions only if enabled
        if useSteps:
            genConfig[0]["steps"] = steps
        if useCFGScale:
            # Extract provider name from model (e.g., "bria:20@1" -> "bria")
            provider_name = runwareModel.split(":")[0] if ":" in runwareModel else runwareModel
            # Cast to int for Bria models
            if provider_name.lower() == "bria":
                genConfig[0]["CFGScale"] = int(cfgScale)
            else:
                genConfig[0]["CFGScale"] = cfgScale
        if useSeed:
            genConfig[0]["seed"] = seed
        if useScheduler:
            genConfig[0]["scheduler"] = scheduler
        if useClipSkip:
            genConfig[0]["clipSkip"] = clipSkip
        if dimensions != "None":
            genConfig[0]["width"] = width
            genConfig[0]["height"] = height

        if (negativePrompt is not None and negativePrompt != ""):
            genConfig[0]["negativePrompt"] = negativePrompt
        if (promptWeighting != "Disabled"):
            if (promptWeighting == "sdEmbeds"):
                genConfig[0]["promptWeighting"] = "sdEmbeds"
            else:
                genConfig[0]["promptWeighting"] = "compel"
        if (runwareAccelerator is not None):
            genConfig[0]["acceleratorOptions"] = runwareAccelerator
        
        # Add acceleration if not "none"
        if acceleration and acceleration != "none":
            genConfig[0]["acceleration"] = acceleration
        
        if (runwareLora is not None):
            if (isinstance(runwareLora, list)):
                genConfig[0]["lora"] = runwareLora
            elif (isinstance(runwareLora, dict)):
                genConfig[0]["lora"] = [runwareLora]
        if (runwareIPAdapters is not None):
            if (isinstance(runwareIPAdapters, list)):
                genConfig[0]["ipAdapters"] = runwareIPAdapters
            elif (isinstance(runwareIPAdapters, dict)):
                genConfig[0]["ipAdapters"] = [runwareIPAdapters]
        if (runwareEmbedding is not None):
            if (isinstance(runwareEmbedding, list)):
                genConfig[0]["embeddings"] = runwareEmbedding
            elif (isinstance(runwareEmbedding, dict)):
                genConfig[0]["embeddings"] = [runwareEmbedding]
        if (runwareOutpainting is not None):
            genConfig[0]["outpaint"] = runwareOutpainting
        if (runwareVAE is not None):
            genConfig[0]["vae"] = runwareVAE
        if (runwareControlNet is not None):
            genConfig[0]["controlNet"] = runwareControlNet
        if (runwareRefiner is not None):
            genConfig[0]["refiner"] = runwareRefiner
        if (seedImage is not None):
            seedImage = rwUtils.convertTensor2IMG(seedImage)
            genConfig[0]["seedImage"] = seedImage
            genConfig[0]["strength"] = seedImageStrength
            if (maskImage is not None):
                maskImage = rwUtils.convertTensor2IMG(maskImage)
                genConfig[0]["maskImage"] = maskImage
                if (enableMaskMargin):
                    genConfig[0]["maskMargin"] = maskImageMargin

        # Handle referenceImages
        if referenceImages is not None:
            genConfig[0]["referenceImages"] = referenceImages

        # Handle inputs (custom inference inputs)
        if inputs is not None:
            genConfig[0]["inputs"] = inputs

        # Handle providerSettings - extract provider name from model and merge with custom settings
        if providerSettings is not None:
            # Extract provider name from model (e.g., "bytedance:1@1" -> "bytedance")
            provider_name = runwareModel.split(":")[0] if ":" in runwareModel else runwareModel
            
            # If providerSettings is a dictionary, create the correct API format
            if isinstance(providerSettings, dict):
                # Create the providerSettings object with provider name as key
                final_provider_settings = {
                    provider_name: providerSettings
                }
                genConfig[0]["providerSettings"] = final_provider_settings
            else:
                # If it's already in the correct format, use it directly
                genConfig[0]["providerSettings"] = providerSettings

        # Add safety inputs if provided
        if safetyInputs is not None and isinstance(safetyInputs, dict) and len(safetyInputs) > 0:
            genConfig[0]["safety"] = safetyInputs

        if (multiInferenceMode):
            return (None, genConfig)
        else:
            # Debug: Print the request being sent
            print(f"[DEBUG] Sending Image Inference Request:")
            print(f"[DEBUG] Request Payload: {rwUtils.safe_json_dumps(genConfig, indent=2)}")
            
            genResult = rwUtils.inferenecRequest(genConfig)
            
            # Debug: Print the response received
            print(f"[DEBUG] Received Image Inference Response:")
            print(f"[DEBUG] Response: {rwUtils.safe_json_dumps(genResult, indent=2)}")
            
            images = rwUtils.convertImageB64List(genResult)
            return (images, None)