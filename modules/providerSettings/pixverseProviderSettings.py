from ..utils import runwareUtils as rwUtils


class RunwarePixverseProviderSettings:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "useEffect": ("BOOLEAN", {
                    "tooltip": "Enable to include effect parameter in API request.",
                    "default": False,
                }),
                "effect": (["none", "boom drop", "zoom in", "zoom out", "pan left", "pan right", "tilt up", "tilt down"], {
                    "default": "none",
                    "tooltip": "Camera effect for Pixverse videos. Only used when 'Use Effect' is enabled.",
                }),
                "useCameraMovement": ("BOOLEAN", {
                    "tooltip": "Enable to include cameraMovement parameter in API request.",
                    "default": False,
                }),
                "cameraMovement": (["none", "static", "dynamic", "smooth"], {
                    "default": "none",
                    "tooltip": "Camera movement style for Pixverse videos. Only used when 'Use Camera Movement' is enabled.",
                }),
                "useStyle": ("BOOLEAN", {
                    "tooltip": "Enable to include style parameter in API request.",
                    "default": False,
                }),
                "style": (["anime", "realistic", "cinematic", "artistic", "vintage", "modern"], {
                    "default": "realistic",
                    "tooltip": "Visual style for Pixverse videos. Only used when 'Use Style' is enabled.",
                }),
                "useMotionMode": ("BOOLEAN", {
                    "tooltip": "Enable to include motionMode parameter in API request.",
                    "default": False,
                }),
                "motionMode": (["normal", "slow", "fast", "smooth", "dynamic"], {
                    "default": "normal",
                    "tooltip": "Motion mode for Pixverse videos. Only used when 'Use Motion Mode' is enabled.",
                }),
                "useSoundEffectSwitch": ("BOOLEAN", {
                    "tooltip": "Enable to include soundEffectSwitch parameter in API request.",
                    "default": False,
                }),
                "soundEffectSwitch": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Enable or disable sound effects for Pixverse videos. Only used when 'Use Sound Effect Switch' is enabled.",
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useSoundEffectContent": ("BOOLEAN", {
                    "tooltip": "Enable to include soundEffectContent parameter in API request.",
                    "default": False,
                }),
                "soundEffectContent": ("STRING", {
                    "multiline": True,
                    "placeholder": "Sound effect description or content",
                    "tooltip": "Sound effect content for Pixverse videos. Only used when 'Use Sound Effect Content' is enabled.",
                }),
                "useAudio": ("BOOLEAN", {
                    "tooltip": "Enable to include audio parameter in API request.",
                    "default": False,
                }),
                "audio": ("BOOLEAN", {
                    "tooltip": "Controls audio generation for Pixverse videos. Only used when 'Use Audio' is enabled.",
                    "default": False,
                }),
                "useMultiClip": ("BOOLEAN", {
                    "tooltip": "Enable to include multiClip parameter in API request.",
                    "default": False,
                }),
                "multiClip": ("BOOLEAN", {
                    "tooltip": "Multi-clip (Multi-shot) for Pixverse videos. Only used when 'Use Multi Clip' is enabled.",
                    "default": False,
                }),
                "useThinking": ("BOOLEAN", {
                    "tooltip": "Enable to include thinking parameter in API request.",
                    "default": False,
                }),
                "thinking": (["enabled", "disabled", "auto"], {
                    "tooltip": "Thinking option for Pixverse videos. Only used when 'Use Thinking' is enabled.",
                    "default": "auto",
                }),
            }
        }

    DESCRIPTION = "Configure Pixverse-specific settings for video generation with effect, style, motion, and sound options."
    FUNCTION = "create_pixverse_settings"
    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("Provider Settings",)
    CATEGORY = "Runware"

    def create_pixverse_settings(self, **kwargs):
        useEffect = kwargs.get("useEffect", False)
        effect = kwargs.get("effect", "none")
        useCameraMovement = kwargs.get("useCameraMovement", False)
        cameraMovement = kwargs.get("cameraMovement", "none")
        useStyle = kwargs.get("useStyle", False)
        style = kwargs.get("style", "realistic")
        useMotionMode = kwargs.get("useMotionMode", False)
        motionMode = kwargs.get("motionMode", "normal")
        useSoundEffectSwitch = kwargs.get("useSoundEffectSwitch", False)
        soundEffectSwitch = kwargs.get("soundEffectSwitch", False)
        useSoundEffectContent = kwargs.get("useSoundEffectContent", False)
        soundEffectContent = kwargs.get("soundEffectContent", "")
        useAudio = kwargs.get("useAudio", False)
        audio = kwargs.get("audio", False)
        useMultiClip = kwargs.get("useMultiClip", False)
        multiClip = kwargs.get("multiClip", False)
        useThinking = kwargs.get("useThinking", False)
        thinking = kwargs.get("thinking", "auto")
        
        # Create Pixverse settings dictionary - only include parameters if their use flags are enabled
        pixverse_settings = {}
        
        if useEffect:
            pixverse_settings["effect"] = effect
        if useCameraMovement:
            pixverse_settings["cameraMovement"] = cameraMovement
        if useStyle:
            pixverse_settings["style"] = style
        if useMotionMode:
            pixverse_settings["motionMode"] = motionMode
        if useSoundEffectSwitch:
            pixverse_settings["soundEffectSwitch"] = soundEffectSwitch
        if useSoundEffectContent and soundEffectContent and soundEffectContent.strip():
            pixverse_settings["soundEffectContent"] = soundEffectContent
        if useAudio:
            pixverse_settings["audio"] = audio
        if useMultiClip:
            pixverse_settings["multiClip"] = multiClip
        if useThinking:
            pixverse_settings["thinking"] = thinking
        
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
