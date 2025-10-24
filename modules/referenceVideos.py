from .utils import runwareUtils as rwUtils
from typing import List, Dict, Any

class referenceVideos:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "Video1": ("STRING", {
                    "tooltip": "MediaUUID for the first reference video from Runware Media Upload node.",
                }),
                "Video2": ("STRING", {
                    "tooltip": "MediaUUID for the second reference video from Runware Media Upload node.",
                }),
                "Video3": ("STRING", {
                    "tooltip": "MediaUUID for the third reference video from Runware Media Upload node.",
                }),
                "Video4": ("STRING", {
                    "tooltip": "MediaUUID for the fourth reference video from Runware Media Upload node.",
                }),
            }
        }

    DESCRIPTION = "Configure multiple reference video inputs (mediaUUIDs) for video generation."
    FUNCTION = "createReferenceVideos"
    RETURN_TYPES = ("RUNWAREREFERENCEVIDEOS",)
    RETURN_NAMES = ("Reference Videos",)
    CATEGORY = "Runware"

    def createReferenceVideos(self, **kwargs) -> tuple[List[str]]:
        video_list = []
        for i in range(1, 5):
            video_key = f"Video{i}"
            video_uuid = kwargs.get(video_key)
            if video_uuid and video_uuid.strip() != "":
                video_list.append(video_uuid.strip())
        return (video_list,)

