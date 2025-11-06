from typing import List
from .utils import runwareUtils as rwUtils


class referenceVideos:
    """Reference Videos node for configuring reference video inputs"""
    
    MAX_VIDEOS = 4
    
    @classmethod
    def INPUT_TYPES(cls):
        optionalInputs = {}
        
        for i in range(1, cls.MAX_VIDEOS + 1):
            ordinal = rwUtils.getOrdinal(i)
            optionalInputs[f"Video{i}"] = ("STRING", {
                "tooltip": f"MediaUUID for the {ordinal} reference video from Runware Media Upload node.",
            })
        
        return {
            "required": {},
            "optional": optionalInputs
        }

    DESCRIPTION = "Configure multiple reference video inputs (mediaUUIDs) for video generation."
    FUNCTION = "createReferenceVideos"
    RETURN_TYPES = ("RUNWAREREFERENCEVIDEOS",)
    RETURN_NAMES = ("Reference Videos",)
    CATEGORY = "Runware"

    def createReferenceVideos(self, **kwargs) -> tuple[List[str]]:
        """Create list of reference video UUIDs"""
        videoList = []
        
        for i in range(1, self.MAX_VIDEOS + 1):
            videoKey = f"Video{i}"
            videoUuid = kwargs.get(videoKey)
            
            if videoUuid and videoUuid.strip() != "":
                videoList.append(videoUuid.strip())
        
        return (videoList,)
