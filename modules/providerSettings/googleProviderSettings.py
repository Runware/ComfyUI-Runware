"""
Runware Google Provider Settings Node
Provides Google-specific settings for image/video generation
"""

from typing import Optional, Dict, Any


class RunwareGoogleProviderSettings:
    """Runware Google Provider Settings Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useGenerateAudio": ("BOOLEAN", {
                    "tooltip": "Enable to include generateAudio parameter in provider settings",
                    "default": False,
                }),
                "generateAudio": ("BOOLEAN", {
                    "tooltip": "Enable audio generation. Only used when 'Use Generate Audio' is enabled.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useEnhancePrompt": ("BOOLEAN", {
                    "tooltip": "Enable to include enhancePrompt parameter in provider settings",
                    "default": False,
                }),
                "enhancePrompt": ("BOOLEAN", {
                    "tooltip": "Enable prompt enhancement for Google generation. Only used when 'Use Enhance Prompt' is enabled.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useSearch": ("BOOLEAN", {
                    "tooltip": "Enable to include search parameter in provider settings",
                    "default": False,
                }),
                "search": ("BOOLEAN", {
                    "tooltip": "Enable search functionality. Only used when 'Use Search' is enabled.",
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
    DESCRIPTION = "Configure Google-specific provider settings for image/video generation including audio generation, prompt enhancement, and search."

    def createProviderSettings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create Google provider settings"""

        # Get control parameters
        useGenerateAudio = kwargs.get("useGenerateAudio", False)
        useEnhancePrompt = kwargs.get("useEnhancePrompt", False)
        useSearch = kwargs.get("useSearch", False)

        # Get value parameters
        generateAudio = kwargs.get("generateAudio", False)
        enhancePrompt = kwargs.get("enhancePrompt", False)
        search = kwargs.get("search", False)

        # Build settings dictionary - only include what is enabled
        googleSettings: Dict[str, Any] = {}

        # Add parameters only if their use toggles are enabled
        if useGenerateAudio:
            googleSettings["generateAudio"] = generateAudio
        if useEnhancePrompt:
            googleSettings["enhancePrompt"] = enhancePrompt
        if useSearch:
            googleSettings["search"] = search

        # Clean up None values
        googleSettings = {k: v for k, v in googleSettings.items() if v is not None}

        # Return flat dictionary - will be wrapped by inference node with provider name
        return (googleSettings,)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareGoogleProviderSettings": RunwareGoogleProviderSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareGoogleProviderSettings": "Runware Google Provider Settings",
}

