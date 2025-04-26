class teaCache:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "TeaCache Distance": (
                    "FLOAT",
                    {
                        "tooltip": "Controls the aggressiveness of the TeaCache feature.\n\nValues range from 0.0 (most conservative) to 1.0 (most aggressive).\n\nLower values prioritize quality by being more selective about which computations to reuse, while higher values prioritize speed by reusing more computations.",
                        "default": 0.5,
                        "min": 0.0,
                        "max": 1.0,
                        "step": 0.1,
                    },
                ),
            },
        }

    DESCRIPTION = "Can Be connected to Runware Inference to accelerate image generation by reusing past computations.\n\nTeaCache is specifically designed for transformer-based models such as Flux and SD3, and does not work with UNet models like SDXL or SD1.5."
    FUNCTION = "teaCache"
    RETURN_TYPES = ("RUNWAREACCELERATOR",)
    RETURN_NAMES = ("Runware Accelerator",)
    CATEGORY = "Runware"

    def teaCache(self, **kwargs):
        teaCacheDistance = kwargs.get("TeaCache Distance")

        return (
            {
                "teaCache": True,
                "teaCacheDistance": round(teaCacheDistance, 2),
            },
        )
