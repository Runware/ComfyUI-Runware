"""Runware Text Inference Inputs — merge Images + Videos blocks into task.inputs for textInference."""

from typing import Any, Dict, Tuple


class RunwareTextInferenceInputs:
    """Merge Runware Text Inference Inputs Images and/or Videos into a single inputs dict."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "images": ("RUNWARETEXTINFERENCEINPUTSIMAGES", {
                    "tooltip": "Connect Runware Text Inference Inputs Images for inputs.images[].",
                }),
                "videos": ("RUNWARETEXTINFERENCEINPUTSVIDEOS", {
                    "tooltip": "Connect Runware Text Inference Inputs Videos for inputs.videos[].",
                }),
            },
        }

    RETURN_TYPES = ("RUNWARETEXTINFERENCEINPUTS",)
    RETURN_NAMES = ("inputs",)
    FUNCTION = "merge_inputs"
    CATEGORY = "Runware/Text"
    DESCRIPTION = (
        "Combine Runware Text Inference Inputs Images and/or Videos into inputs for Runware Text Inference "
        "(inputs.images, inputs.videos)."
    )

    def merge_inputs(self, **kwargs) -> Tuple[Dict[str, Any], ...]:
        images_block = kwargs.get("images")
        videos_block = kwargs.get("videos")

        out: Dict[str, Any] = {}

        if isinstance(images_block, dict) and images_block.get("images"):
            imgs = images_block["images"]
            if isinstance(imgs, list) and len(imgs) > 0:
                filtered_imgs = [str(x).strip() for x in imgs if x is not None and str(x).strip()]
                if filtered_imgs:
                    out["images"] = filtered_imgs

        if isinstance(videos_block, dict) and videos_block.get("videos"):
            vids = videos_block["videos"]
            if isinstance(vids, list) and len(vids) > 0:
                filtered_vids = [str(x).strip() for x in vids if x is not None and str(x).strip()]
                if filtered_vids:
                    out["videos"] = filtered_vids

        return (out,)
