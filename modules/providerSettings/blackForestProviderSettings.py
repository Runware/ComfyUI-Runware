"""
Runware BlackForest Labs Provider Settings Node
Provides BlackForest Labs-specific settings for image generation
"""

from typing import Optional, Dict, Any

class RunwareBlackForestProviderSettings:
    """Runware BlackForest Labs Provider Settings Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useSafetyTolerance": ("BOOLEAN", {
                    "tooltip": "Enable to include safetyTolerance parameter in API request",
                    "default": False,
                }),
                "safetyTolerance": ("INT", {
                    "tooltip": "Safety tolerance value for generation. Only used when 'Use Safety Tolerance' is enabled.",
                    "default": 0,
                    "min": 0,
                    "max": 100,
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("Provider Settings",)
    FUNCTION = "createProviderSettings"
    CATEGORY = "Runware/Provider Settings"
    DESCRIPTION = "Configure BlackForest Labs-specific provider settings for image generation including safety tolerance."

    def createProviderSettings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create BlackForest Labs provider settings"""

        # Get control parameters
        useSafetyTolerance = kwargs.get("useSafetyTolerance", False)

        # Get value parameters
        safetyTolerance = kwargs.get("safetyTolerance", 0)

        # Build settings dictionary - only include what is enabled
        blackForestSettings: Dict[str, Any] = {}

        # Add safetyTolerance only if useSafetyTolerance is enabled
        if useSafetyTolerance:
            blackForestSettings["safetyTolerance"] = safetyTolerance

        # Clean up None values
        blackForestSettings = {k: v for k, v in blackForestSettings.items() if v is not None}

        # Return flat dictionary - will be wrapped by inference node with provider name
        return (blackForestSettings,)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareBlackForestProviderSettings": RunwareBlackForestProviderSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareBlackForestProviderSettings": "Runware BlackForest Labs Provider Settings",
}

