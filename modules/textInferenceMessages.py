from typing import Dict, List


class RunwareTextInferenceMessages:
    """Merge Runware Text Inference Message segments into the API `messages` array (order = segment 1 … N)."""

    _SEGMENT_COUNT = 8

    @classmethod
    def INPUT_TYPES(cls):
        optional = {}
        for i in range(2, cls._SEGMENT_COUNT + 1):
            optional[f"Message Segment {i}"] = (
                "RUNWARETEXTINFERENCEMESSAGE",
                {"tooltip": f"Optional message {i}. Connect Runware Text Inference Message."},
            )
        return {
            "required": {
                "Message Segment 1": ("RUNWARETEXTINFERENCEMESSAGE", {
                    "tooltip": "First message. Connect Runware Text Inference Message.",
                }),
            },
            "optional": optional,
        }

    RETURN_TYPES = ("RUNWARETEXTINFERENCEMESSAGES",)
    RETURN_NAMES = ("messages",)
    FUNCTION = "merge_messages"
    CATEGORY = "Runware/Text"
    DESCRIPTION = (
        "Combine one or more Runware Text Inference Message nodes into a messages list for Runware Text Inference "
        "(same idea as Kling MultiPrompt Segment → Kling Provider Settings MultiPrompt)."
    )

    def merge_messages(self, **kwargs) -> tuple:
        messages: List[Dict[str, str]] = []

        for i in range(1, self._SEGMENT_COUNT + 1):
            key = f"Message Segment {i}"
            seg = kwargs.get(key)
            if seg is None:
                continue
            if not isinstance(seg, dict):
                continue
            content = (seg.get("content") or "").strip()
            if not content:
                continue
            role = seg.get("role", "user")
            if role not in ("user", "assistant"):
                role = "user"
            messages.append({"role": role, "content": content})

        if not messages:
            raise Exception(
                "No messages: connect Runware Text Inference Message to Message Segment 1 with non-empty content."
            )

        return (messages,)
