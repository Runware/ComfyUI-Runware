"""
Runware Alibaba Provider Settings Node
Provides Alibaba-specific settings for image/video generation
"""

from typing import Optional, Dict, Any


class RunwareAlibabaProviderSettings:
    """Runware Alibaba Provider Settings Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "usePromptEnhancer": ("BOOLEAN", {
                    "tooltip": "Enable to include promptEnhancer parameter in provider settings",
                    "default": False,
                }),
                "promptEnhancer": ("BOOLEAN", {
                    "tooltip": "Enable prompt enhancement for Alibaba generation. Only used when 'Use Prompt Enhancer' is enabled.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("Provider Settings",)
    FUNCTION = "createProviderSettings"
    CATEGORY = "Runware/Provider Settings"
    DESCRIPTION = "Configure Alibaba-specific provider settings for image/video generation including prompt enhancement."

    def createProviderSettings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create Alibaba provider settings"""

        # Get control parameters
        usePromptEnhancer = kwargs.get("usePromptEnhancer", False)

        # Get value parameters
        promptEnhancer = kwargs.get("promptEnhancer", False)

        # Build settings dictionary - only include what is enabled
        alibabaSettings: Dict[str, Any] = {}

        # Add promptEnhancer only if usePromptEnhancer is enabled
        if usePromptEnhancer:
            alibabaSettings["promptEnhancer"] = promptEnhancer

        # Clean up None values
        alibabaSettings = {k: v for k, v in alibabaSettings.items() if v is not None}

        # Return flat dictionary - will be wrapped by inference node with provider name
        return (alibabaSettings,)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareAlibabaProviderSettings": RunwareAlibabaProviderSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareAlibabaProviderSettings": "Runware Alibaba Provider Settings",
}

