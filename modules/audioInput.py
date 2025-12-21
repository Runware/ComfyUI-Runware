"""
Runware Audio Input Node
Creates an audio input configuration with id and source
"""

from typing import Optional, Dict, Any


class RunwareAudioInput:
    """Runware Audio Input Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "source": ("STRING", {
                    "tooltip": "URL, base64, data URI, or UUID for the audio file. Audio formats: WAV, MP3, OGG, M4A, M3A, AAC, WMA, FLAC, MP4. Recommended: WAV/MP3 at 44.1kHz or 48kHz sampling rate.",
                    "default": "",
                }),
            },
            "optional": {
                "useId": ("BOOLEAN", {
                    "tooltip": "Enable to include reference ID for mapping audio input. Required when using segments array.",
                    "default": False,
                }),
                "id": ("STRING", {
                    "tooltip": "Reference ID used to map audio input. Required when using segments array.",
                    "default": "",
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREAUDIOINPUT",)
    RETURN_NAMES = ("Audio Input",)
    FUNCTION = "createAudioInput"
    CATEGORY = "Runware"
    DESCRIPTION = "Create an audio input configuration with reference ID and source for video generation."

    def createAudioInput(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create audio input configuration"""
        
        useId = kwargs.get("useId", False)
        audio_id = kwargs.get("id", "").strip()
        source = kwargs.get("source", "").strip()
        
        if not source:
            return ({},)
        
        audioInput: Dict[str, Any] = {
            "source": source,
        }
        
        # Only include id if useId is enabled and id is provided
        if useId and audio_id:
            audioInput["id"] = audio_id
        
        return (audioInput,)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareAudioInput": RunwareAudioInput,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareAudioInput": "Runware Video Audio Input",
}

