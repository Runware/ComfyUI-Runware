class RunwareTextInferenceMessage:
    """One chat message (role + content) for Runware Text Inference Messages combiner."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "role": (["user", "assistant"], {
                    "default": "user",
                    "tooltip": "Speaker role for this message.",
                }),
                "content": ("STRING", {
                    "multiline": True,
                    "default": "What's Photosynthesis?",
                    "tooltip": "Message text sent to the model.",
                }),
            }
        }

    RETURN_TYPES = ("RUNWARETEXTINFERENCEMESSAGE",)
    RETURN_NAMES = ("message",)
    FUNCTION = "create_message"
    CATEGORY = "Runware/Text"
    DESCRIPTION = (
        "One chat message (role + content). Connect to Runware Text Inference Messages."
    )

    def create_message(self, role: str, content: str):
        r = (role or "user").strip().lower()
        if r not in ("user", "assistant"):
            r = "user"
        body = (content or "").strip()
        return ({"role": r, "content": body},)
