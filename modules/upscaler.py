from .utils import runwareUtils as rwUtils

class upscaler:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Image": ("IMAGE", {
                        "tooltip": "Specifies the input image to be upscaled."
                }),
                "upscaleFactor": ("INT", {
                    "tooltip": "Each level will increase the size of the image by the corresponding factor.",
                    "default": 2,
                    "min": 2,
                    "max": 4,
                }),
            },
        }

    DESCRIPTION = "Enhance the resolution and quality of your images using Runware's advanced upscaling API. Transform low-resolution images into sharp, high-definition visuals."
    FUNCTION = "upscale"
    RETURN_TYPES = ("IMAGE",)
    CATEGORY = "Runware"

    def upscale(self, **kwargs):
        image = kwargs.get("Image")
        upscaleFactor = kwargs.get("upscaleFactor", 2)

        genConfig = [
            {
                "taskType": "imageUpscale",
                "taskUUID": rwUtils.genRandUUID(),
                "inputImage": rwUtils.convertTensor2IMG(image),
                "upscaleFactor": upscaleFactor,
                "outputFormat": rwUtils.OUTPUT_FORMAT,
                "outputQuality": rwUtils.OUTPUT_QUALITY,
                "outputType": "base64Data",
            }
        ]

        genResult = rwUtils.inferenecRequest(genConfig)
        images = rwUtils.convertImageB64List(genResult)
        return (images, )