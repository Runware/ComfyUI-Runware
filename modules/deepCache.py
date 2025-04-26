class deepCache:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "DeepCache Interval": (
                    "INT",
                    {
                        "tooltip": "Represents the frequency of feature caching, specified as the number of steps between each cache operation.\n\nA larger interval value will make inference faster but may impact quality. A smaller interval prioritizes quality over speed.",
                        "default": 3,
                        "min": 1,
                        "max": 5,
                        "step": 1,
                    },
                ),
                "DeepCache BranchId": (
                    "INT",
                    {
                        "tooltip": "Determines which branch of the network (ordered from the shallowest to the deepest layer) is responsible for executing the caching processes.\n\nLower branch IDs (e.g., 0) result in more aggressive caching for faster generation, while higher branch IDs produce more conservative caching with potentially higher quality results.",
                        "default": 0,
                        "min": 0,
                        "max": 5,
                        "step": 1,
                    },
                ),
            },
        }

    DESCRIPTION = "Can Be connected to Runware Inference to accelerate image generation by reusing past computations.\n\nDeepCache feature, which speeds up diffusion-based image generation by caching internal feature maps from the neural network.\n\nDeepCache can provide significant performance improvements for high-throughput scenarios or when generating multiple similar images."
    FUNCTION = "deepCache"
    RETURN_TYPES = ("RUNWAREACCELERATOR",)
    RETURN_NAMES = ("Runware Accelerator",)
    CATEGORY = "Runware"

    def deepCache(self, **kwargs):
        deepCacheInterval = kwargs.get("DeepCache Interval")
        deepCacheBranchId = kwargs.get("DeepCache BranchId")

        return (
            {
                "deepCache": True,
                # "deepCacheInterval": deepCacheInterval,
                "deepCacheBranchId": deepCacheBranchId,
            },
        )
