from ..utils import runwareUtils as rwUtils


class RunwareOpenAIProviderSettings:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "quality": (["auto", "high", "medium", "low"], {
                    "default": "auto",
                    "tooltip": "Quality setting for OpenAI DALL-E models.",
                }),
                "useBackground": (["enable", "disabled"], {
                    "default": "disabled",
                    "tooltip": "Enable to include background parameter in API request.",
                }),
                "background": (["transparent", "opaque"], {
                    "default": "opaque",
                    "tooltip": "Background setting for OpenAI image generation. Only used when 'Use Background' is enabled.",
                }),
                "useStyle": (["enable", "disabled"], {
                    "default": "disabled",
                    "tooltip": "Enable to include style parameter in API request.",
                }),
                "style": (["vivid", "natural"], {
                    "default": "vivid",
                    "tooltip": "Style setting for OpenAI DALL-E models. Only used when 'Use Style' is enabled.",
                }),
            }
        }

    DESCRIPTION = "Configure OpenAI-specific settings for image generation with quality, background, and style options."
    FUNCTION = "create_openai_settings"
    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("Provider Settings",)
    CATEGORY = "Runware"

    def create_openai_settings(self, **kwargs):
        quality = kwargs.get("quality", "auto")
        useBackground = kwargs.get("useBackground", "disabled")
        background = kwargs.get("background", "opaque")
        useStyle = kwargs.get("useStyle", "disabled")
        style = kwargs.get("style", "vivid")
        
        # Create OpenAI settings dictionary
        openai_settings = {
            "quality": quality,
        }
        
        # Add background only if enabled
        if useBackground == "enable":
            openai_settings["background"] = background
            
        # Add style only if enabled
        if useStyle == "enable":
            openai_settings["style"] = style
        
        print(f"[OpenAI Provider Settings] Created settings: {openai_settings}")
        return (openai_settings,)


# Node class mappings for ComfyUI registration
NODE_CLASS_MAPPINGS = {
    "RunwareOpenAIProviderSettings": RunwareOpenAIProviderSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareOpenAIProviderSettings": "Runware OpenAI Provider Settings",
}
