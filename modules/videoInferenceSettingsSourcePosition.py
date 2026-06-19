"""
Runware Video Inference Settings Source Position
Exposes settings.sourcePosition for placing source video within the output canvas.
Connect the output to Runware Video Inference Settings → sourcePosition.
"""

from typing import Dict, Any


class RunwareVideoInferenceSettingsSourcePosition:
    """Optional settings.sourcePosition block for video inference."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "width": ("FLOAT", {
                    "tooltip": "Width of the source video, as a fraction of the canvas width (max 2). Paired with height. Requires inputs.video and output width/height on the inference request.",
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.01,
                }),
                "height": ("FLOAT", {
                    "tooltip": "Height of the source video, as a fraction of the canvas height (max 2). Paired with width.",
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.01,
                }),
                "x": ("FLOAT", {
                    "tooltip": "Horizontal position of the source video, as a fraction of the canvas width (-2 to 2).",
                    "default": 0.0,
                    "min": -2.0,
                    "max": 2.0,
                    "step": 0.01,
                }),
                "y": ("FLOAT", {
                    "tooltip": "Vertical position of the source video, as a fraction of the canvas height (-2 to 2).",
                    "default": 0.0,
                    "min": -2.0,
                    "max": 2.0,
                    "step": 0.01,
                }),
            },
        }

    RETURN_TYPES = ("RUNWAREVIDEOINFERENCESETTINGSSOURCEPOSITION",)
    RETURN_NAMES = ("sourcePosition",)
    FUNCTION = "create"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Configure settings.sourcePosition (width, height, x, y) for Runware Video Inference. "
        "Connect to Runware Video Inference Settings → sourcePosition."
    )

    def create(self, **kwargs) -> tuple[Dict[str, Any]]:
        source_position = {
            "width": float(kwargs.get("width", 1.0)),
            "height": float(kwargs.get("height", 1.0)),
            "x": float(kwargs.get("x", 0.0)),
            "y": float(kwargs.get("y", 0.0)),
        }
        return (source_position,)


NODE_CLASS_MAPPINGS = {
    "RunwareVideoInferenceSettingsSourcePosition": RunwareVideoInferenceSettingsSourcePosition,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVideoInferenceSettingsSourcePosition": "Runware Video Inference Settings Source Position",
}
