"""
Runware Audio Inference Settings Node
Provides lyrics, guidanceType, languageBoost, turbo, temperature, textNormalization,
bpm, keyScale, timeSignature, vocalLanguage, coverConditioningScale, repaintingStart,
repaintingEnd, xVectorOnly, maxNewTokens, transcript, and more for Runware Audio Inference.
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
                    "tooltip": "Sampling temperature for text token generation. Lower values produce more coherent, predictable speech content. Higher values increase variety but risk artifacts. Set 0 for greedy decoding. Only used when 'Use Temperature' is enabled.",
                    "default": 0.6,
                    "min": 0.0,
                    "max": 5.0,
                    "step": 0.1,
                }),
                "useAudioTemperature": ("BOOLEAN", {
                    "tooltip": "Enable to include audioTemperature in audio generation settings",
                    "default": False,
                }),
                "audioTemperature": ("FLOAT", {
                    "tooltip": "Sampling temperature for audio token generation. Lower values produce cleaner, more stable audio. Higher values add expressiveness but may introduce noise. Set 0 for greedy decoding. Only used when 'Use Audio Temperature' is enabled.",
                    "default": 0.8,
                    "min": 0.0,
                    "max": 5.0,
                    "step": 0.1,
                }),
                "useTopK": ("BOOLEAN", {
                    "tooltip": "Enable to include topK token sampling in audio generation settings",
                    "default": False,
                }),
                "topK": ("INT", {
                    "tooltip": "Top-K candidates for both text and audio token sampling. Limits sampling to the K most likely next tokens at each step. Only used when 'Use Top K' is enabled.",
                    "default": 50,
                    "min": 1,
                    "max": 500,
                    "step": 1,
                }),
                "useIncludePrefix": ("BOOLEAN", {
                    "tooltip": "Enable to include includePrefix in audio generation settings",
                    "default": False,
                }),
                "includePrefix": ("BOOLEAN", {
                    "tooltip": "When voice cloning, keep prefix audio in output (true) or trim to new speech (false). Requires at least prefix_audio_speaker_1 input. Only used when 'Use Include Prefix' is enabled.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
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
                "timeSignature": ("INT", {
                    "default": 4,
                    "min": 1,
                    "max": 32,
                    "step": 1,
                    "tooltip": "Time signature as integer beats per bar (e.g. 2, 3, 4, 6). Only used when 'Use Time Signature' is enabled.",
                }),
                "useVocalLanguage": ("BOOLEAN", {
                    "tooltip": "Enable to include vocalLanguage (language code) for vocal generation. See dropdown for available codes.",
                    "default": False,
                }),
                "vocalLanguage": (_VOCAL_LANGUAGE_CODES, {
                    "tooltip": "Language code for vocals. Supports values from the dropdown list (including 'yue', 'zh', and 'unknown'). Use 'unknown' for instrumental or automatic detection. Only used when 'Use Vocal Language' is enabled.",
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
                "useXVectorOnly": ("BOOLEAN", {
                    "tooltip": "Enable to include xVectorOnly in audio generation settings.",
                    "default": False,
                }),
                "xVectorOnly": ("BOOLEAN", {
                    "tooltip": "true = speaker embedding only (no transcript needed, lower similarity). false = ICL mode (needs transcript, higher quality). Only used when 'Use X Vector Only' is enabled.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useMaxNewTokens": ("BOOLEAN", {
                    "tooltip": "Enable to include maxNewTokens (audio output token cap) in audio generation settings.",
                    "default": False,
                }),
                "maxNewTokens": ("INT", {
                    "tooltip": "Audio output token cap. Higher = longer audio, but risk of generation hangs. Applies to all variants. Only used when 'Use Max New Tokens' is enabled.",
                    "default": 4096,
                    "min": 1,
                    "max": 262144,
                    "step": 1,
                }),
                "useTranscript": ("BOOLEAN", {
                    "tooltip": "Enable to include transcript (reference audio transcript) in audio generation settings.",
                    "default": False,
                }),
                "transcript": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Transcript of the reference audio. Required for ICL mode; omit or leave empty for x-vector-only mode. Base variant only. Only used when 'Use Transcript' is enabled.",
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREAUDIOSETTINGS",)
    RETURN_NAMES = ("settings",)
    FUNCTION = "createSettings"
    CATEGORY = "Runware/Audio"
    DESCRIPTION = (
        "Configure audio generation settings (lyrics, guidanceType, languageBoost, turbo, temperature, textNormalization, "
        "bpm, keyScale, timeSignature, vocalLanguage, coverConditioningScale, repaintingStart, repaintingEnd, "
        "xVectorOnly, maxNewTokens, transcript, etc.) for Runware Audio Inference. Connect to Runware Audio Inference node."
    )

    def createSettings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create audio settings dict for API"""
        use_temperature = kwargs.get("useTemperature", False)
        temperature = kwargs.get("temperature", 1.0)
        use_audio_temperature = kwargs.get("useAudioTemperature", False)
        audio_temperature = kwargs.get("audioTemperature", 0.8)
        use_top_k = kwargs.get("useTopK", False)
        top_k = kwargs.get("topK", 50)
        use_include_prefix = kwargs.get("useIncludePrefix", False)
        include_prefix = kwargs.get("includePrefix", False)
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
        time_signature = kwargs.get("timeSignature", 4)
        use_vocal_language = kwargs.get("useVocalLanguage", False)
        vocal_language = kwargs.get("vocalLanguage", "en")
        use_cover_conditioning_scale = kwargs.get("useCoverConditioningScale", False)
        cover_conditioning_scale = kwargs.get("coverConditioningScale", 1.0)
        use_repainting_start = kwargs.get("useRepaintingStart", False)
        repainting_start = kwargs.get("repaintingStart", 0.0)
        use_repainting_end = kwargs.get("useRepaintingEnd", False)
        repainting_end = kwargs.get("repaintingEnd", 0.0)
        use_x_vector_only = kwargs.get("useXVectorOnly", False)
        x_vector_only = kwargs.get("xVectorOnly", False)
        use_max_new_tokens = kwargs.get("useMaxNewTokens", False)
        max_new_tokens = kwargs.get("maxNewTokens", 4096)
        use_transcript = kwargs.get("useTranscript", False)
        transcript = kwargs.get("transcript", "") or ""

        settings: Dict[str, Any] = {}

        if use_temperature:
            settings["temperature"] = float(temperature)
        if use_audio_temperature:
            settings["audioTemperature"] = float(audio_temperature)
        if use_top_k:
            settings["topK"] = int(top_k)
        if use_include_prefix:
            settings["includePrefix"] = bool(include_prefix)

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

        if use_key_scale and str(key_scale).strip():
            settings["keyScale"] = str(key_scale).strip()

        if use_time_signature:
            settings["timeSignature"] = int(time_signature)

        if use_vocal_language:
            settings["vocalLanguage"] = vocal_language

        if use_cover_conditioning_scale:
            settings["coverConditioningScale"] = float(cover_conditioning_scale)

        if use_repainting_start:
            settings["repaintingStart"] = float(repainting_start)

        if use_repainting_end:
            settings["repaintingEnd"] = float(repainting_end)

        if use_x_vector_only:
            settings["xVectorOnly"] = bool(x_vector_only)

        if use_max_new_tokens:
            settings["maxNewTokens"] = int(max_new_tokens)

        if use_transcript and transcript.strip():
            settings["transcript"] = transcript.strip()

        return (settings,)


NODE_CLASS_MAPPINGS = {
    "RunwareAudioSettings": RunwareAudioSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareAudioSettings": "Runware Audio Inference Settings",
}
