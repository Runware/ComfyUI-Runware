"""
Runware Kling MultiPrompt Segment Node
Creates a single prompt/duration entry for Kling multiPrompt provider settings
"""

from typing import Dict, Any


class RunwareKlingMultiPromptSegment:
    """Runware Kling MultiPrompt Segment Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Prompt for this segment of the video",
                }),
                "duration": ("INT", {
                    "default": 4,
                    "min": 1,
                    "max": 30,
                    "step": 1,
                    "tooltip": "Duration in seconds for this segment",
                }),
            },
        }

    RETURN_TYPES = ("RUNWAREKLINGMULTIPROMPTSEGMENT",)
    RETURN_NAMES = ("MultiPrompt Segment",)
    FUNCTION = "createSegment"
    CATEGORY = "Runware/Provider Settings"
    DESCRIPTION = "Create a prompt/duration segment for Kling multiPrompt. Connect multiple segments to Runware Kling Provider Settings MultiPrompt."

    def createSegment(self, prompt: str, duration: int) -> tuple[Dict[str, Any]]:
        return ({"prompt": prompt.strip(), "duration": int(duration)},)


NODE_CLASS_MAPPINGS = {
    "RunwareKlingMultiPromptSegment": RunwareKlingMultiPromptSegment,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareKlingMultiPromptSegment": "Runware Kling MultiPrompt Segment",
}
