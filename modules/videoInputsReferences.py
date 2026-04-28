from .utils import runwareUtils as rwUtils
from typing import List, Dict, Any


class videoInputsReferences:
    """Video Inputs References node for configuring reference images with types"""
    
    MAX_REFERENCES = 10
    MAX_GROUPED_REFERENCES = 4
    
    @classmethod
    def INPUT_TYPES(cls):
        optionalInputs = {}
        
        for i in range(1, cls.MAX_REFERENCES + 1):
            ordinal = rwUtils.getOrdinal(i)
            optionalInputs[f"Image{i}"] = ("IMAGE", {
                "tooltip": f"{ordinal.capitalize()} single reference image (mutually exclusive with Images{i}).",
            })
            if i <= cls.MAX_GROUPED_REFERENCES:
                optionalInputs[f"Images{i}"] = ("RUNWAREVIDEOINPUTSREFERENCEMULTIIMAGES", {
                    "tooltip": f"{ordinal.capitalize()} reference image group from the Multiple Images Connector (mutually exclusive with Image{i}).",
                })
                optionalInputs[f"Tag{i}"] = ("STRING", {
                    "tooltip": f"Optional tag for the {ordinal} reference (e.g., @image{i}, @Actor-1).",
                    "default": "",
                })
                optionalInputs[f"Type{i}"] = ("STRING", {
                    "tooltip": f"Type for the {ordinal} reference (e.g., image or grid). Leave empty to omit.",
                    "default": "",
                })
                optionalInputs[f"Audio{i}"] = ("STRING", {
                    "tooltip": f"Optional audio URL/mediaUUID for the {ordinal} reference.",
                    "default": "",
                })
        
        return {
            "required": {},
            "optional": optionalInputs
        }

    DESCRIPTION = (
        "Configure up to 4 reference image entries for video inference inputs. "
        "For each slot, provide either ImageN (single image) or ImagesN (connector output), not both."
    )
    FUNCTION = "createReferences"
    RETURN_TYPES = ("RUNWAREVIDEOINPUTSREFERENCEIMAGES",)
    RETURN_NAMES = ("Video Inputs Reference Images",)
    CATEGORY = "Runware"

    def createReferences(self, **kwargs) -> tuple[List[Any]]:
        """Create list of reference entries from provided parameters."""
        references: List[Any] = []
        
        for i in range(1, self.MAX_REFERENCES + 1):
            imageKey = f"Image{i}"
            imagesKey = f"Images{i}"
            tagKey = f"Tag{i}"
            typeKey = f"Type{i}"
            audioKey = f"Audio{i}"
            
            image = kwargs.get(imageKey)
            images = kwargs.get(imagesKey)
            refTag = (kwargs.get(tagKey) or "").strip()
            refType = kwargs.get(typeKey, "")
            refAudio = (kwargs.get(audioKey) or "").strip()
            
            has_image = image is not None
            has_images = isinstance(images, list) and len(images) > 0
            if has_image and has_images:
                raise ValueError(
                    f"Reference {i}: use either {imageKey} or {imagesKey}, not both."
                )
            
            if has_image or has_images:
                reference = self._createReference(image, images, refTag, refType, refAudio)
                references.append(reference)
        
        return (references,)

    def _createReference(self, image, images, refTag: str, refType: str, refAudio: str):
        """Create reference entry."""
        entry: Dict[str, Any] = {}
        if image is not None:
            entry["image"] = rwUtils.convertTensor2IMG(image)
        elif isinstance(images, list) and len(images) > 0:
            entry["images"] = images
        else:
            return entry

        if refTag:
            entry["tag"] = refTag
        if isinstance(refType, str) and refType.strip():
            entry["type"] = refType.strip()
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
