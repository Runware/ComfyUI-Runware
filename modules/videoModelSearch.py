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
            "klingai:6@1 (KlingAI 2.5 Turbo Pro)",
            "klingai:7@1 (KlingAI Lip-Sync)",
            "klingai:kling@o1 (Kling VIDEO O1)",
            "klingai:kling-video@2.6-pro (Kling VIDEO 2.6 Pro)",
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
            "bytedance:seedance@1.5-pro (Seedance 1.5 Pro)",
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
            "pixverse:1@5-fast (PixVerse v5 Fast)",
            "pixverse:1@6 (PixVerse v5.5)",
            "pixverse:1@7 (PixVerse v5.6)",
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
            "runware:200@8 (Wan 2.2 A14B Animate)",
            "alibaba:wan@2.6 (Wan 2.6)",
            "alibaba:wan@2.6-flash (Wan 2.6 Flash)",
        ],
        "OpenAI": [
            "openai:3@1 (OpenAI Sora 3.1)",
            "openai:3@0 (OpenAI Sora 3.0)",
        ],
        "Lightricks": [
            "lightricks:2@0 (LTX Fast)",
            "lightricks:2@1 (LTX Pro)",
            "lightricks:3@1 (LTX-2 Retake)",
            "lightricks:ltx@2 (LTX-2)",
        ],
        "Ovi": [
            "runware:190@1 (Ovi)",
        ],
        "Runway": [
            "runway:2@1 (Runway Aleph)",
            "runway:1@1 (Runway Gen-4 Turbo)",
        ],
        "Luma": [
            "lumaai:1@1 (Luma Ray 1.6)",
            "lumaai:2@1 (Luma Ray 2)",
            "lumaai:2@2 (Luma Ray 2 Flash)",
        ],
        "Sync": [
            "sync:lipsync-2@1 (Sync LipSync 2)",
            "sync:lipsync-2-pro@1 (Sync LipSync 2 Pro)",
            "sync:react-1@1 (Sync React-1)",
        ],
        "Bria": [
            "bria:60@1 (Bria Video Eraser)",
        ],
        "Creatify": [
            "creatify:aurora@fast (Creatify Aurora Avatar Model API (720p))",
            "creatify:aurora@0 (Creatify Aurora Avatar Model API (720p))",
        ],
        "Hunyuan": [
            "runware:hunyuanvideo@1.5 (HunyuanVideo-1.5)",
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
        "klingai:6@1": {"width": 1920, "height": 1080},
        "klingai:7@1": {"width": 0, "height": 0},
        "klingai:kling@o1": {"width": 1440, "height": 1440},
        "klingai:kling-video@2.6-pro": {"width": 1920, "height": 1080},
        
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
        "bytedance:seedance@1.5-pro": {"width": 864, "height": 496},
        
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
        "pixverse:1@5-fast": {"width": 640, "height": 360},
        "pixverse:1@6": {"width": 640, "height": 360},
        "pixverse:1@7": {"width": 640, "height": 360},
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
        "runware:200@8": {"width": 1104, "height": 832},
        "alibaba:wan@2.6": {"width": 1280, "height": 720},
        "alibaba:wan@2.6-flash": {"width": 1280, "height": 720},
        
        # OpenAI Models
        "openai:3@1": {"width": 1280, "height": 720},
        "openai:3@0": {"width": 1280, "height": 720},
        
        # Lightricks Models
        "lightricks:2@0": {"width": 1920, "height": 1080},
        "lightricks:2@1": {"width": 1920, "height": 1080},
        "lightricks:3@1": {"width": 0, "height": 0},
        "lightricks:ltx@2": {"width": 1024, "height": 1024},
        
        # Ovi Models
        "runware:190@1": {"width": 0, "height": 0},
        
        # Runway Models
        "runway:2@1": {"width": 1280, "height": 720},
        "runway:1@1": {"width": 1280, "height": 720},
        
        # Luma Models
        "lumaai:1@1": {"width": 1080, "height": 720},
        "lumaai:2@1": {"width": 1080, "height": 720},
        "lumaai:2@2": {"width": 1080, "height": 720},
        
        # Sync Models
        "sync:lipsync-2@1": {"width": 0, "height": 0},
        "sync:lipsync-2-pro@1": {"width": 0, "height": 0},
        "sync:react-1@1": {"width": 0, "height": 0},
        
        # Bria Models
        "bria:60@1": {"width": 0, "height": 0},
        
        # Creatify Models
        "creatify:aurora@fast": {"width": 1280, "height": 720},
        "creatify:aurora@0": {"width": 1280, "height": 720},
        
        # Hunyuan Models
        "runware:hunyuanvideo@1.5": {"width": 848, "height": 480},
    }
    
    # Model resolutions mapping
    MODEL_RESOLUTIONS = {
        # KlingAI Models
        "klingai:1@2": "720p",
        "klingai:1@1": "720p",
        "klingai:2@2": "1080p",
        "klingai:2@1": "720p",
        "klingai:3@1": "720p",
        "klingai:3@2": "1080p",
        "klingai:4@3": "720p",
        "klingai:5@1": "720p",
        "klingai:5@2": "1080p",
        "klingai:5@3": "1080p",
        "klingai:6@1": "1080p",
        "klingai:7@1": None,  # No resolution support
        "klingai:kling@o1": None,  # No standard resolution (1440x1440)
        "klingai:kling-video@2.6-pro": "1080p",
        
        # Veo Models
        "google:2@0": "720p",
        "google:3@0": "720p",
        "google:3@1": "720p",
        "google:3@2": "720p",
        "google:3@3": "720p",
        
        # Bytedance Models
        "bytedance:2@1": "480p",
        "bytedance:1@1": "480p",
        "bytedance:5@1": None,  # No resolution support (fixed 1024x1024)
        "bytedance:5@2": None,  # No resolution support (fixed 1024x1024)
        "bytedance:seedance@1.5-pro": "480p",
        
        # MiniMax Models (support both 768p and 720p, using 768p as primary)
        "minimax:1@1": "768p",
        "minimax:2@1": "768p",
        "minimax:2@3": "768p",
        "minimax:3@1": "768p",
        "minimax:4@1": "768p",
        "minimax:4@2": "768p",
        
        # PixVerse Models
        "pixverse:1@1": "360p",
        "pixverse:1@2": "360p",
        "pixverse:1@3": "360p",
        "pixverse:1@5-fast": "360p",
        "pixverse:1@6": "360p",
        "pixverse:1@7": "360p",
        "pixverse:lipsync@1": "360p",
        
        # Vidu Models
        "vidu:1@0": "1080p",
        "vidu:1@1": "1080p",
        "vidu:1@5": "1080p",
        "vidu:2@0": "1080p",
        
        # Wan Models
        "runware:200@1": "480p",
        "runware:200@2": "480p",
        "runware:200@6": "720p",
        "runware:200@8": "720p",
        "alibaba:wan@2.6": "720p",
        "alibaba:wan@2.6-flash": "720p",
        
        # OpenAI Models
        "openai:3@1": "720p",
        "openai:3@0": "720p",
        
        # Lightricks Models
        "lightricks:2@0": "1080p",
        "lightricks:2@1": "1080p",
        "lightricks:3@1": None,  # No resolution support
        "lightricks:ltx@2": None,  # No resolution support (fixed 1024x1024)
        
        # Ovi Models
        "runware:190@1": None,  # No resolution support
        
        # Runway Models
        "runway:2@1": "720p",
        "runway:1@1": "720p",
        
        # Luma Models
        "lumaai:1@1": "720p",
        "lumaai:2@1": "720p",
        "lumaai:2@2": "720p",
        
        # Sync Models
        "sync:lipsync-2@1": "720p",
        "sync:lipsync-2-pro@1": "720p",
        "sync:react-1@1": "720p",
        
        # Bria Models
        "bria:60@1": "720p",
        
        # Creatify Models
        "creatify:aurora@fast": "720p",
        "creatify:aurora@0": "720p",
        
        # Hunyuan Models
        "runware:hunyuanvideo@1.5": "480p",
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
        "Ovi",
        "Runway",
        "Luma",
        "Sync",
        "Bria",
        "Creatify",
        "Hunyuan"
    ]
    
    DEFAULT_DIMENSIONS = {"width": 1024, "height": 576}
    
    @classmethod
    def INPUT_TYPES(cls):
        allModels = cls._getAllModels()
        defaultModel = "klingai:5@3 (KlingAI V2.0 Master)"
        defaultModelCode = defaultModel.split(" (")[0]
        defaultDims = cls.MODEL_DIMENSIONS.get(defaultModelCode, cls.DEFAULT_DIMENSIONS)
        defaultResolution = cls.MODEL_RESOLUTIONS.get(defaultModelCode, None)
        
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
                "useCustomDimensions": (["Model Default", "Custom", "Disabled"], {
                    "tooltip": "Model Default: Use model's recommended resolution. Custom: Use custom Width/Height values. Disabled: Don't pass width/height to API.",
                    "default": "Model Default",
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
                "useResolution": ("BOOLEAN", {
                    "tooltip": "Enable to include resolution parameter in API request. Disable if your model doesn't support resolution.",
                    "default": False,
                }),
                "resolution": (["360p", "480p", "720p", "768p", "1080p"], {
                    "tooltip": "Select a standard resolution for Video Inference. Only used when 'Use Resolution' is enabled.",
                    "default": defaultResolution if defaultResolution else "720p",
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
    RETURN_TYPES = ("RUNWAREVIDEOMODEL",)
    RETURN_NAMES = ("Runware Video Model",)
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
        useCustomDimensions = kwargs.get("useCustomDimensions", "Model Default")
        useResolution = kwargs.get("useResolution", False)
        resolution = kwargs.get("resolution", "720p")

        if enableSearchValue:
            modelAirCode = searchInput
        else:
            currentModel = kwargs.get("VideoList")
            modelAirCode = currentModel.split(" (")[0]

        dimensions = self.MODEL_DIMENSIONS.get(modelAirCode, self.DEFAULT_DIMENSIONS)
        modelResolution = self.MODEL_RESOLUTIONS.get(modelAirCode, None)
        
        if useCustomDimensions == "Custom":
            # Use custom dimensions from Width/Height widgets
            width = customWidth
            height = customHeight
        elif useCustomDimensions == "Disabled":
            # Don't pass width/height (use None in dict)
            width = None
            height = None
        else:  # "Model Default"
            # Use model default dimensions
            width = dimensions["width"]
            height = dimensions["height"]

        resultDict = {
            "model": modelAirCode,
            "useCustomDimensions": useCustomDimensions,
            "width": width,
            "height": height,
        }

        # Add resolution if enabled and model supports it
        if useResolution and modelResolution is not None:
            resultDict["resolution"] = resolution
            resultDict["useResolution"] = True
        else:
            resultDict["useResolution"] = False

        return (resultDict,)
