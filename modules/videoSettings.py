"""
Runware Video Inference Settings Node
Provides settings (draft, audio, promptUpsampling, voiceDescription, etc.) for Runware Video Inference.
"""

from typing import Dict, Any


class RunwareVideoSettings:
    """Runware Video Inference Settings Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useDraft": ("BOOLEAN", {
                    "tooltip": "Enable to include draft (lower-quality preview mode) in video inference settings.",
                    "default": False,
                }),
                "draft": ("BOOLEAN", {
                    "tooltip": "Draft mode for lower-quality preview. Only used when 'Use Draft' is enabled.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useAudio": ("BOOLEAN", {
                    "tooltip": "Enable to include audio (save video with audio) in video inference settings.",
                    "default": True,
                }),
                "audio": ("BOOLEAN", {
                    "tooltip": "Save the video with audio. Only used when 'Use Audio' is enabled.",
                    "default": True,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "usePromptUpsampling": ("BOOLEAN", {
                    "tooltip": "Enable to include promptUpsampling (enhance prompt automatically) in video inference settings.",
                    "default": True,
                }),
                "promptUpsampling": ("BOOLEAN", {
                    "tooltip": "Enhance prompt automatically for better results. Only used when 'Use Prompt Upsampling' is enabled.",
                    "default": True,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useBackgroundColor": ("BOOLEAN", {
                    "tooltip": "Enable to set background color. Required when background.type = color.",
                    "default": False,
                }),
                "backgroundColor": ("STRING", {
                    "tooltip": "Hex color code (e.g. #ff0000). Required when background.type = color. Only used when 'Use Background Color' is enabled.",
                    "default": "",
                }),
                "useRemoveBackground": ("BOOLEAN", {
                    "tooltip": "Enable to remove the avatar background. Video avatars must be trained with matting enabled.",
                    "default": False,
                }),
                "removeBackground": ("BOOLEAN", {
                    "tooltip": "Remove the avatar background. Only used when 'Use Remove Background' is enabled.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useExpressiveness": ("BOOLEAN", {
                    "tooltip": "Enable to set avatar expressiveness level. Applies to photo avatars only.",
                    "default": False,
                }),
                "expressiveness": (["low", "medium", "high"], {
                    "tooltip": "Avatar expressiveness level. Applies to photo avatars only. Only used when 'Use Expressiveness' is enabled.",
                    "default": "low",
                }),
                "useVoiceDescription": ("BOOLEAN", {
                    "tooltip": "Enable to include voiceDescription in video inference settings.",
                    "default": False,
                }),
                "voiceDescription": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Voice description text (max 10000 characters). Not supported when inputs.audio is given.",
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREVIDEOSETTINGS",)
    RETURN_NAMES = ("settings",)
    FUNCTION = "createSettings"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Configure video inference settings (draft, audio, promptUpsampling, voiceDescription, etc.) for Runware Video Inference. "
        "Connect to Runware Video Inference node."
    )

    def createSettings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create settings dict for Video Inference API"""
        use_draft = kwargs.get("useDraft", False)
        draft = kwargs.get("draft", False)
        use_audio = kwargs.get("useAudio", True)
        audio = kwargs.get("audio", True)
        use_prompt_upsampling = kwargs.get("usePromptUpsampling", True)
        prompt_upsampling = kwargs.get("promptUpsampling", True)
        use_background_color = kwargs.get("useBackgroundColor", False)
        background_color = (kwargs.get("backgroundColor") or "").strip()
        use_remove_background = kwargs.get("useRemoveBackground", False)
        remove_background = kwargs.get("removeBackground", False)
        use_expressiveness = kwargs.get("useExpressiveness", False)
        expressiveness = kwargs.get("expressiveness", "low")
        use_voice_description = kwargs.get("useVoiceDescription", False)
        voice_description = (kwargs.get("voiceDescription") or "").strip()

        settings: Dict[str, Any] = {}

        if use_draft:
            settings["draft"] = bool(draft)
        if use_audio:
            settings["audio"] = bool(audio)
        if use_prompt_upsampling:
            settings["promptUpsampling"] = bool(prompt_upsampling)
        if use_background_color and background_color:
            settings["backgroundColor"] = background_color
        if use_remove_background:
            settings["removeBackground"] = bool(remove_background)
        if use_expressiveness:
            settings["expressiveness"] = expressiveness
        if use_voice_description and voice_description:
            settings["voiceDescription"] = voice_description

        return (settings,)


NODE_CLASS_MAPPINGS = {
    "RunwareVideoSettings": RunwareVideoSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVideoSettings": "Runware Video Inference Settings",
}
