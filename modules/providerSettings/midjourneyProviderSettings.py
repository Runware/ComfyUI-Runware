"""
Runware Midjourney Provider Settings Node
Provides Midjourney-specific settings for image generation workflows.
"""

from typing import Any, Dict, Optional, Tuple


class RunwareMidjourneyProviderSettings:
    """Runware Midjourney Provider Settings Node"""

    QUALITY_STEP = 0.25
    QUALITY_MIN = 0.25
    QUALITY_MAX = 2.0
    DEFAULT_QUALITY = 1.0

    DEFAULT_STYLIZE = 0
    STYLIZE_MIN = 0
    STYLIZE_MAX = 1000

    DEFAULT_CHAOS = 0
    CHAOS_MIN = 0
    CHAOS_MAX = 100

    DEFAULT_WEIRD = 0
    WEIRD_MIN = 0
    WEIRD_MAX = 3000

    NIJI_OPTIONS = [
        "",  # Allow provider default when omitted
        "close",
        "0",
        "5",
        "6",
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "quality": ("FLOAT", {
                    "tooltip": "Midjourney quality multiplier (provider key: providerSettings.midjourney.quality).",
                    "default": cls.DEFAULT_QUALITY,
                    "min": cls.QUALITY_MIN,
                    "max": cls.QUALITY_MAX,
                    "step": cls.QUALITY_STEP,
                }),
                "stylize": ("INT", {
                    "tooltip": "Controls how strongly Midjourney's artistic style is applied (provider key: providerSettings.midjourney.stylize).",
                    "default": cls.DEFAULT_STYLIZE,
                    "min": cls.STYLIZE_MIN,
                    "max": cls.STYLIZE_MAX,
                }),
                "chaos": ("INT", {
                    "tooltip": "Controls variation and unpredictability (provider key: providerSettings.midjourney.chaos).",
                    "default": cls.DEFAULT_CHAOS,
                    "min": cls.CHAOS_MIN,
                    "max": cls.CHAOS_MAX,
                }),
                "weird": ("INT", {
                    "tooltip": "Adds surreal, experimental characteristics (provider key: providerSettings.midjourney.weird).",
                    "default": cls.DEFAULT_WEIRD,
                    "min": cls.WEIRD_MIN,
                    "max": cls.WEIRD_MAX,
                }),
                "niji": (cls.NIJI_OPTIONS, {
                    "tooltip": "Select the Midjourney anime-focused rendering engine (provider key: providerSettings.midjourney.niji).",
                    "default": "close",
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("Provider Settings",)
    FUNCTION = "create_provider_settings"
    CATEGORY = "Runware/Provider Settings"
    DESCRIPTION = "Configure Midjourney-specific provider settings such as quality, stylize, chaos, weird, and niji options for image generation."

    def create_provider_settings(self, **kwargs) -> Tuple[Optional[Dict[str, Any]],]:
        """Build Midjourney provider settings payload."""

        quality = kwargs.get("quality", self.DEFAULT_QUALITY)
        stylize = kwargs.get("stylize", self.DEFAULT_STYLIZE)
        chaos = kwargs.get("chaos", self.DEFAULT_CHAOS)
        weird = kwargs.get("weird", self.DEFAULT_WEIRD)
        niji = kwargs.get("niji", "close")

        settings: Dict[str, Any] = {}

        if quality is not None:
            settings["quality"] = float(quality)

        if stylize is not None:
            settings["stylize"] = int(stylize)

        if chaos is not None:
            settings["chaos"] = int(chaos)

        if weird is not None:
            settings["weird"] = int(weird)

        if isinstance(niji, str) and niji.strip():
            settings["niji"] = niji.strip()

        # Clean None values so the inference request only includes populated options.
        settings = {k: v for k, v in settings.items() if v is not None}

        return (settings if settings else None,)


NODE_CLASS_MAPPINGS = {
    "RunwareMidjourneyProviderSettings": RunwareMidjourneyProviderSettings,
}


NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareMidjourneyProviderSettings": "Runware Midjourney Provider Settings",
}

