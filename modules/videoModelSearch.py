class videoModelSearch:
    """Video Model Search node for searching and selecting video models"""
    
    # Define the video models by architecture with their default dimensions
    VIDEO_MODELS = {
        "KlingAI": [
            "klingai:1@2 (KlingAI V1.0 Pro)",
            "klingai:1@1 (KlingAI V1 Standard)",
            "klingai:2@2 (KlingAI V1.5 Pro)",
            "klingai:2@1 (KlingAI V1.5 Standard)",
            "klingai:3@1 (KlingAI V1.6 Standard)",
            "klingai:3@2 (KlingAI V1.6 Pro)",
            "klingai:4@3 (KlingAI V2.1 Master)",
            "klingai:5@1 (KlingAI V2.1 Standard (I2V))",
            "klingai:5@2 (KlingAI V2.1 Pro (I2V))",
            "klingai:5@3 (KlingAI V2.0 Master)",
            "klingai:7@1 (KlingAI Lip-Sync)",
        ],
        "Veo": [
            "google:2@0 (Veo 2.0)",
            "google:3@0 (Veo 3.0)",
            "google:3@1 (Veo 3.0 Fast)",
            "google:3@2 (Veo 3.1)",
            "google:3@3 (Veo 3.1 Fast)",
        ],
        "Bytedance": [
            "bytedance:2@1 (Seedance 1.0 Pro)",
            "bytedance:1@1 (Seedance 1.0 Lite)",
            "bytedance:5@1 (OmniHuman 1)",
            "bytedance:5@2 (OmniHuman 1.5)",
        ],
        "MiniMax": [
            "minimax:1@1 (MiniMax 01 Base)",
            "minimax:2@1 (MiniMax 01 Director)",
            "minimax:2@3 (MiniMax I2V 01 Live)",
            "minimax:3@1 (MiniMax 02 Hailuo)",
            "minimax:4@1 (MiniMax Hailuo 2.3)",
            "minimax:4@2 (MiniMax Hailuo 2.3 Fast)",
        ],
        "PixVerse": [
            "pixverse:1@1 (PixVerse v3.5)",
            "pixverse:1@2 (PixVerse v4)",
            "pixverse:1@3 (PixVerse v4.5)",
            "pixverse:lipsync@1 (PixVerse LipSync)",
        ],
        "Vidu": [
            "vidu:1@0 (Vidu Q1 Classic)",
            "vidu:1@1 (Vidu Q1)",
            "vidu:1@5 (Vidu 1.5)",
            "vidu:2@0 (Vidu 2.0)",
        ],
        "Wan": [
            "runware:200@1 (Wan 2.1 1.3B)",
            "runware:200@2 (Wan 2.1 14B)",
            "runware:200@6 (Wan 2.2)",
        ],
        "OpenAI": [
            "openai:3@1 (OpenAI Sora 3.1)",
            "openai:3@0 (OpenAI Sora 3.0)",
        ],
        "Lightricks": [
            "lightricks:2@0 (LTX Fast)",
            "lightricks:2@1 (LTX Pro)",
        ],
        "Ovi": [
            "runware:190@1 (Ovi)",
        ],
    }
    
    # Model dimensions mapping
    MODEL_DIMENSIONS = {
        # KlingAI Models
        "klingai:1@2": {"width": 1280, "height": 720},
        "klingai:1@1": {"width": 1280, "height": 720},
        "klingai:2@2": {"width": 1920, "height": 1080},
        "klingai:2@1": {"width": 1280, "height": 720},
        "klingai:3@1": {"width": 1280, "height": 720},
        "klingai:3@2": {"width": 1920, "height": 1080},
        "klingai:4@3": {"width": 1280, "height": 720},
        "klingai:5@1": {"width": 1280, "height": 720},
        "klingai:5@2": {"width": 1920, "height": 1080},
        "klingai:5@3": {"width": 1920, "height": 1080},
        "klingai:7@1": {"width": 0, "height": 0},
        
        # Veo Models
        "google:2@0": {"width": 1280, "height": 720},
        "google:3@0": {"width": 1280, "height": 720},
        "google:3@1": {"width": 1280, "height": 720},
        "google:3@2": {"width": 1280, "height": 720},
        "google:3@3": {"width": 1280, "height": 720},
        
        # Bytedance Models
        "bytedance:2@1": {"width": 864, "height": 480},
        "bytedance:1@1": {"width": 864, "height": 480},
        "bytedance:5@1": {"width": 1024, "height": 1024},
        "bytedance:5@2": {"width": 1024, "height": 1024},
        
        # MiniMax Models
        "minimax:1@1": {"width": 1366, "height": 768},
        "minimax:2@1": {"width": 1366, "height": 768},
        "minimax:2@3": {"width": 1366, "height": 768},
        "minimax:3@1": {"width": 1366, "height": 768},
        "minimax:4@1": {"width": 1366, "height": 768},
        "minimax:4@2": {"width": 1366, "height": 768},
        
        # PixVerse Models
        "pixverse:1@1": {"width": 640, "height": 360},
        "pixverse:1@2": {"width": 640, "height": 360},
        "pixverse:1@3": {"width": 640, "height": 360},
        "pixverse:lipsync@1": {"width": 640, "height": 360},
        
        # Vidu Models
        "vidu:1@0": {"width": 1920, "height": 1080},
        "vidu:1@1": {"width": 1920, "height": 1080},
        "vidu:1@5": {"width": 1920, "height": 1080},
        "vidu:2@0": {"width": 1920, "height": 1080},
        
        # Wan Models
        "runware:200@1": {"width": 853, "height": 480},
        "runware:200@2": {"width": 853, "height": 480},
        "runware:200@6": {"width": 1280, "height": 720},
        
        # OpenAI Models
        "openai:3@1": {"width": 1280, "height": 720},
        "openai:3@0": {"width": 1280, "height": 720},
        
        # Lightricks Models
        "lightricks:2@0": {"width": 1920, "height": 1080},
        "lightricks:2@1": {"width": 1920, "height": 1080},
        
        # Ovi Models
        "runware:190@1": {"width": 0, "height": 0},
    }
    
    MODEL_ARCHITECTURES = [
        "All",
        "KlingAI",
        "Veo",
        "Bytedance",
        "MiniMax",
        "PixVerse",
        "Vidu",
        "Wan",
        "OpenAI",
        "Lightricks",
        "Ovi"
    ]
    
    DEFAULT_DIMENSIONS = {"width": 1024, "height": 576}
    
    @classmethod
    def INPUT_TYPES(cls):
        allModels = cls._getAllModels()
        defaultModel = "klingai:5@3 (KlingAI V2.0 Master)"
        defaultModelCode = defaultModel.split(" (")[0]
        defaultDims = cls.MODEL_DIMENSIONS.get(defaultModelCode, cls.DEFAULT_DIMENSIONS)
        
        return {
            "required": {
                "Model Search": ("STRING", {
                    "tooltip": "Search For Specific Video Model By Name Or Civit AIR Code (eg: KlingAI, Veo).",
                }),
                "Model Architecture": (cls.MODEL_ARCHITECTURES, {
                    "tooltip": "Choose Video Model Architecture To Filter Results.",
                    "default": "KlingAI",
                }),
                "VideoList": (allModels, {
                    "tooltip": "Video Model Results Will Show UP Here So You Could Choose From.",
                    "default": defaultModel,
                }),
                "Use Search Value": ("BOOLEAN", {
                    "tooltip": "When Enabled, the value you've set in the search input will be used instead.\n\nThis is useful in case the model search API is down or you prefer to set the model manually.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "Width": ("INT", {
                    "default": defaultDims["width"],
                    "min": 0,
                    "max": 4096,
                    "step": 1,
                    "tooltip": "Custom Width For The Selected Model. Defaults To Model's Recommended Width.",
                }),
                "Height": ("INT", {
                    "default": defaultDims["height"],
                    "min": 0,
                    "max": 4096,
                    "step": 1,
                    "tooltip": "Custom Height For The Selected Model. Defaults To Model's Recommended Height.",
                }),
            },
        }

    @classmethod
    def _getAllModels(cls):
        """Get all models from all architectures"""
        allModels = []
        for models in cls.VIDEO_MODELS.values():
            allModels.extend(models)
        return allModels

    DESCRIPTION = "Directly Search and Connect Video Models to Runware Video Inference Nodes In ComfyUI."
    FUNCTION = "videoModelSearch"
    RETURN_TYPES = ("RUNWAREVIDEOMODEL", "INT", "INT")
    RETURN_NAMES = ("Runware Video Model", "Width", "Height")
    CATEGORY = "Runware"

    @classmethod
    def VALIDATE_INPUTS(cls, VideoList):
        return True

    def videoModelSearch(self, **kwargs):
        """Search and return video model with dimensions"""
        enableSearchValue = kwargs.get("Use Search Value", False)
        searchInput = kwargs.get("Model Search")
        customWidth = kwargs.get("Width", 0)
        customHeight = kwargs.get("Height", 0)

        if enableSearchValue:
            modelAirCode = searchInput
        else:
            currentModel = kwargs.get("VideoList")
            modelAirCode = currentModel.split(" (")[0]

        dimensions = self.MODEL_DIMENSIONS.get(modelAirCode, self.DEFAULT_DIMENSIONS)
        
        width = customWidth if customWidth > 0 else dimensions["width"]
        height = customHeight if customHeight > 0 else dimensions["height"]
        
        if width == 0 and height == 0:
            width = None
            height = None
        
        return ({
            "model": modelAirCode,
        }, width, height)
