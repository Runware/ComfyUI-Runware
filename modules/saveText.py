from .utils import runwareUtils as rwUtils


class RunwareSaveText:
    """Show text in the node (e.g. from Runware Text Inference) and forward it for downstream nodes."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Connect the 'text' output from Runware Text Inference. Text is mirrored here after run.",
                }),
            },
            "hidden": {"node_id": "UNIQUE_ID"},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "forward_text"
    OUTPUT_NODE = True
    CATEGORY = "Runware"
    DESCRIPTION = "Display text in the node and forward the same string to other nodes."

    def forward_text(self, text, **kwargs):
        if text is None:
            text = ""
        elif not isinstance(text, str):
            text = str(text)

        node_id = kwargs.get("node_id")
        if node_id is not None:
            rwUtils.sendSaveText(text, node_id)

        return (text,)
