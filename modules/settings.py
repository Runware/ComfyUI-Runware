"""
Runware Image Inference Settings (registered as Runware Settings for workflow compatibility).
Provides settings for image generation including temperature, systemPrompt, topP, layers,
quality, background, style, search, promptExtend, editRegions, thinking (boolean),
thinkingLevel (low/medium/high/xhigh), backgroundMode (original/transparent/solid), backgroundColor,
enhancePrompt, scoringPrompt, sequential, renderingSpeed (TURBO/DEFAULT/QUALITY),
magicPrompt (AUTO/ON/OFF), autoCrop, dilatePixels, creativity (raw/low/medium/high), colorPalette,
moodboards (from Runware Image Inference Settings Moodboards),
structuredPrompt (from Runware Image Inference Settings Structured Prompt; Ideogram 4.0),
and promptEnhance (from Runware Image Inference Settings Prompt Enhance),
preserveInputSize (return output at original input resolution).
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
                "thinkingLevel": (["high", "medium", "low", "xhigh"], {
                    "default": "high",
                    "tooltip": (
                        "Reasoning level for visual understanding. Riverflow 2.5 also supports xhigh (Pro only). "
                        "Only used when 'Use Thinking Level' is enabled."
                    ),
                }),
                "useBackground": ("BOOLEAN", {
                    "tooltip": "Enable to include background style in API request",
                    "default": False,
                }),
                "background": (["auto", "transparent", "opaque"], {
                    "default": "auto",
                    "tooltip": "Background style for the generated image. Only used when 'Use Background' is enabled.",
                }),
                "useStyle": ("BOOLEAN", {
                    "tooltip": "Enable to include style preset in API request",
                    "default": False,
                }),
                "style": ("STRING", {
                    "default": "auto",
                    "multiline": False,
                    "tooltip": "Style preset for generation. Only used when 'Use Style' is enabled.",
                }),
                "useSearch": ("BOOLEAN", {
                    "tooltip": "Enable to include search grounding in API request",
                    "default": False,
                }),
                "search": ("BOOLEAN", {
                    "tooltip": "Enables web search grounding for reference. Only used when 'Use Search' is enabled.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useRenderingSpeed": ("BOOLEAN", {
                    "tooltip": "Enable to include renderingSpeed in settings.",
                    "default": False,
                }),
                "renderingSpeed": (["TURBO", "DEFAULT", "QUALITY"], {
                    "default": "DEFAULT",
                    "tooltip": "The rendering speed to use. Only used when 'Use Rendering Speed' is enabled.",
                }),
                "useMagicPrompt": ("BOOLEAN", {
                    "tooltip": "Enable to include magicPrompt in settings.",
                    "default": False,
                }),
                "magicPrompt": (["AUTO", "ON", "OFF"], {
                    "default": "AUTO",
                    "tooltip": "Determine if MagicPrompt should be used. Only used when 'Use Magic Prompt' is enabled.",
                }),
                "useAutoCrop": ("BOOLEAN", {
                    "tooltip": "Enable to include autoCrop in settings.",
                    "default": False,
                }),
                "autoCrop": ("BOOLEAN", {
                    "tooltip": "If true, crop the reference image to the canvas bounds when it extends beyond the edges. Defaults to false. Only used when 'Use Auto Crop' is enabled.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useDilatePixels": ("BOOLEAN", {
                    "tooltip": "Enable to include dilatePixels in settings.",
                    "default": False,
                }),
                "dilatePixels": ("INT", {
                    "tooltip": "Expands mask edges for cleaner removal. Only used when 'Use Dilate Pixels' is enabled.",
                    "default": 10,
                    "min": 0,
                    "max": 100,
                    "step": 1,
                }),
                "useCreativity": ("BOOLEAN", {
                    "tooltip": "Enable to include creativity in settings.",
                    "default": False,
                }),
                "creativity": (["raw", "low", "medium", "high"], {
                    "default": "medium",
                    "tooltip": "Creativity level. Only used when 'Use Creativity' is enabled.",
                }),
                "moodboards": ("RUNWAREIMAGEINFERENCEMOODBOARDS", {
                    "tooltip": "Connect Runware Image Inference Settings Moodboards. When connected with at least one entry, it is merged into settings.moodboards.",
                }),
                "structuredPrompt": ("RUNWAREIMAGEINFERENCESTRUCTUREDPROMPT", {
                    "tooltip": "Connect Runware Image Inference Settings Structured Prompt (Ideogram 4.0). Merged into settings.structuredPrompt. Mutually exclusive with positivePrompt on the same API request.",
                }),
                "promptEnhance": ("RUNWAREIMAGEINFERENCEPROMPTENHANCE", {
                    "tooltip": "Connect Runware Image Inference Settings Prompt Enhance. Merged into settings.promptEnhance (temperature, topP). Omit from API when not connected or empty.",
                }),
                "useBackgroundMode": ("BOOLEAN", {
                    "tooltip": "Enable to include backgroundMode in settings (Riverflow 2.5 output background handling).",
                    "default": False,
                }),
                "backgroundMode": (["original", "transparent", "solid"], {
                    "default": "original",
                    "tooltip": (
                        "settings.backgroundMode: original, transparent, or solid. "
                        "Only used when 'Use Background Mode' is enabled."
                    ),
                }),
                "useBackgroundColor": ("BOOLEAN", {
                    "tooltip": "Enable to include backgroundColor in settings (required when backgroundMode is solid).",
                    "default": False,
                }),
                "backgroundColor": ("STRING", {
                    "default": "#FFFFFF",
                    "tooltip": (
                        "Hex color (#RRGGBB) composited when backgroundMode is solid. "
                        "Only used when 'Use Background Color' is enabled."
                    ),
                }),
                "useEnhancePrompt": ("BOOLEAN", {
                    "tooltip": "Enable to include enhancePrompt (boolean) in settings.",
                    "default": False,
                }),
                "enhancePrompt": ("BOOLEAN", {
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                    "tooltip": (
                        "Enhance the prompt with use-case context before generation (Riverflow 2.5). "
                        "Distinct from settings.promptEnhance (nested object). "
                        "Only used when 'Use Enhance Prompt' is enabled."
                    ),
                }),
                "useScoringPrompt": ("BOOLEAN", {
                    "tooltip": "Enable to include scoringPrompt in settings.",
                    "default": False,
                }),
                "scoringPrompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": (
                        "Optional quality rubric used when RF 2.5 scores candidate outputs. "
                        "Only used when 'Use Scoring Prompt' is enabled."
                    ),
                }),
                "scoringRubric": ("RUNWAREIMAGEINFERENCESCORINGRUBRIC", {
                    "tooltip": (
                        "Connect Runware Image Inference Settings Scoring Rubric or Scoring Rubric Combine "
                        "for settings.scoringRubric (up to 4 dimensions via Combine)."
                    ),
                }),
                "useCopyrightDetection": ("BOOLEAN", {
                    "tooltip": "Enable to include copyrightDetection in settings.",
                    "default": False,
                }),
                "copyrightDetection": ("BOOLEAN", {
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                    "tooltip": (
                        "Opt into post-generation copyright detection (Hive likeness + logo checks). "
                        "Only used when 'Use Copyright Detection' is enabled."
                    ),
                }),
                "usePreserveInputSize": ("BOOLEAN", {
                    "tooltip": "Enable to include preserveInputSize in settings.",
                    "default": False,
                }),
                "preserveInputSize": ("BOOLEAN", {
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                    "tooltip": (
                        "Return the output at the original input resolution. "
                        "Only used when 'Use Preserve Input Size' is enabled."
                    ),
                }),
            }
        }

    RETURN_TYPES = ("RUNWARESETTINGS",)
    RETURN_NAMES = ("Settings",)
    FUNCTION = "createSettings"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Configure general settings for image generation: temperature, system prompt, top-p, layers, quality, "
        "backgroundMode (original/transparent/solid), backgroundColor, enhancePrompt, scoringPrompt, background, style, search, "
        "promptExtend, editRegions (JSON), thinking (boolean), thinkingLevel (low/medium/high/xhigh), sequential, "
        "renderingSpeed (TURBO/DEFAULT/QUALITY), magicPrompt (AUTO/ON/OFF), autoCrop, dilatePixels, "
        "creativity (raw/low/medium/high), preserveInputSize, and optional colorPalette, moodboards, structuredPrompt, promptEnhance, "
        "and scoringRubric from dedicated settings nodes."
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
        useStyle = kwargs.get("useStyle", False)
        useSearch = kwargs.get("useSearch", False)
        usePromptExtend = kwargs.get("usePromptExtend", False)
        promptExtend = kwargs.get("promptExtend", False)
        useEditRegions = kwargs.get("useEditRegions", False)
        useThinking = kwargs.get("useThinking", False)
        useThinkingLevel = kwargs.get("useThinkingLevel", False)
        useBackgroundMode = kwargs.get("useBackgroundMode", False)
        useBackgroundColor = kwargs.get("useBackgroundColor", False)
        useEnhancePrompt = kwargs.get("useEnhancePrompt", False)
        useScoringPrompt = kwargs.get("useScoringPrompt", False)
        useCopyrightDetection = kwargs.get("useCopyrightDetection", False)
        usePreserveInputSize = kwargs.get("usePreserveInputSize", False)
        useSequential = kwargs.get("useSequential", False)
        useRenderingSpeed = kwargs.get("useRenderingSpeed", False)
        useMagicPrompt = kwargs.get("useMagicPrompt", False)
        useAutoCrop = kwargs.get("useAutoCrop", False)
        useDilatePixels = kwargs.get("useDilatePixels", False)
        useCreativity = kwargs.get("useCreativity", False)

        # Get value parameters
        temperature = kwargs.get("temperature", 1.0)
        systemPrompt = kwargs.get("systemPrompt", "")
        topP = kwargs.get("topP", 1.0)
        layers = kwargs.get("layers")
        trueCFGScale = kwargs.get("trueCFGScale")
        quality = kwargs.get("quality", "medium")
        background = kwargs.get("background", "auto")
        style = kwargs.get("style", "auto")
        renderingSpeed = kwargs.get("renderingSpeed", "DEFAULT")
        magicPrompt = kwargs.get("magicPrompt", "AUTO")
        creativity = kwargs.get("creativity", "medium")

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
        if useStyle:
            settings["style"] = style
        if useSearch:
            settings["search"] = bool(kwargs.get("search", False))
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

        if useBackgroundMode:
            settings["backgroundMode"] = str(kwargs.get("backgroundMode", "original"))

        if useBackgroundColor:
            background_color = (kwargs.get("backgroundColor") or "").strip()
            if background_color:
                settings["backgroundColor"] = background_color

        if useEnhancePrompt:
            settings["enhancePrompt"] = bool(kwargs.get("enhancePrompt", False))

        if useScoringPrompt:
            scoring_prompt = (kwargs.get("scoringPrompt") or "").strip()
            if scoring_prompt:
                settings["scoringPrompt"] = scoring_prompt

        if useCopyrightDetection:
            settings["copyrightDetection"] = bool(kwargs.get("copyrightDetection", False))

        if usePreserveInputSize:
            settings["preserveInputSize"] = bool(kwargs.get("preserveInputSize", False))

        if useSequential:
            settings["sequential"] = bool(kwargs.get("sequential", False))

        palette: Optional[List[Dict[str, Any]]] = kwargs.get("colorPalette")
        if palette is not None and isinstance(palette, list) and len(palette) > 0:
            settings["colorPalette"] = palette
        moodboards: Optional[List[Dict[str, Any]]] = kwargs.get("moodboards")
        if moodboards is not None and isinstance(moodboards, list) and len(moodboards) > 0:
            settings["moodboards"] = moodboards

        structured_prompt: Optional[Dict[str, Any]] = kwargs.get("structuredPrompt")
        if (
            structured_prompt is not None
            and isinstance(structured_prompt, dict)
            and len(structured_prompt) > 0
        ):
            settings["structuredPrompt"] = structured_prompt

        prompt_enhance: Optional[Dict[str, Any]] = kwargs.get("promptEnhance")
        if (
            prompt_enhance is not None
            and isinstance(prompt_enhance, dict)
            and len(prompt_enhance) > 0
        ):
            settings["promptEnhance"] = prompt_enhance

        scoring_rubric: Optional[List[Dict[str, Any]]] = kwargs.get("scoringRubric")
        if scoring_rubric is not None and isinstance(scoring_rubric, list) and len(scoring_rubric) > 0:
            settings["scoringRubric"] = scoring_rubric

        if useRenderingSpeed:
            settings["renderingSpeed"] = str(renderingSpeed)
        if useMagicPrompt:
            settings["magicPrompt"] = str(magicPrompt)
        if useAutoCrop:
            settings["autoCrop"] = bool(kwargs.get("autoCrop", False))
        if useDilatePixels:
            settings["dilatePixels"] = int(kwargs.get("dilatePixels", 10))
        if useCreativity:
            creativity = str(creativity)
            if creativity not in ("raw", "low", "medium", "high"):
                raise ValueError("creativity must be raw, low, medium, or high when useCreativity is enabled.")
            settings["creativity"] = creativity

        # Clean up None values
        settings = {k: v for k, v in settings.items() if v is not None}

        return (settings,)

