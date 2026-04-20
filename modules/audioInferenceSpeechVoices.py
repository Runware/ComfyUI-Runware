"""
Runware Audio Inference Speech Voices node:
Builds speech.voices[] for multi-speaker audio inference speech payloads.
"""

import re
from typing import Any, Dict, List


class RunwareAudioInferenceSpeechVoices:
    """Build speech.voices[] list for Runware Audio Inference."""

    MAX_VOICES = 4
    _SPEAKER_ALIAS_PATTERN = re.compile(r"^[A-Za-z0-9]+$")

    @classmethod
    def INPUT_TYPES(cls):
        optional_inputs = {}
        for i in range(1, cls.MAX_VOICES + 1):
            optional_inputs[f"useVoice{i}"] = ("BOOLEAN", {
                "default": i == 1,
                "tooltip": f"Enable to include speaker/voice pair #{i} in speech.voices.",
            })
            optional_inputs[f"speaker{i}"] = ("STRING", {
                "default": f"Speaker{i}",
                "tooltip": "Unique alphanumeric speaker alias (speech.voices[].speaker).",
            })
            optional_inputs[f"voice{i}"] = ("STRING", {
                "default": "",
                "tooltip": "Voice name for this speaker (speech.voices[].voice).",
            })

        return {
            "required": {},
            "optional": optional_inputs,
        }

    RETURN_TYPES = ("RUNWAREAUDIOINFERENCESPEECHVOICES",)
    RETURN_NAMES = ("voices",)
    FUNCTION = "createVoices"
    CATEGORY = "Runware/Audio"
    DESCRIPTION = (
        "Build speech.voices[] for multi-speaker synthesis. "
        "Each item contains speaker (unique alphanumeric alias) and voice name."
    )

    def createVoices(self, **kwargs) -> tuple[List[Dict[str, str]]]:
        voices: List[Dict[str, str]] = []
        seen_speakers = set()

        for i in range(1, self.MAX_VOICES + 1):
            use_voice = bool(kwargs.get(f"useVoice{i}", i == 1))
            if not use_voice:
                continue

            speaker = (kwargs.get(f"speaker{i}") or "").strip()
            voice = (kwargs.get(f"voice{i}") or "").strip()

            if not speaker or not voice:
                raise Exception(
                    f"Voice #{i} is enabled, but speaker{i} and voice{i} must both be provided."
                )
            if not self._SPEAKER_ALIAS_PATTERN.match(speaker):
                raise Exception(
                    f"speaker{i} must be alphanumeric only (got: '{speaker}')."
                )
            if speaker in seen_speakers:
                raise Exception(
                    f"Duplicate speaker alias '{speaker}'. Each speaker must be unique."
                )

            seen_speakers.add(speaker)
            voices.append({
                "speaker": speaker,
                "voice": voice,
            })

        return (voices,)


NODE_CLASS_MAPPINGS = {
    "RunwareAudioInferenceSpeechVoices": RunwareAudioInferenceSpeechVoices,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareAudioInferenceSpeechVoices": "Runware Audio Inference Speech Voices",
}
