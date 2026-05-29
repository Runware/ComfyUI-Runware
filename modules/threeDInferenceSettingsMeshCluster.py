"""
Runware 3D Inference Settings Mesh Cluster Node
Outputs meshCluster config: thresholdConeHalfAngleRad, refineIterations,
globalIterations, smoothStrength
"""

import math
from typing import Dict, Any


class Runware3DInferenceSettingsMeshCluster:
    """Runware 3D Inference Settings Mesh Cluster Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useThresholdConeHalfAngleRad": ("BOOLEAN", {
                    "tooltip": "Enable to include thresholdConeHalfAngleRad in meshCluster",
                    "default": False,
                }),
                "thresholdConeHalfAngleRad": ("FLOAT", {
                    "tooltip": "Cone half-angle threshold (radians) used during UV chart clustering. Only used when enabled.",
                    "default": math.pi / 2,
                    "min": 0.0,
                    "max": math.pi,
                    "step": 0.01,
                }),
                "useRefineIterations": ("BOOLEAN", {
                    "tooltip": "Enable to include refineIterations in meshCluster",
                    "default": False,
                }),
                "refineIterations": ("INT", {
                    "tooltip": "Local refinement iterations for chart clustering. Only used when enabled.",
                    "default": 0,
                    "min": 0,
                    "max": 64,
                    "step": 1,
                }),
                "useGlobalIterations": ("BOOLEAN", {
                    "tooltip": "Enable to include globalIterations in meshCluster",
                    "default": False,
                }),
                "globalIterations": ("INT", {
                    "tooltip": "Global iterations for chart clustering. Only used when enabled.",
                    "default": 1,
                    "min": 0,
                    "max": 64,
                    "step": 1,
                }),
                "useSmoothStrength": ("BOOLEAN", {
                    "tooltip": "Enable to include smoothStrength in meshCluster",
                    "default": False,
                }),
                "smoothStrength": ("INT", {
                    "tooltip": "Smoothing strength applied during chart clustering. Only used when enabled.",
                    "default": 1,
                    "min": 0,
                    "max": 10,
                    "step": 1,
                }),
            }
        }

    RETURN_TYPES = ("RUNWARE3DINFERENCESETTINGSLAT",)
    RETURN_NAMES = ("Mesh Cluster",)
    FUNCTION = "create"
    CATEGORY = "Runware"
    DESCRIPTION = "Configure mesh cluster parameters for Runware 3D Inference settings."

    def create(self, **kwargs) -> tuple[Dict[str, Any]]:
        out: Dict[str, Any] = {}
        if kwargs.get("useThresholdConeHalfAngleRad", False):
            out["thresholdConeHalfAngleRad"] = float(kwargs.get("thresholdConeHalfAngleRad", math.pi / 2))
        if kwargs.get("useRefineIterations", False):
            out["refineIterations"] = int(kwargs.get("refineIterations", 0))
        if kwargs.get("useGlobalIterations", False):
            out["globalIterations"] = int(kwargs.get("globalIterations", 1))
        if kwargs.get("useSmoothStrength", False):
            out["smoothStrength"] = int(kwargs.get("smoothStrength", 1))
        return (out,)


NODE_CLASS_MAPPINGS = {
    "Runware3DInferenceSettingsMeshCluster": Runware3DInferenceSettingsMeshCluster,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Runware3DInferenceSettingsMeshCluster": "Runware 3D Inference Settings Mesh Cluster",
}
