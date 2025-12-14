"""
Runware Speech Input Combine Node
Combines multiple speech inputs into a list
"""

from typing import List, Dict, Any


class RunwareSpeechInputCombine:
    """Runware Speech Input Combine Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Speech Input 1": ("RUNWARESPEECHINPUT", {
                    "tooltip": "Connect a Runware Speech Input node.",
                }),
            },
            "optional": {
                "Speech Input 2": ("RUNWARESPEECHINPUT", {
                    "tooltip": "Connect a Runware Speech Input node.",
                }),
                "Speech Input 3": ("RUNWARESPEECHINPUT", {
                    "tooltip": "Connect a Runware Speech Input node.",
                }),
                "Speech Input 4": ("RUNWARESPEECHINPUT", {
                    "tooltip": "Connect a Runware Speech Input node.",
                }),
            },
        }

    DESCRIPTION = "Combine multiple speech inputs to connect with Runware Video Inference Inputs."
    FUNCTION = "speechInputCombine"
    RETURN_TYPES = ("RUNWARESPEECHINPUT",)
    RETURN_NAMES = ("Speech Inputs",)
    CATEGORY = "Runware"

    def speechInputCombine(self, **kwargs):
        """Combine speech inputs into a list"""
        speechInputs = []
        
        for i in range(1, 5):
            speechKey = f"Speech Input {i}"
            speechInput = kwargs.get(speechKey)
            if speechInput is not None and isinstance(speechInput, dict) and len(speechInput) > 0:
                speechInputs.append(speechInput)
        
        return (speechInputs,)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareSpeechInputCombine": RunwareSpeechInputCombine,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareSpeechInputCombine": "Runware Speech Inputs Combine",
}

