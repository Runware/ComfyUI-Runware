class RunwareAudioModelSearch:
    """Audio Model Search node for searching audio models"""
    
    # Define the audio models by provider
    AUDIO_MODELS = {
        "ElevenLabs": [
            "elevenlabs:1@1 (ElevenLabs Multilingual v2)",
            "elevenlabs:2@1 (ElevenLabs Multilingual v2 Turbo)",
            "elevenlabs:3@1 (ElevenLabs Monolingual v1)",
        ],
        "KlingAI": [
            "klingai:8@1 (KlingAI Audio)",
        ],
        "Mirelo": [
            "mirelo:1@1 (Mirelo SFX 1.5)",
        ],
        "Ace": [
            "runware:ace-step@0 (ACE Step v1 3.5B)",
            "runware:ace-step@v1.5-base (ACE-Step v1.5 Base)",
            "runware:ace-step@v1.5-turbo (ACE-Step v1.5 Turbo)",
        ],
        "Dia": [
            "runware:dia@v1.0 (Dia 1.6B)",
        ],
        "xAI": [
            "xai:voice@tts (xAI TTS)",
        ],
        "MiniMax": [
            "minimax:speech@2.8 (MiniMax Speech 2.8)",
        ],
        "Inworld": [
            "inworld:tts@1.5-mini (Inworld TTS-1.5 Mini)",
            "inworld:tts@1.5-max (Inworld TTS-1.5 Max)",
        ],
    }
    
    MODEL_PROVIDERS = [
        "All",
        "ElevenLabs",
        "KlingAI",
        "Mirelo",
        "Ace",
        "Dia",
        "xAI",
        "MiniMax",
        "Inworld",
    ]
    
    @classmethod
    def INPUT_TYPES(cls):
        allModels = cls._getAllModels()
        defaultModel = "elevenlabs:1@1 (ElevenLabs Multilingual v2)"
        
        return {
            "required": {
                "Model Search": ("STRING", {
                    "tooltip": "Search For Specific Audio Model By Name Or Code (eg: elevenlabs, klingai).",
                }),
                "Model Provider": (cls.MODEL_PROVIDERS, {
                    "tooltip": "Choose Audio Model Provider To Filter Results.",
                    "default": "ElevenLabs",
                }),
                "AudioList": (allModels, {
                    "tooltip": "Audio Model Results Will Show UP Here So You Could Choose From.",
                    "default": defaultModel,
                }),
                "Use Search Value": ("BOOLEAN", {
                    "tooltip": "When Enabled, the value you've set in the search input will be used instead.\n\nThis is useful in case the model search API is down or you prefer to set the model manually.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
            }
        }

    @classmethod
    def _getAllModels(cls):
        """Get all models from all providers"""
        allModels = []
        for models in cls.AUDIO_MODELS.values():
            allModels.extend(models)
        return allModels

    RETURN_TYPES = ("RUNWAREAUDIOMODEL",)
    RETURN_NAMES = ("model",)
    FUNCTION = "searchModels"
    CATEGORY = "Runware"
    DESCRIPTION = "Directly Search and Connect Audio Models to Runware Audio Inference Nodes In ComfyUI."

    @classmethod
    def VALIDATE_INPUTS(cls, AudioList):
        return True

    def searchModels(self, **kwargs):
        """Search and return audio model"""
        enableSearchValue = kwargs.get("Use Search Value", False)
        searchInput = kwargs.get("Model Search")
        
        if enableSearchValue:
            modelAirCode = searchInput
        else:
            currentModel = kwargs.get("AudioList")
            modelAirCode = currentModel.split(" (")[0]
        
        return (modelAirCode,)
