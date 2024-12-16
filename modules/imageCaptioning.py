from .utils import runwareUtils as rwUtils

class imageCaptioning:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Always Recaption": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Enable this option to always recaption the image each time you run the workflow.",
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "Image": ("IMAGE", {
                    "tooltip": "Specify The Image to be Captioned."
                }),
            },
            "optional": {
                "Image Description": ("STRING", {
                    "multiline": True,
                    "placeholder": "You Don't Have to write Anything here.\nThe Image Description Will Be Generated Automatically.",
                }),
            },
            "hidden": { "node_id": "UNIQUE_ID" }
        }

    DESCRIPTION = "Image to text, also known as image captioning, allows you to obtain descriptive text prompts based on uploaded or previously generated images. This process is instrumental in generating textual descriptions that can be used to create additional images or provide detailed insights into visual content."

    FUNCTION = "imageCaptioning"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("IMAGE PROMPT",)
    CATEGORY = "Runware"
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(s, **kwargs):
        alwaysRecaption = kwargs.get("Always Recaption")
        if(alwaysRecaption):
            return float("NAN")
        return True

    def imageCaptioning(self, **kwargs):
        image = kwargs.get("Image")
        genConfig = [
            {
                "taskType": "imageCaption",
                "taskUUID": rwUtils.genRandUUID(),
                "inputImage": rwUtils.convertTensor2IMG(image)
            }
        ]

        genResult = rwUtils.inferenecRequest(genConfig)
        genText = genResult["data"][0]["text"]
        rwUtils.sendImageCaption(genText, kwargs.get("node_id"))
        return (genText, )