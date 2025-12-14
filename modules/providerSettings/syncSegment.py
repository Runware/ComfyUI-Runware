"""
Runware Sync Segment Node
Creates a sync segment configuration for sync provider settings
"""

from typing import Optional, Dict, Any


class RunwareSyncSegment:
    """Runware Sync Segment Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "startTime": ("FLOAT", {
                    "tooltip": "Start time of the segment in seconds",
                    "default": 0.0,
                    "min": 0.0,
                    "step": 0.1,
                }),
                "endTime": ("FLOAT", {
                    "tooltip": "End time of the segment in seconds",
                    "default": 1.0,
                    "min": 0.0,
                    "step": 0.1,
                }),
                "ref": ("STRING", {
                    "tooltip": "Reference identifier for the audio track (e.g., 'audio-track-1', 'speech-track-1')",
                    "default": "audio-track-1",
                }),
            },
            "optional": {
                "useAudioStartTime": ("BOOLEAN", {
                    "tooltip": "Enable to include audioStartTime parameter",
                    "default": False,
                }),
                "audioStartTime": ("FLOAT", {
                    "tooltip": "Start time in the audio track in seconds. Only used when 'Use Audio Start Time' is enabled.",
                    "default": 0.0,
                    "min": 0.0,
                    "step": 0.1,
                }),
                "useAudioEndTime": ("BOOLEAN", {
                    "tooltip": "Enable to include audioEndTime parameter",
                    "default": False,
                }),
                "audioEndTime": ("FLOAT", {
                    "tooltip": "End time in the audio track in seconds. Only used when 'Use Audio End Time' is enabled.",
                    "default": 1.0,
                    "min": 0.0,
                    "step": 0.1,
                }),
            }
        }

    RETURN_TYPES = ("RUNWARESYNCSEGMENT",)
    RETURN_NAMES = ("Sync Segment",)
    FUNCTION = "createSyncSegment"
    CATEGORY = "Runware/Provider Settings"
    DESCRIPTION = "Create a sync segment configuration for sync provider settings."

    def createSyncSegment(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create sync segment configuration"""
        
        # Get required parameters
        startTime = kwargs.get("startTime", 0.0)
        endTime = kwargs.get("endTime", 1.0)
        ref = kwargs.get("ref", "audio-track-1")
        
        # Get optional parameters
        useAudioStartTime = kwargs.get("useAudioStartTime", False)
        audioStartTime = kwargs.get("audioStartTime", 0.0)
        useAudioEndTime = kwargs.get("useAudioEndTime", False)
        audioEndTime = kwargs.get("audioEndTime", 1.0)
        
        # Build segment dictionary
        segment: Dict[str, Any] = {
            "startTime": float(startTime),
            "endTime": float(endTime),
            "ref": str(ref),
        }
        
        # Add optional audio timing parameters
        if useAudioStartTime:
            segment["audioStartTime"] = float(audioStartTime)
        if useAudioEndTime:
            segment["audioEndTime"] = float(audioEndTime)
        
        # Clean up None values
        segment = {k: v for k, v in segment.items() if v is not None}
        
        return (segment,)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareSyncSegment": RunwareSyncSegment,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareSyncSegment": "Runware Sync Segment",
}

