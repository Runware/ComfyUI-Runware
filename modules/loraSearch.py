class loraSearch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Lora Search": ("STRING", {
                    "tooltip": "Searchg For Specific Lora By Name Or Civit AIR Code (eg: Cyberpunk).",
                }),
                "Model Architecture": ([
                        "All",
                        "FLUX.1-Schnell",
                        "FLUX.1-Dev",
                        "Pony",
                        "SD 1.5",
                        "SD 1.5 Hyper",
                        "SD 1.5 LCM",
                        "SD 3",
                        "SDXL 1.0",
                        "SDXL 1.0 LCM",
                        "SDXL Distilled",
                        "SDXL Hyper",
                        "SDXL Lightning",
                        "SDXL Turbo",
                    ], {
                    "tooltip": "Choose Lora Model Architecture To Filter Results.",
                    "default": "All",
                }),
                "LoraType": ([
                        "Lora",
                        "LyCORIS"
                    ], {
                    "tooltip": "Choose Lora Type To Filter Out The Results.",
                    "default": "Lora",
                }),
                "LoraList": ([
                        "civitai:58390@62833 (Detail Tweaker LoRA (细节调整LoRA))",
                        "civitai:82098@87153 (Add More Details - Detail Enhancer / Tweaker (细节调整) LoRA)",
                        "civitai:122359@135867 (Detail Tweaker XL)",
                        "civitai:14171@16677 (Cute_girl_mix4)",
                        "civitai:13941@16576 (epi_noiseoffset)",
                        "civitai:25995@32988 (blindbox/大概是盲盒)",
                    ], {
                    "tooltip": "Lora Results Will Show UP Here So You Could Choose From.",
                    "default": "civitai:58390@62833 (Detail Tweaker LoRA (细节调整LoRA))",
                }),
                "weight": ("FLOAT", {
                    "tooltip": "Defines the strength or influence of the LoRA model in the generation process.",
                    "default": 1.0,
                    "min": -4.0,
                    "max": 4.0,
                    "step": 0.1,
                }),
            },
        }

    DESCRIPTION = "Directly Search and Connect Lora's to Runware Inference Nodes In ComfyUI."
    FUNCTION = "loraSearch"
    RETURN_TYPES = ("RUNWARELORA",)
    RETURN_NAMES = ("Runware Lora",)
    CATEGORY = "Runware"

    @classmethod
    def VALIDATE_INPUTS(cls, LoraList):
        return True

    def loraSearch(self, **kwargs):
        currentModel = kwargs.get("LoraList")
        loraWeight = kwargs.get("weight")
        loraAIRCode = currentModel.split(" ")[0]
        return ({
            "model": loraAIRCode,
            "weight": round(loraWeight, 2),
        },)