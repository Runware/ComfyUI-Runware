from typing import List
from .utils import runwareUtils as rwUtils


class referenceVoices:
    """Reference Voices node for configuring reference voice inputs"""
    
    MAX_VOICES = 4
    
    @classmethod
    def INPUT_TYPES(cls):
        optionalInputs = {}
        
        for i in range(1, cls.MAX_VOICES + 1):
            ordinal = rwUtils.getOrdinal(i)
            optionalInputs[f"Voice{i}"] = ("STRING", {
                "tooltip": f"URL or mediaUUID for the {ordinal} reference voice from Runware Media Upload node or external URL.",
            })
        
        return {
            "required": {},
            "optional": optionalInputs
        }

    DESCRIPTION = "Configure multiple reference voice inputs (URLs or mediaUUIDs) for video generation."
    FUNCTION = "createReferenceVoices"
    RETURN_TYPES = ("RUNWAREREFERENCEVOICES",)
    RETURN_NAMES = ("Reference Voices",)
    CATEGORY = "Runware"

    def createReferenceVoices(self, **kwargs) -> tuple[List[str]]:
        """Create list of reference voice URLs/UUIDs"""
        voiceList = []
        
        for i in range(1, self.MAX_VOICES + 1):
            voiceKey = f"Voice{i}"
            voiceUrl = kwargs.get(voiceKey)
            
            if voiceUrl and voiceUrl.strip() != "":
                voiceList.append(voiceUrl.strip())
        
        return (voiceList,)

