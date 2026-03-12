"""
Runware Audio Inference Settings Node
Provides lyrics, guidanceType, languageBoost, turbo, temperature, and textNormalization
settings for Runware Audio Inference.
"""

from typing import Dict, Any


class RunwareAudioSettings:
    """Runware Audio Inference Settings Node (lyrics, guidanceType, languageBoost, turbo, temperature, textNormalization)."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useTemperature": ("BOOLEAN", {
                    "tooltip": "Enable to include temperature in audio generation settings",
                    "default": False,
                }),
                "temperature": ("FLOAT", {
                    "tooltip": "Temperature value for audio generation. Higher values increase diversity, lower values make output more deterministic. Only used when 'Use Temperature' is enabled.",
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                }),
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
                    "auto", "zh", "yue", "en", "ar", "ru", "es", "fr", "pt", "de", "tr", "nl", "uk",
                    "vi", "id", "ja", "it", "ko", "th", "pl", "ro", "el", "cs", "fi", "hi", "bg", "da",
                    "he", "ms", "fa", "sk", "sv", "hr", "fil", "hu", "no", "sl", "ca", "nn", "ta", "af",
                ], {
                    "tooltip": "Language detection setting. Codes: zh, yue, en, ar, ru, es, fr, pt, de, tr, nl, uk, vi, id, ja, it, ko, th, pl, ro, el, cs, fi, hi, bg, da, he, ms, fa, sk, sv, hr, fil, hu, no, sl, ca, nn, ta, af, auto",
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
                "useTextNormalization": ("BOOLEAN", {
                    "tooltip": "Enable to include textNormalization (normalize text before synthesis) in audio generation settings",
                    "default": False,
                }),
                "textNormalization": ("BOOLEAN", {
                    "tooltip": "Normalize text (e.g. numbers, abbreviations) before synthesis to improve pronunciation. Only used when 'Use Text Normalization' is enabled.",
                    "default": True,
                    "label_on": "true",
                    "label_off": "false",
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREAUDIOSETTINGS",)
    RETURN_NAMES = ("settings",)
    FUNCTION = "createSettings"
    CATEGORY = "Runware/Audio"
    DESCRIPTION = "Configure audio generation settings (lyrics, guidanceType, languageBoost, turbo, temperature, textNormalization) for Runware Audio Inference. Connect to Runware Audio Inference node."

    def createSettings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create audio settings dict for API"""
        use_temperature = kwargs.get("useTemperature", False)
        temperature = kwargs.get("temperature", 1.0)
        use_lyrics = kwargs.get("useLyrics", False)
        lyrics = kwargs.get("lyrics", "")
        use_guidance_type = kwargs.get("useGuidanceType", False)
        guidance_type = kwargs.get("guidanceType", "apg")
        use_language_boost = kwargs.get("useLanguageBoost", False)
        language_boost = kwargs.get("languageBoost", "auto")
        use_turbo = kwargs.get("useTurbo", False)
        turbo = kwargs.get("turbo", False)
        use_text_normalization = kwargs.get("useTextNormalization", False)
        text_normalization = kwargs.get("textNormalization", True)

        settings: Dict[str, Any] = {}

        if use_temperature:
            settings["temperature"] = float(temperature)

        if use_lyrics and lyrics and lyrics.strip():
            settings["lyrics"] = lyrics.strip()

        if use_guidance_type:
            settings["guidanceType"] = guidance_type

        if use_language_boost:
            settings["languageBoost"] = language_boost

        if use_turbo:
            settings["turbo"] = bool(turbo)  # API requires true/false

        if use_text_normalization:
            settings["textNormalization"] = bool(text_normalization)

        return (settings,)


NODE_CLASS_MAPPINGS = {
    "RunwareAudioSettings": RunwareAudioSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareAudioSettings": "Runware Audio Inference Settings",
}
