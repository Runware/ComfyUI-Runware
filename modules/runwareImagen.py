from .utils import runwareUtils as rwUtils

class runwareImagen:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Model": ([
                    "google:1@1 (Imagen 3)",
                    "google:1@2 (Imagen 3 Fast)",
                    "google:2@1 (Imagen 4 Preview)",
                    "google:2@2 (Imagen 4 Ultra)",
                    "google:2@3 (Imagen 4 Fast)",
                ], {
                    "tooltip": "Select The Google Imagen Model For Image Generation.",
                    "default": "google:1@1 (Imagen 3)",
                }),
                "positivePrompt": ("STRING", {
                    "multiline": True,
                    "placeholder": "Text instruction to guide the model on generating the image. It is usually a sentence or a paragraph that provides positive guidance for the task. This parameter is essential to shape the desired results.",
                    "tooltip": "Text instruction to guide the model on generating the image."
                }),
                "Aspect Ratio": ([
                    "1:1 (Square)",
                    "9:16 (Vertical)",
                    "16:9 (Wide)",
                    "3:4 (Portrait)",
                    "4:3 (Landscape)"
                ], {
                    "default": "1:1 (Square)",
                    "tooltip": "Adjust the dimensions of the generated image. The width and height will be automatically adjusted based on the selected aspect ratio.",
                }),
                "seed": ("INT", {
                    "tooltip": "A value used to randomize the image generation. If you want to make images reproducible (generate the same image multiple times), you can use the same seed value.",
                    "default": 0,
                    "min": 1,
                    "max": 9223372036854776000,
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
            }
        }

    @classmethod
    def VALIDATE_INPUTS(cls, positivePrompt):
        if (positivePrompt is not None and (positivePrompt == "" or len(positivePrompt) < 3 or len(positivePrompt) > 2000)):
            raise Exception(
                "Positive Prompt Must Be Between 3 And 2000 characters!")
        return True

    DESCRIPTION = "Generate Images Using Google Imagen Models."
    FUNCTION = "imagenInference"
    RETURN_TYPES = ("IMAGE", "RUNWARETASK")
    RETURN_NAMES = ("IMAGE", "RW-Task")
    CATEGORY = "Runware"

    def imagenInference(self, **kwargs):
        runwareModel = kwargs.get("Model")
        runwareModel = runwareModel.split(" ")[0]
        positivePrompt = kwargs.get("positivePrompt")
        aspectRatio = kwargs.get("Aspect Ratio")
        multiInferenceMode = kwargs.get("Multi Inference Mode", False)
        seed = kwargs.get("seed")
        batchSize = kwargs.get("batchSize", 1)

        aspectRatioMap = {
            "1:1": (1024, 1024),
            "9:16": (768, 1408),
            "16:9": (1408, 768),
            "3:4": (896, 1280),
            "4:3": (1280, 896),
        }

        secAspectRatio = aspectRatio.split(" ")[0]
        width, height  = aspectRatioMap.get(secAspectRatio, (1024, 1024))

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
                "numberResults": batchSize
            }
        ]

        # For Debugging Purposes Only
        print(f"[Debugging] Task UUID: {genConfig[0]['taskUUID']}")

        if (multiInferenceMode):
            return (None, genConfig)
        else:
            genResult = rwUtils.inferenecRequest(genConfig)
            images = rwUtils.convertImageB64List(genResult)
            return (images, None)
