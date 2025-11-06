from .utils import runwareUtils as rwUtils

class runwareKontext:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Model": ([
                    "bfl:3@1 (FLUX.1 Kontext Pro)",
                    "bfl:4@1 (FLUX.1 Kontext Max)",
                ], {
                    "tooltip": "Select The Model You Want For Image Generation or Image Editing.",
                    "default": "bfl:3@1 (FLUX.1 Kontext Pro)",
                }),
                "positivePrompt": ("STRING", {
                    "multiline": True,
                    "placeholder": "Text instruction to guide the model on generating the image. It is usually a sentence or a paragraph that provides positive guidance for the task. This parameter is essential to shape the desired results.\n\nYou Can Press (Ctrl + Alt + E) To Enhance The Prompt!",
                    "tooltip": "Text instruction to guide the model on generating the image. You Can Also Press (Ctrl + Alt + E) To Enhance The Prompt!"
                }),
                "Prompt Upsampling": ("BOOLEAN", {
                    "tooltip": "If Enabled it Will automatically modify the prompt at generation time for more creative results.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "Aspect Ratio": ([
                    "21:9 (Ultra-Wide / Landscape)",
                    "16:9 (Wide / Landscape)",
                    "4:3 (Standard / Landscape)",
                    "3:2 (Classic Photo / Landscape)",
                    "1:1 (Square)",
                    "2:3 (Classic Photo / Portrait)",
                    "3:4 (Standard / Portrait)",
                    "9:16 (Vertical Video / Portrait)",
                    "9:21 (Ultra-Tall / Portrait)"
                ], {
                    "default": "16:9 (Wide / Landscape)",
                    "tooltip": "Adjust the dimensions of the generated image. This setting allows you to choose from various aspect ratios, such as 16:9 for wide images or 1:1 for square images. The width and height will be automatically adjusted based on the selected aspect ratio.",
                }),
                "seed": ("INT", {
                    "tooltip": "A value used to randomize the image generation. If you want to make images reproducible (generate the same image multiple times), you can use the same seed value. Set to 0 to auto-generate a random seed.",
                    "default": 0,
                    "min": 0,
                    "max": 4294967295,
                }),
                "Multi Inference Mode": ("BOOLEAN", {
                    "tooltip": "If Enabled the node will skip the image generation process and will only return the Runware Task Object to be used in the Multi Inference Node.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "batchSize": ("INT", {
                    "tooltip": "The number of images to generate in a single request.",
                    "default": 1,
                    "min": 1,
                    "max": 10,
                }),
            },
            "optional": {
                "Reference Images": ("RUNWAREREFERENCEIMAGES", {
                    "tooltip": "Connect a Runware Reference Images Node to use reference images for image editing or generation.",
                }),
            }
        }

    @classmethod
    def VALIDATE_INPUTS(cls, positivePrompt):
        if (positivePrompt is not None and (positivePrompt == "" or len(positivePrompt) < 3 or len(positivePrompt) > 2000)):
            raise Exception(
                "Positive Prompt Must Be Between 3 And 2000 characters!")
        return True

    DESCRIPTION = "Generate And Edit Images Using Runware BFL Kontext Models."
    FUNCTION = "kontextInference"
    RETURN_TYPES = ("IMAGE", "RUNWARETASK")
    RETURN_NAMES = ("IMAGE", "RW-Task")
    CATEGORY = "Runware"

    def kontextInference(self, **kwargs):
        runwareModel = kwargs.get("Model")
        runwareModel = runwareModel.split(" ")[0]
        positivePrompt = kwargs.get("positivePrompt")
        promptUpsampling = kwargs.get("Prompt Upsampling")
        aspectRatio = kwargs.get("Aspect Ratio")
        multiInferenceMode = kwargs.get("Multi Inference Mode", False)
        referenceImages = kwargs.get("Reference Images", None)
        seed = kwargs.get("seed")
        batchSize = kwargs.get("batchSize", 1)

        aspectRatioMap = {
            "21:9": (1568, 672),
            "16:9": (1392, 752),
            "4:3": (1184, 880),
            "3:2": (1248, 832),
            "1:1": (1024, 1024),
            "2:3": (832, 1248),
            "3:4": (880, 1184),
            "9:16": (752, 1392),
            "9:21": (672, 1568),
        }

        secAspectRatio = aspectRatio.split(" ")[0]
        width, height = aspectRatioMap.get(secAspectRatio, (1024, 1024))

        genConfig = [
            {
                "taskType": "imageInference",
                "taskUUID": rwUtils.genRandUUID(),
                "positivePrompt": positivePrompt,
                "height": height,
                "width": width,
                "model": runwareModel,
                "seed": seed,
                "outputType": "base64Data",
                "outputFormat": rwUtils.OUTPUT_FORMAT,
                "outputQuality": rwUtils.OUTPUT_QUALITY,
                "numberResults": batchSize,
            }
        ]

        if (referenceImages is not None):
            genConfig[0]["referenceImages"] = referenceImages

        if (promptUpsampling):
            genConfig[0]["providerSettings"] = {
                "bfl": {
                    "promptUpsampling": True
                }
            }

        # For Debugging Purposes Only
        print(f"[Debugging] Task UUID: {genConfig[0]['taskUUID']}")

        if (multiInferenceMode):
            return (None, genConfig)
        else:
            genResult = rwUtils.inferenecRequest(genConfig)
            images = rwUtils.convertImageB64List(genResult)
            return (images, None)
