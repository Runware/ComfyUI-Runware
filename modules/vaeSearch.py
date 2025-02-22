class vaeSearch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "VAE Search": ("STRING", {
                    "tooltip": "Search For A Specific VAE By Name Or Civit AIR Code (eg: ClearVAE).",
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
                    "tooltip": "Choose VAE's Model Architecture To Filter Out The Results.",
                    "default": "SD 1.5",
                }),
                "VAEList": ([
                        "civitai:23906@28569 (kl-f8-anime2 VAE)",
                        "civitai:22354@88156 (ClearVAE(SD1.5))",
                        "civitai:276082@311162 (vae-ft-mse-840000-ema-pruned | 840000 | 840k SD1.5 VAE)",
                        "civitai:70248@83798 (Color101 VAE)",
                        "civitai:22354@26689 (ClearVAE (SD1.5))",
                        "civitai:88390@94036 (difConsistency RAW VAE (Pack))",
                    ], {
                    "tooltip": "VAE Results Will Show UP Here So You Could Choose From.",
                    "default": "civitai:23906@28569 (kl-f8-anime2 VAE)",
                }),
                "Use Search Value": ("BOOLEAN", {
                    "tooltip": "When Enabled, the value you've set in the search input will be used instead.\n\nThis is useful in case the model search API is down or you prefer to set the model manually.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
            },
        }

    DESCRIPTION = "Directly Search and Connect VAE's to Runware Inference Nodes In ComfyUI."
    FUNCTION = "vaeSearch"
    RETURN_TYPES = ("RUNWAREVAE",)
    RETURN_NAMES = ("Runware VAE",)
    CATEGORY = "Runware"

    @classmethod
    def VALIDATE_INPUTS(cls, VAEList):
        return True

    def vaeSearch(self, **kwargs):
        enableSearchValue = kwargs.get("Use Search Value", False)
        searchInput = kwargs.get("VAE Search")

        if enableSearchValue:
            modelAIRCode = searchInput
        else:
            crModel = kwargs.get("VAEList")
            modelAIRCode = crModel.split(" ")[0]

        return (modelAIRCode,)