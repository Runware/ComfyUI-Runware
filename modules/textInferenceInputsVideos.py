"""Runware Text Inference Inputs Videos — builds inputs.videos (URL or mediaUUID per item)."""

from typing import Any, Dict, List, Tuple

from .utils import runwareUtils as rwUtils


class RunwareTextInferenceInputsVideos:
    """Collect video references for textInference task.inputs.videos."""

    _MAX_VIDEOS = 4

    @classmethod
    def INPUT_TYPES(cls):
        optional: Dict[str, tuple] = {
            "useVideos": ("BOOLEAN", {
                "default": False,
                "tooltip": "Enable to include inputs.videos in the text inference request.",
            }),
        }
        for i in range(1, cls._MAX_VIDEOS + 1):
            ordinal = rwUtils.getOrdinal(i)
            optional[f"Video{i}"] = ("STRING", {
                "default": "",
                "tooltip": f"Video URL or mediaUUID for the {ordinal} video. Only used when 'Use Videos' is enabled.",
            })
        return {"required": {}, "optional": optional}

    RETURN_TYPES = ("RUNWARETEXTINFERENCEINPUTSVIDEOS",)
    RETURN_NAMES = ("videos",)
    FUNCTION = "createVideos"
    CATEGORY = "Runware/Text"
    DESCRIPTION = (
        "Collect one or more video references (URL or mediaUUID) for Runware Text Inference "
        "inputs.videos. Connect the output to Runware Text Inference Inputs."
    )

    def createVideos(self, **kwargs) -> Tuple[Dict[str, Any], ...]:
        if not kwargs.get("useVideos", False):
            return ({},)

        urls: List[str] = []
        for i in range(1, self._MAX_VIDEOS + 1):
            raw = kwargs.get(f"Video{i}", "")
            if raw is not None and str(raw).strip():
                urls.append(str(raw).strip())

        if not urls:
            return ({},)

        return ({"videos": urls},)
