"""
Runware 3D Inference Settings Node
Main settings for 3D inference: textureSize, decimationTarget, remesh, resolution,
imageAutoFix, faceLimit, texture, pbr, Tripo mesh/texture options, and sub-configs
sparseStructure, shapeSlat, texSlat from connected nodes.
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
                "useImageAutoFix": ("BOOLEAN", {
                    "tooltip": "Enable to include imageAutoFix in settings.",
                    "default": False,
                }),
                "imageAutoFix": ("BOOLEAN", {
                    "tooltip": "When true, optimizes the input image for better generation. Only used when 'Use Image Auto Fix' is enabled.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useFaceLimit": ("BOOLEAN", {
                    "tooltip": "Enable to include faceLimit in settings.",
                    "default": False,
                }),
                "faceLimit": ("INT", {
                    "tooltip": "Limits faces on the output mesh; if unset, face count is adaptive. With smartLowPoly: typically 1000–20000; with quad: 500–10000. Only used when enabled.",
                    "default": 10000,
                    "min": 500,
                    "max": 20000,
                    "step": 100,
                }),
                "useTexture": ("BOOLEAN", {
                    "tooltip": "Enable to include texture (enable texturing) in settings.",
                    "default": False,
                }),
                "texture": ("BOOLEAN", {
                    "tooltip": "Enable texturing. Default API behavior is true; set false for untextured base mesh. Only used when 'Use Texture' is enabled.",
                    "default": True,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "usePbr": ("BOOLEAN", {
                    "tooltip": "Enable to include pbr in settings.",
                    "default": False,
                }),
                "pbr": ("BOOLEAN", {
                    "tooltip": "Enable PBR materials. Default API behavior is true; set false for no PBR. Only used when 'Use Pbr' is enabled.",
                    "default": True,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useTextureSeed": ("BOOLEAN", {
                    "tooltip": "Enable to include textureSeed in settings.",
                    "default": False,
                }),
                "textureSeed": ("INT", {
                    "tooltip": "Seed for texture generation. Only used when 'Use Texture Seed' is enabled.",
                    "default": 1,
                    "min": 0,
                    "max": 2147483647,
                }),
                "useTextureAlignment": ("BOOLEAN", {
                    "tooltip": "Enable to include textureAlignment in settings.",
                    "default": False,
                }),
                "textureAlignment": (["original_image", "geometry"], {
                    "tooltip": "original_image: fidelity to source image. geometry: alignment to 3D structure. Only used when 'Use Texture Alignment' is enabled.",
                    "default": "original_image",
                }),
                "useTextureQuality": ("BOOLEAN", {
                    "tooltip": "Enable to include textureQuality in settings.",
                    "default": False,
                }),
                "textureQuality": (["standard", "detailed"], {
                    "tooltip": "Texture quality: standard (default) or detailed (high-res, finer detail). Only used when 'Use Texture Quality' is enabled.",
                    "default": "standard",
                }),
                "useAutoSize": ("BOOLEAN", {
                    "tooltip": "Enable to include autoSize in settings.",
                    "default": False,
                }),
                "autoSize": ("BOOLEAN", {
                    "tooltip": "Scale the model to real-world size (meters). Default false. Only used when 'Use Auto Size' is enabled.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useOrientation": ("BOOLEAN", {
                    "tooltip": "Enable to include orientation in settings.",
                    "default": False,
                }),
                "orientation": (["default", "align_image"], {
                    "tooltip": "align_image rotates the model to align with the source image. Default: default. Only used when 'Use Orientation' is enabled.",
                    "default": "default",
                }),
                "useQuad": ("BOOLEAN", {
                    "tooltip": "Enable to include quad in settings.",
                    "default": False,
                }),
                "quad": ("BOOLEAN", {
                    "tooltip": "Enable quad mesh output. If quad=true and faceLimit is unset, default faceLimit is 10000. Only used when 'Use Quad' is enabled.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useCompress": ("BOOLEAN", {
                    "tooltip": "Enable to include compress in settings.",
                    "default": False,
                }),
                "compress": (["meshopt", "geometry"], {
                    "tooltip": "meshopt: default compression. geometry: geometry-based compression (decompress before editing in most DCC tools). Only used when 'Use Compress' is enabled.",
                    "default": "meshopt",
                }),
                "useSmartLowPoly": ("BOOLEAN", {
                    "tooltip": "Enable to include smartLowPoly in settings.",
                    "default": False,
                }),
                "smartLowPoly": ("BOOLEAN", {
                    "tooltip": "Low-poly meshes with hand-crafted topology; simpler inputs work best. Default false. Only used when 'Use Smart Low Poly' is enabled.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useGenerateParts": ("BOOLEAN", {
                    "tooltip": "Enable to include generateParts in settings.",
                    "default": False,
                }),
                "generateParts": ("BOOLEAN", {
                    "tooltip": "Segmented editable parts. Not compatible with texture/pbr when true, or with quad=true (set texture=false, pbr=false, quad=false). Only used when 'Use Generate Parts' is enabled.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useExportUv": ("BOOLEAN", {
                    "tooltip": "Enable to include exportUv in settings.",
                    "default": False,
                }),
                "exportUv": ("BOOLEAN", {
                    "tooltip": "Whether UV unwrapping runs during generation. Only used when 'Use Export Uv' is enabled.",
                    "default": True,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useGeometryQuality": ("BOOLEAN", {
                    "tooltip": "Enable to include geometryQuality in settings.",
                    "default": False,
                }),
                "geometryQuality": (["standard", "detailed"], {
                    "tooltip": "standard: balanced (default). detailed: maximum detail (ultra mode). Only used when 'Use Geometry Quality' is enabled.",
                    "default": "standard",
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
    DESCRIPTION = (
        "Configure Runware 3D Inference settings: textureSize, decimationTarget, remesh, resolution, imageAutoFix, faceLimit, "
        "texture, pbr, textureSeed, textureAlignment, textureQuality, autoSize, orientation, quad, compress, "
        "smartLowPoly, generateParts, exportUv, geometryQuality, and lat configs."
    )

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

        if kwargs.get("useImageAutoFix", False):
            settings["imageAutoFix"] = bool(kwargs.get("imageAutoFix", False))
        if kwargs.get("useFaceLimit", False):
            settings["faceLimit"] = int(kwargs.get("faceLimit", 10000))
        if kwargs.get("useTexture", False):
            settings["texture"] = bool(kwargs.get("texture", True))
        if kwargs.get("usePbr", False):
            settings["pbr"] = bool(kwargs.get("pbr", True))
        if kwargs.get("useTextureSeed", False):
            settings["textureSeed"] = int(kwargs.get("textureSeed", 1))
        if kwargs.get("useTextureAlignment", False):
            settings["textureAlignment"] = kwargs.get("textureAlignment", "original_image")
        if kwargs.get("useTextureQuality", False):
            settings["textureQuality"] = kwargs.get("textureQuality", "standard")
        if kwargs.get("useAutoSize", False):
            settings["autoSize"] = bool(kwargs.get("autoSize", False))
        if kwargs.get("useOrientation", False):
            settings["orientation"] = kwargs.get("orientation", "default")
        if kwargs.get("useQuad", False):
            settings["quad"] = bool(kwargs.get("quad", False))
        if kwargs.get("useCompress", False):
            settings["compress"] = kwargs.get("compress", "meshopt")
        if kwargs.get("useSmartLowPoly", False):
            settings["smartLowPoly"] = bool(kwargs.get("smartLowPoly", False))
        if kwargs.get("useGenerateParts", False):
            settings["generateParts"] = bool(kwargs.get("generateParts", False))
        if kwargs.get("useExportUv", False):
            settings["exportUv"] = bool(kwargs.get("exportUv", True))
        if kwargs.get("useGeometryQuality", False):
            settings["geometryQuality"] = kwargs.get("geometryQuality", "standard")

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
