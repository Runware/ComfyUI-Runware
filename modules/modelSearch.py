class modelSearch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Model Search": ("STRING", {
                    "tooltip": "Search For Specific Model By Name Or Civit AIR Code (eg: Juggernaut).",
                }),
                "Model Architecture": ([
                        "All",
                        "FLUX.1-Schnell",
                        "FLUX.1-Dev",
                        "FLUX.1 Krea",
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
                        "rundiffusion:110@101 (Juggernaut Lightning Flux by RunDiffusion)",
                        "rundiffusion:130@100 (Juggernaut Pro Flux by RunDiffusion)",
                        "runware:100@1 (Flux Schnell)",
                        "runware:101@1 (Flux Dev)",
                        "runware:107@1 (FLUX.1 Krea)",
                        "runware:5@1 (SD3)",
                        "civitai:4384@128713 (SDXL 1.5 DreamShaper)",
                        "civitai:43331@176425 (SD 1.5 majicMIX realistic 麦橘写实)",
                        "civitai:101055@128078 (SDXL v1.0 VAE fix)",
                        "civitai:133005@288982 (SDXL Juggernaut XL V8)",
                    ], {
                    "tooltip": "Model Results Will Show UP Here So You Could Choose From. If You didn't Search For Anything this will show featured Model List.",
                    "default": "runware:100@1 (Flux Schnell)",
                }),
                "Use Search Value": ("BOOLEAN", {
                    "tooltip": "When Enabled, the value you've set in the search input will be used instead.\n\nThis is useful in case the model search API is down or you prefer to set the model manually.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
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
        enableSearchValue = kwargs.get("Use Search Value", False)
        searchInput = kwargs.get("Model Search")

        if enableSearchValue:
            modelAIRCode = searchInput
        else:
            crModel = kwargs.get("ModelList")
            modelAIRCode = crModel.split(" ")[0]

        return (modelAIRCode,)