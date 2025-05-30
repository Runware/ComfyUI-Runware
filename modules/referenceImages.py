from .utils import runwareUtils as rwUtils

class referenceImages:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
              "Image 1": ("IMAGE", {
                  "tooltip": "Specifies Reference Image 1 that will be used as reference for the subject. These reference images help the AI to maintain identity consistency during the generation process."
              }),
            },
            "optional": {
                "Image 2": ("IMAGE", {
                    "tooltip": "Specifies Reference Image 2 that will be used as reference for the subject. These reference images help the AI to maintain identity consistency during the generation process."
                }),
                "Image 3": ("IMAGE", {
                    "tooltip": "Specifies Reference Image 3 that will be used as reference for the subject. These reference images help the AI to maintain identity consistency during the generation process."
                }),
                "Image 4": ("IMAGE", {
                    "tooltip": "Specifies Reference Image 4 that will be used as reference for the subject. These reference images help the AI to maintain identity consistency during the generation process."
                }),
            }
        }

    DESCRIPTION = "Used With Runware Tasks To Provide Reference Images For The Subject. These Reference Images Help The AI To Maintain Identity Consistency During The Generation Process."
    FUNCTION = "referenceImages"
    RETURN_TYPES = ("RUNWAREREFERENCEIMAGES",)
    RETURN_NAMES = ("Reference Images",)
    CATEGORY = "Runware"

    def referenceImages(self, **kwargs):
        image1 = kwargs.get("Image 1")
        image2 = kwargs.get("Image 2", None)
        image3 = kwargs.get("Image 3", None)
        image4 = kwargs.get("Image 4", None)

        imageList = [rwUtils.convertTensor2IMG(image1)]
        if (image2 is not None):
            imageList.append(rwUtils.convertTensor2IMG(image2))
        if (image3 is not None):
            imageList.append(rwUtils.convertTensor2IMG(image3))
        if (image4 is not None):
            imageList.append(rwUtils.convertTensor2IMG(image4))

        return (imageList, )
