"""
Runware MiniMax Provider Settings Node
Provides MiniMax-specific settings for video generation
"""

from typing import Optional, Dict, Any

class RunwareMiniMaxProviderSettings:
    """Runware MiniMax Provider Settings Node"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "promptOptimizer": ("BOOLEAN", {
                    "tooltip": "Enable/disable prompt optimization.",
                    "default": False,
                }),
            }
        }
    
    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("providerSettings",)
    FUNCTION = "create_provider_settings"
    CATEGORY = "Runware/Provider Settings"
    
    def create_provider_settings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create MiniMax provider settings"""
        
        # Get value parameters
        promptOptimizer = kwargs.get("promptOptimizer", False)
        
        # Build settings dictionary
        # Always include promptOptimizer to ensure it's explicitly set
        settings = {
            "promptOptimizer": promptOptimizer
        }
        
        return (settings,)

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareMiniMaxProviderSettings": RunwareMiniMaxProviderSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareMiniMaxProviderSettings": "Runware MiniMax Provider Settings",
}

