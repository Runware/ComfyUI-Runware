"""
Runware Video Inference Settings Segments
Builds settings.segments[] for Sync models.
Each segment can include startTime, endTime, audio, and optional audio crop range.
"""

from typing import Any


class RunwareVideoInferenceSettingsSegments:
    """Optional settings.segments[] block for video inference (Sync)."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useSegment1": ("BOOLEAN", {"default": False, "tooltip": "Enable segment 1."}),
                "segment1StartTime": ("FLOAT", {"default": 0.0, "step": 0.01, "tooltip": "Segment 1 start time in seconds."}),
                "segment1EndTime": ("FLOAT", {"default": 1.0, "step": 0.01, "tooltip": "Segment 1 end time in seconds."}),
                "segment1Audio": ("STRING", {"default": "", "tooltip": "Segment 1 audio mediaUUID. Connect from Runware Media Upload output."}),
                "useSegment1AudioCrop": ("BOOLEAN", {"default": False, "tooltip": "Enable audioStartTime/audioEndTime for segment 1."}),
                "segment1AudioStartTime": ("FLOAT", {"default": 0.0, "step": 0.01, "tooltip": "Segment 1 audio crop start time in seconds."}),
                "segment1AudioEndTime": ("FLOAT", {"default": 0.0, "step": 0.01, "tooltip": "Segment 1 audio crop end time in seconds."}),

                "useSegment2": ("BOOLEAN", {"default": False, "tooltip": "Enable segment 2."}),
                "segment2StartTime": ("FLOAT", {"default": 0.0, "step": 0.01, "tooltip": "Segment 2 start time in seconds."}),
                "segment2EndTime": ("FLOAT", {"default": 1.0, "step": 0.01, "tooltip": "Segment 2 end time in seconds."}),
                "segment2Audio": ("STRING", {"default": "", "tooltip": "Segment 2 audio mediaUUID. Connect from Runware Media Upload output."}),
                "useSegment2AudioCrop": ("BOOLEAN", {"default": False, "tooltip": "Enable audioStartTime/audioEndTime for segment 2."}),
                "segment2AudioStartTime": ("FLOAT", {"default": 0.0, "step": 0.01, "tooltip": "Segment 2 audio crop start time in seconds."}),
                "segment2AudioEndTime": ("FLOAT", {"default": 0.0, "step": 0.01, "tooltip": "Segment 2 audio crop end time in seconds."}),

                "useSegment3": ("BOOLEAN", {"default": False, "tooltip": "Enable segment 3."}),
                "segment3StartTime": ("FLOAT", {"default": 0.0, "step": 0.01, "tooltip": "Segment 3 start time in seconds."}),
                "segment3EndTime": ("FLOAT", {"default": 1.0, "step": 0.01, "tooltip": "Segment 3 end time in seconds."}),
                "segment3Audio": ("STRING", {"default": "", "tooltip": "Segment 3 audio mediaUUID. Connect from Runware Media Upload output."}),
                "useSegment3AudioCrop": ("BOOLEAN", {"default": False, "tooltip": "Enable audioStartTime/audioEndTime for segment 3."}),
                "segment3AudioStartTime": ("FLOAT", {"default": 0.0, "step": 0.01, "tooltip": "Segment 3 audio crop start time in seconds."}),
                "segment3AudioEndTime": ("FLOAT", {"default": 0.0, "step": 0.01, "tooltip": "Segment 3 audio crop end time in seconds."}),

                "useSegment4": ("BOOLEAN", {"default": False, "tooltip": "Enable segment 4."}),
                "segment4StartTime": ("FLOAT", {"default": 0.0, "step": 0.01, "tooltip": "Segment 4 start time in seconds."}),
                "segment4EndTime": ("FLOAT", {"default": 1.0, "step": 0.01, "tooltip": "Segment 4 end time in seconds."}),
                "segment4Audio": ("STRING", {"default": "", "tooltip": "Segment 4 audio mediaUUID. Connect from Runware Media Upload output."}),
                "useSegment4AudioCrop": ("BOOLEAN", {"default": False, "tooltip": "Enable audioStartTime/audioEndTime for segment 4."}),
                "segment4AudioStartTime": ("FLOAT", {"default": 0.0, "step": 0.01, "tooltip": "Segment 4 audio crop start time in seconds."}),
                "segment4AudioEndTime": ("FLOAT", {"default": 0.0, "step": 0.01, "tooltip": "Segment 4 audio crop end time in seconds."}),
            },
        }

    RETURN_TYPES = ("RUNWAREVIDEOINFERENCESETTINGSSEGMENTS",)
    RETURN_NAMES = ("segments",)
    FUNCTION = "create"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Configure settings.segments[] for Runware Video Inference (Sync). "
        "Each enabled segment includes startTime, endTime, audio and optional audioStartTime/audioEndTime."
    )

    def _build_segment(self, kwargs: dict[str, Any], idx: int) -> dict[str, Any]:
        start = float(kwargs.get(f"segment{idx}StartTime", 0.0))
        end = float(kwargs.get(f"segment{idx}EndTime", 1.0))
        audio = (kwargs.get(f"segment{idx}Audio", "") or "").strip()

        if audio == "":
            raise ValueError(f"segment{idx}Audio is required when segment {idx} is enabled.")
        if end < start:
            raise ValueError(f"segment{idx}EndTime must be >= segment{idx}StartTime.")

        segment: dict[str, Any] = {
            "startTime": start,
            "endTime": end,
            "audio": audio,
        }

        if kwargs.get(f"useSegment{idx}AudioCrop", False):
            astart = float(kwargs.get(f"segment{idx}AudioStartTime", 0.0))
            aend = float(kwargs.get(f"segment{idx}AudioEndTime", 0.0))
            if aend < astart:
                raise ValueError(f"segment{idx}AudioEndTime must be >= segment{idx}AudioStartTime.")
            segment["audioStartTime"] = astart
            segment["audioEndTime"] = aend

        return segment

    def create(self, **kwargs) -> tuple[list]:
        segments: list[dict[str, Any]] = []
        for idx in (1, 2, 3, 4):
            if kwargs.get(f"useSegment{idx}", False):
                segments.append(self._build_segment(kwargs, idx))
        return (segments,)


NODE_CLASS_MAPPINGS = {
    "RunwareVideoInferenceSettingsSegments": RunwareVideoInferenceSettingsSegments,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVideoInferenceSettingsSegments": "Runware Video Inference Settings Segments",
}
