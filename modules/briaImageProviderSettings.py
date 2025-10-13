"""
Runware Bria Image Provider Settings Node
Provides Bria-specific settings for image generation
"""

import torch
from typing import Optional, Dict, Any

class RunwareBriaProviderSettings:
    """Runware Bria Image Provider Settings Node"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "medium": (["photography", "art"], {
                    "tooltip": "Select the medium type for image generation",
                    "default": "photography",
                }),
                "promptEnhancement": ("BOOLEAN", {
                    "tooltip": "When set to true, enhances the provided prompt by generating additional, more descriptive variations, resulting in more diverse and creative output images. Note that turning this flag on may result in a few additional seconds to the inference time.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "enhanceImage": ("BOOLEAN", {
                    "tooltip": "When set to true, generates images with richer details, sharper textures, and enhanced clarity. Slightly increases generation time per image.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "promptContentModeration": ("BOOLEAN", {
                    "tooltip": "When enabled (default: true), the input prompt is scanned for NSFW or ethically restricted terms before image generation. If the prompt violates Bria's ethical guidelines, the request will be rejected with a 408 error.",
                    "default": True,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "contentModeration": ("BOOLEAN", {
                    "tooltip": "When enabled, applies content moderation to both input visuals and generated outputs.",
                    "default": True,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "ipSignal": ("BOOLEAN", {
                    "tooltip": "Flags prompts with potential IP content. If detected, a warning will be included in the response.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
            }
        }
    
    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("providerSettings",)
    FUNCTION = "create_provider_settings"
    CATEGORY = "Runware/Provider Settings"
    DESCRIPTION = "Configure Bria-specific provider settings for image generation including medium type, prompt enhancement, image enhancement, and content moderation options."
    
    def create_provider_settings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create Bria provider settings"""
        
        # Get parameters
        medium = kwargs.get("medium", "photography")
        promptEnhancement = kwargs.get("promptEnhancement", False)
        enhanceImage = kwargs.get("enhanceImage", False)
        promptContentModeration = kwargs.get("promptContentModeration", True)
        contentModeration = kwargs.get("contentModeration", True)
        ipSignal = kwargs.get("ipSignal", False)
        
        # Build settings dictionary
        settings = {}
        
        # Add medium
        if medium is not None:
            settings["medium"] = medium
        
        # Add promptEnhancement
        if promptEnhancement is not None:
            settings["promptEnhancement"] = promptEnhancement
        
        # Add enhanceImage
        if enhanceImage is not None:
            settings["enhanceImage"] = enhanceImage
        
        # Add promptContentModeration
        if promptContentModeration is not None:
            settings["promptContentModeration"] = promptContentModeration
        
        # Add contentModeration
        if contentModeration is not None:
            settings["contentModeration"] = contentModeration
        
        # Add ipSignal
        if ipSignal is not None:
            settings["ipSignal"] = ipSignal
        
        # Clean up None values
        settings = {k: v for k, v in settings.items() if v is not None}
        
        return (settings,)

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareBriaProviderSettings": RunwareBriaProviderSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareBriaProviderSettings": "Runware Bria Provider Settings",
}

