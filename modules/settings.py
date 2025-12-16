"""
Runware Settings Node
Provides general settings for image generation including temperature, systemPrompt, and topP
"""

from typing import Optional, Dict, Any


class RunwareSettings:
    """Runware Settings Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useTemperature": ("BOOLEAN", {
                    "tooltip": "Enable to include temperature parameter in API request",
                    "default": False,
                }),
                "temperature": ("FLOAT", {
                    "tooltip": "Temperature value for generation. Only used when 'Use Temperature' is enabled.",
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                }),
                "useSystemPrompt": ("BOOLEAN", {
                    "tooltip": "Enable to include systemPrompt parameter in API request",
                    "default": False,
                }),
                "systemPrompt": ("STRING", {
                    "multiline": True,
                    "tooltip": "System prompt for generation. Only used when 'Use System Prompt' is enabled.",
                    "default": "",
                }),
                "useTopP": ("BOOLEAN", {
                    "tooltip": "Enable to include topP parameter in API request",
                    "default": False,
                }),
                "topP": ("FLOAT", {
                    "tooltip": "Top-p (nucleus) sampling parameter. Only used when 'Use Top P' is enabled.",
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
            }
        }

    RETURN_TYPES = ("RUNWARESETTINGS",)
    RETURN_NAMES = ("Settings",)
    FUNCTION = "createSettings"
    CATEGORY = "Runware"
    DESCRIPTION = "Configure general settings for image generation including temperature, system prompt, and top-p sampling."

    def createSettings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create settings configuration"""

        # Get control parameters
        useTemperature = kwargs.get("useTemperature", False)
        useSystemPrompt = kwargs.get("useSystemPrompt", False)
        useTopP = kwargs.get("useTopP", False)

        # Get value parameters
        temperature = kwargs.get("temperature", 1.0)
        systemPrompt = kwargs.get("systemPrompt", "")
        topP = kwargs.get("topP", 1.0)

        # Build settings dictionary - only include what is enabled
        settings: Dict[str, Any] = {}

        # Add optional parameters only if enabled
        if useTemperature:
            settings["temperature"] = float(temperature)
        if useSystemPrompt and systemPrompt and systemPrompt.strip():
            settings["systemPrompt"] = systemPrompt.strip()
        if useTopP:
            settings["topP"] = float(topP)

        # Clean up None values
        settings = {k: v for k, v in settings.items() if v is not None}

        return (settings,)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareSettings": RunwareSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareSettings": "Runware Settings",
}

