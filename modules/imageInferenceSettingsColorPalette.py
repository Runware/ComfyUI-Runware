"""
Runware Image Inference Settings Color Palette
Builds settings.colorPalette: list of { "hex": "#...", "ratio": "NN.NN%" } for Runware Image Inference Settings.
"""

from typing import Any, Dict, List, Tuple


def _normalize_hex(raw: str) -> str:
    h = raw.strip()
    if not h:
        return ""
    return h if h.startswith("#") else f"#{h}"


class RunwareImageInferenceSettingsColorPalette:
    """Up to 8 hex/ratio pairs; each slot is included only when use_{i} is enabled."""

    _SLOTS = 8

    @classmethod
    def INPUT_TYPES(cls):
        optional: Dict[str, tuple] = {}
        for i in range(1, cls._SLOTS + 1):
            optional[f"use_{i}"] = ("BOOLEAN", {
                "default": False,
                "label_on": "Enabled",
                "label_off": "Disabled",
                "tooltip": f"Include swatch {i} in the output colorPalette.",
            })
            optional[f"hex_{i}"] = ("STRING", {
                "default": "",
                "tooltip": f"Swatch {i} hex, e.g. #C2D1E6. Required when use_{i} is enabled.",
            })
            optional[f"ratio_{i}"] = ("STRING", {
                "default": "",
                "tooltip": f"Swatch {i} ratio, e.g. 23.51%%. Optional.",
            })
        return {"required": {}, "optional": optional}

    RETURN_TYPES = ("RUNWAREIMAGEINFERENCECOLORPALETTE",)
    RETURN_NAMES = ("colorPalette",)
    FUNCTION = "build_palette"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Build a colorPalette list for image inference settings (hex + optional ratio per swatch). "
        "Enable use_1…use_8 for each swatch to include; connect the output to Runware Image Inference Settings."
    )

    def build_palette(self, **kwargs) -> Tuple[List[Dict[str, Any]]]:
        out: List[Dict[str, Any]] = []
        for i in range(1, self._SLOTS + 1):
            if not kwargs.get(f"use_{i}", False):
                continue
            hx = _normalize_hex(str(kwargs.get(f"hex_{i}") or ""))
            if not hx or hx == "#":
                raise ValueError(
                    f"use_{i} is enabled but hex_{i} is empty or invalid. "
                    "Provide a hex color (e.g. #C2D1E6) or disable this swatch."
                )
            ratio = str(kwargs.get(f"ratio_{i}") or "").strip()
            entry: Dict[str, Any] = {"hex": hx}
            if ratio:
                entry["ratio"] = ratio
            out.append(entry)
        return (out,)
