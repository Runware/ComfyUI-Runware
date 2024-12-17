class embeddingsCombine:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Embedding 1": ("RUNWAREEMBEDDING", {
                    "tooltip": "Connect a Runware Embedding From an Embedding Node.",
                }),
            },
            "optional": {
                "Embedding 2": ("RUNWAREEMBEDDING", {
                    "tooltip": "Connect a Runware Embedding From an Embedding Node.",
                }),
                "Embedding 3": ("RUNWAREEMBEDDING", {
                    "tooltip": "Connect a Runware Embedding From an Embedding Node.",
                }),
            },
        }

    DESCRIPTION = "Combine One or More Embeddings To Connect It With Runware Image Inference."
    FUNCTION = "embeddingsCombine"
    RETURN_TYPES = ("RUNWAREEMBEDDING",)
    RETURN_NAMES = ("Runware Embeddings",)
    CATEGORY = "Runware"

    def embeddingsCombine(self, **kwargs):
        embeddingV1 = kwargs.get("Embedding 1")
        embeddingV2 = kwargs.get("Embedding 2", None)
        embeddingV3 = kwargs.get("Embedding 3", None)

        embeddingsObjArray = []
        embeddingsObjArray.append(embeddingV1)
        if(embeddingV2):
            embeddingsObjArray.append(embeddingV2)
        if(embeddingV3):
            embeddingsObjArray.append(embeddingV3)
        return (embeddingsObjArray,)