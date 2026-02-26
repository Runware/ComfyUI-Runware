"""
Runware Video Inference Settings Node
Provides settings (draft, audio, promptUpsampling) for Runware Video Inference.
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
            }
        }

    RETURN_TYPES = ("RUNWAREVIDEOSETTINGS",)
    RETURN_NAMES = ("settings",)
    FUNCTION = "createSettings"
    CATEGORY = "Runware"
    DESCRIPTION = "Configure video inference settings (draft, audio, promptUpsampling) for Runware Video Inference. Connect to Runware Video Inference node."

    def createSettings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create settings dict for Video Inference API"""
        use_draft = kwargs.get("useDraft", False)
        draft = kwargs.get("draft", False)
        use_audio = kwargs.get("useAudio", True)
        audio = kwargs.get("audio", True)
        use_prompt_upsampling = kwargs.get("usePromptUpsampling", True)
        prompt_upsampling = kwargs.get("promptUpsampling", True)

        settings: Dict[str, Any] = {}

        if use_draft:
            settings["draft"] = bool(draft)
        if use_audio:
            settings["audio"] = bool(audio)
        if use_prompt_upsampling:
            settings["promptUpsampling"] = bool(prompt_upsampling)

        return (settings,)


NODE_CLASS_MAPPINGS = {
    "RunwareVideoSettings": RunwareVideoSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVideoSettings": "Runware Video Inference Settings",
}
