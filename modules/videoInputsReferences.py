from .utils import runwareUtils as rwUtils
from typing import List, Dict, Any


class videoInputsReferences:
    """Video Inputs References node for configuring reference images with types"""
    
    MAX_REFERENCES = 10
    
    @classmethod
    def INPUT_TYPES(cls):
        optionalInputs = {}
        
        for i in range(1, cls.MAX_REFERENCES + 1):
            ordinal = rwUtils.getOrdinal(i)
            optionalInputs[f"Image{i}"] = ("IMAGE", {
                "tooltip": f"{ordinal.capitalize()} reference image (primary image for this reference entry).",
            })
            optionalInputs[f"Tag{i}"] = ("STRING", {
                "tooltip": f"Optional tag for the {ordinal} reference (e.g., @image{i}, @Actor-1).",
                "default": "",
            })
            optionalInputs[f"Type{i}"] = ("STRING", {
                "tooltip": f"Type for the {ordinal} reference (e.g., grid or image).",
                "default": "",
            })
            optionalInputs[f"Audio{i}"] = ("STRING", {
                "tooltip": f"Optional audio URL/mediaUUID for the {ordinal} reference (supported for type=image).",
                "default": "",
            })
        
        return {
            "required": {},
            "optional": optionalInputs
        }

    DESCRIPTION = (
        "Configure multiple reference image entries for video inference inputs, "
        "with optional tag, type, images list, and audio per entry."
    )
    FUNCTION = "createReferences"
    RETURN_TYPES = ("RUNWAREVIDEOINPUTSREFERENCEIMAGES",)
    RETURN_NAMES = ("Video Inputs Reference Images",)
    CATEGORY = "Runware"

    def createReferences(self, **kwargs) -> tuple[List[Any]]:
        """Create list of reference entries from provided parameters."""
        references = []
        
        for i in range(1, self.MAX_REFERENCES + 1):
            imageKey = f"Image{i}"
            tagKey = f"Tag{i}"
            typeKey = f"Type{i}"
            audioKey = f"Audio{i}"
            
            image = kwargs.get(imageKey)
            refTag = (kwargs.get(tagKey) or "").strip()
            refType = (kwargs.get(typeKey) or "").strip()
            refAudio = (kwargs.get(audioKey) or "").strip()
            
            if image is not None:
                reference = self._createReference(image, refTag, refType, refAudio)
                references.append(reference)
        
        return (references,)

    def _createReference(self, image, refTag: str, refType: str, refAudio: str):
        """
        Backward compatible behavior:
        - If no extra metadata is provided, return legacy string entry.
        - If tag/type/images/audio are provided, return object entry.
        """
        imageUrl = rwUtils.convertTensor2IMG(image)
        images = [imageUrl]

        has_extended_fields = bool(refTag or refType or refAudio or len(images) > 1)
        if not has_extended_fields:
            return imageUrl

        entry: Dict[str, Any] = {"images": images}
        if refTag:
            entry["tag"] = refTag
        if refType:
            entry["type"] = refType
        if refAudio:
            entry["audio"] = refAudio
        return entry


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareVideoInputsReferences": videoInputsReferences,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVideoInputsReferences": "Runware Video Inference Inputs Reference Images",
}
