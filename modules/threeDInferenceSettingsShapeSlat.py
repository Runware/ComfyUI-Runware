"""
Runware 3D Inference Settings Shape Slat Node
Outputs shapeSlat config: guidanceStrength, guidanceRescale, steps, rescaleT
"""

from typing import Dict, Any


class Runware3DInferenceSettingsShapeSlat:
    """Runware 3D Inference Settings Shape Slat Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useGuidanceStrength": ("BOOLEAN", {
                    "tooltip": "Enable to include guidanceStrength in shapeSlat",
                    "default": False,
                }),
                "guidanceStrength": ("FLOAT", {
                    "tooltip": "Guidance strength for shape slat (1.0-10.0). Only used when enabled.",
                    "default": 7.5,
                    "min": 1.0,
                    "max": 10.0,
                    "step": 0.1,
                }),
                "useGuidanceRescale": ("BOOLEAN", {
                    "tooltip": "Enable to include guidanceRescale in shapeSlat",
                    "default": False,
                }),
                "guidanceRescale": ("FLOAT", {
                    "tooltip": "Guidance rescale for shape slat. Only used when enabled.",
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                }),
                "useSteps": ("BOOLEAN", {
                    "tooltip": "Enable to include steps in shapeSlat",
                    "default": False,
                }),
                "steps": ("INT", {
                    "tooltip": "Number of steps for shape slat (1-50). Only used when enabled.",
                    "default": 12,
                    "min": 1,
                    "max": 50,
                    "step": 1,
                }),
                "useRescaleT": ("BOOLEAN", {
                    "tooltip": "Enable to include rescaleT in shapeSlat",
                    "default": False,
                }),
                "rescaleT": ("FLOAT", {
                    "tooltip": "Rescale T for shape slat (1.0-6.0). Only used when enabled.",
                    "default": 3.0,
                    "min": 1.0,
                    "max": 6.0,
                    "step": 0.1,
                }),
            }
        }

    RETURN_TYPES = ("RUNWARE3DINFERENCESETTINGSLAT",)
    RETURN_NAMES = ("Shape Slat",)
    FUNCTION = "create"
    CATEGORY = "Runware"
    DESCRIPTION = "Configure shape slat parameters for Runware 3D Inference settings."

    def create(self, **kwargs) -> tuple[Dict[str, Any]]:
        out: Dict[str, Any] = {}
        if kwargs.get("useGuidanceStrength", False):
            out["guidanceStrength"] = float(kwargs.get("guidanceStrength", 7.5))
        if kwargs.get("useGuidanceRescale", False):
            out["guidanceRescale"] = float(kwargs.get("guidanceRescale", 0.5))
        if kwargs.get("useSteps", False):
            out["steps"] = int(kwargs.get("steps", 12))
        if kwargs.get("useRescaleT", False):
            out["rescaleT"] = float(kwargs.get("rescaleT", 3.0))
        return (out,)


NODE_CLASS_MAPPINGS = {
    "Runware3DInferenceSettingsShapeSlat": Runware3DInferenceSettingsShapeSlat,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Runware3DInferenceSettingsShapeSlat": "Runware 3D Inference Settings Shape Slat",
}
