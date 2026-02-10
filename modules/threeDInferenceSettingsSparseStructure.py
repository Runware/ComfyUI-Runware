"""
Runware 3D Inference Settings Sparse Structure Node
Outputs sparseStructure config: guidanceStrength, guidanceRescale, steps, rescaleT
"""

from typing import Dict, Any


class Runware3DInferenceSettingsSparseStructure:
    """Runware 3D Inference Settings Sparse Structure Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useGuidanceStrength": ("BOOLEAN", {
                    "tooltip": "Enable to include guidanceStrength in sparseStructure",
                    "default": False,
                }),
                "guidanceStrength": ("FLOAT", {
                    "tooltip": "Guidance strength for sparse structure (1.0-10.0). Only used when enabled.",
                    "default": 7.5,
                    "min": 1.0,
                    "max": 10.0,
                    "step": 0.1,
                }),
                "useGuidanceRescale": ("BOOLEAN", {
                    "tooltip": "Enable to include guidanceRescale in sparseStructure",
                    "default": False,
                }),
                "guidanceRescale": ("FLOAT", {
                    "tooltip": "Guidance rescale for sparse structure. Only used when enabled.",
                    "default": 0.7,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                }),
                "useSteps": ("BOOLEAN", {
                    "tooltip": "Enable to include steps in sparseStructure",
                    "default": False,
                }),
                "steps": ("INT", {
                    "tooltip": "Number of steps for sparse structure (1-50). Only used when enabled.",
                    "default": 12,
                    "min": 1,
                    "max": 50,
                    "step": 1,
                }),
                "useRescaleT": ("BOOLEAN", {
                    "tooltip": "Enable to include rescaleT in sparseStructure",
                    "default": False,
                }),
                "rescaleT": ("FLOAT", {
                    "tooltip": "Rescale T for sparse structure (1.0-6.0). Only used when enabled.",
                    "default": 5.0,
                    "min": 1.0,
                    "max": 6.0,
                    "step": 0.1,
                }),
            }
        }

    RETURN_TYPES = ("RUNWARE3DINFERENCESETTINGSLAT",)
    RETURN_NAMES = ("Sparse Structure",)
    FUNCTION = "create"
    CATEGORY = "Runware"
    DESCRIPTION = "Configure sparse structure parameters for Runware 3D Inference settings."

    def create(self, **kwargs) -> tuple[Dict[str, Any]]:
        out: Dict[str, Any] = {}
        if kwargs.get("useGuidanceStrength", False):
            out["guidanceStrength"] = float(kwargs.get("guidanceStrength", 7.5))
        if kwargs.get("useGuidanceRescale", False):
            out["guidanceRescale"] = float(kwargs.get("guidanceRescale", 0.7))
        if kwargs.get("useSteps", False):
            out["steps"] = int(kwargs.get("steps", 12))
        if kwargs.get("useRescaleT", False):
            out["rescaleT"] = float(kwargs.get("rescaleT", 5.0))
        return (out,)


NODE_CLASS_MAPPINGS = {
    "Runware3DInferenceSettingsSparseStructure": Runware3DInferenceSettingsSparseStructure,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Runware3DInferenceSettingsSparseStructure": "Runware 3D Inference Settings Sparse Structure",
}
