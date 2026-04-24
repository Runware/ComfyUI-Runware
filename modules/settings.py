"""
Runware Image Inference Settings (registered as Runware Settings for workflow compatibility).
Provides settings for image generation including temperature, systemPrompt, topP, layers,
quality, background, promptExtend, editRegions, thinking (boolean),
thinkingLevel (high/medium/low), sequential, and colorPalette
(from Runware Image Inference Settings Color Palette).
"""

import json
from typing import Any, Dict, List, Optional


class RunwareSettings:
    """Runware Image Inference Settings node (display name); API registration key remains Runware Settings."""

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
                "usePromptExtend": ("BOOLEAN", {
                    "tooltip": "Enable to include promptExtend (automatic prompt rewriting/expansion) in API request.",
                    "default": False,
                }),
                "promptExtend": ("BOOLEAN", {
                    "tooltip": "Enables automatic prompt rewriting/expansion to improve quality. Adds 3–5s latency. Disable for detailed prompts or latency-sensitive use cases. Only used when 'Use Prompt Extend' is enabled.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useEditRegions": ("BOOLEAN", {
                    "tooltip": "Enable to include editRegions in settings (per-input-image bounding boxes for edit flows).",
                    "default": False,
                }),
                "editRegions": ("STRING", {
                    "multiline": True,
                    "tooltip": "JSON array: one entry per input image; each entry is a list of boxes [x1,y1,x2,y2]. Example: [[[0,0,12,12],[25,25,100,100]],[],[[10,10,50,50]]]",
                    "default": "",
                }),
                "useThinking": ("BOOLEAN", {
                    "tooltip": "Enable to include thinking (boolean) in settings.",
                    "default": False,
                }),
                "thinking": ("BOOLEAN", {
                    "tooltip": "Thinking / reasoning flag passed in settings. Only used when 'Use Thinking' is enabled.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useSequential": ("BOOLEAN", {
                    "tooltip": "Enable to include sequential (boolean) in settings.",
                    "default": False,
                }),
                "sequential": ("BOOLEAN", {
                    "tooltip": "Sequential / image-set mode flag. Only used when 'Use Sequential' is enabled.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "colorPalette": ("RUNWAREIMAGEINFERENCECOLORPALETTE", {
                    "tooltip": "Connect Runware Image Inference Color Palette. When the palette node outputs at least one swatch, it is merged into settings.colorPalette.",
                }),
                "useThinkingLevel": ("BOOLEAN", {
                    "tooltip": "Enable to include thinkingLevel (string) in settings.",
                    "default": False,
                }),
                "thinkingLevel": (["high", "medium", "low"], {
                    "default": "high",
                    "tooltip": "Reasoning level for visual understanding. Only used when 'Use Thinking Level' is enabled.",
                }),
                "useBackground": ("BOOLEAN", {
                    "tooltip": "Enable to include background style in API request",
                    "default": False,
                }),
                "background": (["auto", "transparent", "opaque"], {
                    "default": "auto",
                    "tooltip": "Background style for the generated image. Only used when 'Use Background' is enabled.",
                }),
            }
        }

    RETURN_TYPES = ("RUNWARESETTINGS",)
    RETURN_NAMES = ("Settings",)
    FUNCTION = "createSettings"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Configure general settings for image generation: temperature, system prompt, top-p, layers, quality, background, "
        "promptExtend, editRegions (JSON), thinking (boolean), thinkingLevel (high/medium/low), sequential, and optional colorPalette from the Color Palette node."
    )

    def createSettings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create settings configuration"""

        # Get control parameters
        useTemperature = kwargs.get("useTemperature", False)
        useSystemPrompt = kwargs.get("useSystemPrompt", False)
        useTopP = kwargs.get("useTopP", False)
        useLayers = kwargs.get("useLayers", False)
        useTrueCFGScale = kwargs.get("useTrueCFGScale", False)
        useQuality = kwargs.get("useQuality", False)
        useBackground = kwargs.get("useBackground", False)
        usePromptExtend = kwargs.get("usePromptExtend", False)
        promptExtend = kwargs.get("promptExtend", False)
        useEditRegions = kwargs.get("useEditRegions", False)
        useThinking = kwargs.get("useThinking", False)
        useThinkingLevel = kwargs.get("useThinkingLevel", False)
        useSequential = kwargs.get("useSequential", False)

        # Get value parameters
        temperature = kwargs.get("temperature", 1.0)
        systemPrompt = kwargs.get("systemPrompt", "")
        topP = kwargs.get("topP", 1.0)
        layers = kwargs.get("layers")
        trueCFGScale = kwargs.get("trueCFGScale")
        quality = kwargs.get("quality", "medium")
        background = kwargs.get("background", "auto")

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
        if useBackground:
            settings["background"] = background
        if usePromptExtend:
            settings["promptExtend"] = bool(promptExtend)

        if useEditRegions:
            raw_er = (kwargs.get("editRegions") or "").strip()
            if raw_er:
                try:
                    parsed = json.loads(raw_er)
                except json.JSONDecodeError as e:
                    raise ValueError(f"editRegions must be valid JSON: {e}") from e
                if not isinstance(parsed, list):
                    raise ValueError("editRegions JSON must be an array (one element per input image).")
                settings["editRegions"] = parsed

        if useThinking:
            settings["thinking"] = bool(kwargs.get("thinking", False))

        if useThinkingLevel:
            settings["thinkingLevel"] = str(kwargs.get("thinkingLevel", "high"))

        if useSequential:
            settings["sequential"] = bool(kwargs.get("sequential", False))

        palette: Optional[List[Dict[str, Any]]] = kwargs.get("colorPalette")
        if palette is not None and isinstance(palette, list) and len(palette) > 0:
            settings["colorPalette"] = palette

        # Clean up None values
        settings = {k: v for k, v in settings.items() if v is not None}

        return (settings,)

