"""
Runware Audio Inference Inputs Reference Audio node.
Builds inputs.referenceVoices for zero-shot voice cloning (up to 4 entries).
"""

from typing import Any, Dict, List

from .utils import runwareUtils as rwUtils


class RunwareAudioInferenceReferenceVoices:
    """Build inputs.referenceVoices[] for Fish Audio and other TTS models."""

    MAX_REFERENCE_VOICES = 4

    @classmethod
    def INPUT_TYPES(cls):
        optional_inputs = {}
        for i in range(1, cls.MAX_REFERENCE_VOICES + 1):
            ordinal = rwUtils.getOrdinal(i)
            optional_inputs[f"useReferenceVoice{i}"] = ("BOOLEAN", {
                "default": False,
                "tooltip": f"Enable to include the {ordinal} reference voice in inputs.referenceVoices.",
            })
            optional_inputs[f"audio{i}"] = ("STRING", {
                "default": "",
                "tooltip": f"Reference audio clip ({ordinal}) as media UUID, URL, or base64. Required when enabled.",
            })
            optional_inputs[f"text{i}"] = ("STRING", {
                "multiline": True,
                "default": "",
                "tooltip": f"Transcript of the {ordinal} reference audio clip (1–1000 characters). Required when enabled.",
            })

        return {
            "required": {},
            "optional": optional_inputs,
        }

    RETURN_TYPES = ("RUNWAREAUDIOINFERENCEREFERENCEVOICES",)
    RETURN_NAMES = ("referenceVoices",)
    FUNCTION = "createReferenceVoices"
    CATEGORY = "Runware/Audio"
    DESCRIPTION = (
        "Configure inputs.referenceVoices for zero-shot voice cloning (up to 4 entries). "
        "Each entry: { \"audio\": \"<UUID/URL/base64>\", \"text\": \"<transcript>\" }. "
        "Connect to Runware Audio Inference Inputs."
    )

    def createReferenceVoices(self, **kwargs) -> tuple[List[Dict[str, Any]]]:
        reference_voices: List[Dict[str, Any]] = []

        for i in range(1, self.MAX_REFERENCE_VOICES + 1):
            if not kwargs.get(f"useReferenceVoice{i}", False):
                continue

            audio = (kwargs.get(f"audio{i}") or "").strip()
            text = (kwargs.get(f"text{i}") or "").strip()

            if not audio or not text:
                continue

            reference_voices.append({"audio": audio, "text": text})

        return (reference_voices,)


NODE_CLASS_MAPPINGS = {
    "RunwareAudioInferenceReferenceVoices": RunwareAudioInferenceReferenceVoices,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareAudioInferenceReferenceVoices": "Runware Audio Inference Inputs Reference Audio",
}
