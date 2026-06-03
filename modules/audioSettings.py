"""
Runware Audio Inference Settings Node
Provides lyrics, lyricsOptimizer, instrumental, guidanceType, languageBoost, turbo, temperature, textNormalization,
bpm, keyScale, timeSignature, vocalLanguage, coverConditioningScale, repaintingStart, repaintingEnd,
cfgIntervalStart, cfgIntervalEnd, xVectorOnly, maxNewTokens, maxTokens, transcript,
normalizeLoudness, topP, chunkLength, minChunkLength, normalize, latency, repetitionPenalty,
conditionOnPreviousChunks, earlyStopThreshold, and more for Runware Audio Inference.
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
                    "tooltip": "When voice cloning, keep prefix audio in output (true) or trim to new speech (false). Only relevant when compatible prefix/reference audio is provided. Only used when 'Use Include Prefix' is enabled.",
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
                "useInstrumental": ("BOOLEAN", {
                    "tooltip": "Enable to include instrumental in audio generation settings.",
                    "default": False,
                }),
                "instrumental": ("BOOLEAN", {
                    "tooltip": "When true, generates instrumental audio. For Music 2.6, this mode rejects settings.lyrics and settings.lyricsOptimizer, and positivePrompt becomes required.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useLyricsOptimizer": ("BOOLEAN", {
                    "tooltip": "Enable to include lyricsOptimizer in audio generation settings.",
                    "default": False,
                }),
                "lyricsOptimizer": ("BOOLEAN", {
                    "tooltip": "Provider-side lyric generation from prompt when lyrics is empty/omitted. Supported for non-instrumental Music 2.6 requests only; rejected when instrumental=true.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useCfgIntervalStart": ("BOOLEAN", {
                    "tooltip": "Enable to include cfgIntervalStart (diffusion ratio where CFG begins). ACE-Step Base only — not supported on Turbo variants.",
                    "default": False,
                }),
                "cfgIntervalStart": ("FLOAT", {
                    "tooltip": "Diffusion ratio where CFG begins (0.0 = first step). Only used when 'Use Cfg Interval Start' is enabled.",
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
                "useCfgIntervalEnd": ("BOOLEAN", {
                    "tooltip": "Enable to include cfgIntervalEnd (diffusion ratio where CFG ends). ACE-Step Base only — not supported on Turbo variants.",
                    "default": False,
                }),
                "cfgIntervalEnd": ("FLOAT", {
                    "tooltip": "Diffusion ratio where CFG ends (1.0 = last step). Only used when 'Use Cfg Interval End' is enabled.",
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
                "useNormalizeLoudness": ("BOOLEAN", {
                    "tooltip": "Enable to include normalizeLoudness in settings.",
                    "default": False,
                }),
                "normalizeLoudness": ("BOOLEAN", {
                    "tooltip": "Normalize output loudness for consistent perceived volume. Only used when 'Use Normalize Loudness' is enabled.",
                    "default": True,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useTopP": ("BOOLEAN", {
                    "tooltip": "Enable to include topP in settings.",
                    "default": False,
                }),
                "topP": ("FLOAT", {
                    "tooltip": "Controls diversity via nucleus sampling. Must be between 0.0001 and 1. Only used when 'Use Top P' is enabled.",
                    "default": 0.7,
                    "min": 0.0001,
                    "max": 1.0,
                    "step": 0.0001,
                }),
                "useChunkLength": ("BOOLEAN", {
                    "tooltip": "Enable to include chunkLength in settings.",
                    "default": False,
                }),
                "chunkLength": ("INT", {
                    "tooltip": "Text segment size for processing. Only used when 'Use Chunk Length' is enabled.",
                    "default": 300,
                    "min": 100,
                    "max": 300,
                    "step": 1,
                }),
                "useMinChunkLength": ("BOOLEAN", {
                    "tooltip": "Enable to include minChunkLength in settings.",
                    "default": False,
                }),
                "minChunkLength": ("INT", {
                    "tooltip": "Minimum characters before splitting into a new chunk. Only used when 'Use Min Chunk Length' is enabled.",
                    "default": 50,
                    "min": 0,
                    "max": 100,
                    "step": 1,
                }),
                "useNormalize": ("BOOLEAN", {
                    "tooltip": "Enable to include normalize in settings (text normalization for English and Chinese).",
                    "default": False,
                }),
                "normalize": ("BOOLEAN", {
                    "tooltip": "Normalizes text for English and Chinese, improving stability for numbers. Only used when 'Use Normalize' is enabled.",
                    "default": True,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useLatency": ("BOOLEAN", {
                    "tooltip": "Enable to include latency in settings.",
                    "default": False,
                }),
                "latency": (["low", "normal", "balanced"], {
                    "tooltip": "Latency / quality trade-off. normal = best quality, balanced = reduced latency, low = lowest latency. Only used when 'Use Latency' is enabled.",
                    "default": "normal",
                }),
                "useMaxTokens": ("BOOLEAN", {
                    "tooltip": "Enable to include maxTokens in settings (e.g. Fish Audio TTS).",
                    "default": False,
                }),
                "maxTokens": ("INT", {
                    "tooltip": "Maximum audio tokens to generate per text chunk. Only used when 'Use Max Tokens' is enabled.",
                    "default": 1024,
                    "min": 1,
                    "max": 4294967295,
                    "step": 1,
                }),
                "useRepetitionPenalty": ("BOOLEAN", {
                    "tooltip": "Enable to include repetitionPenalty in settings.",
                    "default": False,
                }),
                "repetitionPenalty": ("FLOAT", {
                    "tooltip": "Penalty for repeating audio patterns. Values above 1.0 reduce repetition. Only used when 'Use Repetition Penalty' is enabled.",
                    "default": 1.2,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.01,
                }),
                "useConditionOnPreviousChunks": ("BOOLEAN", {
                    "tooltip": "Enable to include conditionOnPreviousChunks in settings.",
                    "default": False,
                }),
                "conditionOnPreviousChunks": ("BOOLEAN", {
                    "tooltip": "Use previous audio as context for voice consistency across chunks. Only used when 'Use Condition On Previous Chunks' is enabled.",
                    "default": True,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useEarlyStopThreshold": ("BOOLEAN", {
                    "tooltip": "Enable to include earlyStopThreshold in settings.",
                    "default": False,
                }),
                "earlyStopThreshold": ("FLOAT", {
                    "tooltip": "Early stopping threshold for batch processing. Only used when 'Use Early Stop Threshold' is enabled.",
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREAUDIOSETTINGS",)
    RETURN_NAMES = ("settings",)
    FUNCTION = "createSettings"
    CATEGORY = "Runware/Audio"
    DESCRIPTION = (
        "Configure audio generation settings (lyrics, lyricsOptimizer, instrumental, guidanceType, languageBoost, turbo, temperature, textNormalization, "
        "bpm, keyScale, timeSignature, vocalLanguage, coverConditioningScale, repaintingStart, repaintingEnd, "
        "cfgIntervalStart, cfgIntervalEnd, xVectorOnly, maxNewTokens, maxTokens, transcript, "
        "normalizeLoudness, topP, chunkLength, minChunkLength, normalize, latency, repetitionPenalty, "
        "conditionOnPreviousChunks, earlyStopThreshold, etc.) "
        "for Runware Audio Inference. Connect to Runware Audio Inference node."
    )

    def createSettings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create audio settings dict for API"""
        use_temperature = kwargs.get("useTemperature", False)
        temperature = kwargs.get("temperature", 0.6)
        use_audio_temperature = kwargs.get("useAudioTemperature", False)
        audio_temperature = kwargs.get("audioTemperature", 0.8)
        use_top_k = kwargs.get("useTopK", False)
        top_k = kwargs.get("topK", 50)
        use_include_prefix = kwargs.get("useIncludePrefix", False)
        include_prefix = kwargs.get("includePrefix", False)
        use_lyrics = kwargs.get("useLyrics", False)
        lyrics = kwargs.get("lyrics", "")
        use_instrumental = kwargs.get("useInstrumental", False)
        instrumental = kwargs.get("instrumental", False)
        use_lyrics_optimizer = kwargs.get("useLyricsOptimizer", False)
        lyrics_optimizer = kwargs.get("lyricsOptimizer", False)
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
        use_cfg_interval_start = kwargs.get("useCfgIntervalStart", False)
        cfg_interval_start = kwargs.get("cfgIntervalStart", 0.0)
        use_cfg_interval_end = kwargs.get("useCfgIntervalEnd", False)
        cfg_interval_end = kwargs.get("cfgIntervalEnd", 1.0)
        use_normalize_loudness = kwargs.get("useNormalizeLoudness", False)
        use_top_p = kwargs.get("useTopP", False)
        top_p = kwargs.get("topP", 0.7)
        use_chunk_length = kwargs.get("useChunkLength", False)
        chunk_length = kwargs.get("chunkLength", 300)
        use_min_chunk_length = kwargs.get("useMinChunkLength", False)
        min_chunk_length = kwargs.get("minChunkLength", 50)
        use_normalize = kwargs.get("useNormalize", False)
        normalize = kwargs.get("normalize", True)
        use_latency = kwargs.get("useLatency", False)
        latency = kwargs.get("latency", "normal")
        use_max_tokens = kwargs.get("useMaxTokens", False)
        max_tokens = kwargs.get("maxTokens", 1024)
        use_repetition_penalty = kwargs.get("useRepetitionPenalty", False)
        repetition_penalty = kwargs.get("repetitionPenalty", 1.2)
        use_condition_on_previous_chunks = kwargs.get("useConditionOnPreviousChunks", False)
        use_early_stop_threshold = kwargs.get("useEarlyStopThreshold", False)
        early_stop_threshold = kwargs.get("earlyStopThreshold", 1.0)

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
        if use_instrumental:
            settings["instrumental"] = bool(instrumental)
        if use_lyrics_optimizer:
            settings["lyricsOptimizer"] = bool(lyrics_optimizer)

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

        if use_cfg_interval_start:
            settings["cfgIntervalStart"] = float(cfg_interval_start)

        if use_cfg_interval_end:
            settings["cfgIntervalEnd"] = float(cfg_interval_end)

        if use_normalize_loudness:
            settings["normalizeLoudness"] = bool(kwargs.get("normalizeLoudness", True))

        if use_top_p:
            settings["topP"] = float(top_p)

        if use_chunk_length:
            settings["chunkLength"] = int(chunk_length)

        if use_min_chunk_length:
            settings["minChunkLength"] = int(min_chunk_length)

        if use_normalize:
            settings["normalize"] = bool(normalize)

        if use_latency:
            settings["latency"] = str(latency)

        if use_max_tokens:
            settings["maxTokens"] = int(max_tokens)

        if use_repetition_penalty:
            settings["repetitionPenalty"] = float(repetition_penalty)

        if use_condition_on_previous_chunks:
            settings["conditionOnPreviousChunks"] = bool(kwargs.get("conditionOnPreviousChunks", True))

        if use_early_stop_threshold:
            settings["earlyStopThreshold"] = float(early_stop_threshold)

        return (settings,)


NODE_CLASS_MAPPINGS = {
    "RunwareAudioSettings": RunwareAudioSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareAudioSettings": "Runware Audio Inference Settings",
}
