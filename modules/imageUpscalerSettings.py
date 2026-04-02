"""
Runware Image Upscaler Settings — builds settings (enhanceDetails, realism). Connect to Runware Image Upscaler.
"""

from typing import Any, Dict, Tuple


class RunwareImageUpscalerSettings:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useEnhanceDetails": ("BOOLEAN", {
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                    "tooltip": "Include settings.enhanceDetails in the upscale request.",
                }),
                "enhanceDetails": ("BOOLEAN", {
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                    "tooltip": "Enhance fine textures and small details. May increase contrast and introduce minor deviations from the original.",
                }),
                "useRealism": ("BOOLEAN", {
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                    "tooltip": "Include settings.realism in the upscale request.",
                }),
                "realism": ("BOOLEAN", {
                    "default": True,
                    "label_on": "true",
                    "label_off": "false",
                    "tooltip": "Improve realism. May deviate more from the original. Recommended for AI-generated images.",
                }),
            },
        }

    RETURN_TYPES = ("RUNWAREIMAGEUPSCALERSETTINGS",)
    RETURN_NAMES = ("Upscaler Settings",)
    FUNCTION = "build_settings"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Optional settings.enhanceDetails and settings.realism for image upscale. "
        "Connect to Runware Image Upscaler."
    )

    def build_settings(self, **kwargs) -> Tuple[Dict[str, Any]]:
        out: Dict[str, Any] = {}

        settings: Dict[str, Any] = {}
        if kwargs.get("useEnhanceDetails", False):
            settings["enhanceDetails"] = bool(kwargs.get("enhanceDetails", False))
        if kwargs.get("useRealism", False):
            settings["realism"] = bool(kwargs.get("realism", True))
        if settings:
            out["settings"] = settings

        return (out,)
