class videoModelSearch:
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
        ],
        "Veo": [
            "google:2@0 (Veo 2.0)",
            "google:3@0 (Veo 3.0)",
            "google:3@1 (Veo 3.0 Fast)",
            "google:3@2 (Veo 3.1)",
            "google:3@3 (Veo 3.1 Fast)",
        ],
        "Seedance": [
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
        "klingai:1@2": {"width": 1280, "height": 720},  # KlingAI V1.0 Pro
        "klingai:1@1": {"width": 1280, "height": 720},  # KlingAI V1 Standard
        "klingai:2@2": {"width": 1920, "height": 1080}, # KlingAI V1.5 Pro
        "klingai:2@1": {"width": 1280, "height": 720},  # KlingAI V1.5 Standard
        "klingai:3@1": {"width": 1280, "height": 720},  # KlingAI V1.6 Standard
        "klingai:3@2": {"width": 1920, "height": 1080}, # KlingAI V1.6 Pro
        "klingai:4@3": {"width": 1280, "height": 720},  # KlingAI V2.1 Master
        "klingai:5@1": {"width": 1280, "height": 720},  # KlingAI V2.1 Standard (I2V)
        "klingai:5@2": {"width": 1920, "height": 1080}, # KlingAI V2.1 Pro (I2V)
        "klingai:5@3": {"width": 1920, "height": 1080}, # KlingAI V2.0 Master
        
        # Veo Models
        "google:2@0": {"width": 1280, "height": 720},   # Veo 2.0
        "google:3@0": {"width": 1280, "height": 720},   # Veo 3.0
        "google:3@1": {"width": 1280, "height": 720},   # Veo 3.0 Fast
        "google:3@2": {"width": 1280, "height": 720},   # Veo 3.1
        "google:3@3": {"width": 1280, "height": 720},   # Veo 3.1 Fast
        
        # Seedance Models
        "bytedance:2@1": {"width": 864, "height": 480},  # Seedance 1.0 Pro
        "bytedance:1@1": {"width": 864, "height": 480},  # Seedance 1.0 Lite
        "bytedance:5@1": {"width": 1024, "height": 1024},  # OmniHuman 1
        "bytedance:5@2": {"width": 1024, "height": 1024},  # OmniHuman 1.5
        
        # MiniMax Models
        "minimax:1@1": {"width": 1366, "height": 768},  # MiniMax 01 Base
        "minimax:2@1": {"width": 1366, "height": 768},  # MiniMax 01 Director
        "minimax:2@3": {"width": 1366, "height": 768},  # MiniMax I2V 01 Live
        "minimax:3@1": {"width": 1366, "height": 768},  # MiniMax 02 Hailuo
        "minimax:4@1": {"width": 1366, "height": 768},  # MiniMax Hailuo 2.3
        "minimax:4@2": {"width": 1366, "height": 768},  # MiniMax Hailuo 2.3 Fast
        
        # PixVerse Models
        "pixverse:1@1": {"width": 640, "height": 360},  # PixVerse v3.5
        "pixverse:1@2": {"width": 640, "height": 360},  # PixVerse v4
        "pixverse:1@3": {"width": 640, "height": 360},  # PixVerse v4.5
        "pixverse:lipsync@1": {"width": 640, "height": 360},  # PixVerse LipSync
        
        # Vidu Models
        "vidu:1@0": {"width": 1920, "height": 1080},    # Vidu Q1 Classic
        "vidu:1@1": {"width": 1920, "height": 1080},    # Vidu Q1
        "vidu:1@5": {"width": 1920, "height": 1080},    # Vidu 1.5
        "vidu:2@0": {"width": 1920, "height": 1080},    # Vidu 2.0
        
        # Wan Models
        "runware:200@1": {"width": 853, "height": 480}, # Wan 2.1 1.3B
        "runware:200@2": {"width": 853, "height": 480}, # Wan 2.1 14B
        
        # OpenAI Models
        "openai:3@1": {"width": 1280, "height": 720}, # OpenAI Sora 3.1
        "openai:3@0": {"width": 1280, "height": 720}, # OpenAI Sora 3.0
        
        # Lightricks Models
        "lightricks:2@0": {"width": 1920, "height": 1080}, # Lightricks v2.0 Fast
        "lightricks:2@1": {"width": 1920, "height": 1080}, # Lightricks v2.1 Pro
        
        # Ovi Models
        "runware:190@1": {"width": 0, "height": 0}, # Ovi
    }
    
    
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
                        "Wan",
                        "OpenAI",
                        "Lightricks",
                        "Ovi"
                    ], {
                    "tooltip": "Choose Video Model Architecture To Filter Results.",
                    "default": "KlingAI",
                }),
                "VideoList": (all_models, {
                    "tooltip": "Video Model Results Will Show UP Here So You Could Choose From.",
                    "default": "klingai:5@3 (KlingAI V2.0 Master)",
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