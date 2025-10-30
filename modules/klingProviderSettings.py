"""
Runware KlingAI Provider Settings Node
Provides KlingAI-specific settings for video generation
"""

from typing import Dict, Any


class RunwareKlingProviderSettings:
    """Runware KlingAI Provider Settings Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "soundVolume": ("FLOAT", {
                    "tooltip": "Background sound volume to mix with generated audio (provider key: soundVolume).",
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                }),
                "originalAudioVolume": ("FLOAT", {
                    "tooltip": "Original video volume mix level (provider key: originalAudioVolume). No effect if source has no audio.",
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("Provider Settings",)
    FUNCTION = "create_provider_settings"
    CATEGORY = "Runware"
    DESCRIPTION = "Configure KlingAI-specific provider settings for video generation including sound and original audio volume controls."

    def create_provider_settings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create KlingAI provider settings"""

        sound_volume = kwargs.get("soundVolume", None)
        original_audio_volume = kwargs.get("originalAudioVolume", None)

        kling_settings: Dict[str, Any] = {}

        if sound_volume is not None:
            kling_settings["soundVolume"] = float(sound_volume)
        if original_audio_volume is not None:
            kling_settings["originalAudioVolume"] = float(original_audio_volume)

        # Remove unset values
        kling_settings = {k: v for k, v in kling_settings.items() if v is not None}

        return (kling_settings,)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareKlingProviderSettings": RunwareKlingProviderSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareKlingProviderSettings": "Runware KlingAI Provider Settings",
}


