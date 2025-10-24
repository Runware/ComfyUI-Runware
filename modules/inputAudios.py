from .utils import runwareUtils as rwUtils
from typing import List, Dict, Any

class inputAudios:
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
        audio_list = []
        for i in range(1, 5):
            audio_key = f"Audio{i}"
            audio_uuid = kwargs.get(audio_key)
            if audio_uuid and audio_uuid.strip() != "":
                audio_list.append(audio_uuid.strip())
        return (audio_list,)

