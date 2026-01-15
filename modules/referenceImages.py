from .utils import runwareUtils as rwUtils


class referenceImages:
    """Reference Images node for providing reference images for identity consistency"""
    
    MAX_IMAGES = 14
    
    @classmethod
    def INPUT_TYPES(cls):
        requiredInputs = {
            "Image 1": ("IMAGE", {
                "tooltip": "Specifies Reference Image 1 that will be used as reference for the subject. These reference images help the AI to maintain identity consistency during the generation process."
            }),
        }
        
        optionalInputs = {}
        for i in range(2, cls.MAX_IMAGES + 1):
            ordinal = rwUtils.getOrdinal(i)
            optionalInputs[f"Image {i}"] = ("IMAGE", {
                "tooltip": f"Specifies {ordinal.capitalize()} Reference Image that will be used as reference for the subject. These reference images help the AI to maintain identity consistency during the generation process."
            })
        
        return {
            "required": requiredInputs,
            "optional": optionalInputs
        }

    DESCRIPTION = "Used With Runware Tasks To Provide Reference Images For The Subject. These Reference Images Help The AI To Maintain Identity Consistency During The Generation Process."
    FUNCTION = "referenceImages"
    RETURN_TYPES = ("RUNWAREREFERENCEIMAGES",)
    RETURN_NAMES = ("Reference Images",)
    CATEGORY = "Runware"

    def referenceImages(self, **kwargs):
        """Collect and convert reference images to list"""
        imageList = []
        
        # Always include Image 1 (required)
        image1 = kwargs.get("Image 1")
        if image1 is not None:
            imageList.append(rwUtils.convertTensor2IMG(image1))
        
        # Add optional images 2 through MAX_IMAGES
        for i in range(2, self.MAX_IMAGES + 1):
            image = kwargs.get(f"Image {i}", None)
            if image is not None:
                imageList.append(rwUtils.convertTensor2IMG(image))

        return (imageList,)
