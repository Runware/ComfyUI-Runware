"""
Runware Text Inference Tool Choice Node
Builds the toolChoice object for Runware Text Inference (textInference).

Strategies (type):
  - auto: model decides whether to call a tool (recommended default)
  - any:  model must call at least one tool but chooses which one
  - tool: model must call the specific tool identified by `name`
  - none: model will not call any tool
"""

from typing import Dict, Any


class RunwareTextInferenceToolChoice:
    """Runware Text Inference Tool Choice node."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "type": (["auto", "any", "tool", "none"], {
                    "default": "auto",
                    "tooltip": (
                        "Strategy the model uses to decide when and which tools to call.\n"
                        "- auto: model decides (recommended default).\n"
                        "- any:  model must call at least one tool, of its choosing.\n"
                        "- tool: model must call the specific tool named below.\n"
                        "- none: model will not call any tool."
                    ),
                }),
                "name": ("STRING", {
                    "default": "",
                    "tooltip": "Name of the specific tool the model must call. Required when type is 'tool'; ignored otherwise.",
                }),
            }
        }

    RETURN_TYPES = ("RUNWARETEXTINFERENCETOOLCHOICE",)
    RETURN_NAMES = ("toolChoice",)
    FUNCTION = "createToolChoice"
    CATEGORY = "Runware/Text"
    DESCRIPTION = (
        "Build a toolChoice object (type + optional tool name) and connect it to "
        "Runware Text Inference. Required when type is 'tool'."
    )

    def createToolChoice(self, **kwargs) -> tuple[Dict[str, Any]]:
        choice_type = (kwargs.get("type") or "auto").strip().lower()
        if choice_type not in ("auto", "any", "tool", "none"):
            choice_type = "auto"

        name = (kwargs.get("name") or "").strip()

        result: Dict[str, Any] = {"type": choice_type}
        if choice_type == "tool":
            if not name:
                raise Exception(
                    "Tool Choice: 'name' is required when type is 'tool'. "
                    "Provide the exact tool name the model must call."
                )
            result["name"] = name

        return (result,)


NODE_CLASS_MAPPINGS = {
    "RunwareTextInferenceToolChoice": RunwareTextInferenceToolChoice,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareTextInferenceToolChoice": "Runware Text Inference Tool Choice",
}
