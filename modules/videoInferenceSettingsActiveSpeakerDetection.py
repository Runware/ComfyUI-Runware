"""
Runware Video Inference Settings Active Speaker Detection
Exposes settings.activeSpeakerDetection fields for Sync models.
Connect optional boundingBoxes from the dedicated bounding-boxes node.
Connect the output to Runware Video Inference Settings -> activeSpeakerDetection.
"""

from typing import Dict, Any


class RunwareVideoInferenceSettingsActiveSpeakerDetection:
    """Optional settings.activeSpeakerDetection block for video inference (Sync)."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useAutoDetect": ("BOOLEAN", {
                    "tooltip": "Enable to include autoDetect in settings.activeSpeakerDetection.",
                    "default": False,
                }),
                "autoDetect": ("BOOLEAN", {
                    "tooltip": "Let Sync choose the active speaker automatically. Only used when 'Use Auto Detect' is enabled.",
                    "default": True,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useFrameNumber": ("BOOLEAN", {
                    "tooltip": "Enable to include frameNumber in settings.activeSpeakerDetection.",
                    "default": False,
                }),
                "frameNumber": ("INT", {
                    "tooltip": "Frame index corresponding to the provided face coordinates. Only used when 'Use Frame Number' is enabled.",
                    "default": 0,
                    "min": 0,
                    "max": 1000000,
                    "step": 1,
                }),
                "useCoordinates": ("BOOLEAN", {
                    "tooltip": "Enable to include coordinates ([x, y]) in settings.activeSpeakerDetection.",
                    "default": False,
                }),
                "coordinateX": ("FLOAT", {
                    "tooltip": "X point on the target speaker face for the selected frame. Must be an integer in range 1-4096. Only used when 'Use Coordinates' is enabled.",
                    "default": 512.0,
                    "min": 1.0,
                    "max": 4096.0,
                    "step": 1.0,
                }),
                "coordinateY": ("FLOAT", {
                    "tooltip": "Y point on the target speaker face for the selected frame. Must be an integer in range 1-4096. Only used when 'Use Coordinates' is enabled.",
                    "default": 512.0,
                    "min": 1.0,
                    "max": 4096.0,
                    "step": 1.0,
                }),
                "boundingBoxes": ("RUNWAREVIDEOINFERENCESETTINGSACTIVESPEAKERBOUNDINGBOXES", {
                    "tooltip": "Connect Runware Video Inference Settings Active Speaker Bounding Boxes (up to 4 elements).",
                }),
            },
        }

    RETURN_TYPES = ("RUNWAREVIDEOINFERENCESETTINGSACTIVESPEAKERDETECTION",)
    RETURN_NAMES = ("activeSpeakerDetection",)
    FUNCTION = "create"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Configure settings.activeSpeakerDetection (autoDetect, frameNumber, coordinates, boundingBoxes) "
        "for Runware Video Inference. Connect to Runware Video Inference Settings -> activeSpeakerDetection (Sync)."
    )

    def create(self, **kwargs) -> tuple[Dict[str, Any]]:
        active_speaker: Dict[str, Any] = {}
        if kwargs.get("useAutoDetect", False):
            active_speaker["autoDetect"] = bool(kwargs.get("autoDetect", True))
        if kwargs.get("useFrameNumber", False):
            active_speaker["frameNumber"] = int(kwargs.get("frameNumber", 0))
        if kwargs.get("useCoordinates", False):
            x = int(round(float(kwargs.get("coordinateX", 512.0))))
            y = int(round(float(kwargs.get("coordinateY", 512.0))))
            x = max(1, min(4096, x))
            y = max(1, min(4096, y))
            active_speaker["coordinates"] = [x, y]
        bounding_boxes = kwargs.get("boundingBoxes", None)
        if isinstance(bounding_boxes, list) and len(bounding_boxes) > 0:
            active_speaker["boundingBoxes"] = bounding_boxes[:4]
        return (active_speaker,)


NODE_CLASS_MAPPINGS = {
    "RunwareVideoInferenceSettingsActiveSpeakerDetection": RunwareVideoInferenceSettingsActiveSpeakerDetection,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVideoInferenceSettingsActiveSpeakerDetection": "Runware Video Inference Settings Active Speaker Detection",
}
