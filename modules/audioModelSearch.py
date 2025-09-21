class RunwareAudioModelSearch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "searchQuery": ("STRING", {
                    "default": "elevenlabs:1@1",
                    "tooltip": "Search for audio models by name, provider, or capabilities"
                }),
                "provider": (["elevenlabs"], {
                    "default": "elevenlabs",
                    "tooltip": "Currently only ElevenLabs is supported"
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREAUDIOMODEL",)
    RETURN_NAMES = ("model",)
    FUNCTION = "search_models"
    CATEGORY = "Runware/Audio"

    def search_models(self, **kwargs):
        searchQuery = kwargs.get("searchQuery", "")
        provider = kwargs.get("provider", "elevenlabs")
        
        return (searchQuery,)
        
       
