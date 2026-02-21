"""
Runware Audio Inference Settings Voice Modify node.
Outputs settings.voiceModify (pitch, intensity, timbre, soundEffects) for Runware Audio Inference.
"""

from typing import Dict, Any

SOUND_EFFECTS = ["", "spacious_echo", "auditorium_echo", "lofi_telephone", "robotic"]


class RunwareAudioSettingsVoiceModify:
    """Runware Audio Inference Settings Voice Modify – pitch, intensity, timbre, sound effects."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "usePitch": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Include pitch in voice modification",
                }),
                "pitch": ("INT", {
                    "default": 0,
                    "min": -100,
                    "max": 100,
                    "step": 1,
                    "tooltip": "Voice pitch modification (settings.voiceModify.pitch)",
                }),
                "useIntensity": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Include intensity in voice modification",
                }),
                "intensity": ("INT", {
                    "default": 0,
                    "min": -100,
                    "max": 100,
                    "step": 1,
                    "tooltip": "Voice intensity modification (settings.voiceModify.intensity)",
                }),
                "useTimbre": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Include timbre in voice modification",
                }),
                "timbre": ("INT", {
                    "default": 0,
                    "min": -100,
                    "max": 100,
                    "step": 1,
                    "tooltip": "Voice timbre modification (settings.voiceModify.timbre)",
                }),
                "useSoundEffects": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Include sound effect in voice modification",
                }),
                "soundEffects": (SOUND_EFFECTS, {
                    "default": "",
                    "tooltip": "Sound effect: spacious_echo, auditorium_echo, lofi_telephone, robotic",
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREVOICEMODIFY",)
    RETURN_NAMES = ("voiceModify",)
    FUNCTION = "createVoiceModify"
    CATEGORY = "Runware/Audio"
    DESCRIPTION = "Voice modification settings (pitch, intensity, timbre, sound effects). Connect to Runware Audio Inference voiceModify input."

    def createVoiceModify(self, **kwargs) -> tuple:
        """Build voiceModify dict for settings.voiceModify. Only includes keys when the corresponding use toggle is on."""
        use_pitch = kwargs.get("usePitch", False)
        pitch = kwargs.get("pitch", 0)
        use_intensity = kwargs.get("useIntensity", False)
        intensity = kwargs.get("intensity", 0)
        use_timbre = kwargs.get("useTimbre", False)
        timbre = kwargs.get("timbre", 0)
        use_sound_effects = kwargs.get("useSoundEffects", False)
        sound_effects = (kwargs.get("soundEffects") or "").strip()

        voice_modify: Dict[str, Any] = {}
        if use_pitch:
            voice_modify["pitch"] = pitch
        if use_intensity:
            voice_modify["intensity"] = intensity
        if use_timbre:
            voice_modify["timbre"] = timbre
        if use_sound_effects and sound_effects:
            voice_modify["soundEffects"] = sound_effects
        return (voice_modify,)


NODE_CLASS_MAPPINGS = {
    "RunwareAudioSettingsVoiceModify": RunwareAudioSettingsVoiceModify,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareAudioSettingsVoiceModify": "Runware Audio Inference Settings Voice Modify",
}
