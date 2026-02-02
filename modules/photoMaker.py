from .utils import runwareUtils as rwUtils


class photoMaker:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Model": ("RUNWAREMODEL", {
                    "tooltip": "Connect a Runware Model From Runware Model Node.",
                }),
                "Image 1": ("IMAGE", {
                    "tooltip": "Specifies Input Image 1 that will be used as reference for the subject. These reference images help the AI to maintain identity consistency during the generation process."
                }),
                "positivePrompt": ("STRING", {
                    "multiline": True,
                    "placeholder": "Positive Prompt: a text instruction to guide the model on generating the image. It is usually a sentence or a paragraph that provides positive guidance for the task. This parameter is essential to shape the desired results.\n\nThe PhotoMaker positive prompt must follow a specific format: the class word (like \"man\", \"woman\", \"girl\") must be followed by the trigger word \"img\".\nExample: man img, wearing a suit",
                    "tooltip": "Positive Prompt: a text instruction to guide the model on generating the image.\nDo not Forget To Add trigger word \"img\" after the class word (like \"man\", \"woman\", \"girl\")",
                }),
                "negativePrompt": ("STRING", {
                    "multiline": True,
                    "placeholder": "Negative Prompt: a text instruction to guide the model on generating the image. It is usually a sentence or a paragraph that provides negative guidance for the task. This parameter helps to avoid certain undesired results.",
                    "tooltip": "Negative Prompt: a text instruction to guide the model on generating the image."
                }),
                "Prompt Weighting": (["Disabled", "Compel"], {
                    "default": "Disabled",
                    "tooltip": "Prompt weighting allows you to adjust how strongly different parts of your prompt influence the generated image.",
                }),
                "style": ([
                    "No style", "Cinematic", "Disney Character", "Digital Art", "Photographic", "Fantasy art",
                    "Neonpunk", "Enhance", "Comic book", "Lowpoly", "Line art"
                ], {
                    "default": "No style",
                    "tooltip": "Specifies the artistic style to be applied to the generated images."
                }),
                "dimensions": ([
                    "Square (512x512)", "Square HD (1024x1024)", "Portrait 3:4 (768x1024)",
                    "Portrait 9:16 (576x1024)", "Landscape 4:3 (1024x768)",
                    "Landscape 16:9 (1024x576)", "Custom"
                ], {
                    "default": "Square HD (1024x1024)",
                    "tooltip": "Adjust the dimensions of the generated image by specifying its width and height in pixels, or select from the predefined options. Image dimensions must be multiples of 64 (e.g., 512x512, 1024x768).",
                }),
                "width": ("INT", {
                    "tooltip": "The Width of the image in pixels.",
                    "default": 1024,
                    "min": 512,
                    "max": 2048,
                    "step": 64,
                }),
                "height": ("INT", {
                    "tooltip": "The Height of the image in pixels.",
                    "default": 1024,
                    "min": 512,
                    "max": 2048,
                    "step": 64,
                }),
                "steps": ("INT", {
                    "tooltip": "The number of steps is the number of iterations the model will perform to generate the image. The higher the number of steps, the more detailed the image will be. However, increasing the number of steps will also increase the time it takes to generate the image and may not always result in a better image.",
                    "default": 25,
                    "min": 1,
                    "max": 100,
                }),
                "scheduler": (['Default', 'DDIM', 'DDIMScheduler', 'DDPMScheduler', 'DEISMultistepScheduler', 'DPMSolverSinglestepScheduler', 'DPMSolverMultistepScheduler', 'DPMSolverMultistepInverse', 'DPM++', 'DPM++ Karras', 'DPM++ 2M', 'DPM++ 2M Karras', 'DPM++ 2M SDE Karras', 'DPM++ 2M SDE', 'DPM++ 3M', 'DPM++ 3M Karras', 'DPM++ SDE Karras', 'DPM++ SDE', 'EDMEulerScheduler', 'EDMDPMSolverMultistepScheduler', 'Euler', 'EulerDiscreteScheduler', 'Euler Karras', 'Euler a', 'EulerAncestralDiscreteScheduler', 'FlowMatchEulerDiscreteScheduler', 'Heun', 'HeunDiscreteScheduler', 'Heun Karras', 'IPNDMScheduler', 'KDPM2DiscreteScheduler', 'KDPM2AncestralDiscreteScheduler', 'LCM', 'LCMScheduler', 'LMS', 'LMSDiscreteScheduler', 'LMS Karras', 'PNDMScheduler', 'TCDScheduler', 'UniPC', 'UniPCMultistepScheduler', 'UniPC Karras', 'UniPC 2M', 'UniPC 2M Karras', 'UniPC 3M', 'UniPC 3M Karras'], {
                    "tooltip": "An scheduler is a component that manages the inference process. Different schedulers can be used to achieve different results like more detailed images, faster inference, or more accurate results.",
                    "default": "Default",
                }),
                "cfgScale": ("FLOAT", {
                    "tooltip": "Guidance scale represents how closely the images will resemble the prompt or how much freedom the AI model has. Higher values are closer to the prompt. Low values may reduce the quality of the results.",
                    "default": 6.5,
                    "min": 1.0,
                    "max": 30.0,
                    "step": 0.5,
                }),
                "strength": ("INT", {
                    "default": 15,
                    "min": 15,
                    "max": 50,
                    "tooltip": "Controls the balance between preserving the subject's original features and the creative transformation specified in the prompt.\n- Lower values provide stronger subject fidelity.\n- Higher values allow more creative freedom in the transformation."
                }),
                "clipSkip": ("INT", {
                    "tooltip": "Enables skipping layers of the CLIP embedding process, leading to quicker and more varied image generation.",
                    "default": 0,
                    "min": 0,
                    "max": 2,
                }),
                "seed": ("INT", {
                    "tooltip": "A value used to randomize the image generation. If you want to make images reproducible (generate the same image multiple times), you can use the same seed value. Set to 0 to auto-generate a random seed.",
                    "default": 0,
                    "min": 0,
                    "max": 4294967295,
                }),
                "batchSize": ("INT", {
                    "tooltip": "The number of images to generate in a single request.",
                    "default": 1,
                    "min": 1,
                    "max": 10,
                }),
            },
            "optional": {
                "Image 2": ("IMAGE", {
                    "tooltip": "Specifies Input Image 2 that will be used as reference for the subject. These reference images help the AI to maintain identity consistency during the generation process."
                }),
                "Image 3": ("IMAGE", {
                    "tooltip": "Specifies Input Image 3 that will be used as reference for the subject. These reference images help the AI to maintain identity consistency during the generation process."
                }),
                "Image 4": ("IMAGE", {
                    "tooltip": "Specifies Input Image 4 that will be used as reference for the subject. These reference images help the AI to maintain identity consistency during the generation process."
                }),
            }
        }

    DESCRIPTION = "Transform and style images using PhotoMaker's advanced personalization technology. Create consistent, high-quality image variations with precise subject fidelity and style control."
    FUNCTION = "photoMaker"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("IMAGE",)
    CATEGORY = "Runware"

    @classmethod
    def VALIDATE_INPUTS(cls, positivePrompt, negativePrompt):
        if (positivePrompt is not None and (positivePrompt == "" or len(positivePrompt) < 3 or len(positivePrompt) > 2000)):
            raise Exception(
                "Positive Prompt Must Be Between 3 And 2000 characters!")
        if (negativePrompt is not None and negativePrompt != "" and (len(negativePrompt) < 3 or len(negativePrompt) > 2000)):
            raise Exception(
                "Negative Prompt Must Be Between 3 And 2000 characters!")
        return True

    def photoMaker(self, **kwargs):
        runwareModel = kwargs.get("Model")
        image1 = kwargs.get("Image 1")
        image2 = kwargs.get("Image 2", None)
        image3 = kwargs.get("Image 3", None)
        image4 = kwargs.get("Image 4", None)
        positivePrompt = kwargs.get("positivePrompt")
        negativePrompt = kwargs.get("negativePrompt", None)
        promptWeighting = kwargs.get("Prompt Weighting", "Disabled")
        style = kwargs.get("style", "No style")
        dimensions = kwargs.get("dimensions", "Square HD (1024x1024)")
        width = kwargs.get("width", 1024)
        height = kwargs.get("height", 1024)
        steps = kwargs.get("steps", 25)
        scheduler = kwargs.get("scheduler", "Default")
        cfgScale = kwargs.get("cfgScale", 6.5)
        strength = kwargs.get("strength", 15)
        clipSkip = kwargs.get("clipSkip", 0)
        seed = kwargs.get("seed")
        batchSize = kwargs.get("batchSize", 1)

        imageList = [rwUtils.convertTensor2IMG(image1)]
        if (image2 is not None):
            imageList.append(rwUtils.convertTensor2IMG(image2))
        if (image3 is not None):
            imageList.append(rwUtils.convertTensor2IMG(image3))
        if (image4 is not None):
            imageList.append(rwUtils.convertTensor2IMG(image4))

        genConfig = [
            {
                "taskType": "photoMaker",
                "taskUUID": rwUtils.genRandUUID(),
                "model": runwareModel,
                "inputImages": imageList,
                "positivePrompt": positivePrompt,
                "style": style,
                "strength": strength,
                "height": height,
                "width": width,
                "steps": steps,
                "scheduler": scheduler,
                "seed": seed,
                "CFGScale": cfgScale,
                "clipSkip": clipSkip,
                "numberResults": batchSize,
                "outputType": "URL",
                "outputFormat": rwUtils.OUTPUT_FORMAT,
                "outputQuality": rwUtils.OUTPUT_QUALITY,
            }
        ]

        if (negativePrompt is not None and negativePrompt != ""):
            genConfig[0]["negativePrompt"] = negativePrompt
        if (promptWeighting != "Disabled"):
            if (promptWeighting == "sdEmbeds"):
                genConfig[0]["promptWeighting"] = "sdEmbeds"
            else:
                genConfig[0]["promptWeighting"] = "compel"

        genResult = rwUtils.inferenecRequest(genConfig)
        images = rwUtils.extractImageURLs(genResult)
        return (images,)
