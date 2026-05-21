def _round_to_multiple_of_64(value: int) -> int:
    """Round pixel extension to the nearest multiple of 64 (API constraint)."""
    return max(0, min(2048, round(value / 64) * 64))


class outpaintSettings:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "useTop": ("BOOLEAN", {
                    "tooltip": "Enable to include top extension in outpaint settings.",
                    "default": False,
                }),
                "Top": (
                    "INT",
                    {
                        "tooltip": "Number of pixels to extend at the top of the image. Rounded to the nearest multiple of 64 when sent to the API. Only used when 'Use Top' is enabled.",
                        "default": 64,
                        "min": 0,
                        "max": 2048,
                        "step": 1,
                    },
                ),
                "useRight": ("BOOLEAN", {
                    "tooltip": "Enable to include right extension in outpaint settings.",
                    "default": False,
                }),
                "Right": (
                    "INT",
                    {
                        "tooltip": "Number of pixels to extend at the right of the image. Rounded to the nearest multiple of 64 when sent to the API. Only used when 'Use Right' is enabled.",
                        "default": 64,
                        "min": 0,
                        "max": 2048,
                        "step": 1,
                    },
                ),
                "useBottom": ("BOOLEAN", {
                    "tooltip": "Enable to include bottom extension in outpaint settings.",
                    "default": False,
                }),
                "Bottom": (
                    "INT",
                    {
                        "tooltip": "Number of pixels to extend at the bottom of the image. Rounded to the nearest multiple of 64 when sent to the API. Only used when 'Use Bottom' is enabled.",
                        "default": 64,
                        "min": 0,
                        "max": 2048,
                        "step": 1,
                    },
                ),
                "useLeft": ("BOOLEAN", {
                    "tooltip": "Enable to include left extension in outpaint settings.",
                    "default": False,
                }),
                "Left": (
                    "INT",
                    {
                        "tooltip": "Number of pixels to extend at the left of the image. Rounded to the nearest multiple of 64 when sent to the API. Only used when 'Use Left' is enabled.",
                        "default": 64,
                        "min": 0,
                        "max": 2048,
                        "step": 1,
                    },
                ),
                "useBlur": ("BOOLEAN", {
                    "tooltip": "Enable to include blur in outpaint settings.",
                    "default": False,
                }),
                "Blur": (
                    "INT",
                    {
                        "tooltip": "The amount of blur to apply at the boundaries between the original image and the extended areas, measured in pixels. Only used when 'Use Blur' is enabled.",
                        "default": 0,
                        "min": 0,
                        "max": 32,
                        "step": 1,
                    },
                ),
            },
        }

    DESCRIPTION = "Can Be Added To Image Inference Nodes To Extend the image boundaries in specified directions. \n\nYou must provide the final dimensions using width and height parameters, which should account for the original image size plus the total extension (seedImage dimensions + top + bottom, left + right)."
    FUNCTION = "outpaintSettings"
    RETURN_TYPES = ("RUNWAREOUTPAINT",)
    RETURN_NAMES = ("Outpaint Settings",)
    CATEGORY = "Runware"

    def outpaintSettings(self, **kwargs):
        outpaint = {}

        if kwargs.get("useTop", False):
            outpaint["top"] = _round_to_multiple_of_64(int(kwargs.get("Top", 0)))
        if kwargs.get("useRight", False):
            outpaint["right"] = _round_to_multiple_of_64(int(kwargs.get("Right", 0)))
        if kwargs.get("useBottom", False):
            outpaint["bottom"] = _round_to_multiple_of_64(int(kwargs.get("Bottom", 0)))
        if kwargs.get("useLeft", False):
            outpaint["left"] = _round_to_multiple_of_64(int(kwargs.get("Left", 0)))
        if kwargs.get("useBlur", False):
            outpaint["blur"] = int(kwargs.get("Blur", 0))

        return (outpaint if outpaint else None,)
