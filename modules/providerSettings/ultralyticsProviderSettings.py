"""
Runware Image Inference Ultralytics Node
Provides Ultralytics-specific settings for image generation (providerSettings.ultralytics.*)
"""

from typing import Dict, Any


class RunwareUltralyticsProviderSettings:
    """Runware Image Inference Ultralytics - Ultralytics provider settings"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useMaskBlur": ("BOOLEAN", {
                    "tooltip": "Enable to include maskBlur parameter.",
                    "default": False,
                }),
                "maskBlur": ("INT", {
                    "default": 5,
                    "min": 0,
                    "max": 100,
                    "tooltip": "Mask feathering amount (0-100).",
                }),
                "useMaskPadding": ("BOOLEAN", {
                    "tooltip": "Enable to include maskPadding parameter.",
                    "default": False,
                }),
                "maskPadding": ("INT", {
                    "default": 5,
                    "min": 0,
                    "max": 20,
                    "tooltip": "Padding around face region (0-20).",
                }),
                "useConfidence": ("BOOLEAN", {
                    "tooltip": "Enable to include confidence parameter.",
                    "default": False,
                }),
                "confidence": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "Detection confidence threshold (0-1).",
                }),
                "usePositivePrompt": ("BOOLEAN", {
                    "tooltip": "Enable to include positivePrompt parameter.",
                    "default": False,
                }),
                "positivePrompt": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Prompt for diffusion model.",
                }),
                "useNegativePrompt": ("BOOLEAN", {
                    "tooltip": "Enable to include negativePrompt parameter.",
                    "default": False,
                }),
                "negativePrompt": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Negative prompt for model.",
                }),
                "useSteps": ("BOOLEAN", {
                    "tooltip": "Enable to include steps parameter.",
                    "default": False,
                }),
                "steps": ("INT", {
                    "default": 20,
                    "min": 1,
                    "max": 100,
                    "tooltip": "Number of diffusion steps (1-100).",
                }),
                "useCFGScale": ("BOOLEAN", {
                    "tooltip": "Enable to include CFGScale parameter.",
                    "default": False,
                }),
                "CFGScale": ("FLOAT", {
                    "default": 8.0,
                    "min": 0.0,
                    "max": 50.0,
                    "step": 0.1,
                    "tooltip": "Classifier-free guidance scale (0-50).",
                }),
                "useStrength": ("BOOLEAN", {
                    "tooltip": "Enable to include strength parameter.",
                    "default": False,
                }),
                "strength": ("FLOAT", {
                    "default": 0.3,
                    "min": 0.0001,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "Denoising strength (0.0001-1).",
                }),
            }
        }

    DESCRIPTION = "Configure Ultralytics-specific settings for Runware Image Inference. providerSettings.ultralytics.*"
    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("providerSettings",)
    FUNCTION = "create_provider_settings"
    CATEGORY = "Runware/Provider Settings"

    def create_provider_settings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create Ultralytics provider settings"""

        settings = {}

        if kwargs.get("useMaskBlur", False):
            settings["maskBlur"] = kwargs.get("maskBlur", 5)
        if kwargs.get("useMaskPadding", False):
            settings["maskPadding"] = kwargs.get("maskPadding", 5)
        if kwargs.get("useConfidence", False):
            settings["confidence"] = kwargs.get("confidence", 0.5)
        if kwargs.get("usePositivePrompt", False):
            val = kwargs.get("positivePrompt", "")
            if val is not None and str(val).strip():
                settings["positivePrompt"] = str(val).strip()
        if kwargs.get("useNegativePrompt", False):
            val = kwargs.get("negativePrompt", "")
            if val is not None and str(val).strip():
                settings["negativePrompt"] = str(val).strip()
        if kwargs.get("useSteps", False):
            settings["steps"] = kwargs.get("steps", 20)
        if kwargs.get("useCFGScale", False):
            settings["CFGScale"] = kwargs.get("CFGScale", 8.0)
        if kwargs.get("useStrength", False):
            settings["strength"] = kwargs.get("strength", 0.3)

        return (settings,)


NODE_CLASS_MAPPINGS = {
    "RunwareUltralyticsProviderSettings": RunwareUltralyticsProviderSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareUltralyticsProviderSettings": "Runware Image Inference Ultralytics",
}
