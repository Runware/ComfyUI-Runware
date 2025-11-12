"""
Runware Runway Provider Settings Node
Provides Runway-specific settings for video generation
"""

from typing import Dict, Any


class RunwareRunwayProviderSettings:
    """Runware Runway Provider Settings Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "publicFigureThreshold": (["auto", "low"], {
                    "tooltip": "Select the public figure detection threshold (provider key: contentModeration.publicFigureThreshold).",
                    "default": "auto",
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("Provider Settings",)
    FUNCTION = "createProviderSettings"
    CATEGORY = "Runware"
    DESCRIPTION = "Configure Runway-specific provider settings for video generation including content moderation options."

    def createProviderSettings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create Runway provider settings"""

        publicFigureThreshold = kwargs.get("publicFigureThreshold")

        runwaySettings: Dict[str, Any] = {}

        if isinstance(publicFigureThreshold, str) and publicFigureThreshold.strip() != "":
            contentModeration: Dict[str, Any] = {}
            contentModeration["publicFigureThreshold"] = publicFigureThreshold.strip()
            runwaySettings["contentModeration"] = contentModeration

        # Remove unset values
        runwaySettings = {k: v for k, v in runwaySettings.items() if v is not None}

        return (runwaySettings,)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareRunwayProviderSettings": RunwareRunwayProviderSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareRunwayProviderSettings": "Runware Runway Provider Settings",
}

