from .utils import runwareUtils as rwUtils

class ipAdapter:
    RUNWARE_IPADAPTER_MODELS = {
        "FLUX.1 Dev Redux": "runware:105@1",
        "IP Adapter SDXL": "runware:55@1",
        "IP Adapter SDXL Plus": "runware:55@2",
        "IP Adapter SDXL Plus Face": "runware:55@3",
        "IP Adapter SDXL Vit-H": "runware:55@4",
        "IP Adapter SD 1.5": "runware:55@5",
        "IP Adapter SD 1.5 Plus": "runware:55@6",
        "IP Adapter SD 1.5 Light": "runware:55@7",
        "IP Adapter SD 1.5 Plus Face": "runware:55@8",
        "IP Adapter SD 1.5 Full Face": "runware:55@9",
        "IP Adapter SD 1.5 Vit-G": "runware:55@10"
    }
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Reference Image": ("IMAGE",),
                "Model": (list(cls.RUNWARE_IPADAPTER_MODELS.keys()), {
                    "tooltip": "Choose IP Adapter model to use for reference-based image generation.",
                    "default": "IP Adapter SDXL",
                }),
                "weight": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                    "tooltip": "Represents the strength or influence of this IP-Adapter in the generation process.\n\nA value of 0 means no influence, while 1 means maximum influence.\n\nNote: This Value Is Ignored For Flux Redux.",
                }),
            },
        }

    RETURN_TYPES = ("RUNWAREIPAdapter",)
    RETURN_NAMES = ("IPAdapter",)
    FUNCTION = "ipAdapter"
    CATEGORY = "Runware"
    DESCRIPTION = "IP-Adapters enable image-prompted generation, allowing you to use reference images to guide the style and content of your generations. Multiple IP Adapters can be used simultaneously."

    def ipAdapter(self, **kwargs):
        refImage = kwargs.get("Reference Image")
        modelName = kwargs.get("Model")
        weight = kwargs.get("weight")
        modelAirCode = self.RUNWARE_IPADAPTER_MODELS.get(modelName)
        guideImage = rwUtils.convertTensor2IMG(refImage)
        return ({
            "model": modelAirCode,
            "guideImage": guideImage,
            "weight": round(weight, 2),
        },)