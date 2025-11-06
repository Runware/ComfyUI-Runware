class RunwareAudioModelSearch:
    """Audio Model Search node for searching audio models"""
    
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
    FUNCTION = "searchModels"
    CATEGORY = "Runware/Audio"

    def searchModels(self, **kwargs):
        """Search for audio models"""
        searchQuery = kwargs.get("searchQuery", "")
        provider = kwargs.get("provider", "elevenlabs")
        
        return (searchQuery,)
