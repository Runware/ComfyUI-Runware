"""
Runware Recraft Provider Settings Node
IRecraftProviderSettings: styleId, colors (List[IRecraftRGB]), backgroundColor (IRecraftRGB)
"""

from typing import Dict, Any, List


class RunwareRecraftProviderSettings:
    """Runware Recraft Provider Settings Node"""

    @classmethod
    def INPUT_TYPES(cls):
        color_input = ("RUNWARERECRAFTCOLOR", {"tooltip": "IRecraftRGB - connect Runware Recraft Color"})
        return {
            "required": {},
            "optional": {
                "useStyleId": ("BOOLEAN", {
                    "tooltip": "Enable to include styleId parameter",
                    "default": False,
                }),
                "styleId": ("STRING", {
                    "default": "",
                    "tooltip": "Style ID for Recraft image generation.",
                }),
                "color1": color_input,
                "color2": color_input,
                "color3": color_input,
                "color4": color_input,
                "color5": color_input,
                "backgroundColor": color_input,
            }
        }

    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("Provider Settings",)
    FUNCTION = "createProviderSettings"
    CATEGORY = "Runware/Provider Settings"
    DESCRIPTION = "IRecraftProviderSettings. Connect Runware Recraft Color nodes for colors (palette) and backgroundColor."

    def createProviderSettings(self, **kwargs) -> tuple[Dict[str, Any]]:
        settings: Dict[str, Any] = {}

        if kwargs.get("useStyleId") and (sid := kwargs.get("styleId", "").strip()):
            settings["styleId"] = sid

        colors: List[Dict[str, List[int]]] = []
        for i in range(1, 6):
            c = kwargs.get(f"color{i}")
            if c and isinstance(c, dict) and "rgb" in c:
                colors.append(c)
        if colors:
            settings["colors"] = colors

        bg = kwargs.get("backgroundColor")
        if bg and isinstance(bg, dict) and "rgb" in bg:
            settings["backgroundColor"] = bg

        return (settings,)


NODE_CLASS_MAPPINGS = {
    "RunwareRecraftProviderSettings": RunwareRecraftProviderSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareRecraftProviderSettings": "Runware Recraft Provider Settings",
}
