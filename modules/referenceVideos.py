from typing import Any, Dict, List
from .utils import runwareUtils as rwUtils


class referenceVideos:
    """Reference Videos node for configuring reference video inputs"""
    
    MAX_VIDEOS = 4
    
    @classmethod
    def INPUT_TYPES(cls):
        optionalInputs = {}
        
        for i in range(1, cls.MAX_VIDEOS + 1):
            ordinal = rwUtils.getOrdinal(i)
            optionalInputs[f"useVideo{i}"] = ("BOOLEAN", {
                "default": False,
                "tooltip": f"Enable to include the {ordinal} reference video.",
            })
            optionalInputs[f"Video{i}"] = ("STRING", {
                "tooltip": f"MediaUUID for the {ordinal} reference video from Runware Media Upload node.",
            })
            optionalInputs[f"Tag{i}"] = ("STRING", {
                "default": "",
                "tooltip": f"Optional tag for the {ordinal} reference video (e.g., @video{i}). Must be used in the prompt.",
            })
            optionalInputs[f"Type{i}"] = ("STRING", {
                "default": "reference",
                "tooltip": (
                    f"Optional type for the {ordinal} reference video. "
                    "For example: reference or extend."
                ),
            })
        
        return {
            "required": {},
            "optional": optionalInputs
        }

    DESCRIPTION = (
        "Configure multiple reference video inputs (mediaUUIDs) for video generation, "
        "with optional tag and type per reference."
    )
    FUNCTION = "createReferenceVideos"
    RETURN_TYPES = ("RUNWAREREFERENCEVIDEOS",)
    RETURN_NAMES = ("Reference Videos",)
    CATEGORY = "Runware"

    def createReferenceVideos(self, **kwargs) -> tuple[List[Any]]:
        """Create list of reference video entries (string UUIDs or objects with tag/type)."""
        videoList: List[Any] = []
        
        for i in range(1, self.MAX_VIDEOS + 1):
            useKey = f"useVideo{i}"
            videoKey = f"Video{i}"
            tagKey = f"Tag{i}"
            typeKey = f"Type{i}"
            useVideo = bool(kwargs.get(useKey, False))
            videoUuid = kwargs.get(videoKey)
            tagValue = (kwargs.get(tagKey) or "").strip()
            typeValue = (kwargs.get(typeKey) or "reference").strip()
            
            if useVideo and videoUuid and videoUuid.strip() != "":
                normalized_video = videoUuid.strip()

                # Backward compatible payload:
                # - If tag/type are not provided, keep legacy string entry.
                # - If tag or non-default type is provided, emit object entry.
                if tagValue or typeValue != "reference":
                    entry: Dict[str, str] = {"video": normalized_video}
                    if tagValue:
                        entry["tag"] = tagValue
                    if typeValue:
                        entry["type"] = typeValue
                    videoList.append(entry)
                else:
                    videoList.append(normalized_video)
        
        return (videoList,)
