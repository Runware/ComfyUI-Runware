"""
Runware Image Inference Advanced Features Node
Provides advancedFeatures (layerDiffuse, hiresFix) for Runware Image Inference.
"""

from typing import Dict, Any


class RunwareImageInferenceAdvancedFeatures:
    """Runware Image Inference Advanced Features Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useLayerDiffuse": ("BOOLEAN", {
                    "tooltip": "Enable to include layerDiffuse in advancedFeatures. When enabled, LayerDiffuse generates images with transparency (alpha) without post-processing background removal.",
                    "default": False,
                }),
                "layerDiffuse": ("BOOLEAN", {
                    "tooltip": "Enable LayerDiffuse technology for direct generation of images with transparency (alpha channels). Only used when 'Use Layer Diffuse' is enabled.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useHiresFix": ("BOOLEAN", {
                    "tooltip": "Enable to include hiresFix in advancedFeatures. When enabled, uses a two-stage process for higher-resolution, higher-detail images.",
                    "default": False,
                }),
                "hiresFix": ("BOOLEAN", {
                    "tooltip": "Enable a two-stage generation: first at native resolution, then upscale and refine in a second pass. Only used when 'Use Hires Fix' is enabled.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREIMAGEINFERENCEADVANCEDFEATURES",)
    RETURN_NAMES = ("advancedFeatures",)
    FUNCTION = "createAdvancedFeatures"
    CATEGORY = "Runware"
    DESCRIPTION = "Configure advanced features for Runware Image Inference (layerDiffuse for transparency, hiresFix for two-stage high-res generation). Connect to Runware Image Inference advancedFeatures input."

    def createAdvancedFeatures(self, **kwargs) -> tuple:
        """Build advancedFeatures dict for the API."""
        use_layer_diffuse = kwargs.get("useLayerDiffuse", False)
        layer_diffuse = kwargs.get("layerDiffuse", False)
        use_hires_fix = kwargs.get("useHiresFix", False)
        hires_fix = kwargs.get("hiresFix", False)

        advanced_features: Dict[str, Any] = {}

        if use_layer_diffuse:
            advanced_features["layerDiffuse"] = bool(layer_diffuse)
        if use_hires_fix:
            advanced_features["hiresFix"] = bool(hires_fix)

        return (advanced_features,)


NODE_CLASS_MAPPINGS = {
    "RunwareImageInferenceAdvancedFeatures": RunwareImageInferenceAdvancedFeatures,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareImageInferenceAdvancedFeatures": "Runware Image Inference Advanced Features",
}
