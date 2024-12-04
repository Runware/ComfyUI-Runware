class modelSearch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Model Search": ("STRING", {
                    "tooltip": "Searchg For Specific Model By Name Or Civit AIR Code (eg: Juggernaut).",
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
                    "tooltip": "Choose Model Architecture To Filter Results.",
                    "default": "All",
                }),
                "ModelType": ([
                        "Base Model",
                        "Inpainting Model",
                    ], {
                    "tooltip": "Choose Model Type To Filter Results.",
                    "default": "Base Model",
                }),
                "ModelList": ([
                        "runware:100@1 (Flux Schnell)",
                        "runware:101@1 (Flux Dev)",
                        "runware:5@1 (SD3)",
                        "civitai:4384@128713 (SDXL 1.5 DreamShaper)",
                        "civitai:43331@176425 (SD 1.5 majicMIX realistic 麦橘写实)",
                        "civitai:101055@128078 (SDXL v1.0 VAE fix)",
                        "civitai:133005@288982 (SDXL Juggernaut XL V8)",
                    ], {
                    "tooltip": "Model Results Will Show UP Here So You Could Choose From. If You didn't Search For Anything this will show featured Model List.",
                    "default": "runware:100@1 (Flux Schnell)",
                }),
            },
        }

    DESCRIPTION = "Directly Search and Connect Model Checkpoints to Runware Inference Nodes In ComfyUI."
    FUNCTION = "modelSearch"
    RETURN_TYPES = ("RUNWAREMODEL",)
    RETURN_NAMES = ("Runware Model",)
    CATEGORY = "Runware"

    @classmethod
    def VALIDATE_INPUTS(cls, ModelList):
        return True

    def modelSearch(self, **kwargs):
        currentModel = kwargs.get("ModelList")
        modelAIRCode = currentModel.split(" ")[0]
        return (modelAIRCode,)