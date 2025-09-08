from .utils import runwareUtils as rwUtils


class RunwareProviderSettings:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "customSettings": ("DICT", {
                    "tooltip": "Custom provider settings as a dictionary. Add any provider-specific parameters here.",
                    "default": {},
                }),
            }
        }

    DESCRIPTION = "Configure custom provider-specific settings for video and image generation. Add any provider parameters as a dictionary."
    FUNCTION = "create_provider_settings"
    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("Provider Settings",)
    CATEGORY = "Runware"

    def create_provider_settings(self, **kwargs):
        custom_settings = kwargs.get("customSettings", {})
        
        print(f"[Provider Settings] Custom settings: {custom_settings}")
        return (custom_settings,)


# Node class mappings for ComfyUI registration
NODE_CLASS_MAPPINGS = {
    "RunwareProviderSettings": RunwareProviderSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareProviderSettings": "Runware Provider Settings",
}
