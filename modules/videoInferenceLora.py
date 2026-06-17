class RunwareVideoInferenceLora:
    """LoRA config for Runware Video Inference."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("STRING", {
                    "default": "",
                    "tooltip": "LoRA model AIR code (e.g. lvs:mayflower@lora-test).",
                }),
                "weight": ("FLOAT", {
                    "tooltip": "LoRA strength for video generation.",
                    "default": 0.7,
                    "min": -4.0,
                    "max": 4.0,
                    "step": 0.1,
                }),
            },
        }

    DESCRIPTION = (
        "Configure a LoRA for Runware Video Inference. Connect the output to "
        "Runware Video Inference → lora."
    )
    FUNCTION = "createLora"
    RETURN_TYPES = ("RUNWAREVIDEOINFERENCELORA",)
    RETURN_NAMES = ("lora",)
    CATEGORY = "Runware"

    def createLora(self, model, weight):
        return ({
            "model": model.strip(),
            "weight": round(weight, 2),
        },)
