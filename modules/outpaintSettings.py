class outpaintSettings:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Top": (
                    "INT",
                    {
                        "tooltip": "Number of pixels to extend at the top of the image. Must be a multiple of 64.",
                        "default": 64,
                        "min": 0,
                        "max": 2048,
                        "step": 64,
                    },
                ),
                "Right": (
                    "INT",
                    {
                        "tooltip": "Number of pixels to extend at the right of the image. Must be a multiple of 64.",
                        "default": 64,
                        "min": 0,
                        "max": 2048,
                        "step": 64,
                    },
                ),
                "Bottom": (
                    "INT",
                    {
                        "tooltip": "Number of pixels to extend at the bottom of the image. Must be a multiple of 64.",
                        "default": 64,
                        "min": 0,
                        "max": 2048,
                        "step": 64,
                    },
                ),
                "Left": (
                    "INT",
                    {
                        "tooltip": "Number of pixels to extend at the left of the image. Must be a multiple of 64.",
                        "default": 64,
                        "min": 0,
                        "max": 2048,
                        "step": 64,
                    },
                ),
                "Blur": (
                    "INT",
                    {
                        "tooltip": "The amount of blur to apply at the boundaries between the original image and the extended areas, measured in pixels.",
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
        top = kwargs.get("Top", 0)
        right = kwargs.get("Right", 0)
        bottom = kwargs.get("Bottom", 0)
        left = kwargs.get("Left", 0)
        blur = kwargs.get("Blur", 0)

        outpaint = {
            "top": top,
            "right": right,
            "bottom": bottom,
            "left": left,
            "blur": blur,
        }

        return (outpaint,)
