"""
Runware Speech Input Node
Creates a speech input configuration with TTS provider settings
"""

from typing import Optional, Dict, Any


class RunwareSpeechInput:
    """Runware Speech Input Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "id": ("STRING", {
                    "tooltip": "Reference ID used to map speech input. Required when using segments array.",
                    "default": "",
                }),
                "provider": ("STRING", {
                    "tooltip": "TTS provider name. Currently supports: elevenlabs",
                    "default": "elevenlabs",
                }),
                "voiceId": ("STRING", {
                    "tooltip": "ElevenLabs voice ID for text-to-speech generation",
                    "default": "",
                }),
                "text": ("STRING", {
                    "multiline": True,
                    "tooltip": "The text script to be spoken",
                    "default": "",
                }),
            },
            "optional": {}
        }

    RETURN_TYPES = ("RUNWARESPEECHINPUT",)
    RETURN_NAMES = ("Speech Input",)
    FUNCTION = "createSpeechInput"
    CATEGORY = "Runware"
    DESCRIPTION = "Create a speech input configuration with TTS provider settings for video generation."

    def createSpeechInput(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create speech input configuration"""
        
        speech_id = kwargs.get("id", "").strip()
        provider = kwargs.get("provider", "elevenlabs").strip()
        voiceId = kwargs.get("voiceId", "").strip()
        text = kwargs.get("text", "").strip()
        
        if not speech_id or not provider or not voiceId or not text:
            return ({},)
        
        speechInput: Dict[str, Any] = {
            "id": speech_id,
            "provider": provider,
            "voiceId": voiceId,
            "text": text,
        }
        
        return (speechInput,)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareSpeechInput": RunwareSpeechInput,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareSpeechInput": "Runware Video Speech Input",
}

