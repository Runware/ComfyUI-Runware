"""
Runware Audio Inference Settings Node
Provides lyrics and guidanceType settings for Runware Audio Inference
"""

from typing import Dict, Any


class RunwareAudioSettings:
    """Runware Audio Inference Settings Node"""

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
                "useLanguageBoost": ("BOOLEAN", {
                    "tooltip": "Enable to include languageBoost (language detection setting) in audio generation settings",
                    "default": False,
                }),
                "languageBoost": ([
                    "auto", "Chinese", "Chinese,Yue", "English", "Arabic", "Russian", "Spanish", "French",
                    "Portuguese", "German", "Turkish", "Dutch", "Ukrainian", "Vietnamese", "Indonesian",
                    "Japanese", "Italian", "Korean", "Thai", "Polish", "Romanian", "Greek", "Czech",
                    "Finnish", "Hindi", "Bulgarian", "Danish", "Hebrew", "Malay", "Persian", "Slovak",
                    "Swedish", "Croatian", "Filipino", "Hungarian", "Norwegian", "Slovenian", "Catalan",
                    "Nynorsk", "Tamil", "Afrikaans",
                ], {
                    "tooltip": "Language detection setting for audio generation.",
                    "default": "auto",
                }),
                "useTurbo": ("BOOLEAN", {
                    "tooltip": "Enable to include turbo (select turbo model or not) in audio generation settings",
                    "default": False,
                }),
                "turbo": ("BOOLEAN", {
                    "tooltip": "When enabled, use turbo model. Only used when 'Use Turbo' is enabled.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREAUDIOSETTINGS",)
    RETURN_NAMES = ("settings",)
    FUNCTION = "createSettings"
    CATEGORY = "Runware/Audio"
    DESCRIPTION = "Configure audio generation settings (lyrics, guidanceType, languageBoost, turbo) for Runware Audio Inference. Connect to Runware Audio Inference node."

    def createSettings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create audio settings dict for API"""
        use_lyrics = kwargs.get("useLyrics", False)
        lyrics = kwargs.get("lyrics", "")
        use_guidance_type = kwargs.get("useGuidanceType", False)
        guidance_type = kwargs.get("guidanceType", "apg")
        use_language_boost = kwargs.get("useLanguageBoost", False)
        language_boost = kwargs.get("languageBoost", "auto")
        use_turbo = kwargs.get("useTurbo", False)
        turbo = kwargs.get("turbo", False)

        settings: Dict[str, Any] = {}

        if use_lyrics and lyrics and lyrics.strip():
            settings["lyrics"] = lyrics.strip()

        if use_guidance_type:
            settings["guidanceType"] = guidance_type

        if use_language_boost:
            settings["languageBoost"] = language_boost

        if use_turbo:
            settings["turbo"] = bool(turbo)  # API requires true/false

        return (settings,)


NODE_CLASS_MAPPINGS = {
    "RunwareAudioSettings": RunwareAudioSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareAudioSettings": "Runware Audio Inference Settings",
}
