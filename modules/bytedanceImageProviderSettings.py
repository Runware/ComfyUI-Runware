"""
Runware Bytedance Image Provider Settings Node
Provides Bytedance-specific settings for image generation
"""

from typing import Optional, Dict, Any

class RunwareBytedanceProviderSettings:
    """Runware Bytedance Image Provider Settings Node"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useCameraFixed": ("BOOLEAN", {
                    "tooltip": "Enable to include cameraFixed parameter in provider settings",
                    "default": False,
                }),
                "cameraFixed": ("BOOLEAN", {
                    "tooltip": "Enable to fix camera position during video generation",
                    "default": False,
                }),
                "useMaxSequentialImages": ("BOOLEAN", {
                    "tooltip": "Enable to include maxSequentialImages parameter in provider settings",
                    "default": False,
                }),
                "maxSequentialImages": ("INT", {
                    "tooltip": "Maximum number of sequential images to generate (1-15)",
                    "default": 1,
                    "min": 1,
                    "max": 15,
                }),
                "useFastMode": ("BOOLEAN", {
                    "tooltip": "Enable to include fastMode parameter in provider settings",
                    "default": False,
                }),
                "fastMode": ("BOOLEAN", {
                    "tooltip": "When enabled, speeds up generation by sacrificing some effects. Default: false. RTF: 25-28 (fast) vs 35 (normal). Supported by OmniHuman 1.5.",
                    "default": False,
                }),
            }
        }
    
    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("providerSettings",)
    FUNCTION = "create_provider_settings"
    CATEGORY = "Runware/Provider Settings"
    
    def create_provider_settings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create Bytedance provider settings"""
        
        # Get control parameters
        useCameraFixed = kwargs.get("useCameraFixed", False)
        useMaxSequentialImages = kwargs.get("useMaxSequentialImages", False)
        useFastMode = kwargs.get("useFastMode", False)
        
        # Get value parameters
        cameraFixed = kwargs.get("cameraFixed", False)
        maxSequentialImages = kwargs.get("maxSequentialImages", 1)
        fastMode = kwargs.get("fastMode", False)
        
        # Build settings dictionary - only include what is enabled
        settings = {}
        
        # Add cameraFixed only if useCameraFixed is enabled
        if useCameraFixed:
            settings["cameraFixed"] = cameraFixed
        
        # Add maxSequentialImages only if useMaxSequentialImages is enabled
        if useMaxSequentialImages:
            settings["maxSequentialImages"] = maxSequentialImages
        
        # Add fastMode only if useFastMode is enabled
        if useFastMode:
            settings["fastMode"] = fastMode
        
        # Clean up None values
        settings = {k: v for k, v in settings.items() if v is not None}
        
        return (settings,)

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareBytedanceProviderSettings": RunwareBytedanceProviderSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareBytedanceProviderSettings": "Runware Bytedance Provider Settings",
}
