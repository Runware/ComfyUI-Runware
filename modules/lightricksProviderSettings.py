"""
Runware Lightricks Provider Settings Node
Provides Lightricks-specific settings for video generation
"""

from typing import Optional, Dict, Any

class RunwareLightricksProviderSettings:
    """Runware Lightricks Provider Settings Node"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "generateAudio": ("BOOLEAN", {
                    "tooltip": "Enable to generate audio for the video. Disable to generate video without audio. Default: false.",
                    "default": False,
                }),
            }
        }
    
    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("providerSettings",)
    FUNCTION = "create_provider_settings"
    CATEGORY = "Runware/Provider Settings"
    
    def create_provider_settings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create Lightricks provider settings"""
        
        # Get value parameters
        generateAudio = kwargs.get("generateAudio", False)
        
        # Build settings dictionary
        # Always include generateAudio to ensure it's explicitly set
        settings = {
            "generateAudio": generateAudio
        }
        
        return (settings,)

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareLightricksProviderSettings": RunwareLightricksProviderSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareLightricksProviderSettings": "Runware Lightricks Provider Settings",
}

