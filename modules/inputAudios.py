from typing import List


class inputAudios:
    """Input Audios node for configuring multiple audio inputs"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "Audio1": ("STRING", {
                    "tooltip": "MediaUUID for the first audio file from Runware Media Upload node.",
                }),
                "Audio2": ("STRING", {
                    "tooltip": "MediaUUID for the second audio file from Runware Media Upload node.",
                }),
                "Audio3": ("STRING", {
                    "tooltip": "MediaUUID for the third audio file from Runware Media Upload node.",
                }),
                "Audio4": ("STRING", {
                    "tooltip": "MediaUUID for the fourth audio file from Runware Media Upload node.",
                }),
            }
        }

    DESCRIPTION = "Configure multiple audio inputs (mediaUUIDs) for video generation with audio synchronization."
    FUNCTION = "createInputAudios"
    RETURN_TYPES = ("RUNWAREINPUTAUDIOS",)
    RETURN_NAMES = ("Input Audios",)
    CATEGORY = "Runware"

    def createInputAudios(self, **kwargs) -> tuple[List[str]]:
        """Create list of audio UUIDs from provided parameters"""
        audioList = []
        
        for i in range(1, 5):
            audioKey = f"Audio{i}"
            audioUuid = kwargs.get(audioKey)
            
            if audioUuid and audioUuid.strip() != "":
                audioList.append(audioUuid.strip())
        
        return (audioList,)
