"""
Runware Video Inference Settings Edit
Exposes settings.edit (autoControls, strength, controls) for video editing models.
Connect the output to Runware Video Inference Settings → edit.
"""

from typing import Dict, Any

_STRENGTH_PRESETS = [
    "adhere_1", "adhere_2", "adhere_3",
    "flex_1", "flex_2", "flex_3",
    "reimagine_1", "reimagine_2", "reimagine_3",
]


class RunwareVideoInferenceSettingsControl:
    """Optional settings.edit block for video inference (e.g. Luma Ray 3.2)."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useAutoControls": ("BOOLEAN", {
                    "tooltip": "Enable to include autoControls in settings.edit.",
                    "default": False,
                }),
                "autoControls": ("BOOLEAN", {
                    "tooltip": "Derives the full conditioning schedule from the source video. Cannot be combined with settings.edit.strength or settings.edit.controls. Only used when 'Use Auto Controls' is enabled.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useStrength": ("BOOLEAN", {
                    "tooltip": "Enable to include strength in settings.edit.",
                    "default": False,
                }),
                "strength": (_STRENGTH_PRESETS, {
                    "tooltip": "Preservation preset: adhere (stay close to source), flex (moderate changes), or reimagine (loose guidance). Cannot be combined with autoControls. Only used when 'Use Strength' is enabled.",
                    "default": "flex_2",
                }),
                "useDepthBlur": ("BOOLEAN", {
                    "tooltip": "Enable to include depthBlur in settings.edit.controls.",
                    "default": False,
                }),
                "depthBlur": ("FLOAT", {
                    "tooltip": "Scene-geometry depth blur (0–1). Higher values allow more freedom. Only used when 'Use Depth Blur' is enabled.",
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
                "useFace": ("BOOLEAN", {
                    "tooltip": "Enable to include face in settings.edit.controls.",
                    "default": False,
                }),
                "face": ("BOOLEAN", {
                    "tooltip": "Enable face-identity conditioning. Only used when 'Use Face' is enabled.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useNormalsAugmentation": ("BOOLEAN", {
                    "tooltip": "Enable to include normalsAugmentation in settings.edit.controls.",
                    "default": False,
                }),
                "normalsAugmentation": ("FLOAT", {
                    "tooltip": "Surface-geometry normals augmentation (0–1). Higher values allow more reinterpretation. Only used when 'Use Normals Augmentation' is enabled.",
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
                "usePoseStrength": ("BOOLEAN", {
                    "tooltip": "Enable to include poseStrength in settings.edit.controls.",
                    "default": False,
                }),
                "poseStrength": (["precise", "coarse"], {
                    "tooltip": "Skeleton conditioning strength. Only used when 'Use Pose Strength' is enabled.",
                    "default": "precise",
                }),
                "useTrajectorySparsity": ("BOOLEAN", {
                    "tooltip": "Enable to include trajectorySparsity in settings.edit.controls.",
                    "default": False,
                }),
                "trajectorySparsity": ("FLOAT", {
                    "tooltip": "Motion-anchoring sparsity (0–1). Higher values use fewer anchors. Only used when 'Use Trajectory Sparsity' is enabled.",
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
            },
        }

    RETURN_TYPES = ("RUNWAREVIDEOINFERENCESETTINGSEDIT",)
    RETURN_NAMES = ("edit",)
    FUNCTION = "create"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Configure settings.edit (autoControls, strength, controls) for Runware Video Inference. "
        "Connect to Runware Video Inference Settings → edit."
    )

    def create(self, **kwargs) -> tuple[Dict[str, Any]]:
        edit: Dict[str, Any] = {}

        if kwargs.get("useAutoControls", False):
            edit["autoControls"] = bool(kwargs.get("autoControls", False))
        if kwargs.get("useStrength", False):
            edit["strength"] = str(kwargs.get("strength", "flex_2"))

        controls: Dict[str, Any] = {}
        if kwargs.get("useDepthBlur", False):
            controls["depthBlur"] = float(kwargs.get("depthBlur", 0.0))
        if kwargs.get("useFace", False):
            controls["face"] = bool(kwargs.get("face", False))
        if kwargs.get("useNormalsAugmentation", False):
            controls["normalsAugmentation"] = float(kwargs.get("normalsAugmentation", 0.0))
        if kwargs.get("usePoseStrength", False):
            controls["poseStrength"] = str(kwargs.get("poseStrength", "precise"))
        if kwargs.get("useTrajectorySparsity", False):
            controls["trajectorySparsity"] = float(kwargs.get("trajectorySparsity", 0.0))

        if len(controls) > 0:
            edit["controls"] = controls

        return (edit,)


NODE_CLASS_MAPPINGS = {
    "RunwareVideoInferenceSettingsControl": RunwareVideoInferenceSettingsControl,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVideoInferenceSettingsControl": "Runware Video Inference Settings Edit",
}
