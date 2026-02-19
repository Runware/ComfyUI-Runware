"""
Runware Audio Settings Node
Provides lyrics and guidanceType settings for Runware Audio Inference
"""

from typing import Dict, Any


class RunwareAudioSettings:
    """Runware Audio Settings Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useLyrics": ("BOOLEAN", {
                    "tooltip": "Enable to include lyrics in audio generation settings",
                    "default": False,
                }),
                "lyrics": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "[verse] ... [chorus] ... (format like genius.com)",
                    "tooltip": "Lyrics for the audio generation. Format like lyrics from genius.com with [verse], [chorus], [refrain], etc.",
                }),
                "useGuidanceType": ("BOOLEAN", {
                    "tooltip": "Enable to include guidanceType (controls how guidance value is used)",
                    "default": False,
                }),
                "guidanceType": (["apg", "cfg"], {
                    "tooltip": "Controls how the guidance value is used. apg = Adversarial Perceptual Guidance, cfg = Classifier-Free Guidance",
                    "default": "apg",
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREAUDIOSETTINGS",)
    RETURN_NAMES = ("settings",)
    FUNCTION = "createSettings"
    CATEGORY = "Runware/Audio"
    DESCRIPTION = "Configure audio generation settings (lyrics, guidanceType) for Runware Audio Inference. Connect to Runware Audio Inference node."

    def createSettings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create audio settings dict for API"""
        use_lyrics = kwargs.get("useLyrics", False)
        lyrics = kwargs.get("lyrics", "")
        use_guidance_type = kwargs.get("useGuidanceType", False)
        guidance_type = kwargs.get("guidanceType", "apg")

        settings: Dict[str, Any] = {}

        if use_lyrics and lyrics and lyrics.strip():
            settings["lyrics"] = lyrics.strip()

        if use_guidance_type:
            settings["guidanceType"] = guidance_type

        return (settings,)


NODE_CLASS_MAPPINGS = {
    "RunwareAudioSettings": RunwareAudioSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareAudioSettings": "Runware Audio Settings",
}
