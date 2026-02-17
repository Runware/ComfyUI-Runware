"""
Runware Recraft Color Node - IRecraftRGB
Outputs {rgb: [r, g, b]} for use as palette color or backgroundColor in Recraft Provider Settings
"""

from typing import Dict, List


def _clamp_rgb(value: int) -> int:
    return max(0, min(255, int(value)))


class RunwareRecraftColor:
    """Outputs IRecraftRGB {rgb: [r,g,b]} - use for colors palette or backgroundColor"""

    @classmethod
    def INPUT_TYPES(cls):
        rgb = ("INT", {"default": 128, "min": 0, "max": 255})
        return {
            "required": {},
            "optional": {"r": rgb, "g": rgb, "b": rgb}
        }

    RETURN_TYPES = ("RUNWARERECRAFTCOLOR",)
    RETURN_NAMES = ("Color",)
    FUNCTION = "create"
    CATEGORY = "Runware/Provider Settings"
    DESCRIPTION = "IRecraftRGB - use for palette (colors) or backgroundColor. Connect to Runware Recraft Provider Settings."

    def create(self, r: int = 128, g: int = 128, b: int = 128) -> tuple[Dict[str, List[int]]]:
        return ({"rgb": [_clamp_rgb(r), _clamp_rgb(g), _clamp_rgb(b)]},)


NODE_CLASS_MAPPINGS = {
    "RunwareRecraftColor": RunwareRecraftColor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareRecraftColor": "Runware Provider Settings Recraft Color",
}
