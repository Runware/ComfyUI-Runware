"""
Runware Audio Inference Settings Node
Provides lyrics, guidanceType, languageBoost, turbo, temperature, textNormalization,
bpm, keyScale, timeSignature, vocalLanguage, coverConditioningScale, repaintingStart,
and repaintingEnd for Runware Audio Inference.
"""

from typing import Dict, Any

_VOCAL_LANGUAGE_CODES = [
    "ar", "az", "bg", "bn", "ca", "cs", "da", "de", "el", "en", "es", "fa", "fi", "fr",
    "he", "hi", "hr", "ht", "hu", "id", "is", "it", "ja", "ko", "la", "lt", "ms", "ne",
    "nl", "no", "pa", "pl", "pt", "ro", "ru", "sa", "sk", "sr", "sv", "sw", "ta", "te",
    "th", "tl", "tr", "uk", "ur", "vi", "yue", "zh", "unknown",
]


class RunwareAudioSettings:
    """Runware Audio Inference Settings Node."""

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
                    "tooltip": "Controls how the guidance value is used. See API GuidanceType: apg | cfg.",
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
                "useBpm": ("BOOLEAN", {
                    "tooltip": "Enable to include bpm (tempo) in audio generation settings. If disabled, the model decides automatically.",
                    "default": False,
                }),
                "bpm": ("INT", {
                    "tooltip": "Beats per minute (30–300). If not set via API, the model decides. Common: 60–80 ballad, 90–110 pop, 120–130 house, 140–170 DnB. Only used when 'Use Bpm' is enabled.",
                    "default": 120,
                    "min": 30,
                    "max": 300,
                    "step": 1,
                }),
                "useKeyScale": ("BOOLEAN", {
                    "tooltip": "Enable to include keyScale (musical key and scale). Empty value lets the model decide.",
                    "default": False,
                }),
                "keyScale": ("STRING", {
                    "default": "",
                    "tooltip": "Musical key and scale. Empty string lets the model decide. Format: '{Note}{Accidental} {Mode}' (Note A–G, Accidental '' | '#' | 'b' | '♯' | '♭', Mode 'major' | 'minor'). Examples: 'C major', 'F# minor', 'B♭ major'.",
                }),
                "useTimeSignature": ("BOOLEAN", {
                    "tooltip": "Enable to include timeSignature (beats per measure). If disabled, the model decides automatically.",
                    "default": False,
                }),
                "timeSignature": (["", "2", "3", "4", "6"], {
                    "tooltip": "Time signature: '2' duple, '3' waltz, '4' common time, '6' compound duple. Empty = model decides. Most pop uses '4'. Only used when 'Use Time Signature' is enabled.",
                    "default": "",
                }),
                "useVocalLanguage": ("BOOLEAN", {
                    "tooltip": "Enable to include vocalLanguage (ISO 639-1) for vocal generation.",
                    "default": False,
                }),
                "vocalLanguage": (_VOCAL_LANGUAGE_CODES, {
                    "tooltip": "ISO 639-1 language code for vocals. Use 'unknown' for instrumental or automatic detection. Only used when 'Use Vocal Language' is enabled.",
                    "default": "en",
                }),
                "useCoverConditioningScale": ("BOOLEAN", {
                    "tooltip": "Enable to include coverConditioningScale (source-audio conditioning fraction for cover tasks). Only effective when input audio is provided.",
                    "default": False,
                }),
                "coverConditioningScale": ("FLOAT", {
                    "tooltip": "Fraction of denoising steps using source-audio conditioning (cover task). 1.0 = all steps; 0.5 = first half source then text-only. Only used when 'Use Cover Conditioning Scale' is enabled.",
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
                "useRepaintingStart": ("BOOLEAN", {
                    "tooltip": "Enable to include repaintingStart (seconds). Requires input audio. Sets repaint region with repaintingEnd; negative values prepend (outpaint before start).",
                    "default": False,
                }),
                "repaintingStart": ("FLOAT", {
                    "tooltip": "Start time in seconds for repaint/inpaint/outpaint region. Only used when 'Use Repainting Start' is enabled.",
                    "default": 0.0,
                    "step": 0.01,
                }),
                "useRepaintingEnd": ("BOOLEAN", {
                    "tooltip": "Enable to include repaintingEnd (seconds). Requires input audio. Values beyond source duration append (outpaint).",
                    "default": False,
                }),
                "repaintingEnd": ("FLOAT", {
                    "tooltip": "End time in seconds for repaint region. Only used when 'Use Repainting End' is enabled.",
                    "default": 0.0,
                    "step": 0.01,
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREAUDIOSETTINGS",)
    RETURN_NAMES = ("settings",)
    FUNCTION = "createSettings"
    CATEGORY = "Runware/Audio"
    DESCRIPTION = "Configure audio generation settings (lyrics, guidanceType, languageBoost, turbo, temperature, textNormalization, bpm, keyScale, timeSignature, vocalLanguage, coverConditioningScale, repaintingStart, repaintingEnd) for Runware Audio Inference. Connect to Runware Audio Inference node."

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
        use_bpm = kwargs.get("useBpm", False)
        bpm = kwargs.get("bpm", 120)
        use_key_scale = kwargs.get("useKeyScale", False)
        key_scale = kwargs.get("keyScale", "")
        use_time_signature = kwargs.get("useTimeSignature", False)
        time_signature = kwargs.get("timeSignature", "")
        use_vocal_language = kwargs.get("useVocalLanguage", False)
        vocal_language = kwargs.get("vocalLanguage", "en")
        use_cover_conditioning_scale = kwargs.get("useCoverConditioningScale", False)
        cover_conditioning_scale = kwargs.get("coverConditioningScale", 1.0)
        use_repainting_start = kwargs.get("useRepaintingStart", False)
        repainting_start = kwargs.get("repaintingStart", 0.0)
        use_repainting_end = kwargs.get("useRepaintingEnd", False)
        repainting_end = kwargs.get("repaintingEnd", 0.0)

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

        if use_bpm:
            settings["bpm"] = int(bpm)

        if use_key_scale:
            settings["keyScale"] = key_scale if key_scale is not None else ""

        if use_time_signature:
            settings["timeSignature"] = time_signature

        if use_vocal_language:
            settings["vocalLanguage"] = vocal_language

        if use_cover_conditioning_scale:
            settings["coverConditioningScale"] = round(float(cover_conditioning_scale), 2)

        if use_repainting_start:
            settings["repaintingStart"] = round(float(repainting_start), 2)

        if use_repainting_end:
            settings["repaintingEnd"] = round(float(repainting_end), 2)

        return (settings,)


NODE_CLASS_MAPPINGS = {
    "RunwareAudioSettings": RunwareAudioSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareAudioSettings": "Runware Audio Inference Settings",
}
