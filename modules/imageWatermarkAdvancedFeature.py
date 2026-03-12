from typing import Dict, Any, Tuple

from .utils.runwareUtils import convertTensor2IMG


class RunwareWatermarkAdvancedFeature:
    """Runware Watermark Advanced Feature Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useText": ("BOOLEAN", {
                    "tooltip": "Enable to set text content for the watermark (2-32 characters).",
                    "default": False,
                }),
                "text": ("STRING", {
                    "tooltip": "Text content for the watermark (2-32 characters). Only used when 'Use Text' is enabled.",
                    "default": "",
                }),
                "useImage": ("BOOLEAN", {
                    "tooltip": "Enable to set image content for the watermark (connect an IMAGE, UUID, URL, data URI, or base64).",
                    "default": False,
                }),
                "image": ("IMAGE", {
                    "tooltip": "Image to use as watermark. Can be connected from a Load Image node; internally converted to a data URI/UUID when used.",
                }),
                "useDisplayPosition": ("BOOLEAN", {
                    "tooltip": "Enable to set watermark display position.",
                    "default": False,
                }),
                "displayPosition": ([
                    "top-left", "top-center", "top-right",
                    "center-left", "center-center", "center-right",
                    "bottom-left", "bottom-center", "bottom-right",
                ], {
                    "tooltip": "Watermark position on the image.",
                    "default": "bottom-right",
                }),
                "useTiled": ("BOOLEAN", {
                    "tooltip": "Enable to tile the watermark across the image at -45 degrees.",
                    "default": False,
                }),
                "tiled": ("BOOLEAN", {
                    "tooltip": "When enabled, distribute watermark across the image at -45 degrees. Only used when 'Use Tiled' is enabled.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useOpacity": ("BOOLEAN", {
                    "tooltip": "Enable to set watermark opacity (0.1 - 1.0).",
                    "default": False,
                }),
                "opacity": ("FLOAT", {
                    "tooltip": "Watermark opacity (0.1 - 1.0). Only used when 'Use Opacity' is enabled.",
                    "default": 0.6,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.05,
                }),
                "useFontColor": ("BOOLEAN", {
                    "tooltip": "Enable to set watermark font color (hex).",
                    "default": False,
                }),
                "fontColor": ("STRING", {
                    "tooltip": "Text color in hex format (e.g. #ffffff). Only used when 'Use Font Color' is enabled.",
                    "default": "#ffffff",
                }),
                "useBgColor": ("BOOLEAN", {
                    "tooltip": "Enable to set watermark background color (hex).",
                    "default": False,
                }),
                "bgColor": ("STRING", {
                    "tooltip": "Background color in hex format (e.g. #000000 or transparent). Only used when 'Use Bg Color' is enabled.",
                    "default": "transparent",
                }),
            },
        }

    RETURN_TYPES: Tuple[str] = ("RUNWAREIMAGEWATERMARKADVFEATURE",)
    RETURN_NAMES = ("watermark",)
    FUNCTION = "createWatermark"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Configure watermark advanced feature for Runware Image Inference. "
        "You must provide exactly one of text or image. Connect output to "
        "Runware Image  Advanced Feature Input watermark connection."
    )

    def createWatermark(self, **kwargs) -> tuple:
        """Build watermark dict for advancedFeatures.watermark."""
        use_text = kwargs.get("useText", False)
        text = (kwargs.get("text", "") or "").strip()
        use_image = kwargs.get("useImage", False)
        raw_image = kwargs.get("image", None)

        has_text = use_text and bool(text)

        image_str: str = ""
        if use_image:
            if raw_image is None:
                raise Exception(
                    "Watermark 'useImage' is enabled but no IMAGE input was provided. "
                    "Connect an IMAGE (e.g., from a Load Image node) to the watermark node."
                )
            # If an IMAGE tensor is connected, convert it to a data URI / UUID.
            try:
                # convertTensor2IMG handles caching and returns either UUID or data URI.
                image_str = convertTensor2IMG(raw_image)
            except Exception as e:
                raise Exception(
                    f"Failed to convert watermark IMAGE input. "
                    f"Ensure the connected image is valid. Details: {e}"
                ) from e

        has_image = use_image and bool(image_str)

        if has_text == has_image:
            raise Exception(
                "Watermark configuration requires exactly one of text or image (but not both or neither)."
            )

        use_pos = kwargs.get("useDisplayPosition", False)
        pos = kwargs.get("displayPosition", "bottom-right")
        use_tiled = kwargs.get("useTiled", False)
        tiled = bool(kwargs.get("tiled", False))
        use_opacity = kwargs.get("useOpacity", False)
        opacity = float(kwargs.get("opacity", 0.6))
        use_font = kwargs.get("useFontColor", False)
        font_color = (kwargs.get("fontColor", "#ffffff") or "").strip()
        use_bg = kwargs.get("useBgColor", False)
        bg_color = (kwargs.get("bgColor", "transparent") or "").strip()

        watermark: Dict[str, Any] = {}

        if has_text:
            watermark["text"] = text
        if has_image:
            watermark["image"] = image_str
        if use_pos:
            watermark["displayPosition"] = pos
        if use_tiled:
            watermark["tiled"] = tiled
        if use_opacity:
            watermark["opacity"] = opacity
        if use_font and font_color:
            watermark["fontColor"] = font_color
        if use_bg and bg_color:
            watermark["bgColor"] = bg_color

        return (watermark,)


NODE_CLASS_MAPPINGS = {
    "RunwareWatermarkAdvancedFeature": RunwareWatermarkAdvancedFeature,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareWatermarkAdvancedFeature": "Runware Watermark Advanced Feature",
}

