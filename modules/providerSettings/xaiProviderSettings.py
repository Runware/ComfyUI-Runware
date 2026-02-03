"""
Runware xAI Provider Settings Node
Provides xAI-specific settings for image generation (providerSettings.xai.quality)
"""

from typing import Dict, Any


class RunwareXAIProviderSettings:
    """Runware xAI Provider Settings Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useQuality": ("BOOLEAN", {
                    "tooltip": "Enable to include quality parameter in API request.",
                    "default": False,
                }),
                "quality": (["low", "medium", "high"], {
                    "default": "medium",
                    "tooltip": "Quality of the output image. Can be low, medium, or high. Currently a no-op, reserved for future use.",
                }),
            }
        }

    DESCRIPTION = "Configure xAI-specific settings for image generation. providerSettings.xai.quality"
    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("providerSettings",)
    FUNCTION = "create_provider_settings"
    CATEGORY = "Runware/Provider Settings"

    def create_provider_settings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create xAI provider settings"""

        useQuality = kwargs.get("useQuality", False)
        quality = kwargs.get("quality", "medium")

        settings = {}

        if useQuality:
            settings["quality"] = quality

        return (settings,)


NODE_CLASS_MAPPINGS = {
    "RunwareXAIProviderSettings": RunwareXAIProviderSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareXAIProviderSettings": "Runware xAI Provider Settings",
}
