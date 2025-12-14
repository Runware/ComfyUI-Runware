"""
Runware Sync Provider Settings Node
Provides Sync-specific settings for video generation with lip-sync capabilities
"""

from typing import Optional, Dict, Any, List


class RunwareSyncProviderSettings:
    """Runware Sync Provider Settings Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "syncMode": (["bounce", "loop", "cut_off", "silence", "remap"], {
                    "tooltip": "Synchronization strategy. Enum: bounce, loop, cut_off, silence, remap",
                    "default": "bounce",
                }),
            },
            "optional": {
                "useEditRegion": ("BOOLEAN", {
                    "tooltip": "Enable to include editRegion parameter",
                    "default": False,
                }),
                "editRegion": (["lips", "face", "head"], {
                    "tooltip": "Edit region for the model. Only works with react-1. Defaults to face, which affects lipsync + emotions in the face region. When head is selected, model generates natural talking head movements along with emotions + lipsync. Only used when 'Use Edit Region' is enabled.",
                    "default": "face",
                }),
                "useEmotionPrompt": ("BOOLEAN", {
                    "tooltip": "Enable to include emotionPrompt parameter",
                    "default": False,
                }),
                "emotionPrompt": (["happy", "sad", "angry", "disgusted", "surprised", "neutral"], {
                    "tooltip": "Emotion prompt for the generation. Only works for react-1 model. Only single word emotions are supported. Only used when 'Use Emotion Prompt' is enabled.",
                    "default": "happy",
                }),
                "useTemperature": ("BOOLEAN", {
                    "tooltip": "Enable to include temperature parameter",
                    "default": False,
                }),
                "temperature": ("FLOAT", {
                    "tooltip": "Sampling temperature. 0 -> least expressive, 1 -> most expressive. Only used when 'Use Temperature' is enabled.",
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                }),
                "useActiveSpeakerDetection": ("BOOLEAN", {
                    "tooltip": "Enable to include activeSpeakerDetection parameter",
                    "default": False,
                }),
                "activeSpeakerDetection": ("BOOLEAN", {
                    "tooltip": "Enable active speaker detection. Only used when 'Use Active Speaker Detection' is enabled.",
                    "default": True,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useOcclusionDetectionEnabled": ("BOOLEAN", {
                    "tooltip": "Enable to include occlusionDetectionEnabled parameter",
                    "default": False,
                }),
                "occlusionDetectionEnabled": ("BOOLEAN", {
                    "tooltip": "Enable occlusion detection. Only used when 'Use Occlusion Detection Enabled' is enabled.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "Sync Segment 1": ("RUNWARESYNCSEGMENT", {
                    "tooltip": "Connect a Runware Sync Segment node (optional)",
                }),
                "Sync Segment 2": ("RUNWARESYNCSEGMENT", {
                    "tooltip": "Connect a Runware Sync Segment node (optional)",
                }),
                "Sync Segment 3": ("RUNWARESYNCSEGMENT", {
                    "tooltip": "Connect a Runware Sync Segment node (optional)",
                }),
                "Sync Segment 4": ("RUNWARESYNCSEGMENT", {
                    "tooltip": "Connect a Runware Sync Segment node (optional)",
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("Provider Settings",)
    FUNCTION = "createProviderSettings"
    CATEGORY = "Runware/Provider Settings"
    DESCRIPTION = "Configure Sync-specific provider settings for video generation including lip-sync, emotion prompts, and segment configurations."

    def createProviderSettings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create Sync provider settings"""

        # Get required parameters
        syncMode = kwargs.get("syncMode", "bounce")

        # Get control parameters
        useEditRegion = kwargs.get("useEditRegion", False)
        useEmotionPrompt = kwargs.get("useEmotionPrompt", False)
        useTemperature = kwargs.get("useTemperature", False)
        useActiveSpeakerDetection = kwargs.get("useActiveSpeakerDetection", False)
        useOcclusionDetectionEnabled = kwargs.get("useOcclusionDetectionEnabled", False)

        # Get value parameters
        editRegion = kwargs.get("editRegion", "face")
        emotionPrompt = kwargs.get("emotionPrompt", "happy")
        temperature = kwargs.get("temperature", 0.5)
        activeSpeakerDetection = kwargs.get("activeSpeakerDetection", True)
        occlusionDetectionEnabled = kwargs.get("occlusionDetectionEnabled", False)

        # Get sync segments (up to 4)
        segments: List[Dict[str, Any]] = []
        for i in range(1, 5):
            segmentKey = f"Sync Segment {i}"
            segment = kwargs.get(segmentKey)
            if segment is not None and isinstance(segment, dict):
                segments.append(segment)

        # Build settings dictionary
        syncSettings: Dict[str, Any] = {
            "syncMode": syncMode,
        }

        # Add optional parameters only if enabled
        if useEditRegion:
            syncSettings["editRegion"] = editRegion
        if useEmotionPrompt:
            syncSettings["emotionPrompt"] = emotionPrompt
        if useTemperature:
            syncSettings["temperature"] = float(temperature)
        if useActiveSpeakerDetection:
            syncSettings["activeSpeakerDetection"] = activeSpeakerDetection
        if useOcclusionDetectionEnabled:
            syncSettings["occlusionDetectionEnabled"] = occlusionDetectionEnabled

        # Add segments if any are provided
        if segments:
            syncSettings["segments"] = segments

        # Clean up None values
        syncSettings = {k: v for k, v in syncSettings.items() if v is not None}

        # Return settings wrapped with provider key "sync"
        if syncSettings:
            return ({"sync": syncSettings},)
        else:
            return ({},)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareSyncProviderSettings": RunwareSyncProviderSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareSyncProviderSettings": "Runware Sync Provider Settings",
}

