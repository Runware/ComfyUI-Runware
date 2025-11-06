from .utils import runwareUtils as rwUtils
from typing import List, Dict, Any


class videoInputsReferences:
    """Video Inputs References node for configuring reference images with types"""
    
    MAX_REFERENCES = 4
    
    @classmethod
    def INPUT_TYPES(cls):
        optionalInputs = {}
        
        for i in range(1, cls.MAX_REFERENCES + 1):
            ordinal = rwUtils.getOrdinal(i)
            optionalInputs[f"Image{i}"] = ("IMAGE", {
                "tooltip": f"{ordinal.capitalize()} reference image.",
            })
            optionalInputs[f"Type{i}"] = ("STRING", {
                "tooltip": f"Type for the {ordinal} reference (e.g., 'asset'). Leave empty to omit.",
                "default": "",
            })
        
        return {
            "required": {},
            "optional": optionalInputs
        }

    DESCRIPTION = "Configure multiple reference images with optional types for video inference inputs."
    FUNCTION = "createReferences"
    RETURN_TYPES = ("RUNWAREVIDEOINPUTSREFERENCES",)
    RETURN_NAMES = ("Video Inputs References",)
    CATEGORY = "Runware"

    def createReferences(self, **kwargs) -> tuple[List[Dict[str, Any]]]:
        """Create list of reference objects from provided parameters"""
        references = []
        
        for i in range(1, self.MAX_REFERENCES + 1):
            imageKey = f"Image{i}"
            typeKey = f"Type{i}"
            
            image = kwargs.get(imageKey)
            refType = kwargs.get(typeKey, "")
            
            if image is not None:
                reference = self._createReference(image, refType)
                references.append(reference)
        
        return (references,)

    def _createReference(self, image, refType):
        """Create reference object from image and type"""
        imageUrl = rwUtils.convertTensor2IMG(image)
        reference = {"image": imageUrl}
        
        if refType and refType.strip() != "":
            reference["type"] = refType.strip()
        
        return reference


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareVideoInputsReferences": videoInputsReferences,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVideoInputsReferences": "Runware Video Inputs References",
}
