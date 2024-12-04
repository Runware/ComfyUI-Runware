from .utils import runwareUtils as rwUtils

class imageCaptioning:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Image": ("IMAGE", {
                        "tooltip": "Specifies the input image to be processed."
                }),
            },
            "optional": {
                "Image Description": ("STRING", {
                    "multiline": True,
                    "placeholder": "Don't Write Anything Here, The Image Description Will Be Generated Automatically.",
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

    def imageCaptioning(self, **kwargs):
        print(kwargs)
        image = kwargs.get("Image")
        kwargs.set("Image Description", "Don't Write Anything Here, The Image Description Will Be Generated Automatically.")
        genConfig = [
            {
                "taskType": "imageCaption",
                "taskUUID": rwUtils.genRandUUID(),
                "inputImage": rwUtils.convertTensor2IMG(image)
            }
        ]

        genResult = rwUtils.inferenecRequest(genConfig)
        genText = genResult["data"][0]["text"]
        return (genText, )