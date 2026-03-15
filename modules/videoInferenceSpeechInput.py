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
        "Configure speech synthesis for Runware Video Inference (voice and text). "
        "Connect to Runware Video Inference speech input. Both voice and text must be set for speech to be included."
    )

    def createSpeech(self, **kwargs) -> tuple:
        """Build speech dict for genConfig[0]['speech']."""
        
        speech: Dict[str, Any] = {}
        if kwargs.get("useVoice"):
            speech["voice"] = kwargs.get("voice")
        if kwargs.get("useText"):
            speech["text"] = kwargs.get("text")
        if kwargs.get("useSpeed"):
            speech["speed"] = float(kwargs.get("speed", 1.0))
        if kwargs.get("usePitch"):
            speech["pitch"] = float(kwargs.get("pitch", 0.0))
        if kwargs.get("useLanguage"):
            lang = (kwargs.get("language") or "").strip()
            if lang:
                speech["language"] = lang

        return (speech or None,)


NODE_CLASS_MAPPINGS = {
    "RunwareVideoInferenceSpeechInput": RunwareVideoInferenceSpeechInput,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVideoInferenceSpeechInput": "Runware Video Inference Speech Input",
}
