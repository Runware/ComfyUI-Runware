"""
Runware Video Inference Settings Active Speaker Bounding Boxes
Builds settings.activeSpeakerDetection.boundingBoxes for Sync models.
Each element is [x1, y1, x2, y2] or null. Up to 4 elements.
"""

from typing import Dict, Any


def _parse_box(raw: str, label: str):
    value = (raw or "").strip()
    if value == "" or value.lower() == "null":
        return None

    parts = [p.strip() for p in value.split(",")]
    if len(parts) != 4:
        raise ValueError(f"{label} must be 'x1,y1,x2,y2' or null.")

    try:
        return [float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3])]
    except ValueError as exc:
        raise ValueError(f"{label} values must be numbers.") from exc


class RunwareVideoInferenceSettingsActiveSpeakerBoundingBoxes:
    """Optional settings.activeSpeakerDetection.boundingBoxes block for Sync."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useBox1": ("BOOLEAN", {"tooltip": "Enable bounding box element 1.", "default": False}),
                "box1": ("STRING", {"tooltip": "Element 1 as 'x1,y1,x2,y2' or null.", "default": ""}),
                "useBox2": ("BOOLEAN", {"tooltip": "Enable bounding box element 2.", "default": False}),
                "box2": ("STRING", {"tooltip": "Element 2 as 'x1,y1,x2,y2' or null.", "default": ""}),
                "useBox3": ("BOOLEAN", {"tooltip": "Enable bounding box element 3.", "default": False}),
                "box3": ("STRING", {"tooltip": "Element 3 as 'x1,y1,x2,y2' or null.", "default": ""}),
                "useBox4": ("BOOLEAN", {"tooltip": "Enable bounding box element 4.", "default": False}),
                "box4": ("STRING", {"tooltip": "Element 4 as 'x1,y1,x2,y2' or null.", "default": ""}),
            },
        }

    RETURN_TYPES = ("RUNWAREVIDEOINFERENCESETTINGSACTIVESPEAKERBOUNDINGBOXES",)
    RETURN_NAMES = ("boundingBoxes",)
    FUNCTION = "create"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Configure settings.activeSpeakerDetection.boundingBoxes for Runware Video Inference. "
        "Supports up to 4 elements, each [x1, y1, x2, y2] or null."
    )

    def create(self, **kwargs) -> tuple[list]:
        boxes = []

        if kwargs.get("useBox1", False):
            boxes.append(_parse_box(kwargs.get("box1", ""), "box1"))
        if kwargs.get("useBox2", False):
            boxes.append(_parse_box(kwargs.get("box2", ""), "box2"))
        if kwargs.get("useBox3", False):
            boxes.append(_parse_box(kwargs.get("box3", ""), "box3"))
        if kwargs.get("useBox4", False):
            boxes.append(_parse_box(kwargs.get("box4", ""), "box4"))

        return (boxes[:4],)


NODE_CLASS_MAPPINGS = {
    "RunwareVideoInferenceSettingsActiveSpeakerBoundingBoxes": RunwareVideoInferenceSettingsActiveSpeakerBoundingBoxes,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVideoInferenceSettingsActiveSpeakerBoundingBoxes": "Runware Video Inference Settings Active Speaker Bounding Boxes",
}
