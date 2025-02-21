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
                    "tooltip": "Change Runware API Request Timeout In Seconds.\n\n(e.g; 90 Seconds).",
                    "min": 5,
                    "max": 99,
                    "default": int(rwUtils.getTimeout()),
                }),
                "Image Output Quality": ("INT", {
                    "tooltip": "Sets the compression quality of the output image. Higher values preserve more quality but increase file size, lower values reduce file size but decrease quality.",
                    "min": 20,
                    "max": 99,
                    "default": int(rwUtils.getOutputQuality()),
                }),
                "Image Output Format": (["WEBP", "PNG", "JPEG"], {
                    "tooltip": "Change the Default Image Output Format.",
                    "default": rwUtils.getOutputFormat(),
                }),
            },
        }

    DESCRIPTION = "API Managers is a Runware Utility That helps you define or change your API Key, Session Timeout, or Image Output Format & Quality From The ComfyUI Interface Without having to adjust the env file locally."
    CATEGORY = "Runware"
    RETURN_TYPES = ()