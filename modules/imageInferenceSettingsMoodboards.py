"""
Runware Image Inference Settings Moodboards
Builds settings.moodboards: list of { "id": "<uuid>", "strength": <number> }.
"""

from typing import Any, Dict, List, Tuple


class RunwareImageInferenceSettingsMoodboards:
    """Build moodboards list for image inference settings."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "id": ("STRING", {
                    "default": "",
                    "tooltip": "Moodboard UUID (settings.moodboards[].id).",
                }),
            },
            "optional": {
                "useStrength": ("BOOLEAN", {
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                    "tooltip": "Include strength in moodboards entry.",
                }),
                "strength": ("FLOAT", {
                    "default": 0.35,
                    "min": -0.5,
                    "max": 1.5,
                    "step": 0.01,
                    "tooltip": "Moodboard strength (-0.5 to 1.5). Only used when useStrength is enabled.",
                }),
            },
        }

    RETURN_TYPES = ("RUNWAREIMAGEINFERENCEMOODBOARDS",)
    RETURN_NAMES = ("moodboards",)
    FUNCTION = "build_moodboards"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Build settings.moodboards for image inference settings. "
        "Outputs one-element array with required id and optional strength."
    )

    def build_moodboards(self, **kwargs) -> Tuple[List[Dict[str, Any]]]:
        moodboard_id = str(kwargs.get("id") or "").strip()
        if not moodboard_id:
            return ([],)

        entry: Dict[str, Any] = {"id": moodboard_id}
        if kwargs.get("useStrength", False):
            entry["strength"] = float(kwargs.get("strength", 0.35))

        return ([entry],)
