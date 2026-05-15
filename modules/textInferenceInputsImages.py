"""Runware Text Inference Inputs Images — builds inputs.images from ComfyUI IMAGE tensors."""

from typing import Any, Dict, List, Tuple

from .utils import runwareUtils as rwUtils


class RunwareTextInferenceInputsImages:
    """Collect IMAGE tensors and convert them for textInference task.inputs.images.

    Each connected IMAGE is converted via runwareUtils.convertTensor2IMG, which returns
    either a cached mediaUUID (when caching is enabled) or a base64 data URI.
    """

    _MAX_IMAGES = 8

    @classmethod
    def INPUT_TYPES(cls):
        optional: Dict[str, tuple] = {}
        for i in range(1, cls._MAX_IMAGES + 1):
            ordinal = rwUtils.getOrdinal(i)
            optional[f"Image {i}"] = ("IMAGE", {
                "tooltip": (
                    f"{ordinal.capitalize()} image for the model. Connect a Load Image (or any IMAGE source) node. "
                    "Tensor is converted to base64 / mediaUUID before being sent to the API."
                ),
            })
        return {"required": {}, "optional": optional}

    RETURN_TYPES = ("RUNWARETEXTINFERENCEINPUTSIMAGES",)
    RETURN_NAMES = ("images",)
    FUNCTION = "createImages"
    CATEGORY = "Runware/Text"
    DESCRIPTION = (
        "Collect one or more IMAGE tensors (Load Image, generated images, etc.) for Runware Text Inference "
        "inputs.images. Connect the output to Runware Text Inference Inputs."
    )

    def createImages(self, **kwargs) -> Tuple[Dict[str, Any], ...]:
        urls: List[str] = []
        for i in range(1, self._MAX_IMAGES + 1):
            tensor = kwargs.get(f"Image {i}", None)
            if tensor is None:
                continue
            urls.append(rwUtils.convertTensor2IMG(tensor))

        if not urls:
            return ({},)

        return ({"images": urls},)
