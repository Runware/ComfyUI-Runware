"""
Runware 3D Inference Settings Node
Main settings for 3D inference: textureSize, decimationTarget, remesh, resolution,
imageAutoFix, faceLimit, texture, pbr, Tripo mesh/texture options, material/quality,
polyCount, taPose, boundingBox, meshMode, addons, hdTexture, and sub-configs
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
                "useOriginalAlpha": ("BOOLEAN", {
                    "tooltip": "Enable to include originalAlpha in settings.",
                    "default": False,
                }),
                "originalAlpha": ("BOOLEAN", {
                    "tooltip": "If true, use the original transparency channel while processing the image. Only used when 'Use Original Alpha' is enabled.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useMaterial": ("BOOLEAN", {
                    "tooltip": "Enable to include material in settings.",
                    "default": False,
                }),
                "material": (["PBR", "Shaded", "All"], {
                    "tooltip": "Material type. PBR: physically based textures. Shaded: base color with baked lighting. All: return both. Only used when 'Use Material' is enabled.",
                    "default": "PBR",
                }),
                "useQuality": ("BOOLEAN", {
                    "tooltip": "Enable to include quality in settings.",
                    "default": False,
                }),
                "quality": (["high", "medium", "low", "extra-low"], {
                    "tooltip": "Generation quality. For Raw defaults to high; for Quad defaults to medium. Ignored when polyCount is used.",
                    "default": "medium",
                }),
                "usePolyCount": ("BOOLEAN", {
                    "tooltip": "Enable to include polyCount in settings.",
                    "default": False,
                }),
                "polyCount": ("FLOAT", {
                    "tooltip": "Advanced face-count control. Raw: 500-1000000 (default 500000). Quad: 1000-200000 (default 18000). Overrides quality.",
                    "default": 18000.0,
                    "min": 500.0,
                    "max": 1000000.0,
                    "step": 100.0,
                }),
                "useTaPose": ("BOOLEAN", {
                    "tooltip": "Enable to include taPose in settings.",
                    "default": False,
                }),
                "taPose": ("BOOLEAN", {
                    "tooltip": "When true, human-like models are generated in T/A pose. Only used when 'Use Ta Pose' is enabled.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useBoundingBox": ("BOOLEAN", {
                    "tooltip": "Enable to include boundingBox in settings.",
                    "default": False,
                }),
                "boundingBox": ("STRING", {
                    "multiline": False,
                    "tooltip": "Comma-separated integers in fixed order y,z,x (width,height,length), e.g. 2,3,4. Only used when 'Use Bounding Box' is enabled.",
                    "default": "",
                }),
                "useMeshMode": ("BOOLEAN", {
                    "tooltip": "Enable to include meshMode in settings.",
                    "default": False,
                }),
                "meshMode": (["Raw", "Quad"], {
                    "tooltip": "Raw: triangular faces. Quad: quadrilateral faces. Only used when 'Use Mesh Mode' is enabled.",
                    "default": "Quad",
                }),
                "useAddons": ("BOOLEAN", {
                    "tooltip": "Enable to include addons in settings.",
                    "default": False,
                }),
                "addons": ("STRING", {
                    "multiline": False,
                    "tooltip": "Comma-separated addon values, e.g. HighPack. Leave empty to skip addons. Only used when 'Use Addons' is enabled.",
                    "default": "",
                }),
                "useHdTexture": ("BOOLEAN", {
                    "tooltip": "Enable to include hdTexture in settings.",
                    "default": False,
                }),
                "hdTexture": ("BOOLEAN", {
                    "tooltip": "If true, provides high-quality texture output. Only used when 'Use Hd Texture' is enabled.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useMeshType": ("BOOLEAN", {
                    "tooltip": "Enable to include meshType in settings.",
                    "default": False,
                }),
                "meshType": (["standard", "lowpoly"], {
                    "tooltip": "Mesh type: standard or lowpoly. Only used when 'Use Mesh Type' is enabled.",
                    "default": "standard",
                }),
                "useTopology": ("BOOLEAN", {
                    "tooltip": "Enable to include topology in settings.",
                    "default": False,
                }),
                "topology": (["triangle", "quad"], {
                    "tooltip": "Mesh topology mode. Only used when 'Use Topology' is enabled.",
                    "default": "triangle",
                }),
                "useDecimation": ("BOOLEAN", {
                    "tooltip": "Enable to include decimation in settings.",
                    "default": False,
                }),
                "decimation": ("INT", {
                    "tooltip": "Adaptive decimation level (1=ultra, 2=high, 3=medium, 4=low). Only used when enabled.",
                    "default": 2,
                    "min": 1,
                    "max": 4,
                    "step": 1,
                }),
                "useSymmetry": ("BOOLEAN", {
                    "tooltip": "Enable to include symmetry in settings.",
                    "default": False,
                }),
                "symmetry": (["auto", "on", "off"], {
                    "tooltip": "Symmetry behavior for generation. Only used when 'Use Symmetry' is enabled.",
                    "default": "auto",
                }),
                "usePose": ("BOOLEAN", {
                    "tooltip": "Enable to include pose in settings.",
                    "default": False,
                }),
                "pose": (["none", "a-pose", "t-pose"], {
                    "tooltip": "Pose preset for generated model. Use 'none' for no pose preset.",
                    "default": "none",
                }),
                "useImageEnhancement": ("BOOLEAN", {
                    "tooltip": "Enable to include imageEnhancement in settings.",
                    "default": False,
                }),
                "imageEnhancement": ("BOOLEAN", {
                    "tooltip": "Optimize input image for improved 3D results. Only used when enabled.",
                    "default": True,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useRemoveLighting": ("BOOLEAN", {
                    "tooltip": "Enable to include removeLighting in settings.",
                    "default": False,
                }),
                "removeLighting": ("BOOLEAN", {
                    "tooltip": "Remove baked lighting from texture output. Only used when enabled.",
                    "default": True,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useOrigin": ("BOOLEAN", {
                    "tooltip": "Enable to include origin in settings.",
                    "default": False,
                }),
                "origin": (["bottom", "center"], {
                    "tooltip": "Origin point position used with autoSize. Only used when 'Use Origin' is enabled.",
                    "default": "bottom",
                }),
                "useModeration": ("BOOLEAN", {
                    "tooltip": "Enable to include moderation in settings.",
                    "default": False,
                }),
                "moderation": ("BOOLEAN", {
                    "tooltip": "Enable moderation checks before generation. Only used when enabled.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useSavePreRemeshedModel": ("BOOLEAN", {
                    "tooltip": "Enable to include savePreRemeshedModel in settings.",
                    "default": False,
                }),
                "savePreRemeshedModel": ("BOOLEAN", {
                    "tooltip": "Store extra GLB before remesh completion. Only used when enabled.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useTexturePrompt": ("BOOLEAN", {
                    "tooltip": "Enable to include texturePrompt in settings.",
                    "default": False,
                }),
                "texturePrompt": ("STRING", {
                    "multiline": True,
                    "tooltip": "Additional text prompt to guide texture generation. Only used when enabled.",
                    "default": "",
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
                "useFaceCount": ("BOOLEAN", {
                    "tooltip": "Enable to include faceCount in settings (Tencent Hunyuan Pro).",
                    "default": False,
                }),
                "faceCount": ("INT", {
                    "tooltip": "Target number of mesh faces for Hunyuan Pro (3000-1500000).",
                    "default": 500000,
                    "min": 3000,
                    "max": 1500000,
                    "step": 1000,
                }),
                "useGenerateType": ("BOOLEAN", {
                    "tooltip": "Enable to include generateType in settings (Tencent Hunyuan Pro).",
                    "default": False,
                }),
                "generateType": (["Normal", "Geometry"], {
                    "tooltip": "Hunyuan Pro generation mode: Normal or Geometry.",
                    "default": "Normal",
                }),
                "usePolygonType": ("BOOLEAN", {
                    "tooltip": "Enable to include polygonType in settings (Tencent Hunyuan Pro).",
                    "default": False,
                }),
                "polygonType": (["triangle", "quadrilateral"], {
                    "tooltip": "Polygon type for low-poly style output. For Hunyuan 3.1, lowpoly mode is not supported by provider.",
                    "default": "triangle",
                }),
                "useGeometryOnly": ("BOOLEAN", {
                    "tooltip": "Enable to include geometryOnly in settings (Tencent Hunyuan Rapid).",
                    "default": False,
                }),
                "geometryOnly": ("BOOLEAN", {
                    "tooltip": "Rapid-only: texture-free white model generation.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
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
        "smartLowPoly, generateParts, exportUv, geometryQuality, originalAlpha, material, quality, polyCount, "
        "taPose, boundingBox, meshMode, addons, hdTexture, and lat configs."
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
        if kwargs.get("useFaceCount", False):
            settings["faceCount"] = int(kwargs.get("faceCount", 500000))
        if kwargs.get("useGenerateType", False):
            settings["generateType"] = kwargs.get("generateType", "Normal")
        if kwargs.get("usePolygonType", False):
            settings["polygonType"] = kwargs.get("polygonType", "triangle")
        if kwargs.get("useGeometryOnly", False):
            settings["geometryOnly"] = bool(kwargs.get("geometryOnly", False))
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
        if kwargs.get("useOriginalAlpha", False):
            settings["originalAlpha"] = bool(kwargs.get("originalAlpha", False))
        if kwargs.get("useMaterial", False):
            settings["material"] = kwargs.get("material", "PBR")
        if kwargs.get("useQuality", False):
            settings["quality"] = kwargs.get("quality", "medium")
        if kwargs.get("usePolyCount", False):
            settings["polyCount"] = float(kwargs.get("polyCount", 18000.0))
        if kwargs.get("useTaPose", False):
            settings["taPose"] = bool(kwargs.get("taPose", False))
        if kwargs.get("useBoundingBox", False):
            raw_bounding_box = (kwargs.get("boundingBox") or "").strip()
            if raw_bounding_box:
                parts = [part.strip() for part in raw_bounding_box.split(",") if part.strip()]
                if len(parts) != 3:
                    raise ValueError("boundingBox must contain exactly 3 comma-separated integers in y,z,x order.")
                try:
                    settings["boundingBox"] = [int(parts[0]), int(parts[1]), int(parts[2])]
                except ValueError as exc:
                    raise ValueError("boundingBox values must be integers (y,z,x).") from exc
        if kwargs.get("useMeshMode", False):
            settings["meshMode"] = kwargs.get("meshMode", "Quad")
        if kwargs.get("useAddons", False):
            raw_addons = (kwargs.get("addons") or "").strip()
            addons = [addon.strip() for addon in raw_addons.split(",") if addon.strip()] if raw_addons else []
            if addons:
                settings["addons"] = addons
        if kwargs.get("useHdTexture", False):
            settings["hdTexture"] = bool(kwargs.get("hdTexture", False))
        if kwargs.get("useMeshType", False):
            settings["meshType"] = kwargs.get("meshType", "standard")
        if kwargs.get("useTopology", False):
            settings["topology"] = kwargs.get("topology", "triangle")
        if kwargs.get("useDecimation", False):
            settings["decimation"] = int(kwargs.get("decimation", 2))
        if kwargs.get("useSymmetry", False):
            settings["symmetry"] = kwargs.get("symmetry", "auto")
        if kwargs.get("usePose", False):
            pose_value = kwargs.get("pose", "none")
            settings["pose"] = "" if pose_value == "none" else pose_value
        if kwargs.get("useImageEnhancement", False):
            settings["imageEnhancement"] = bool(kwargs.get("imageEnhancement", True))
        if kwargs.get("useRemoveLighting", False):
            settings["removeLighting"] = bool(kwargs.get("removeLighting", True))
        if kwargs.get("useOrigin", False):
            settings["origin"] = kwargs.get("origin", "bottom")
        if kwargs.get("useModeration", False):
            settings["moderation"] = bool(kwargs.get("moderation", False))
        if kwargs.get("useSavePreRemeshedModel", False):
            settings["savePreRemeshedModel"] = bool(kwargs.get("savePreRemeshedModel", False))
        if kwargs.get("useTexturePrompt", False):
            texture_prompt = (kwargs.get("texturePrompt") or "").strip()
            if texture_prompt:
                settings["texturePrompt"] = texture_prompt

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
