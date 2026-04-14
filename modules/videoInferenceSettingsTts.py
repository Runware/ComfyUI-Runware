"""
Runware Video Inference Settings TTS
Exposes settings.tts fields (stability, similarityBoost) for Sync / ElevenLabs-style tuning.
Connect the output to Runware Video Inference Settings → tts.
"""

from typing import Dict, Any


class RunwareVideoInferenceSettingsTts:
    """Optional settings.tts block for video inference (Sync)."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useStability": ("BOOLEAN", {
                    "tooltip": "Enable to include stability in settings.tts.",
                    "default": False,
                }),
                "stability": ("FLOAT", {
                    "tooltip": "TTS stability (0–1). Optional Sync / ElevenLabs-style tuning. Only used when 'Use Stability' is enabled.",
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
                "useSimilarityBoost": ("BOOLEAN", {
                    "tooltip": "Enable to include similarityBoost in settings.tts.",
                    "default": False,
                }),
                "similarityBoost": ("FLOAT", {
                    "tooltip": "TTS similarity boost (0–1). Optional Sync / ElevenLabs-style tuning. Only used when 'Use Similarity Boost' is enabled.",
                    "default": 0.75,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
            },
        }

    RETURN_TYPES = ("RUNWAREVIDEOINFERENCESETTINGSTTS",)
    RETURN_NAMES = ("tts",)
    FUNCTION = "create"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Configure settings.tts (stability, similarityBoost) for Runware Video Inference. "
        "Connect to Runware Video Inference Settings → tts (Sync)."
    )

    def create(self, **kwargs) -> tuple[Dict[str, Any]]:
        tts: Dict[str, Any] = {}
        if kwargs.get("useStability", False):
            tts["stability"] = float(kwargs.get("stability", 0.5))
        if kwargs.get("useSimilarityBoost", False):
            tts["similarityBoost"] = float(kwargs.get("similarityBoost", 0.75))
        return (tts,)


NODE_CLASS_MAPPINGS = {
    "RunwareVideoInferenceSettingsTts": RunwareVideoInferenceSettingsTts,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVideoInferenceSettingsTts": "Runware Video Inference Settings TTS",
}
