"""
Runware Bria Image Provider Settings Node
Provides Bria-specific settings for image generation
"""

import torch
from typing import Optional, Dict, Any

class RunwareBriaProviderSettings:
    """Runware Bria Image Provider Settings Node"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useMedium": ("BOOLEAN", {
                    "tooltip": "Enable to include medium parameter in API request. Disable if not needed.",
                    "default": False,
                }),
                "medium": (["None", "photography", "art"], {
                    "tooltip": "Select the medium type for image generation. Only used when 'Use Medium' is enabled.",
                    "default": "photography",
                }),
                "usePromptEnhancement": ("BOOLEAN", {
                    "tooltip": "Enable to include promptEnhancement parameter in API request.",
                    "default": False,
                }),
                "promptEnhancement": ("BOOLEAN", {
                    "tooltip": "When set to true, enhances the provided prompt by generating additional, more descriptive variations, resulting in more diverse and creative output images. Note that turning this flag on may result in a few additional seconds to the inference time. Only used when 'Use Prompt Enhancement' is enabled.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useEnhanceImage": ("BOOLEAN", {
                    "tooltip": "Enable to include enhanceImage parameter in API request.",
                    "default": False,
                }),
                "enhanceImage": ("BOOLEAN", {
                    "tooltip": "When set to true, generates images with richer details, sharper textures, and enhanced clarity. Slightly increases generation time per image. Only used when 'Use Enhance Image' is enabled.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "usePromptContentModeration": ("BOOLEAN", {
                    "tooltip": "Enable to include promptContentModeration parameter in API request.",
                    "default": False,
                }),
                "promptContentModeration": ("BOOLEAN", {
                    "tooltip": "When enabled (default: true), the input prompt is scanned for NSFW or ethically restricted terms before image generation. If the prompt violates Bria's ethical guidelines, the request will be rejected with a 408 error. Only used when 'Use Prompt Content Moderation' is enabled.",
                    "default": True,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useContentModeration": ("BOOLEAN", {
                    "tooltip": "Enable to include contentModeration parameter in API request.",
                    "default": False,
                }),
                "contentModeration": ("BOOLEAN", {
                    "tooltip": "When enabled, applies content moderation to both input visuals and generated outputs. Only used when 'Use Content Moderation' is enabled.",
                    "default": True,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useIpSignal": ("BOOLEAN", {
                    "tooltip": "Enable to include ipSignal parameter in API request.",
                    "default": False,
                }),
                "ipSignal": ("BOOLEAN", {
                    "tooltip": "Flags prompts with potential IP content. If detected, a warning will be included in the response. Only used when 'Use IP Signal' is enabled.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "usePreserveAlpha": ("BOOLEAN", {
                    "tooltip": "Enable to include preserveAlpha parameter in API request.",
                    "default": False,
                }),
                "preserveAlpha": ("BOOLEAN", {
                    "tooltip": "Preserve alpha channel in the image. Only used when 'Use Preserve Alpha' is enabled.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useMode": ("BOOLEAN", {
                    "tooltip": "Enable to include mode parameter in API request for Background Replace.",
                    "default": False,
                }),
                "mode": (["None", "base", "high_control", "fast"], {
                    "tooltip": "Selects the background-generation mode for Background Replace. Base: clean, high quality backgrounds. High_control: stronger prompt adherence and scene context, finer control over layout and details. Fast: same core capabilities as base, optimal speed and quality balance. Only used when 'Use Mode' is enabled.",
                    "default": "base",
                }),
                "useEnhanceReferenceImages": ("BOOLEAN", {
                    "tooltip": "Enable to include enhanceReferenceImages parameter in API request.",
                    "default": False,
                }),
                "enhanceReferenceImages": ("BOOLEAN", {
                    "tooltip": "When set to true, additional logic processes the included reference image to make adjustments for optimal results. Only used when 'Use Enhance Reference Images' is enabled.",
                    "default": True,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useRefinePrompt": ("BOOLEAN", {
                    "tooltip": "Enable to include refinePrompt parameter in API request.",
                    "default": False,
                }),
                "refinePrompt": ("BOOLEAN", {
                    "tooltip": "When true, an additional logic takes the prompt that was included and adjusts it to achieve optimal results. Only used when 'Use Refine Prompt' is enabled.",
                    "default": True,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useOriginalQuality": ("BOOLEAN", {
                    "tooltip": "Enable to include originalQuality parameter in API request.",
                    "default": False,
                }),
                "originalQuality": ("BOOLEAN", {
                    "tooltip": "When true, the output image retains the original input image's size; otherwise, the image is scaled to 1 megapixel (1MP) while preserving its aspect ratio. Only used when 'Use Original Quality' is enabled.",
                    "default": True,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useForceBackgroundDetection": ("BOOLEAN", {
                    "tooltip": "Enable to include forceBackgroundDetection parameter in API request.",
                    "default": False,
                }),
                "forceBackgroundDetection": ("BOOLEAN", {
                    "tooltip": "When true, forces background detection and removal, even if the original image already contains an alpha channel. Useful for refining existing foreground/background separation or ignoring unnecessary alpha channels. Only used when 'Use Force Background Detection' is enabled.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "usePreserveAudio": ("BOOLEAN", {
                    "tooltip": "Enable to include preserveAudio parameter in API request.",
                    "default": False,
                }),
                "preserveAudio": ("BOOLEAN", {
                    "tooltip": "Whether to keep the original audio track. Only used when 'Use Preserve Audio' is enabled.",
                    "default": True,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useAutoTrim": ("BOOLEAN", {
                    "tooltip": "Enable to include autoTrim parameter in API request.",
                    "default": False,
                }),
                "autoTrim": ("BOOLEAN", {
                    "tooltip": "If true, videos longer than 5 seconds are trimmed to the first 5 seconds. If false, videos longer than 5 seconds are rejected. Only used when 'Use Auto Trim' is enabled.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useSeason": ("BOOLEAN", {
                    "tooltip": "Enable to include season parameter (maps to /reseason).",
                    "default": False,
                }),
                "season": (["spring", "summer", "autumn", "winter"], {
                    "tooltip": "Desired season. Maps to /reseason.",
                    "default": "spring",
                }),
                "useEdit": ("BOOLEAN", {
                    "tooltip": "Enable to include edit parameter.",
                    "default": False,
                }),
                "edit": (["colorize", "relight", "restore", "blend", "reseason", "sketch_to_image"], {
                    "tooltip": "Edit mode: colorize, relight, restore, blend, reseason, sketch_to_image.",
                    "default": "restore",
                }),
                "useColor": ("BOOLEAN", {
                    "tooltip": "Enable to include color parameter (maps to /colorize).",
                    "default": False,
                }),
                "color": (["contemporary color", "vivid color", "black and white colors", "sepia vintage"], {
                    "tooltip": "Restoration/color style. Maps to /colorize.",
                    "default": "contemporary color",
                }),
                "useLightDirection": ("BOOLEAN", {
                    "tooltip": "Enable to include lightDirection parameter (maps to /relight).",
                    "default": False,
                }),
                "lightDirection": (["front", "side", "bottom", "top-down"], {
                    "tooltip": "Direction of light. Maps to /relight.",
                    "default": "front",
                }),
                "useLightType": ("BOOLEAN", {
                    "tooltip": "Enable to include lightType parameter (maps to /relight).",
                    "default": False,
                }),
                "lightType": ([
                    "midday", "blue hour light", "low-angle sunlight", "sunrise light",
                    "spotlight on subject, keep background settings", "overcast light",
                    "soft overcast daylight lighting", "cloud-filtered lighting", "fog-diffused lighting",
                    "moonlight lighting", "starlight lighting nighttime", "soft bokeh lighting",
                    "harsh studio lighting keep background setting",
                ], {
                    "tooltip": "Type of lighting. Maps to /relight.",
                    "default": "midday",
                }),
                "Bria Provider Setting Mask": ("RUNWAREBRIAPROVIDERMASK", {
                    "tooltip": "Connect Runware Bria Provider Mask node to provide mask configuration for video eraser operations.",
                }),
            }
        }
    
    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("providerSettings",)
    FUNCTION = "create_provider_settings"
    CATEGORY = "Runware/Provider Settings"
    DESCRIPTION = "Configure Bria-specific provider settings for image generation and background replacement including medium type, prompt enhancement, image enhancement, content moderation options, and background replace mode settings."
    
    def create_provider_settings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create Bria provider settings"""
        
        # Get use parameters
        useMedium = kwargs.get("useMedium", False)
        usePromptEnhancement = kwargs.get("usePromptEnhancement", False)
        useEnhanceImage = kwargs.get("useEnhanceImage", False)
        usePromptContentModeration = kwargs.get("usePromptContentModeration", False)
        useContentModeration = kwargs.get("useContentModeration", False)
        useIpSignal = kwargs.get("useIpSignal", False)
        usePreserveAlpha = kwargs.get("usePreserveAlpha", False)
        useMode = kwargs.get("useMode", False)
        useEnhanceReferenceImages = kwargs.get("useEnhanceReferenceImages", False)
        useRefinePrompt = kwargs.get("useRefinePrompt", False)
        useOriginalQuality = kwargs.get("useOriginalQuality", False)
        useForceBackgroundDetection = kwargs.get("useForceBackgroundDetection", False)
        usePreserveAudio = kwargs.get("usePreserveAudio", False)
        useAutoTrim = kwargs.get("useAutoTrim", False)
        useSeason = kwargs.get("useSeason", False)
        useEdit = kwargs.get("useEdit", False)
        useColor = kwargs.get("useColor", False)
        useLightDirection = kwargs.get("useLightDirection", False)
        useLightType = kwargs.get("useLightType", False)
        
        # Get actual parameters
        medium = kwargs.get("medium", "photography")
        promptEnhancement = kwargs.get("promptEnhancement", False)
        enhanceImage = kwargs.get("enhanceImage", False)
        promptContentModeration = kwargs.get("promptContentModeration", True)
        contentModeration = kwargs.get("contentModeration", True)
        ipSignal = kwargs.get("ipSignal", False)
        preserveAlpha = kwargs.get("preserveAlpha", False)
        mode = kwargs.get("mode", "base")
        enhanceReferenceImages = kwargs.get("enhanceReferenceImages", True)
        refinePrompt = kwargs.get("refinePrompt", True)
        originalQuality = kwargs.get("originalQuality", True)
        forceBackgroundDetection = kwargs.get("forceBackgroundDetection", False)
        preserveAudio = kwargs.get("preserveAudio", True)
        autoTrim = kwargs.get("autoTrim", False)
        season = kwargs.get("season", "spring")
        edit = kwargs.get("edit", "restore")
        color = kwargs.get("color", "contemporary color")
        lightDirection = kwargs.get("lightDirection", "front")
        lightType = kwargs.get("lightType", "midday")
        mask = kwargs.get("Bria Provider Setting Mask", None)
        
        # Build settings dictionary
        settings = {}
        
        # Add medium only if useMedium is enabled
        if useMedium and medium is not None and medium != "None":
            settings["medium"] = medium
        
        # Add promptEnhancement only if usePromptEnhancement is enabled
        if usePromptEnhancement:
            settings["promptEnhancement"] = promptEnhancement
        
        # Add enhanceImage only if useEnhanceImage is enabled
        if useEnhanceImage:
            settings["enhanceImage"] = enhanceImage
        
        # Add promptContentModeration only if usePromptContentModeration is enabled
        if usePromptContentModeration:
            settings["promptContentModeration"] = promptContentModeration
        
        # Add contentModeration only if useContentModeration is enabled
        if useContentModeration:
            settings["contentModeration"] = contentModeration
        
        # Add ipSignal only if useIpSignal is enabled
        if useIpSignal:
            settings["ipSignal"] = ipSignal
        
        # Add preserveAlpha only if usePreserveAlpha is enabled
        if usePreserveAlpha:
            settings["preserveAlpha"] = preserveAlpha
        
        # Add mode only if useMode is enabled (for Background Replace)
        if useMode and mode is not None and mode != "None":
            settings["mode"] = mode
        
        # Add enhanceReferenceImages only if useEnhanceReferenceImages is enabled
        if useEnhanceReferenceImages:
            settings["enhanceReferenceImages"] = enhanceReferenceImages
        
        # Add refinePrompt only if useRefinePrompt is enabled
        if useRefinePrompt:
            settings["refinePrompt"] = refinePrompt
        
        # Add originalQuality only if useOriginalQuality is enabled
        if useOriginalQuality:
            settings["originalQuality"] = originalQuality
        
        # Add forceBackgroundDetection only if useForceBackgroundDetection is enabled
        if useForceBackgroundDetection:
            settings["forceBackgroundDetection"] = forceBackgroundDetection
        
        # Add preserveAudio only if usePreserveAudio is enabled
        if usePreserveAudio:
            settings["preserveAudio"] = preserveAudio
        
        # Add autoTrim only if useAutoTrim is enabled
        if useAutoTrim:
            settings["autoTrim"] = autoTrim
        
        # Add season only if useSeason is enabled (maps to /reseason)
        if useSeason:
            settings["season"] = season
        
        # Add edit only if useEdit is enabled
        if useEdit:
            settings["edit"] = edit
        
        # Add color only if useColor is enabled (maps to /colorize)
        if useColor:
            settings["color"] = color
        
        # Add lightDirection only if useLightDirection is enabled (maps to /relight
        if useLightDirection:
            settings["lightDirection"] = lightDirection
        
        # Add lightType only if useLightType is enabled (maps to /relight)
        if useLightType:
            settings["lightType"] = lightType
        
        # Add mask if provided from Mask node
        if mask is not None and isinstance(mask, dict) and len(mask) > 0:
            settings["mask"] = mask
        
        # Clean up None values
        settings = {k: v for k, v in settings.items() if v is not None}
        
        return (settings,)

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareBriaProviderSettings": RunwareBriaProviderSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareBriaProviderSettings": "Runware Bria Provider Settings",
}

