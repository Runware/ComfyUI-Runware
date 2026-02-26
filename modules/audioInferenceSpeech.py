"""
Runware Audio Inference Speech node: builds the speech payload for Runware Audio Inference.
Connect its output to the "speech" input of Runware Audio Inference for speech synthesis (e.g. Minimax).
"""

from typing import Dict, Any


class RunwareAudioInferenceSpeech:
    """Builds speech payload (text, voice, speed, volume, pitch?, emotion?, tone?) for Runware Audio Inference."""

    EMOTIONS = [
        "happy", "sad", "angry", "fearful", "disgusted", "surprised",
        "calm", "fluent", "whisper",
    ]

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": "Hello, this is a test of the speech synthesis model.",
                    "tooltip": "Text to synthesize as speech (speech.text)",
                }),
                "voice": ("STRING", {
                    "default": "English_Whispering_girl",
                    "tooltip": "Voice identifier - see System Voice ID List (speech.voice)",
                }),
            },
            "optional": {
                "useSpeed": ("BOOLEAN", {"default": True, "tooltip": "Include speed (speech.speed)"}),
                "speed": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.5,
                    "max": 2.0,
                    "step": 0.01,
                    "tooltip": "Speech rate multiplier (speech.speed)",
                }),
                "useVolume": ("BOOLEAN", {"default": True, "tooltip": "Include volume (speech.volume)"}),
                "volume": ("FLOAT", {
                    "default": 1.0,
                    "min": 1.0,
                    "max": 10.0,
                    "step": 0.1,
                    "tooltip": "Volume level 1-10 (speech.volume)",
                }),
                "usePitch": ("BOOLEAN", {"default": False, "tooltip": "Include pitch (speech.pitch)"}),
                "pitch": ("FLOAT", {
                    "default": 0.0,
                    "min": -12.0,
                    "max": 12.0,
                    "step": 0.1,
                    "tooltip": "Pitch multiplier -12 to 12 (speech.pitch)",
                }),
                "useEmotion": ("BOOLEAN", {"default": False, "tooltip": "Include emotion (not available for speech.turbo)"}),
                "emotion": (cls.EMOTIONS, {"default": "calm", "tooltip": "Emotion for speech (speech.emotion)"}),
                "useTone": ("BOOLEAN", {"default": False, "tooltip": "Include pronunciation dictionary (speech.tone)"}),
                "tone": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "omg/oh my god\nother/other expansion",
                    "tooltip": "Pronunciation dictionary, one mapping per line (e.g. omg/oh my god)",
                }),
            }
        }

    RETURN_TYPES = ("RUNWARESPEECH",)
    RETURN_NAMES = ("speech",)
    FUNCTION = "createSpeech"
    CATEGORY = "Runware/Audio"
    DESCRIPTION = "Build speech parameters for Runware Audio Inference. Connect output to the 'speech' input of Runware Audio Inference."

    def createSpeech(self, **kwargs) -> tuple:
        """Build the speech object for the API (connect to Runware Audio Inference 'speech' input)."""
        text = (kwargs.get("text") or "").strip()
        voice = (kwargs.get("voice") or "").strip()
        use_speed = kwargs.get("useSpeed", True)
        speed = float(kwargs.get("speed", 1.0))
        use_volume = kwargs.get("useVolume", True)
        volume = float(kwargs.get("volume", 1.0))
        use_pitch = kwargs.get("usePitch", False)
        pitch = float(kwargs.get("pitch", 0.0))
        use_emotion = kwargs.get("useEmotion", False)
        emotion = kwargs.get("emotion", "calm")
        use_tone = kwargs.get("useTone", False)
        tone_str = kwargs.get("tone", "") or ""

        speech: Dict[str, Any] = {"text": text, "voice": voice}
        if use_speed:
            speech["speed"] = speed
        if use_volume:
            speech["volume"] = volume
        if use_pitch:
            speech["pitch"] = pitch
        if use_emotion:
            speech["emotion"] = emotion
        if use_tone and tone_str.strip():
            tone_lines = [s.strip() for s in tone_str.replace(",", "\n").split("\n") if s.strip()]
            if tone_lines:
                speech["tone"] = tone_lines

        return (speech,)


NODE_CLASS_MAPPINGS = {
    "RunwareAudioInferenceSpeech": RunwareAudioInferenceSpeech,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareAudioInferenceSpeech": "Runware Audio Inference Speech",
}
