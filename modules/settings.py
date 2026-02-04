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
                "useLayers": ("BOOLEAN", {
                    "tooltip": "Enable to include layers parameter in API request",
                    "default": False,
                }),
                "layers": ("INT", {
                    "tooltip": "The number of layers to generate. Only used when 'Use Layers' is enabled.",
                    "default": 4,
                    "min": 1,
                    "max": 10,
                    "step": 1,
                }),
                "useTrueCFGScale": ("BOOLEAN", {
                    "tooltip": "Enable to include true_cfg_scale parameter in API request",
                    "default": False,
                }),
                "trueCFGScale": ("FLOAT", {
                    "tooltip": "Guidance scale as defined in Classifier-Free Diffusion Guidance. Classifier-free guidance is enabled by setting true_cfg_scale > 1 and a provided negative_prompt. Higher guidance scale encourages to generate images that are closely linked to the text prompt, usually at the expense of lower image quality. Only used when 'Use True CFG Scale' is enabled.",
                    "default": 1.0,
                    "min": 1.0,
                    "step": 0.1,
                }),
                "useQuality": ("BOOLEAN", {
                    "tooltip": "Enable to include quality parameter in API request",
                    "default": False,
                }),
                "quality": (["low", "medium", "high"], {
                    "default": "medium",
                    "tooltip": "Quality of the output image. Only used when 'Use Quality' is enabled.",
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
        useLayers = kwargs.get("useLayers", False)
        useTrueCFGScale = kwargs.get("useTrueCFGScale", False)
        useQuality = kwargs.get("useQuality", False)

        # Get value parameters
        temperature = kwargs.get("temperature", 1.0)
        systemPrompt = kwargs.get("systemPrompt", "")
        topP = kwargs.get("topP", 1.0)
        layers = kwargs.get("layers")
        trueCFGScale = kwargs.get("trueCFGScale")
        quality = kwargs.get("quality", "medium")

        # Build settings dictionary - only include what is enabled
        settings: Dict[str, Any] = {}

        # Add optional parameters only if enabled
        if useTemperature:
            settings["temperature"] = float(temperature)
        if useSystemPrompt and systemPrompt and systemPrompt.strip():
            settings["systemPrompt"] = systemPrompt.strip()
        if useTopP:
            settings["topP"] = float(topP)
        if useLayers:
            settings["layers"] = int(layers)
        if useTrueCFGScale:
            settings["true_cfg_scale"] = float(trueCFGScale)
        if useQuality:
            settings["quality"] = quality

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

