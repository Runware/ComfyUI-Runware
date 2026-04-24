from typing import List
from .utils import runwareUtils as rwUtils


class RunwareVideoInputsReferenceImagesMultipleImagesConnector:
    """Collect up to 4 images for one referenceImages entry."""

    MAX_IMAGES = 4

    @classmethod
    def INPUT_TYPES(cls):
        optionalInputs = {}
        for i in range(1, cls.MAX_IMAGES + 1):
            optionalInputs[f"Image{i}"] = ("IMAGE", {
                "tooltip": f"Optional image {i} for this reference group.",
            })
        return {
            "required": {},
            "optional": optionalInputs,
        }

    DESCRIPTION = (
        "Collect up to 4 images for one referenceImages item. "
        "Connect this output to Images1/Images2/... on Runware Video Inference Inputs Reference Images."
    )
    FUNCTION = "createImages"
    RETURN_TYPES = ("RUNWAREVIDEOINPUTSREFERENCEMULTIIMAGES",)
    RETURN_NAMES = ("Images",)
    CATEGORY = "Runware"

    def createImages(self, **kwargs) -> tuple[List[str]]:
        images: List[str] = []
        for i in range(1, self.MAX_IMAGES + 1):
            image = kwargs.get(f"Image{i}")
            if image is not None:
                images.append(rwUtils.convertTensor2IMG(image))
        return (images,)


NODE_CLASS_MAPPINGS = {
    "RunwareVideoInputsReferenceImagesMultipleImagesConnector": RunwareVideoInputsReferenceImagesMultipleImagesConnector,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVideoInputsReferenceImagesMultipleImagesConnector": "Runware Video Inference Inputs Reference Images Multiple Images Connector",
}
