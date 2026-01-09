"""
Runware Mirelo Provider Settings Node
Provides Mirelo-specific settings for audio generation
"""

from typing import Optional, Dict, Any


class RunwareMireloProviderSettings:
    """Runware Mirelo Provider Settings Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useStartOffset": ("BOOLEAN", {
                    "tooltip": "Enable to include startOffset parameter in provider settings",
                    "default": False,
                }),
                "startOffset": ("INT", {
                    "tooltip": "Start offset in seconds for audio generation. Specifies the starting point in the video (0-10 seconds). Only used when 'Use Start Offset' is enabled.",
                    "default": 0,
                    "min": 0,
                    "max": 10,
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("Provider Settings",)
    FUNCTION = "createProviderSettings"
    CATEGORY = "Runware/Provider Settings"
    DESCRIPTION = "Configure Mirelo-specific provider settings for audio generation including start offset for video-to-audio conversion."

    def createProviderSettings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create Mirelo provider settings"""

        # Get control parameters
        useStartOffset = kwargs.get("useStartOffset", False)

        # Get value parameters
        startOffset = kwargs.get("startOffset", 0)

        # Build settings dictionary - only include what is enabled
        mireloSettings: Dict[str, Any] = {}

        # Add startOffset only if useStartOffset is enabled
        if useStartOffset:
            mireloSettings["startOffset"] = startOffset

        # Clean up None values
        mireloSettings = {k: v for k, v in mireloSettings.items() if v is not None}

        # Return flat dictionary - will be wrapped by inference node with provider name
        return (mireloSettings,)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareMireloProviderSettings": RunwareMireloProviderSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareMireloProviderSettings": "Runware Mirelo Provider Settings",
}

