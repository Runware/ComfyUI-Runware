"""
Runware Sourceful Provider Settings Fonts Node
Creates font inputs array for Sourceful provider (up to 2 font references with fontUrl and text).
"""

from typing import Dict, List


class RunwareSourcefulProviderSettingsFonts:
    """Runware Sourceful Provider Settings Fonts Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useFont1": ("BOOLEAN", {
                    "tooltip": "Enable to include first font reference in fontInputs array",
                    "default": False,
                }),
                "fontUrl1": ("STRING", {
                    "tooltip": "URL of the font file (e.g. .woff2). Only used when 'Use Font 1' is enabled.",
                    "default": "",
                }),
                "text1": ("STRING", {
                    "multiline": True,
                    "tooltip": "Text to render with the first font. Only used when 'Use Font 1' is enabled.",
                    "default": "",
                }),
                "useFont2": ("BOOLEAN", {
                    "tooltip": "Enable to include second font reference in fontInputs array",
                    "default": False,
                }),
                "fontUrl2": ("STRING", {
                    "tooltip": "URL of the font file (e.g. .woff2). Only used when 'Use Font 2' is enabled.",
                    "default": "",
                }),
                "text2": ("STRING", {
                    "multiline": True,
                    "tooltip": "Text to render with the second font. Only used when 'Use Font 2' is enabled.",
                    "default": "",
                }),
            }
        }

    RETURN_TYPES = ("RUNWARESOURCEFULFONTINPUTS",)
    RETURN_NAMES = ("Font Inputs",)
    FUNCTION = "create_font_inputs"
    CATEGORY = "Runware/Provider Settings"
    DESCRIPTION = "Create font inputs for Sourceful provider. Up to 2 font references, each with font URL and text to render."

    def create_font_inputs(self, **kwargs) -> tuple[List[Dict[str, str]]]:
        """Create font inputs array"""
        font_inputs: List[Dict[str, str]] = []

        for i in range(1, 3):
            use_font = kwargs.get(f"useFont{i}", False)
            if use_font:
                font_url = (kwargs.get(f"fontUrl{i}", "") or "").strip()
                text = (kwargs.get(f"text{i}", "") or "").strip()
                if font_url and text:
                    font_inputs.append({
                        "fontUrl": font_url,
                        "text": text,
                    })

        return (font_inputs,)


NODE_CLASS_MAPPINGS = {
    "RunwareSourcefulProviderSettingsFonts": RunwareSourcefulProviderSettingsFonts,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareSourcefulProviderSettingsFonts": "Runware Sourceful Provider Settings Fonts",
}
