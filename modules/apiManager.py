class apiManager:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "API Key": ("STRING", {
                    "tooltip": "Set Your Runware API Key To Start Using Runware Image Inference Services.\n\n(eg: BcVr1JVQM8FGzrRwb3GsbCq5ww1QwabV)\n\nIf You Don't Have One, You Can Get It From: https://my.runware.ai/keys",
                }),
            },
        }

    DESCRIPTION = "API Managers is a Runware Utility That helps you set your API Key From The ComfyUI Interface Without having to adjust the env file locally."
    CATEGORY = "Runware"
    RETURN_TYPES = ()
    OUTPUT_NODE = True