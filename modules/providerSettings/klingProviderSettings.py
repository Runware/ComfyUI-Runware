"""
Runware KlingAI Provider Settings Node
Provides KlingAI-specific settings for video generation
"""

from typing import Optional, Dict, Any, List


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
                "useSound": ("BOOLEAN", {
                    "tooltip": "Enable to include sound parameter in provider settings",
                    "default": False,
                }),
                "sound": ("BOOLEAN", {
                    "tooltip": "Whether sound is generated simultaneously when generating a video",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useCharacterOrientation": ("BOOLEAN", {
                    "tooltip": "Enable to include characterOrientation parameter in provider settings",
                    "default": False,
                }),
                "characterOrientation": (["image", "video"], {
                    "tooltip": "Character orientation mode. 'image': has the same orientation as the person in the picture (reference video duration should not exceed 10 seconds). 'video': consistent with the orientation of the characters in the video (reference video duration should not exceed 30 seconds). Only used when 'Use Character Orientation' is enabled.",
                    "default": "image",
                }),
                "useMultiprompt": ("BOOLEAN", {
                    "tooltip": "Enable to include multiPrompt in provider settings. When enabled, connect Runware Kling MultiPrompt Segment nodes.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "MultiPrompt Segment 1": ("RUNWAREKLINGMULTIPROMPTSEGMENT", {
                    "tooltip": "Connect a Runware Kling MultiPrompt Segment. Only used when 'Use Multiprompt' is enabled.",
                }),
                "MultiPrompt Segment 2": ("RUNWAREKLINGMULTIPROMPTSEGMENT", {
                    "tooltip": "Connect a Runware Kling MultiPrompt Segment. Only used when 'Use Multiprompt' is enabled.",
                }),
                "MultiPrompt Segment 3": ("RUNWAREKLINGMULTIPROMPTSEGMENT", {
                    "tooltip": "Connect a Runware Kling MultiPrompt Segment. Only used when 'Use Multiprompt' is enabled.",
                }),
                "MultiPrompt Segment 4": ("RUNWAREKLINGMULTIPROMPTSEGMENT", {
                    "tooltip": "Connect a Runware Kling MultiPrompt Segment. Only used when 'Use Multiprompt' is enabled.",
                }),
                "MultiPrompt Segment 5": ("RUNWAREKLINGMULTIPROMPTSEGMENT", {
                    "tooltip": "Connect a Runware Kling MultiPrompt Segment. Only used when 'Use Multiprompt' is enabled.",
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("Provider Settings",)
    FUNCTION = "createProviderSettings"
    CATEGORY = "Runware/Provider Settings"
    DESCRIPTION = "Configure KlingAI-specific provider settings for video generation including camera control, audio volume, sound effects, ASMR mode, and sound generation."

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
        useSound = kwargs.get("useSound", False)
        useCharacterOrientation = kwargs.get("useCharacterOrientation", False)
        useMultiprompt = kwargs.get("useMultiprompt", False)

        # Get value parameters
        cameraControl = kwargs.get("cameraControl", "none")
        soundVolume = kwargs.get("soundVolume", 1.0)
        originalAudioVolume = kwargs.get("originalAudioVolume", 1.0)
        soundEffectPrompt = kwargs.get("soundEffectPrompt", "")
        bgmPrompt = kwargs.get("bgmPrompt", "")
        asmrMode = kwargs.get("asmrMode", False)
        keepOriginalSound = kwargs.get("keepOriginalSound", True)
        sound = kwargs.get("sound", False)
        characterOrientation = kwargs.get("characterOrientation", "image")

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

        # Add sound only if useSound is enabled
        if useSound:
            klingSettings["sound"] = sound

        # Add characterOrientation only if useCharacterOrientation is enabled
        if useCharacterOrientation and characterOrientation:
            klingSettings["characterOrientation"] = characterOrientation

        # Add multiPrompt only if useMultiprompt is enabled
        if useMultiprompt:
            segments: List[Dict[str, Any]] = []
            for i in range(1, 6):
                segment = kwargs.get(f"MultiPrompt Segment {i}")
                if segment is not None and isinstance(segment, dict):
                    prompt = segment.get("prompt", "").strip()
                    if prompt:
                        segments.append({
                            "prompt": prompt,
                            "duration": int(segment.get("duration", 4)),
                        })
            if segments:
                klingSettings["multiPrompt"] = segments

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


