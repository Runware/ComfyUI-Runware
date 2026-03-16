"""
Runware Video Inference Speech Input Node.
Provides voice and text for speech synthesis; connect to Runware Video Inference speech input.
"""

from typing import Any, Dict, Tuple


class RunwareVideoInferenceSpeechInput:
    """Runware Video Inference Speech Input Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useVoice": ("BOOLEAN", {
                    "tooltip": "Enable to include voice in speech synthesis.",
                    "default": False,
                }),
                "voice": ("STRING", {
                    "tooltip": "Voice ID for text-to-speech or speech-to-speech. Required when text script is provided. Only used when 'Use Voice' is enabled.",
                    "default": "",
                }),
                "useText": ("BOOLEAN", {
                    "tooltip": "Enable to include text in speech synthesis.",
                    "default": False,
                }),
                "text": ("STRING", {
                    "multiline": True,
                    "tooltip": "Text script for the avatar to speak. Requires voice. Mutually exclusive with audio-driven input. Only used when 'Use Text' is enabled.",
                    "default": "",
                }),
                "useSpeed": ("BOOLEAN", {
                    "tooltip": "Enable to set voice playback speed multiplier.",
                    "default": False,
                }),
                "speed": ("FLOAT", {
                    "tooltip": "Voice playback speed multiplier (0.5 - 1.5). Only used when 'Use Speed' is enabled.",
                    "default": 1.0,
                    "min": 0.5,
                    "max": 1.5,
                    "step": 0.05,
                }),
                "usePitch": ("BOOLEAN", {
                    "tooltip": "Enable to set voice pitch adjustment in semitones.",
                    "default": False,
                }),
                "pitch": ("FLOAT", {
                    "tooltip": "Voice pitch adjustment in semitones (-50 to 50). Only used when 'Use Pitch' is enabled.",
                    "default": 0.0,
                    "min": -50.0,
                    "max": 50.0,
                    "step": 0.5,
                }),
                "useLanguage": ("BOOLEAN", {
                    "tooltip": "Enable to set locale or accent hint for multilingual voices.",
                    "default": False,
                }),
                "language": ("STRING", {
                    "tooltip": "Locale or accent hint for multilingual voices, e.g. en-US. Only used when 'Use Language' is enabled.",
                    "default": "",
                }),
            },
        }

    RETURN_TYPES: Tuple[str] = ("RUNWAREVIDEOINFERENCESPEECHINPUT",)
    RETURN_NAMES = ("speech",)
    FUNCTION = "createSpeech"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Configure speech synthesis for Runware Video Inference. Connect to Runware Video Inference speech input. "
        "Speech is only sent when both voice and text are enabled and non-empty; otherwise the node outputs nothing. "
        "Optional fields (speed, pitch, language) are added only when their toggles are on."
    )

    def createSpeech(self, **kwargs) -> tuple:
        """Build speech dict for genConfig[0]['speech']. Only include non-empty values; return None unless both voice and text are present."""
        speech: Dict[str, Any] = {}

        voice = (kwargs.get("voice") or "").strip()
        if kwargs.get("useVoice") and voice:
            speech["voice"] = voice

        text = (kwargs.get("text") or "").strip()
        if kwargs.get("useText") and text:
            speech["text"] = text

        if kwargs.get("useSpeed"):
            speech["speed"] = float(kwargs.get("speed", 1.0))
        if kwargs.get("usePitch"):
            speech["pitch"] = float(kwargs.get("pitch", 0.0))
        if kwargs.get("useLanguage"):
            lang = (kwargs.get("language") or "").strip()
            if lang:
                speech["language"] = lang

        if "voice" not in speech or "text" not in speech:
            return (None,)
        return (speech,)


NODE_CLASS_MAPPINGS = {
    "RunwareVideoInferenceSpeechInput": RunwareVideoInferenceSpeechInput,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVideoInferenceSpeechInput": "Runware Video Inference Speech Input",
}
