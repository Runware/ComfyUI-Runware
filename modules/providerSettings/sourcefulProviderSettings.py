"""
Runware Sourceful Provider Settings Node
Provides Sourceful-specific settings for image generation (providerSettings.sourceful.*)
"""

from typing import Dict, Any, List


class RunwareSourcefulProviderSettings:
    """Runware Sourceful Provider Settings Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useTransparency": ("BOOLEAN", {
                    "tooltip": "Enable to include transparency parameter in API request",
                    "default": False,
                }),
                "transparency": ("BOOLEAN", {
                    "tooltip": "Transparency setting for image generation. Only used when 'Use Transparency' is enabled.",
                    "default": False,
                }),
                "useEnhancePrompt": ("BOOLEAN", {
                    "tooltip": "Enable to include enhancePrompt parameter in API request",
                    "default": False,
                }),
                "enhancePrompt": ("BOOLEAN", {
                    "tooltip": "When true, enhances the provided prompt. Only used when 'Use Enhance Prompt' is enabled.",
                    "default": True,
                }),
                "fontInputs": ("RUNWARESOURCEFULFONTINPUTS", {
                    "tooltip": "Connect Runware Sourceful Provider Settings Fonts node to provide font references (fontUrl and text). Up to 2 fonts.",
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("providerSettings",)
    FUNCTION = "create_provider_settings"
    CATEGORY = "Runware/Provider Settings"
    DESCRIPTION = "Configure Sourceful-specific provider settings for image generation: transparency, enhancePrompt, and font inputs."

    def create_provider_settings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create Sourceful provider settings"""

        useTransparency = kwargs.get("useTransparency", False)
        transparency = kwargs.get("transparency", False)
        useEnhancePrompt = kwargs.get("useEnhancePrompt", False)
        enhancePrompt = kwargs.get("enhancePrompt", True)
        font_inputs = kwargs.get("fontInputs", None)

        settings: Dict[str, Any] = {}

        if useTransparency:
            settings["transparency"] = transparency
        if useEnhancePrompt:
            settings["enhancePrompt"] = enhancePrompt
        if font_inputs is not None and isinstance(font_inputs, list) and len(font_inputs) > 0:
            settings["fontInputs"] = font_inputs

        return (settings,)


NODE_CLASS_MAPPINGS = {
    "RunwareSourcefulProviderSettings": RunwareSourcefulProviderSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareSourcefulProviderSettings": "Runware Sourceful Provider Settings",
}
