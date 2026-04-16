from typing import List


class referenceAudios:
    """Reference Audios node for configuring reference audio inputs"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "Audio1": ("STRING", {
                    "default": "",
                    "tooltip": "MediaUUID for the first reference audio from Runware Media Upload node.",
                }),
                "Audio2": ("STRING", {
                    "default": "",
                    "tooltip": "MediaUUID for the second reference audio from Runware Media Upload node.",
                }),
                "Audio3": ("STRING", {
                    "default": "",
                    "tooltip": "MediaUUID for the third reference audio from Runware Media Upload node.",
                }),
                "Audio4": ("STRING", {
                    "default": "",
                    "tooltip": "MediaUUID for the fourth reference audio from Runware Media Upload node.",
                }),
            }
        }

    DESCRIPTION = "Configure multiple reference audios (mediaUUIDs) for video inference inputs."
    FUNCTION = "createReferenceAudios"
    RETURN_TYPES = ("RUNWAREINPUTAUDIOS",)
    RETURN_NAMES = ("Reference Audios",)
    CATEGORY = "Runware"

    def createReferenceAudios(self, **kwargs) -> tuple[List[str]]:
        """Create list of reference audio UUIDs from provided parameters"""
        audioList = []

        for i in range(1, 5):
            audioKey = f"Audio{i}"
            audioUuid = kwargs.get(audioKey)

            if audioUuid and audioUuid.strip() != "":
                audioList.append(audioUuid.strip())

        return (audioList,)
