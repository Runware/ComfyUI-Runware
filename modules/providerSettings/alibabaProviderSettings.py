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
                "usePromptExtend": ("BOOLEAN", {
                    "tooltip": "Enable to include promptExtend parameter in provider settings",
                    "default": False,
                }),
                "promptExtend": ("BOOLEAN", {
                    "tooltip": "Enable LLM prompt rewriting. If enabled, a large language model (LLM) rewrites the input prompt. This can significantly improve the generation quality for shorter prompts but increases the time required. Only used when 'Use Prompt Extend' is enabled.",
                    "default": True,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useAudio": ("BOOLEAN", {
                    "tooltip": "Enable to include audio parameter in provider settings",
                    "default": False,
                }),
                "audio": ("BOOLEAN", {
                    "tooltip": "Automatically add audio (ignored if audio_url is set). Only used when 'Use Audio' is enabled.",
                    "default": True,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useShotType": ("BOOLEAN", {
                    "tooltip": "Enable to include shotType parameter in provider settings. Only applicable if promptExtend is enabled.",
                    "default": False,
                }),
                "shotType": (["single", "multi"], {
                    "tooltip": "Shot type for generation. Only applicable if promptExtend is true. Only used when 'Use Shot Type' is enabled.",
                    "default": "single",
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("Provider Settings",)
    FUNCTION = "createProviderSettings"
    CATEGORY = "Runware/Provider Settings"
    DESCRIPTION = "Configure Alibaba-specific provider settings for image/video generation including prompt enhancement, prompt extension, audio, and shot type."

    def createProviderSettings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create Alibaba provider settings"""

        # Get control parameters
        usePromptEnhancer = kwargs.get("usePromptEnhancer", False)
        usePromptExtend = kwargs.get("usePromptExtend", False)
        useAudio = kwargs.get("useAudio", False)
        useShotType = kwargs.get("useShotType", False)

        # Get value parameters
        promptEnhancer = kwargs.get("promptEnhancer", False)
        promptExtend = kwargs.get("promptExtend", True)
        audio = kwargs.get("audio", True)
        shotType = kwargs.get("shotType", "single")

        # Build settings dictionary - only include what is enabled
        alibabaSettings: Dict[str, Any] = {}

        # Add promptEnhancer only if usePromptEnhancer is enabled
        if usePromptEnhancer:
            alibabaSettings["promptEnhancer"] = promptEnhancer

        # Add promptExtend only if usePromptExtend is enabled
        if usePromptExtend:
            alibabaSettings["promptExtend"] = promptExtend

        # Add audio only if useAudio is enabled
        if useAudio:
            alibabaSettings["audio"] = audio

        # Add shotType only if useShotType is enabled and promptExtend is enabled
        if useShotType and usePromptExtend and promptExtend:
            if shotType is not None and shotType != "None":
                alibabaSettings["shotType"] = shotType

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

