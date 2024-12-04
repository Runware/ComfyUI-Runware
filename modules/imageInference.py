from .utils import runwareUtils as rwUtils

class txt2img:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Model": ("RUNWAREMODEL", {
                    "tooltip": "Connect a Runware Model From Runware Model Node.",
                }),
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
                "Prompt Weighting": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Prompt weighting allows you to adjust how strongly different parts of your prompt influence the generated image.",
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "dimensions": ([
                    "Square (512x512)", "Square HD (1024x1024)", "Portrait 3:4 (768x1024)",
                    "Portrait 9:16 (576x1024)", "Landscape 4:3 (1024x768)",
                    "Landscape 16:9 (1024x576)", "Custom"
                ], {
                    "default": "Square (512x512)",
                    "tooltip": "Adjust the dimensions of the generated image by specifying its width and height in pixels, or select from the predefined options. Image dimensions must be multiples of 64 (e.g., 512x512, 1024x768).",
                }),
                "width": ("INT", {
                        "tooltip": "The Width of the image in pixels.",
                        "default": 512,
                        "min": 512,
                        "max": 2048,
                        "step": 64,
                }),
                "height": ("INT", {
                        "tooltip": "The Height of the image in pixels.",
                        "default": 512,
                        "min": 512,
                        "max": 2048,
                        "step": 64,
                    }),
                "steps": ("INT", {
                        "tooltip": "The number of steps is the number of iterations the model will perform to generate the image. The higher the number of steps, the more detailed the image will be. However, increasing the number of steps will also increase the time it takes to generate the image and may not always result in a better image.",
                        "default": 4,
                        "min": 1,
                        "max": 100,
                    }),
                "scheduler": ([
                        "Default", "DDIMScheduler", "DDIMInverseScheduler", "DDPMScheduler", "DEISMultistepScheduler",
                        "DPMSolverSinglestepScheduler", "DPMSolverMultistepScheduler", "DPMSolverMultistepInverse", "DPMSolverSDEScheduler", "HeunDiscreteScheduler", "KDPM2DiscreteScheduler", "KDPM2AncestralDiscreteScheduler", "KarrasVeScheduler", "LMSDiscreteScheduler", "PNDMScheduler", "ScoreSdeVeScheduler", "ScoreSdeVpScheduler", "IPNDMScheduler", "EulerDiscreteScheduler", "EulerAncestralDiscreteScheduler", "EDMEulerScheduler", "FlowMatchEulerDiscreteScheduler", "VQDiffusionScheduler", "UniPCMultistepScheduler", "RePaintScheduler", "DPM++ 2M Karras", "DPM++ 2M SDE Karras", "DPM++ 2M SDE", "DPM++ SDE Karras", "DPM++ SDE", "LCMScheduler", "EDMDPMSolverMultistepScheduler", "TCDScheduler"
                    ], {
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
                "seed": ("INT", {
                        "tooltip": "A value used to randomize the image generation. If you want to make images reproducible (generate the same image multiple times), you can use the same seed value.",
                        "default": rwUtils.genRandSeed(),
                        "min": 1,
                        "max": 9223372036854776000,
                    }),
                            "clipSkip": ("INT", {
                    "tooltip": "Enables skipping layers of the CLIP embedding process, leading to quicker and more varied image generation.",
                    "default": 0,
                    "min": 0,
                    "max": 2,
                }),
                "strength": ("FLOAT", {
                    "tooltip": "When doing Image-to-Image or Inpainting, this parameter is used to determine the influence of the seedImage image in the generated output. A lower value results in more influence from the original image, while a higher value allows more creative deviation.",
                    "default": 0.80,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
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
                "batchSize": ("INT", {
                        "tooltip": "The number of images to generate in a single request.",
                        "default": 1,
                        "min": 1,
                        "max": 10,
                }),
            },
            "optional": {
                "Lora": ("RUNWARELORA", {
                    "tooltip": "Connect a Runware Lora From Lora Search Node Or Lora Combine For Multiple Lora's Together.",
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
            }
        }

    @classmethod
    def VALIDATE_INPUTS(cls, positivePrompt, negativePrompt):
        if (positivePrompt is None or len(positivePrompt) < 3 or len(positivePrompt) > 2000):
            raise Exception("Positive Prompt Must Be Between 3 And 2000 characters!")
        if (negativePrompt is not None and negativePrompt != "" and (len(negativePrompt) < 3 or len(negativePrompt) > 2000)):
            raise Exception("Negative Prompt Must Be Between 3 And 2000 characters!")
        return True

    DESCRIPTION = "Generates Images Lightning Fast With Runware Image Inference Sonic Engine."
    FUNCTION = "generateImage"
    RETURN_TYPES = ("IMAGE",)
    CATEGORY = "Runware"

    def generateImage(self, **kwargs):
        runwareModel = kwargs.get("Model")
        positivePrompt = kwargs.get("positivePrompt")
        negativePrompt = kwargs.get("negativePrompt", None)
        promptWeighting = kwargs.get("Prompt Weighting", False)
        runwareControlNet = kwargs.get("ControlNet", None)
        runwareLora = kwargs.get("Lora", None)
        runwareRefiner = kwargs.get("Refiner", None)
        seedImage = kwargs.get("seedImage", None)
        seedImageStrength = kwargs.get("strength", 0.8)
        maskImage = kwargs.get("maskImage", None)
        enableMaskMargin = kwargs.get("Mask Margin", False)
        maskImageMargin = kwargs.get("maskMargin", 32)
        clipSkip = kwargs.get("clipSkip", 0)
        height = kwargs.get("height", 512)
        width = kwargs.get("width", 512)
        steps = kwargs.get("steps", 4)
        scheduler = kwargs.get("scheduler", "Default")
        cfgScale = kwargs.get("cfgScale", 6.5)
        seed = kwargs.get("seed")
        batchSize = kwargs.get("batchSize", 1)

        if(maskImage is not None and seedImage is None):
            raise Exception("Mask Image Requires Seed Image To Be Provided!")

        genConfig = [
            {
                "taskType": "imageInference",
                "taskUUID": rwUtils.genRandUUID(),
                "positivePrompt": positivePrompt,
                "height": height,
                "width": width,
                "model": runwareModel,
                "steps": steps,
                "CFGScale": cfgScale,
                "scheduler": scheduler,
                "clipSkip": clipSkip,
                "seed": seed,
                "outputFormat": "WEBP",
                "outputType": "base64Data",
                "numberResults": batchSize,
            }
        ]

        # For Debugging Purposes Only
        print(f"[Debugging] Task UUID: {genConfig[0]['taskUUID']}")

        if(negativePrompt is not None and negativePrompt != ""):
            genConfig[0]["negativePrompt"] = negativePrompt
        if(promptWeighting):
            genConfig[0]["promptWeighting"] = "sdEmbeds"
        if(runwareLora is not None):
            if(isinstance(runwareLora, list)):
                genConfig[0]["lora"] = runwareLora
            elif(isinstance(runwareLora, dict)):
                genConfig[0]["lora"] = [runwareLora]
        if(runwareControlNet is not None):
            genConfig[0]["controlNet"] = runwareControlNet
        if(runwareRefiner is not None):
            genConfig[0]["refiner"] = runwareRefiner
        if(seedImage is not None):
            seedImage = rwUtils.convertTensor2IMG(seedImage)
            genConfig[0]["seedImage"] = seedImage
            genConfig[0]["strength"] = seedImageStrength
            if(maskImage is not None):
                maskImage = rwUtils.convertTensor2IMG(maskImage)
                genConfig[0]["maskImage"] = maskImage
                if(enableMaskMargin):
                    genConfig[0]["maskMargin"] = maskImageMargin

        genResult = rwUtils.inferenecRequest(genConfig)
        images = rwUtils.convertImageB64List(genResult)
        return images