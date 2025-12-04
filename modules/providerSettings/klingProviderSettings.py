"""
Runware KlingAI Provider Settings Node
Provides KlingAI-specific settings for video generation
"""

from typing import Optional, Dict, Any


class RunwareKlingProviderSettings:
    """Runware KlingAI Provider Settings Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useCameraControl": ("BOOLEAN", {
                    "tooltip": "Enable to include cameraControl parameter in provider settings",
                    "default": False,
                }),
                "cameraControl": (["none", "static", "dynamic", "zoom_in", "zoom_out", "pan_left", "pan_right", "tilt_up", "tilt_down", "smooth"], {
                    "tooltip": "Camera control mode for KlingAI video generation",
                    "default": "none",
                }),
                "useSoundVolume": ("BOOLEAN", {
                    "tooltip": "Enable to include soundVolume parameter in provider settings",
                    "default": False,
                }),
                "soundVolume": ("FLOAT", {
                    "tooltip": "Background sound volume to mix with generated audio (provider key: soundVolume).",
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                }),
                "useOriginalAudioVolume": ("BOOLEAN", {
                    "tooltip": "Enable to include originalAudioVolume parameter in provider settings",
                    "default": False,
                }),
                "originalAudioVolume": ("FLOAT", {
                    "tooltip": "Original video volume mix level (provider key: originalAudioVolume). No effect if source has no audio.",
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                }),
                "useSoundEffectPrompt": ("BOOLEAN", {
                    "tooltip": "Enable to include soundEffectPrompt parameter in provider settings",
                    "default": False,
                }),
                "soundEffectPrompt": ("STRING", {
                    "multiline": True,
                    "tooltip": "Prompt describing the sound effect to generate",
                    "default": "",
                }),
                "useBgmPrompt": ("BOOLEAN", {
                    "tooltip": "Enable to include bgmPrompt parameter in provider settings",
                    "default": False,
                }),
                "bgmPrompt": ("STRING", {
                    "multiline": True,
                    "tooltip": "Prompt describing the background music to generate",
                    "default": "",
                }),
                "useAsmrMode": ("BOOLEAN", {
                    "tooltip": "Enable to include asmrMode parameter in provider settings",
                    "default": False,
                }),
                "asmrMode": ("BOOLEAN", {
                    "tooltip": "Enable ASMR mode for audio generation",
                    "default": False,
                }),
                "useKeepOriginalSound": ("BOOLEAN", {
                    "tooltip": "Enable to include keepOriginalSound parameter in provider settings",
                    "default": False,
                }),
                "keepOriginalSound": ("BOOLEAN", {
                    "tooltip": "Keep the original sound from the source video. Only used when 'Use Keep Original Sound' is enabled.",
                    "default": True,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("Provider Settings",)
    FUNCTION = "createProviderSettings"
    CATEGORY = "Runware/Provider Settings"
    DESCRIPTION = "Configure KlingAI-specific provider settings for video generation including camera control, audio volume, sound effects, and ASMR mode."

    def createProviderSettings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create KlingAI provider settings"""

        # Get control parameters
        useCameraControl = kwargs.get("useCameraControl", False)
        useSoundVolume = kwargs.get("useSoundVolume", False)
        useOriginalAudioVolume = kwargs.get("useOriginalAudioVolume", False)
        useSoundEffectPrompt = kwargs.get("useSoundEffectPrompt", False)
        useBgmPrompt = kwargs.get("useBgmPrompt", False)
        useAsmrMode = kwargs.get("useAsmrMode", False)
        useKeepOriginalSound = kwargs.get("useKeepOriginalSound", False)

        # Get value parameters
        cameraControl = kwargs.get("cameraControl", "none")
        soundVolume = kwargs.get("soundVolume", 1.0)
        originalAudioVolume = kwargs.get("originalAudioVolume", 1.0)
        soundEffectPrompt = kwargs.get("soundEffectPrompt", "")
        bgmPrompt = kwargs.get("bgmPrompt", "")
        asmrMode = kwargs.get("asmrMode", False)
        keepOriginalSound = kwargs.get("keepOriginalSound", True)

        # Build settings dictionary - only include what is enabled
        klingSettings: Dict[str, Any] = {}

        # Add cameraControl only if useCameraControl is enabled and not "none"
        if useCameraControl and cameraControl != "none":
            klingSettings["cameraControl"] = cameraControl

        # Add soundVolume only if useSoundVolume is enabled
        if useSoundVolume:
            klingSettings["soundVolume"] = float(soundVolume)

        # Add originalAudioVolume only if useOriginalAudioVolume is enabled
        if useOriginalAudioVolume:
            klingSettings["originalAudioVolume"] = float(originalAudioVolume)

        # Add soundEffectPrompt only if useSoundEffectPrompt is enabled and not empty
        if useSoundEffectPrompt and soundEffectPrompt and soundEffectPrompt.strip():
            klingSettings["soundEffectPrompt"] = soundEffectPrompt.strip()

        # Add bgmPrompt only if useBgmPrompt is enabled and not empty
        if useBgmPrompt and bgmPrompt and bgmPrompt.strip():
            klingSettings["bgmPrompt"] = bgmPrompt.strip()

        # Add asmrMode only if useAsmrMode is enabled
        if useAsmrMode:
            klingSettings["asmrMode"] = asmrMode

        # Add keepOriginalSound only if useKeepOriginalSound is enabled
        if useKeepOriginalSound:
            klingSettings["keepOriginalSound"] = keepOriginalSound

        # Clean up None values
        klingSettings = {k: v for k, v in klingSettings.items() if v is not None}

        # Return flat dictionary - will be wrapped by inference node with provider name (same pattern as video provider settings)
        return (klingSettings,)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareKlingProviderSettings": RunwareKlingProviderSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareKlingProviderSettings": "Runware KlingAI Provider Settings",
}


