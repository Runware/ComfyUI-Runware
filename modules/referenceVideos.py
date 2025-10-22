from .utils import runwareUtils as rwUtils

class referenceVideos:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "Video1": ("STRING", {
                    "tooltip": "Connect mediaUUID from Runware Media Upload node. This video will be used as a reference.",
                }),
                "Video2": ("STRING", {
                    "tooltip": "Connect mediaUUID from Runware Media Upload node.",
                }),
                "Video3": ("STRING", {
                    "tooltip": "Connect mediaUUID from Runware Media Upload node.",
                }),
                "Video4": ("STRING", {
                    "tooltip": "Connect mediaUUID from Runware Media Upload node.",
                }),
            }
        }

    DESCRIPTION = "Configure multiple reference video inputs (mediaUUIDs) for video generation with reference video guidance."
    FUNCTION = "create_reference_videos"
    RETURN_TYPES = ("RUNWAREREFERENCEVIDEOS",)
    RETURN_NAMES = ("Reference Videos",)
    CATEGORY = "Runware"

    def create_reference_videos(self, **kwargs):
        video_list = []
        for i in range(1, 5):
            video_key = f"Video{i}"
            video_uuid = kwargs.get(video_key, None)
            if video_uuid and video_uuid.strip() != "":
                video_list.append(video_uuid.strip())
        
        return (video_list,)
