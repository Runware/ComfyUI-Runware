"""
Runware Image Inference Settings Prompt Enhance
Builds settings.promptEnhance for image inference (e.g. Ernie).
Connect the output to Runware Image Inference Settings → promptEnhance.
"""

from typing import Any, Dict, Tuple


class RunwareImageInferenceSettingsPromptEnhance:
    """Build settings.promptEnhance object (temperature, topP)."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useTemperature": ("BOOLEAN", {
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                    "tooltip": "Include temperature in settings.promptEnhance.",
                }),
                "temperature": ("FLOAT", {
                    "default": 1.2,
                    "min": 0.1,
                    "max": 5.0,
                    "step": 0.1,
                    "tooltip": (
                        "settings.promptEnhance.temperature (0.1–5). "
                        "Ernie-specific API default when omitted: 0.6."
                    ),
                }),
                "useTopP": ("BOOLEAN", {
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                    "tooltip": "Include topP in settings.promptEnhance.",
                }),
                "topP": ("FLOAT", {
                    "default": 0.95,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": (
                        "settings.promptEnhance.topP (0.1–1). "
                        "Ernie-specific API default when omitted: 0.95."
                    ),
                }),
            },
        }

    RETURN_TYPES = ("RUNWAREIMAGEINFERENCEPROMPTENHANCE",)
    RETURN_NAMES = ("promptEnhance",)
    FUNCTION = "build_prompt_enhance"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Build settings.promptEnhance (temperature, topP) for image inference. "
        "Connect to Runware Image Inference Settings."
    )

    def build_prompt_enhance(self, **kwargs) -> Tuple[Dict[str, Any]]:
        prompt_enhance: Dict[str, Any] = {}

        if kwargs.get("useTemperature", False):
            prompt_enhance["temperature"] = float(kwargs.get("temperature", 1.2))

        if kwargs.get("useTopP", False):
            prompt_enhance["topP"] = float(kwargs.get("topP", 0.95))

        return (prompt_enhance,)


NODE_CLASS_MAPPINGS = {
    "RunwareImageInferenceSettingsPromptEnhance": RunwareImageInferenceSettingsPromptEnhance,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareImageInferenceSettingsPromptEnhance": "Runware Image Inference Settings Prompt Enhance",
}
