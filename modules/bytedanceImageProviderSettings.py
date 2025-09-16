"""
Runware Bytedance Image Provider Settings Node
Provides Bytedance-specific settings for image generation
"""

import torch
from typing import Optional, Dict, Any

class RunwareBytedanceProviderSettings:
    """Runware Bytedance Image Provider Settings Node"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "cameraFixed": ("BOOLEAN", {
                    "tooltip": "Enable to fix camera position during video generation",
                    "default": False,
                }),
                "maxSequentialImages": ("INT", {
                    "tooltip": "Maximum number of sequential images to generate (1-15)",
                    "default": 1,
                    "min": 1,
                    "max": 15,
                }),
            }
        }
    
    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("providerSettings",)
    FUNCTION = "create_provider_settings"
    CATEGORY = "Runware/Provider Settings"
    
    def create_provider_settings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create Bytedance provider settings"""
        
        # Get parameters
        cameraFixed = kwargs.get("cameraFixed", False)
        maxSequentialImages = kwargs.get("maxSequentialImages", 1)
        
        # Build settings dictionary
        settings = {}
        
        # Add cameraFixed only if it's true
        if cameraFixed is True:
            settings["cameraFixed"] = cameraFixed
        
        # Add maxSequentialImages if provided and valid
        if maxSequentialImages is not None and 1 <= maxSequentialImages <= 15:
            settings["maxSequentialImages"] = maxSequentialImages
        
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
