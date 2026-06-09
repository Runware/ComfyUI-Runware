"""
Runware 3D Inference Settings Draco Compression Node
Outputs dracoCompression config: enabled, level, quantizationPosition,
quantizationNormal, quantizationTexCoord
"""

from typing import Dict, Any


class Runware3DInferenceSettingsDracoCompression:
    """Runware 3D Inference Settings Draco Compression Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useEnabled": ("BOOLEAN", {
                    "tooltip": "Enable to include enabled in dracoCompression",
                    "default": False,
                }),
                "enabled": ("BOOLEAN", {
                    "tooltip": (
                        "If true, applies KHR_draco_mesh_compression to the output GLB "
                        "(5-10x geometry size reduction with no triangle loss). "
                        "Only used when 'Use Enabled' is on."
                    ),
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useLevel": ("BOOLEAN", {
                    "tooltip": "Enable to include level in dracoCompression",
                    "default": False,
                }),
                "level": ("INT", {
                    "tooltip": "Draco compression level (0-10). Higher = better compression but slower encoding. Only used when enabled.",
                    "default": 7,
                    "min": 0,
                    "max": 10,
                    "step": 1,
                }),
                "useQuantizationPosition": ("BOOLEAN", {
                    "tooltip": "Enable to include quantizationPosition in dracoCompression",
                    "default": False,
                }),
                "quantizationPosition": ("INT", {
                    "tooltip": "Quantization bits for vertex positions (8-30). Higher = better quality, larger file. Only used when enabled.",
                    "default": 16,
                    "min": 8,
                    "max": 30,
                    "step": 1,
                }),
                "useQuantizationNormal": ("BOOLEAN", {
                    "tooltip": "Enable to include quantizationNormal in dracoCompression",
                    "default": False,
                }),
                "quantizationNormal": ("INT", {
                    "tooltip": "Quantization bits for vertex normals (8-30). Higher = smoother shading, larger file. Only used when enabled.",
                    "default": 14,
                    "min": 8,
                    "max": 30,
                    "step": 1,
                }),
                "useQuantizationTexCoord": ("BOOLEAN", {
                    "tooltip": "Enable to include quantizationTexCoord in dracoCompression",
                    "default": False,
                }),
                "quantizationTexCoord": ("INT", {
                    "tooltip": "Quantization bits for texture coordinates (8-30). Higher = sharper textures at UV seams. Only used when enabled.",
                    "default": 14,
                    "min": 8,
                    "max": 30,
                    "step": 1,
                }),
            }
        }

    RETURN_TYPES = ("RUNWARE3DINFERENCESETTINGSLAT",)
    RETURN_NAMES = ("Draco Compression",)
    FUNCTION = "create"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Configure settings.dracoCompression for Runware 3D Inference "
        "(enabled, level, quantizationPosition, quantizationNormal, quantizationTexCoord). "
        "Connect to Runware 3D Inference Settings."
    )

    def create(self, **kwargs) -> tuple[Dict[str, Any]]:
        out: Dict[str, Any] = {}
        if kwargs.get("useEnabled", False):
            out["enabled"] = bool(kwargs.get("enabled", False))
        if kwargs.get("useLevel", False):
            out["level"] = int(kwargs.get("level", 7))
        if kwargs.get("useQuantizationPosition", False):
            out["quantizationPosition"] = int(kwargs.get("quantizationPosition", 16))
        if kwargs.get("useQuantizationNormal", False):
            out["quantizationNormal"] = int(kwargs.get("quantizationNormal", 14))
        if kwargs.get("useQuantizationTexCoord", False):
            out["quantizationTexCoord"] = int(kwargs.get("quantizationTexCoord", 14))
        return (out,)


NODE_CLASS_MAPPINGS = {
    "Runware3DInferenceSettingsDracoCompression": Runware3DInferenceSettingsDracoCompression,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Runware3DInferenceSettingsDracoCompression": "Runware 3D Inference Settings Draco Compression",
}
