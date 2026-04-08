from .utils import runwareUtils as rwUtils
from typing import Dict, Any, List


class audioInferenceInputs:
    """Audio Inference Inputs node for configuring audio generation inputs"""
    
    MAX_VIDEOS = 4
    MAX_AUDIOS = 4
    
    @classmethod
    def INPUT_TYPES(cls):
        optionalInputs = {
            "useAudio": ("BOOLEAN", {
                "tooltip": "Enable to include single audio input in API request.",
                "default": False,
            }),
            "Audio": ("STRING", {
                "tooltip": "Audio URL or mediaUUID for audio generation. Can be a direct URL or a mediaUUID from Runware Media Upload node. Only used when 'Use Audio' is enabled.",
                "default": "",
            }),
            "useVideo": ("BOOLEAN", {
                "tooltip": "Enable to include single video input in API request.",
                "default": False,
            }),
            "Video": ("STRING", {
                "tooltip": "Video URL or mediaUUID for audio generation. Can be a direct URL or a mediaUUID from Runware Media Upload node. Only used when 'Use Video' is enabled.",
                "default": "",
            }),
            "useVideos": ("BOOLEAN", {
                "tooltip": "Enable to include multiple videos input in API request.",
                "default": False,
            }),
        }
        
        # Add Video1, Video2, Video3, Video4 inputs
        for i in range(1, cls.MAX_VIDEOS + 1):
            ordinal = rwUtils.getOrdinal(i)
            optionalInputs[f"Video{i}"] = ("STRING", {
                "tooltip": f"Video URL or mediaUUID for the {ordinal} video. Only used when 'Use Videos' is enabled.",
                "default": "",
            })
        
        # Multiple audios last so the UI groups useAudios with Audio1…Audio4 (ComfyUI order = dict insertion order)
        optionalInputs["useAudios"] = ("BOOLEAN", {
            "tooltip": "Enable to include multiple audio inputs in API request (inputs.audios array).",
            "default": False,
        })
        for i in range(1, cls.MAX_AUDIOS + 1):
            ordinal = rwUtils.getOrdinal(i)
            optionalInputs[f"Audio{i}"] = ("STRING", {
                "tooltip": f"Audio URL or mediaUUID for the {ordinal} audio. Only used when 'Use Audios' is enabled.",
                "default": "",
            })
        
        return {
            "required": {},
            "optional": optionalInputs
        }

    DESCRIPTION = "Configure custom inputs for Runware Audio Inference, including optional single or multiple audio URL/mediaUUID (inputs.audio or inputs.audios), and single or multiple video inputs for audio extraction or generation."
    FUNCTION = "createInputs"
    RETURN_TYPES = ("RUNWAREAUDIOINFERENCEINPUTS",)
    RETURN_NAMES = ("Audio Inference Inputs",)
    CATEGORY = "Runware"

    def createInputs(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create audio inference inputs from provided parameters"""
        useAudio = kwargs.get("useAudio", False)
        audio = kwargs.get("Audio", None)
        useAudios = kwargs.get("useAudios", False)
        useVideo = kwargs.get("useVideo", False)
        video = kwargs.get("Video", None)
        useVideos = kwargs.get("useVideos", False)
        
        inputs = {}

        # Handle single audio (inputs.audio)
        if useAudio and audio is not None and audio.strip() != "":
            inputs["audio"] = audio.strip()

        # Handle multiple audios (inputs.audios as array)
        if useAudios:
            audioList = []
            for i in range(1, self.MAX_AUDIOS + 1):
                audioKey = f"Audio{i}"
                audioUrl = kwargs.get(audioKey)
                if audioUrl and audioUrl.strip() != "":
                    audioList.append(audioUrl.strip())

            if len(audioList) > 0:
                inputs["audios"] = audioList

        # Handle single video (inputs.video)
        if useVideo and video is not None and video.strip() != "":
            inputs["video"] = video.strip()
        
        # Handle multiple videos (inputs.videos as array)
        if useVideos:
            videoList = []
            for i in range(1, self.MAX_VIDEOS + 1):
                videoKey = f"Video{i}"
                videoUrl = kwargs.get(videoKey)
                if videoUrl and videoUrl.strip() != "":
                    videoList.append(videoUrl.strip())
            
            if len(videoList) > 0:
                inputs["videos"] = videoList
        
        return (inputs,)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareAudioInferenceInputs": audioInferenceInputs,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareAudioInferenceInputs": "Runware Audio Inference Inputs",
}

