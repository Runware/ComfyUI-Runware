from .utils import runwareUtils as rwUtils
from typing import List, Dict, Any

class videoInputsReferences:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "Image1": ("IMAGE", {
                    "tooltip": "First reference image.",
                }),
                "Type1": ("STRING", {
                    "tooltip": "Type for the first reference (e.g., 'asset'). Leave empty to omit.",
                    "default": "",
                }),
                "Image2": ("IMAGE", {
                    "tooltip": "Second reference image.",
                }),
                "Type2": ("STRING", {
                    "tooltip": "Type for the second reference (e.g., 'asset'). Leave empty to omit.",
                    "default": "",
                }),
                "Image3": ("IMAGE", {
                    "tooltip": "Third reference image.",
                }),
                "Type3": ("STRING", {
                    "tooltip": "Type for the third reference (e.g., 'asset'). Leave empty to omit.",
                    "default": "",
                }),
                "Image4": ("IMAGE", {
                    "tooltip": "Fourth reference image.",
                }),
                "Type4": ("STRING", {
                    "tooltip": "Type for the fourth reference (e.g., 'asset'). Leave empty to omit.",
                    "default": "",
                }),
            }
        }

    DESCRIPTION = "Configure multiple reference images with optional types for video inference inputs."
    FUNCTION = "createReferences"
    RETURN_TYPES = ("RUNWAREVIDEOINPUTSREFERENCES",)
    RETURN_NAMES = ("Video Inputs References",)
    CATEGORY = "Runware"

    def createReferences(self, **kwargs) -> tuple[List[Dict[str, Any]]]:
        references = []
        
        for i in range(1, 5):
            image_key = f"Image{i}"
            type_key = f"Type{i}"
            
            image = kwargs.get(image_key)
            ref_type = kwargs.get(type_key, "")
            
            if image is not None:
                # Convert image tensor to URL
                image_url = rwUtils.convertTensor2IMG(image)
                
                reference = {"image": image_url}
                
                # Only add type if it's not empty
                if ref_type and ref_type.strip() != "":
                    reference["type"] = ref_type.strip()
                
                references.append(reference)
        
        return (references,)

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareVideoInputsReferences": videoInputsReferences,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVideoInputsReferences": "Runware Video Inputs References",
}

