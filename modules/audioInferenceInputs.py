from .utils import runwareUtils as rwUtils
from typing import Dict, Any


class audioInferenceInputs:
    """Audio Inference Inputs node for configuring audio generation inputs"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "Video": ("STRING", {
                    "tooltip": "Video URL or mediaUUID for audio generation. Can be a direct URL or a mediaUUID from Runware Media Upload node.",
                    "default": "",
                }),
            }
        }

    DESCRIPTION = "Configure custom inputs for Runware Audio Inference, including video input for audio extraction or generation."
    FUNCTION = "createInputs"
    RETURN_TYPES = ("RUNWAREAUDIOINFERENCEINPUTS",)
    RETURN_NAMES = ("Audio Inference Inputs",)
    CATEGORY = "Runware"

    def createInputs(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create audio inference inputs from provided parameters"""
        video = kwargs.get("Video", None)
        
        inputs = {}
        
        if video is not None and video.strip() != "":
            inputs["video"] = video.strip()
        
        return (inputs,)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareAudioInferenceInputs": audioInferenceInputs,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareAudioInferenceInputs": "Runware Audio Inference Inputs",
}

