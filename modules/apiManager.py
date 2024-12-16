from .utils import runwareUtils as rwUtils

class apiManager:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "API Key": ("STRING", {
                    "tooltip": "Define Or Change Your Runware API Key To Start Using Runware Image Inference Services.\n\n(e.g; BcVr1JVQM8FGzrRwb3GsbCq5ww1QwabV)\n\nIf You Don't Have One, You Can Get It From: https://my.runware.ai/keys",
                }),
                "Max Timeout": ("INT", {
                    "tooltip": "Define Or Change Runware API Timeout In Seconds.\n\n(e.g; 90 Seconds).",
                    "min": 5,
                    "max": 99,
                    "default": int(rwUtils.getTimeout()),
                }),
            },
        }

    DESCRIPTION = "API Managers is a Runware Utility That helps you define or change your API Key or Session Timeout From The ComfyUI Interface Without having to adjust the env file locally."
    CATEGORY = "Runware"
    RETURN_TYPES = ()