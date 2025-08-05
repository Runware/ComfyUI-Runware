class videoModelSearch:
    # Define the video models by architecture with their default dimensions
    VIDEO_MODELS = {
        "KlingAI": [
            "urn:air:video:klingai:1@2 (KlingAI V1.0 Pro)",
            "urn:air:video:klingai:1@1 (KlingAI V1 Standard)",
            "urn:air:video:klingai:2@2 (KlingAI V1.5 Pro)",
            "urn:air:video:klingai:2@1 (KlingAI V1.5 Standard)",
            "urn:air:video:klingai:3@1 (KlingAI V1.6 Standard)",
            "urn:air:video:klingai:3@2 (KlingAI V1.6 Pro)",
            "urn:air:video:klingai:4@3 (KlingAI V2.1 Master)",
            "urn:air:video:klingai:5@1 (KlingAI V2.1 Standard (I2V))",
            "urn:air:video:klingai:5@2 (KlingAI V2.1 Pro (I2V))",
            "urn:air:video:klingai:5@3 (KlingAI V2.0 Master)",
        ],
        "Veo": [
            "urn:air:video:google:2@0 (Veo 2.0)",
            "urn:air:video:google:3@0 (Veo 3.0)",
            "urn:air:video:google:3@1 (Veo 3.0 Fast)",
        ],
        "Seedance": [
            "urn:air:video:bytedance:2@1 (Seedance 1.0 Pro)",
            "urn:air:video:bytedance:1@1 (Seedance 1.0 Lite)",
        ],
        "MiniMax": [
            "urn:air:video:minimax:1@1 (MiniMax 01 Base)",
            "urn:air:video:minimax:2@1 (MiniMax 01 Director)",
            "urn:air:video:minimax:2@3 (MiniMax I2V 01 Live)",
            "urn:air:video:minimax:3@1 (MiniMax 02 Hailuo)",
        ],
        "PixVerse": [
            "urn:air:video:pixverse:1@1 (PixVerse v3.5)",
            "urn:air:video:pixverse:1@2 (PixVerse v4)",
            "urn:air:video:pixverse:1@3 (PixVerse v4.5)",
        ],
        "Vidu": [
            "urn:air:video:vidu:1@0 (Vidu Q1 Classic)",
            "urn:air:video:vidu:1@1 (Vidu Q1)",
            "urn:air:video:vidu:1@5 (Vidu 1.5)",
            "urn:air:video:vidu:2@0 (Vidu 2.0)",
        ],
        "Wan": [
            "urn:air:video:runware:200@1 (Wan 2.1 1.3B)",
            "urn:air:video:runware:200@2 (Wan 2.1 14B)",
        ],
    }
    
    # Model dimensions mapping
    MODEL_DIMENSIONS = {
        # KlingAI Models
        "urn:air:video:klingai:1@2": {"width": 1280, "height": 720},  # KlingAI V1.0 Pro
        "urn:air:video:klingai:1@1": {"width": 1280, "height": 720},  # KlingAI V1 Standard
        "urn:air:video:klingai:2@2": {"width": 1920, "height": 1080}, # KlingAI V1.5 Pro
        "urn:air:video:klingai:2@1": {"width": 1280, "height": 720},  # KlingAI V1.5 Standard
        "urn:air:video:klingai:3@1": {"width": 1280, "height": 720},  # KlingAI V1.6 Standard
        "urn:air:video:klingai:3@2": {"width": 1920, "height": 1080}, # KlingAI V1.6 Pro
        "urn:air:video:klingai:4@3": {"width": 1280, "height": 720},  # KlingAI V2.1 Master
        "urn:air:video:klingai:5@1": {"width": 1280, "height": 720},  # KlingAI V2.1 Standard (I2V)
        "urn:air:video:klingai:5@2": {"width": 1920, "height": 1080}, # KlingAI V2.1 Pro (I2V)
        "urn:air:video:klingai:5@3": {"width": 1920, "height": 1080}, # KlingAI V2.0 Master
        
        # Veo Models
        "urn:air:video:google:2@0": {"width": 1280, "height": 720},   # Veo 2.0
        "urn:air:video:google:3@0": {"width": 1280, "height": 720},   # Veo 3.0
        "urn:air:video:google:3@1": {"width": 1280, "height": 720},   # Veo 3.0 Fast
        
        # Seedance Models
        "urn:air:video:bytedance:2@1": {"width": 864, "height": 480},  # Seedance 1.0 Pro
        "urn:air:video:bytedance:1@1": {"width": 864, "height": 480},  # Seedance 1.0 Lite
        
        # MiniMax Models
        "urn:air:video:minimax:1@1": {"width": 1366, "height": 768},  # MiniMax 01 Base
        "urn:air:video:minimax:2@1": {"width": 1366, "height": 768},  # MiniMax 01 Director
        "urn:air:video:minimax:2@3": {"width": 1366, "height": 768},  # MiniMax I2V 01 Live
        "urn:air:video:minimax:3@1": {"width": 1366, "height": 768},  # MiniMax 02 Hailuo
        
        # PixVerse Models
        "urn:air:video:pixverse:1@1": {"width": 640, "height": 360},  # PixVerse v3.5
        "urn:air:video:pixverse:1@2": {"width": 640, "height": 360},  # PixVerse v4
        "urn:air:video:pixverse:1@3": {"width": 640, "height": 360},  # PixVerse v4.5
        
        # Vidu Models
        "urn:air:video:vidu:1@0": {"width": 1920, "height": 1080},    # Vidu Q1 Classic
        "urn:air:video:vidu:1@1": {"width": 1920, "height": 1080},    # Vidu Q1
        "urn:air:video:vidu:1@5": {"width": 1920, "height": 1080},    # Vidu 1.5
        "urn:air:video:vidu:2@0": {"width": 1920, "height": 1080},    # Vidu 2.0
        
        # Wan Models
        "urn:air:video:runware:200@1": {"width": 853, "height": 480}, # Wan 2.1 1.3B
        "urn:air:video:runware:200@2": {"width": 853, "height": 480}, # Wan 2.1 14B
    }
    
    # Models that support seed parameter
    SEED_SUPPORTED_MODELS = [
        "urn:air:video:runware:200@1",  # Wan 2.1 1.3B
        "urn:air:video:runware:200@2",  # Wan 2.1 14B
    ]
    
    @classmethod
    def INPUT_TYPES(cls):
        # Get all models for "All" option
        all_models = []
        for models in cls.VIDEO_MODELS.values():
            all_models.extend(models)
        
        return {
            "required": {
                "Model Search": ("STRING", {
                    "tooltip": "Search For Specific Video Model By Name Or Civit AIR Code (eg: KlingAI, Veo).",
                }),
                "Model Architecture": ([
                        "All",
                        "KlingAI",
                        "Veo",
                        "Seedance",
                        "MiniMax",
                        "PixVerse",
                        "Vidu",
                        "Wan"
                    ], {
                    "tooltip": "Choose Video Model Architecture To Filter Results.",
                    "default": "KlingAI",
                }),
                "VideoList": (all_models, {
                    "tooltip": "Video Model Results Will Show UP Here So You Could Choose From.",
                    "default": "urn:air:video:klingai:5@3 (KlingAI 2.1)",
                }),
                "Use Search Value": ("BOOLEAN", {
                    "tooltip": "When Enabled, the value you've set in the search input will be used instead.\n\nThis is useful in case the model search API is down or you prefer to set the model manually.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
            },
        }

    DESCRIPTION = "Directly Search and Connect Video Models to Runware Video Inference Nodes In ComfyUI."
    FUNCTION = "videoModelSearch"
    RETURN_TYPES = ("RUNWAREVIDEOMODEL", "INT", "INT")
    RETURN_NAMES = ("Runware Video Model", "Width", "Height")
    CATEGORY = "Runware"

    @classmethod
    def VALIDATE_INPUTS(cls, VideoList):
        return True

    def videoModelSearch(self, **kwargs):
        enableSearchValue = kwargs.get("Use Search Value", False)
        searchInput = kwargs.get("Model Search")

        if enableSearchValue:
            modelAIRCode = searchInput
        else:
            crModel = kwargs.get("VideoList")
            # Extract the full AIR identifier (everything before the first space)
            modelAIRCode = crModel.split(" (")[0]

        # Get dimensions for the selected model
        dimensions = self.MODEL_DIMENSIONS.get(modelAIRCode, {"width": 1024, "height": 576})
        
        return ({
            "model": modelAIRCode,
        }, dimensions["width"], dimensions["height"]) 