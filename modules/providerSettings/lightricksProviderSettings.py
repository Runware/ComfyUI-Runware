"""
Runware Lightricks Provider Settings Node
Provides Lightricks-specific settings for video generation
"""

from typing import Optional, Dict, Any

class RunwareLightricksProviderSettings:
    """Runware Lightricks Provider Settings Node"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                
                "useGenerateAudio": ("BOOLEAN", {
                    "tooltip": "Enable to override the audio generation flag. Disable to keep the default behavior.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "generateAudio": ("BOOLEAN", {
                    "tooltip": "Enable to generate audio for the video. Disable to generate video without audio. Default: false.",
                    "default": False,
                }),
                "useStartTime": ("BOOLEAN", {
                    "tooltip": "Enable to include a custom start time for the replacement segment.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "startTime": ("INT", {
                    "tooltip": "Start time (seconds) where the replacement should begin.",
                    "default": 0,
                    "min": 0,
                }),
                "useDuration": ("BOOLEAN", {
                    "tooltip": "Enable to include a custom duration for the replacement segment.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "duration": ("INT", {
                    "tooltip": "Duration (seconds) for the replacement segment.",
                    "default": 5,
                    "min": 1,
                }),
                "useMode": ("BOOLEAN", {
                    "tooltip": "Enable to select what parts of the video should be replaced.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Default",
                }),
                "mode": (["replace_audio", "replace_video", "replace_audio_and_video"], {
                    "tooltip": "Choose what to replace in the video task.",
                    "default": "replace_audio",
                }),
            }
        }
    
    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("providerSettings",)
    FUNCTION = "create_provider_settings"
    CATEGORY = "Runware/Provider Settings"
    
    def create_provider_settings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create Lightricks provider settings"""
        
        # Get value parameters
        generateAudio = kwargs.get("generateAudio", False)
        useStartTime = kwargs.get("useStartTime", False)
        useDuration = kwargs.get("useDuration", False)
        useMode = kwargs.get("useMode", False)
        useGenerateAudio = kwargs.get("useGenerateAudio", False)
        startTime = kwargs.get("startTime", 0)
        duration = kwargs.get("duration", 5)
        mode = kwargs.get("mode", "replace_audio")
        
        # Build settings dictionary
        # Always include generateAudio to ensure it's explicitly set
        settings = {}
        if useGenerateAudio:
            settings["generateAudio"] = generateAudio
        if useStartTime:
            settings["startTime"] = startTime
        if useDuration:
            settings["duration"] = duration
        if useMode:
            settings["mode"] = mode
        
        return (settings,)

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareLightricksProviderSettings": RunwareLightricksProviderSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareLightricksProviderSettings": "Runware Lightricks Provider Settings",
}

