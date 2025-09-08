from .utils import runwareUtils as rwUtils


class RunwarePixverseProviderSettings:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "effect": (["none", "boom drop", "zoom in", "zoom out", "pan left", "pan right", "tilt up", "tilt down"], {
                    "default": "none",
                    "tooltip": "Camera effect for Pixverse videos.",
                }),
                "cameraMovement": (["none", "static", "dynamic", "smooth"], {
                    "default": "none",
                    "tooltip": "Camera movement style for Pixverse videos.",
                }),
                "style": (["anime", "realistic", "cinematic", "artistic", "vintage", "modern"], {
                    "default": "realistic",
                    "tooltip": "Visual style for Pixverse videos.",
                }),
                "motionMode": (["normal", "slow", "fast", "smooth", "dynamic"], {
                    "default": "normal",
                    "tooltip": "Motion mode for Pixverse videos.",
                }),
                "soundEffectSwitch": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Enable or disable sound effects for Pixverse videos.",
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "soundEffectContent": ("STRING", {
                    "multiline": True,
                    "placeholder": "Sound effect description or content",
                    "tooltip": "Sound effect content for Pixverse videos.",
                }),
            }
        }

    DESCRIPTION = "Configure Pixverse-specific settings for video generation with effect, style, motion, and sound options."
    FUNCTION = "create_pixverse_settings"
    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("Provider Settings",)
    CATEGORY = "Runware"

    def create_pixverse_settings(self, **kwargs):
        effect = kwargs.get("effect", "none")
        cameraMovement = kwargs.get("cameraMovement", "none")
        style = kwargs.get("style", "realistic")
        motionMode = kwargs.get("motionMode", "normal")
        soundEffectSwitch = kwargs.get("soundEffectSwitch", False)
        soundEffectContent = kwargs.get("soundEffectContent", "")
        
        # Create Pixverse settings dictionary
        pixverse_settings = {
            "effect": effect,
            "cameraMovement": cameraMovement,
            "style": style,
            "motionMode": motionMode,
            "soundEffectSwitch": soundEffectSwitch,
        }
        
        # Only add soundEffectContent if it's not empty
        if soundEffectContent and soundEffectContent.strip():
            pixverse_settings["soundEffectContent"] = soundEffectContent
        
        # Remove "none" values to keep the settings clean
        pixverse_settings = {k: v for k, v in pixverse_settings.items() if v != "none" and v is not None}
        
        print(f"[Pixverse Provider Settings] Created settings: {pixverse_settings}")
        return (pixverse_settings,)


# Node class mappings for ComfyUI registration
NODE_CLASS_MAPPINGS = {
    "RunwarePixverseProviderSettings": RunwarePixverseProviderSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwarePixverseProviderSettings": "Runware Pixverse Provider Settings",
}
