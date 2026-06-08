"""
Runware Image Inference Inputs Fonts node.
Builds inputs.fonts for image inference (up to 2 font references with url and text).
"""

from typing import Any, Dict, List, Tuple


class RunwareImageInferenceInputsFonts:
    """Build inputs.fonts[] for image inference requests."""

    MAX_FONTS = 2

    @classmethod
    def INPUT_TYPES(cls):
        optional_inputs = {}
        for i in range(1, cls.MAX_FONTS + 1):
            optional_inputs[f"fontUrl{i}"] = ("STRING", {
                "default": "",
                "tooltip": (
                    f"Font file URL for reference {i}. Must be ttf, otf, woff, or woff2. "
                    "Included when both fontUrl and text are non-empty."
                ),
            })
            optional_inputs[f"text{i}"] = ("STRING", {
                "multiline": True,
                "default": "",
                "tooltip": f"Text to render with font reference {i}. Included when both fontUrl and text are non-empty.",
            })

        return {
            "required": {},
            "optional": optional_inputs,
        }

    RETURN_TYPES = ("RUNWAREIMAGEINFERENCEFONTS",)
    RETURN_NAMES = ("fonts",)
    FUNCTION = "create_fonts"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Configure inputs.fonts for Runware Image Inference (up to 2 entries). "
        "Each entry: { \"url\": \"<font URL>\", \"text\": \"<text to render>\" }. "
        "A slot is included only when both fontUrl and text are non-empty. "
        "Connect to Runware Image Inference Inputs."
    )

    def create_fonts(self, **kwargs) -> Tuple[List[Dict[str, Any]]]:
        fonts: List[Dict[str, Any]] = []

        for i in range(1, self.MAX_FONTS + 1):
            font_url = (kwargs.get(f"fontUrl{i}") or "").strip()
            text = (kwargs.get(f"text{i}") or "").strip()

            if len(font_url) > 0 and len(text) > 0:
                fonts.append({
                    "url": font_url,
                    "text": text,
                })

        return (fonts,)
