"""
Runware Video Inference Settings Node
Provides settings (draft, audio, voicePrompt, safetyFilter, promptUpsampling, voiceDescription, style, thinking, multiClip, shotType, promptExtend, syncMode, mode, emotion, temperature, occlusionDetection, tts, activeSpeakerDetection, segments, etc.) for Runware Video Inference.
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
                    "default": False,
                }),
                "audio": ("BOOLEAN", {
                    "tooltip": "Save the video with audio. Only used when 'Use Audio' is enabled.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useSafetyFilter": ("BOOLEAN", {
                    "tooltip": "Enable to include safetyFilter in video inference settings.",
                    "default": False,
                }),
                "safetyFilter": ("BOOLEAN", {
                    "tooltip": "When false, enables safety filtering on prompts and input images. Only used when 'Use Safety Filter' is enabled.",
                    "default": True,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "usePromptUpsampling": ("BOOLEAN", {
                    "tooltip": "Enable to include promptUpsampling (enhance prompt automatically) in video inference settings.",
                    "default": False,
                }),
                "promptUpsampling": ("BOOLEAN", {
                    "tooltip": "Enhance prompt automatically for better results. Only used when 'Use Prompt Upsampling' is enabled.",
                    "default": False,
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
                "useStyle": ("BOOLEAN", {
                    "tooltip": "Enable to include style (visual style of the video) in video inference settings.",
                    "default": False,
                }),
                "style": (["anime", "3d_animation", "clay", "comic", "cyberpunk"], {
                    "tooltip": "Visual style of the video. Only used when 'Use Style' is enabled.",
                    "default": "anime",
                }),
                "useThinking": ("BOOLEAN", {
                    "tooltip": "Enable to include thinking in video inference settings.",
                    "default": False,
                }),
                "thinking": (["enabled", "disabled", "auto"], {
                    "tooltip": "Thinking mode. Only used when 'Use Thinking' is enabled.",
                    "default": "auto",
                }),
                "useMultiClip": ("BOOLEAN", {
                    "tooltip": "Enable to include multiClip (multi-clip generation with dynamic camera changes; transition endpoint).",
                    "default": False,
                }),
                "multiClip": ("BOOLEAN", {
                    "tooltip": "Multi-clip generation with dynamic camera changes. Available on transition endpoint. Only used when 'Use Multi Clip' is enabled.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useShotType": ("BOOLEAN", {
                    "tooltip": "Enable to include shotType in video inference settings.",
                    "default": False,
                }),
                "shotType": (["single", "multi"], {
                    "tooltip": "Shot type: single (one continuous shot) or multi (multiple switching shots). Parameter priority: shot_type > prompt. Only used when 'Use Shot Type' is enabled.",
                    "default": "single",
                }),
                "usePromptExtend": ("BOOLEAN", {
                    "tooltip": "Enable to include promptExtend in video inference settings.",
                    "default": False,
                }),
                "promptExtend": ("BOOLEAN", {
                    "tooltip": "Prompt extend flag. Only used when 'Use Prompt Extend' is enabled.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useSyncMode": ("BOOLEAN", {
                    "tooltip": "Enable to include syncMode in video inference settings.",
                    "default": False,
                }),
                "syncMode": (["bounce", "cut_off", "silence", "remap"], {
                    "tooltip": "Controls how mismatched audio/video lengths are handled. Default provider behavior is usually cropping to shorter duration. Only used when 'Use Sync Mode' is enabled.",
                    "default": "cut_off",
                }),
                "tts": ("RUNWAREVIDEOINFERENCESETTINGSTTS", {
                    "tooltip": "Connect Runware Video Inference Settings TTS for settings.tts (stability, similarityBoost). Sync / ElevenLabs-style optional tuning.",
                }),
                "activeSpeakerDetection": ("RUNWAREVIDEOINFERENCESETTINGSACTIVESPEAKERDETECTION", {
                    "tooltip": "Connect Runware Video Inference Settings Active Speaker Detection for settings.activeSpeakerDetection (autoDetect, frameNumber, coordinates).",
                }),
                "useMode": ("BOOLEAN", {
                    "tooltip": "Enable to include mode in video inference settings.",
                    "default": False,
                }),
                "mode": (["lips", "face", "head"], {
                    "tooltip": "Sync processing mode. Only used when 'Use Mode' is enabled.",
                    "default": "lips",
                }),
                "useEmotion": ("BOOLEAN", {
                    "tooltip": "Enable to include emotion in video inference settings.",
                    "default": False,
                }),
                "emotion": (["happy", "sad", "angry", "disgusted", "surprised", "neutral"], {
                    "tooltip": "Target emotion for generation. Only used when 'Use Emotion' is enabled.",
                    "default": "neutral",
                }),
                "useTemperature": ("BOOLEAN", {
                    "tooltip": "Enable to include temperature in video inference settings.",
                    "default": False,
                }),
                "temperature": ("FLOAT", {
                    "tooltip": "Sampling temperature. Only used when 'Use Temperature' is enabled.",
                    "default": 0.7,
                    "min": 0.0,
                    "max": 5.0,
                    "step": 0.01,
                }),
                "useOcclusionDetection": ("BOOLEAN", {
                    "tooltip": "Enable to include occlusionDetection in video inference settings.",
                    "default": False,
                }),
                "occlusionDetection": ("BOOLEAN", {
                    "tooltip": "Enable occlusion detection. Only used when 'Use Occlusion Detection' is enabled.",
                    "default": False,
                    "label_on": "true",
                    "label_off": "false",
                }),
                "useKeyframeId": ("BOOLEAN", {
                    "tooltip": "Enable to include settings.keyframe.keyframe_id in video inference settings.",
                    "default": False,
                }),
                "keyframeId": ("INT", {
                    "tooltip": "Keyframe ID for settings.keyframe.keyframe_id. Only used when 'Use Keyframe ID' is enabled.",
                    "default": 0,
                    "min": 0,
                    "max": 2147483647,
                    "step": 1,
                }),
                "segments": ("RUNWAREVIDEOINFERENCESETTINGSSEGMENTS", {
                    "tooltip": "Connect Runware Video Inference Settings Segments for settings.segments[] (startTime, endTime, audio, audioStartTime, audioEndTime).",
                }),
                "useVoicePrompt": ("BOOLEAN", {
                    "tooltip": "Enable to include voicePrompt (delivery style instructions) in video inference settings.",
                    "default": False,
                }),
                "voicePrompt": ("STRING", {
                    "default": "Say the following.",
                    "multiline": True,
                    "tooltip": "Speaking style, tone, pacing or emotion instructions for delivery. Only used when 'Use Voice Prompt' is enabled.",
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREVIDEOSETTINGS",)
    RETURN_NAMES = ("settings",)
    FUNCTION = "createSettings"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Configure video inference settings (draft, audio, voicePrompt, safetyFilter, promptUpsampling, voiceDescription, style, thinking, multiClip, shotType, promptExtend, syncMode, mode, emotion, temperature, occlusionDetection, tts, activeSpeakerDetection, segments, etc.) for Runware Video Inference. "
        "Connect to Runware Video Inference node."
    )

    def createSettings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create settings dict for Video Inference API"""
        use_draft = kwargs.get("useDraft", False)
        draft = kwargs.get("draft", False)
        use_audio = kwargs.get("useAudio", False)
        audio = kwargs.get("audio", False)
        use_voice_prompt = kwargs.get("useVoicePrompt", False)
        voice_prompt = (kwargs.get("voicePrompt") or "").strip()
        use_safety_filter = kwargs.get("useSafetyFilter", False)
        safety_filter = kwargs.get("safetyFilter", True)
        use_prompt_upsampling = kwargs.get("usePromptUpsampling", False)
        prompt_upsampling = kwargs.get("promptUpsampling", False)
        use_background_color = kwargs.get("useBackgroundColor", False)
        background_color = (kwargs.get("backgroundColor") or "").strip()
        use_remove_background = kwargs.get("useRemoveBackground", False)
        remove_background = kwargs.get("removeBackground", False)
        use_expressiveness = kwargs.get("useExpressiveness", False)
        expressiveness = kwargs.get("expressiveness", "low")
        use_voice_description = kwargs.get("useVoiceDescription", False)
        voice_description = (kwargs.get("voiceDescription") or "").strip()
        use_style = kwargs.get("useStyle", False)
        style = kwargs.get("style", "anime")
        use_thinking = kwargs.get("useThinking", False)
        thinking = kwargs.get("thinking", "auto")
        use_multi_clip = kwargs.get("useMultiClip", False)
        multi_clip = kwargs.get("multiClip", False)
        use_shot_type = kwargs.get("useShotType", False)
        shot_type = kwargs.get("shotType", "single")
        use_prompt_extend = kwargs.get("usePromptExtend", False)
        prompt_extend = kwargs.get("promptExtend", False)
        use_sync_mode = kwargs.get("useSyncMode", False)
        sync_mode = kwargs.get("syncMode", "cut_off")
        tts_cfg = kwargs.get("tts", None)
        active_speaker_cfg = kwargs.get("activeSpeakerDetection", None)
        use_mode = kwargs.get("useMode", False)
        mode = kwargs.get("mode", "lips")
        use_emotion = kwargs.get("useEmotion", False)
        emotion = kwargs.get("emotion", "neutral")
        use_temperature = kwargs.get("useTemperature", False)
        temperature = kwargs.get("temperature", 0.7)
        use_occlusion_detection = kwargs.get("useOcclusionDetection", False)
        occlusion_detection = kwargs.get("occlusionDetection", False)
        use_keyframe_id = kwargs.get("useKeyframeId", False)
        keyframe_id = kwargs.get("keyframeId", 0)
        segments_cfg = kwargs.get("segments", None)

        settings: Dict[str, Any] = {}

        if use_draft:
            settings["draft"] = bool(draft)
        if use_audio:
            settings["audio"] = bool(audio)
        if use_voice_prompt and voice_prompt:
            settings["voicePrompt"] = voice_prompt
        if use_safety_filter:
            settings["safetyFilter"] = bool(safety_filter)
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
        if use_style:
            settings["style"] = style
        if use_thinking:
            settings["thinking"] = thinking
        if use_multi_clip:
            settings["multiClip"] = bool(multi_clip)
        if use_shot_type:
            settings["shotType"] = shot_type
        if use_prompt_extend:
            settings["promptExtend"] = bool(prompt_extend)
        if use_sync_mode:
            settings["syncMode"] = sync_mode
        if use_mode:
            settings["mode"] = mode
        if use_emotion:
            settings["emotion"] = emotion
        if use_temperature:
            settings["temperature"] = float(temperature)
        if use_occlusion_detection:
            settings["occlusionDetection"] = bool(occlusion_detection)
        if use_keyframe_id:
            settings["keyframe"] = int(keyframe_id)

        if tts_cfg is not None and isinstance(tts_cfg, dict) and len(tts_cfg) > 0:
            settings["tts"] = tts_cfg
        if active_speaker_cfg is not None and isinstance(active_speaker_cfg, dict) and len(active_speaker_cfg) > 0:
            settings["activeSpeakerDetection"] = active_speaker_cfg
        if segments_cfg is not None and isinstance(segments_cfg, list) and len(segments_cfg) > 0:
            settings["segments"] = segments_cfg

        return (settings,)


NODE_CLASS_MAPPINGS = {
    "RunwareVideoSettings": RunwareVideoSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVideoSettings": "Runware Video Inference Settings",
}
