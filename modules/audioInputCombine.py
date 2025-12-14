"""
Runware Audio Input Combine Node
Combines multiple audio inputs into a list
"""

from typing import List, Dict, Any


class RunwareAudioInputCombine:
    """Runware Audio Input Combine Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Audio Input 1": ("RUNWAREAUDIOINPUT", {
                    "tooltip": "Connect a Runware Audio Input node.",
                }),
            },
            "optional": {
                "Audio Input 2": ("RUNWAREAUDIOINPUT", {
                    "tooltip": "Connect a Runware Audio Input node.",
                }),
                "Audio Input 3": ("RUNWAREAUDIOINPUT", {
                    "tooltip": "Connect a Runware Audio Input node.",
                }),
                "Audio Input 4": ("RUNWAREAUDIOINPUT", {
                    "tooltip": "Connect a Runware Audio Input node.",
                }),
            },
        }

    DESCRIPTION = "Combine multiple audio inputs to connect with Runware Video Inference Inputs."
    FUNCTION = "audioInputCombine"
    RETURN_TYPES = ("RUNWAREAUDIOINPUT",)
    RETURN_NAMES = ("Audio Inputs",)
    CATEGORY = "Runware"

    def audioInputCombine(self, **kwargs):
        """Combine audio inputs into a list"""
        audioInputs = []
        
        for i in range(1, 5):
            audioKey = f"Audio Input {i}"
            audioInput = kwargs.get(audioKey)
            if audioInput is not None and isinstance(audioInput, dict) and len(audioInput) > 0:
                audioInputs.append(audioInput)
        
        return (audioInputs,)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareAudioInputCombine": RunwareAudioInputCombine,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareAudioInputCombine": "Runware Audio Inputs Combine",
}

