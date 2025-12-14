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
                "id": ("STRING", {
                    "tooltip": "Reference ID used to map audio input. Required when using segments array.",
                    "default": "",
                }),
                "source": ("STRING", {
                    "tooltip": "URL, base64, data URI, or UUID for the audio file. Audio formats: WAV, MP3, OGG, M4A, M3A, AAC, WMA, FLAC, MP4. Recommended: WAV/MP3 at 44.1kHz or 48kHz sampling rate.",
                    "default": "",
                }),
            },
            "optional": {}
        }

    RETURN_TYPES = ("RUNWAREAUDIOINPUT",)
    RETURN_NAMES = ("Audio Input",)
    FUNCTION = "createAudioInput"
    CATEGORY = "Runware"
    DESCRIPTION = "Create an audio input configuration with reference ID and source for video generation."

    def createAudioInput(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create audio input configuration"""
        
        audio_id = kwargs.get("id", "").strip()
        source = kwargs.get("source", "").strip()
        
        if not audio_id or not source:
            return ({},)
        
        audioInput: Dict[str, Any] = {
            "id": audio_id,
            "source": source,
        }
        
        return (audioInput,)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareAudioInput": RunwareAudioInput,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareAudioInput": "Runware Video Audio Input",
}

