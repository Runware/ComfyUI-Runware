"""
Runware 3D Inference Settings Node
Main settings for 3D inference: textureSize, decimationTarget, remesh, resolution,
and sub-configs sparseStructure, shapeSlat, texSlat from connected nodes.
"""

from typing import Dict, Any


class Runware3DInferenceSettings:
    """Runware 3D Inference Settings Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useTextureSize": ("BOOLEAN", {
                    "tooltip": "Enable to include textureSize in settings",
                    "default": False,
                }),
                "textureSize": ("INT", {
                    "tooltip": "Texture size for 3D output (1024-4096, step 1024). Only used when enabled.",
                    "default": 2048,
                    "min": 1024,
                    "max": 4096,
                    "step": 1024,
                }),
                "useDecimationTarget": ("BOOLEAN", {
                    "tooltip": "Enable to include decimationTarget in settings",
                    "default": False,
                }),
                "decimationTarget": ("INT", {
                    "tooltip": "Decimation target for mesh (100000-1000000). Only used when enabled.",
                    "default": 500000,
                    "min": 100000,
                    "max": 1000000,
                    "step": 10000,
                }),
                "useRemesh": ("BOOLEAN", {
                    "tooltip": "Enable to include remesh in settings",
                    "default": False,
                }),
                "remesh": ("BOOLEAN", {
                    "tooltip": "Whether to remesh the output. Only used when enabled.",
                    "default": True,
                }),
                "useResolution": ("BOOLEAN", {
                    "tooltip": "Enable to include resolution in settings",
                    "default": False,
                }),
                "resolution": ([512, 1024, 1536], {
                    "tooltip": "Resolution for 3D generation (512, 1024, or 1536). Only used when enabled.",
                    "default": 1024,
                }),
                "sparseStructure": ("RUNWARE3DINFERENCESETTINGSLAT", {
                    "tooltip": "Connect Runware 3D Inference Settings Sparse Structure node.",
                }),
                "shapeSlat": ("RUNWARE3DINFERENCESETTINGSLAT", {
                    "tooltip": "Connect Runware 3D Inference Settings Shape Slat node.",
                }),
                "texSlat": ("RUNWARE3DINFERENCESETTINGSLAT", {
                    "tooltip": "Connect Runware 3D Inference Settings Tex Slat node.",
                }),
            }
        }

    RETURN_TYPES = ("RUNWARE3DINFERENCESETTINGS",)
    RETURN_NAMES = ("Settings",)
    FUNCTION = "create"
    CATEGORY = "Runware"
    DESCRIPTION = "Configure Runware 3D Inference settings: texture, decimation, remesh, resolution, and lat configs."

    def create(self, **kwargs) -> tuple[Dict[str, Any]]:
        settings: Dict[str, Any] = {}

        if kwargs.get("useTextureSize", False):
            settings["textureSize"] = int(kwargs.get("textureSize", 2048))
        if kwargs.get("useDecimationTarget", False):
            settings["decimationTarget"] = int(kwargs.get("decimationTarget", 500000))
        if kwargs.get("useRemesh", False):
            settings["remesh"] = bool(kwargs.get("remesh", True))
        if kwargs.get("useResolution", False):
            settings["resolution"] = int(kwargs.get("resolution", 1024))

        sparse = kwargs.get("sparseStructure", None)
        if sparse is not None and isinstance(sparse, dict) and len(sparse) > 0:
            settings["sparseStructure"] = sparse

        shape = kwargs.get("shapeSlat", None)
        if shape is not None and isinstance(shape, dict) and len(shape) > 0:
            settings["shapeSlat"] = shape

        tex = kwargs.get("texSlat", None)
        if tex is not None and isinstance(tex, dict) and len(tex) > 0:
            settings["texSlat"] = tex

        return (settings,)


NODE_CLASS_MAPPINGS = {
    "Runware3DInferenceSettings": Runware3DInferenceSettings,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Runware3DInferenceSettings": "Runware 3D Inference Settings",
}
