class Runware3DModelSearch:
    """3D Model Search node for searching and selecting 3D generation models"""

    THREED_MODELS = {
        "Tencent": [
            "tencent:hunyuan-3d@3.1-pro (Tencent Hunyuan 3D 3.1 Pro)",
            "tencent:hunyuan-3d@3.1-rapid (Tencent Hunyuan 3D 3.1 Rapid)",
        ],
        "Meta": [
            "meta:sam@3d (Meta SAM 3D)",
        ],
        "Microsoft": [
            "microsoft:trellis-2@4b (TRELLIS.2)",
        ],
        "Tripo": [
            "tripo:v3.1@0 (Tripo 3D v3.1)",
        ],
        "Hyper3D": [
            "hyper3d:rodin@gen-1 (Rodin Gen-1)",
            "hyper3d:rodin@gen-2 (Rodin Gen-2)",
        ],
        "Meshy": [
            "meshy:meshy@6 (Meshy 6)",
        ],
    }

    MODEL_ARCHITECTURES = [
        "All",
        "Tencent",
        "Meta",
        "Microsoft",
        "Tripo",
        "Hyper3D",
        "Meshy",
    ]

    @classmethod
    def INPUT_TYPES(cls):
        allModels = cls._getAllModels()
        defaultModel = "meta:sam@3d (Meta SAM 3D)"

        return {
            "required": {
                "Model Search": ("STRING", {
                    "tooltip": "Search for a specific 3D model by name or AIR code (e.g. hunyuan, trellis, tripo).",
                }),
                "Model Architecture": (cls.MODEL_ARCHITECTURES, {
                    "tooltip": "Choose 3D model architecture to filter results.",
                    "default": "Meta",
                }),
                "ThreeDList": (allModels, {
                    "tooltip": "3D model results will show up here so you can choose from.",
                    "default": defaultModel,
                }),
                "Use Search Value": ("BOOLEAN", {
                    "tooltip": "When enabled, the value in the search input is used instead of the selected list entry.\n\nUseful if you prefer to set the model manually.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
            },
        }

    @classmethod
    def _getAllModels(cls):
        allModels = []
        for models in cls.THREED_MODELS.values():
            allModels.extend(models)
        return allModels

    DESCRIPTION = "Search and connect 3D models to Runware 3D Inference nodes in ComfyUI."
    FUNCTION = "threeDModelSearch"
    RETURN_TYPES = ("RUNWARE3DMODEL",)
    RETURN_NAMES = ("Runware 3D Model",)
    CATEGORY = "Runware"

    @classmethod
    def VALIDATE_INPUTS(cls, ThreeDList):
        return True

    def threeDModelSearch(self, **kwargs):
        enableSearchValue = kwargs.get("Use Search Value", False)
        searchInput = kwargs.get("Model Search")

        if enableSearchValue:
            modelAirCode = searchInput
        else:
            currentModel = kwargs.get("ThreeDList")
            modelAirCode = currentModel.split(" (")[0]

        return (modelAirCode,)
