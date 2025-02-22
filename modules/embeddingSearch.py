class embeddingSearch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Embedding Search": ("STRING", {
                    "tooltip": "Search For A Specific Embedding By Name Or Civit AIR Code (eg: EasyNegative).",
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
                    "tooltip": "Choose Embedding Model Architecture To Filter Out The Results.",
                    "default": "SD 1.5",
                }),
                "EmbeddingList": ([
                        "civitai:7808@9208 (EasyNegative)",
                        "civitai:4629@5637 (Deep Negative V1.x)",
                        "civitai:56519@60938 (negative_hand Negative Embedding)",
                        "civitai:72437@77169 (BadDream + UnrealisticDream (Negative Embeddings))",
                        "civitai:11772@25820 (veryBadImageNegative)",
                        "civitai:71961@94057 (Fast Negative Embedding (+ FastNegativeV2))",
                    ], {
                    "tooltip": "Embedding Results Will Show UP Here So You Could Choose From.",
                    "default": "civitai:7808@9208 (EasyNegative)",
                }),
                "weight": ("FLOAT", {
                    "tooltip": "Defines the strength or influence of the Embedding on the generation process.",
                    "default": 1.0,
                    "min": 0,
                    "max": 1,
                    "step": 0.1,
                }),
                "Use Search Value": ("BOOLEAN", {
                    "tooltip": "When Enabled, the value you've set in the search input will be used instead.\n\nThis is useful in case the model search API is down or you prefer to set the model manually.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
            },
        }

    DESCRIPTION = "Directly Search and Connect Embeddings to Runware Inference Nodes In ComfyUI."
    FUNCTION = "embeddingSearch"
    RETURN_TYPES = ("RUNWAREEMBEDDING",)
    RETURN_NAMES = ("Runware Embedding",)
    CATEGORY = "Runware"

    @classmethod
    def VALIDATE_INPUTS(cls, EmbeddingList):
        return True

    def embeddingSearch(self, **kwargs):
        enableSearchValue = kwargs.get("Use Search Value", False)
        searchInput = kwargs.get("Embedding Search")
        embedding_weight = kwargs.get("weight")

        if enableSearchValue:
            modelAIRCode = searchInput
        else:
            crModel = kwargs.get("EmbeddingList")
            modelAIRCode = crModel.split(" ")[0]

        return ({
            "model": modelAIRCode,
            "weight": round(embedding_weight, 2),
        },)