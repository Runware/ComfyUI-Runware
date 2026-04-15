from .utils import runwareUtils as rwUtils
from typing import List


class videoInferenceInputs:
    """Video Inference Inputs node for configuring video generation inputs"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "Image": ("IMAGE", {
                    "tooltip": "Portrait image for video generation (main subject that will speak and move). Mutually exclusive with Avatar: when Avatar is set, Image is ignored."
                }),
                "Avatar": ("STRING", {
                    "default": "",
                    "tooltip": "HeyGen avatar ID for a photo or video avatar. Mutually exclusive with Image: when set, Image is ignored; use one or the other.",
                }),
                "Frame Images": ("RUNWAREVIDEOINPUTSFRAMEIMAGES", {
                    "tooltip": "Connect the Runware Video Inputs Frame node to provide timeline-constrained frame images."
                }),
                "Audio": ("STRING", {
                    "tooltip": "Connect the mediaUUID output from Runware Media Upload node with audio file. This audio will be synchronized with the generated video. (Legacy: single audio string)"
                }),
                "Audio Inputs": ("RUNWAREAUDIOINPUT", {
                    "tooltip": "Connect Runware Video Audio Input node(s) to provide audio inputs with reference IDs."
                }),
                "Speech Inputs": ("RUNWARESPEECHINPUT", {
                    "tooltip": "Connect Runware Video Speech Input node or Runware Speech Inputs Combine node to provide TTS speech inputs with reference IDs."
                }),
                "Video": ("STRING", {
                    "tooltip": "Connect the mediaUUID output from Runware Media Upload node with a reference/input video."
                }),
                "Mask": ("IMAGE", {
                    "tooltip": "Mask image to specify a specific subject in the image to speak. Use white/black mask format."
                }),
                "Frame": ("IMAGE", {
                    "tooltip": "Frame image for video generation. Connect a Load Image node to provide the frame image."
                }),
                "Background": ("IMAGE", {
                    "tooltip": "Background image for video generation. Connect a Load Image node to provide the background.",
                }),
                "References Images": ("RUNWAREVIDEOINPUTSREFERENCEIMAGES", {
                    "tooltip": "Connect the Runware Video Inference Inputs Reference Images node to provide reference images."
                }),
                "Reference Videos": ("RUNWAREREFERENCEVIDEOS", {
                    "tooltip": "Connect the Runware Video Inference Inputs Reference Videos node to provide reference video mediaUUIDs."
                }),
                "Reference Audios": ("RUNWAREINPUTAUDIOS", {
                    "tooltip": "Connect the Runware Video Inference Inputs Reference Audios node to provide reference audio mediaUUIDs."
                }),
                "Reference Voices": ("RUNWAREREFERENCEVOICES", {
                    "tooltip": "Connect the Runware Video Inference Inputs Reference Voices node to provide reference voice URLs or mediaUUIDs."
                }),
                "draftId": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "Draft ID from a previous Bytedance video generation. Used when continuing or extending a draft output",
                }),
                "videoId": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "Video ID from a previous generation. Used when extending or editing an existing OpenAI Sora video",
                }),
                "Elements": ("RUNWAREVIDEOINFERENCEELEMENTS", {
                    "tooltip": "Connect Runware Video Inference Elements (one element) or Runware Video Inference Elements Combine (several) for inputs.elements (Kling, etc.).",
                }),
            }
        }

    DESCRIPTION = (
        "Configure custom inputs for Runware Video Inference (image, audio, video, mask, avatar, etc.). "
        "Avatar and Image are mutually exclusive: if Avatar is set, Image is ignored; provide only one."
    )
    FUNCTION = "createInputs"
    RETURN_TYPES = ("RUNWAREVIDEOINFERENCEINPUTS",)
    RETURN_NAMES = ("Video Inference Inputs",)
    CATEGORY = "Runware"

    def createInputs(self, **kwargs):
        """Create video inference inputs from provided parameters"""
        image = kwargs.get("Image", None)
        audio = kwargs.get("Audio", None)
        audioInputs = kwargs.get("Audio Inputs", None)
        speechInputs = kwargs.get("Speech Inputs", None)
        video = kwargs.get("Video", None)
        mask = kwargs.get("Mask", None)
        frame = kwargs.get("Frame", None)
        background = kwargs.get("Background", None)
        frameImages = kwargs.get("Frame Images", None)
        references = kwargs.get("References Images", None)
        referenceVideos = kwargs.get("Reference Videos", None)
        referenceAudios = kwargs.get("Reference Audios", None)
        referenceVoices = kwargs.get("Reference Voices", None)
        draftId = kwargs.get("draftId", "")
        videoId = kwargs.get("videoId", "")
        avatar = kwargs.get("Avatar", "")
        elements_list = kwargs.get("Elements", None)

        inputs = {}

        has_avatar = avatar is not None and avatar.strip() != ""
        if has_avatar:
            inputs["avatar"] = avatar.strip()
        if image is not None:
            inputs["image"] = rwUtils.convertTensor2IMG(image)

        # Handle audio: can be either a string (legacy), a single dict, or a list of audio inputs
        if audioInputs is not None:
            if isinstance(audioInputs, list) and len(audioInputs) > 0:
                # List from combine node
                inputs["audio"] = audioInputs
            elif isinstance(audioInputs, dict) and len(audioInputs) > 0:
                # Single audio input dict
                inputs["audio"] = [audioInputs]
        elif audio is not None and audio.strip() != "":
            inputs["audio"] = audio.strip()
        
        # Handle speech inputs: can be a single dict or a list of speech inputs
        if speechInputs is not None:
            if isinstance(speechInputs, list) and len(speechInputs) > 0:
                # List from combine node
                inputs["speech"] = speechInputs
            elif isinstance(speechInputs, dict) and len(speechInputs) > 0:
                # Single speech input dict
                inputs["speech"] = [speechInputs]

        if video is not None and video.strip() != "":
            inputs["video"] = video.strip()

        if mask is not None:
            inputs["mask"] = rwUtils.convertTensor2IMG(mask)

        if frame is not None:
            inputs["frame"] = rwUtils.convertTensor2IMG(frame)

        if background is not None:
            inputs["background"] = rwUtils.convertTensor2IMG(background)

        if frameImages is not None and len(frameImages) > 0:
            inputs["frameImages"] = frameImages

        if references is not None and len(references) > 0:
            inputs["referenceImages"] = references

        if referenceVideos is not None and len(referenceVideos) > 0:
            inputs["referenceVideos"] = referenceVideos

        if referenceAudios is not None and len(referenceAudios) > 0:
            inputs["referenceAudios"] = referenceAudios

        if referenceVoices is not None and len(referenceVoices) > 0:
            inputs["referenceVoices"] = referenceVoices

        if draftId is not None and draftId.strip() != "":
            inputs["draftId"] = draftId.strip()

        if videoId is not None and videoId.strip() != "":
            inputs["videoId"] = videoId.strip()

        if elements_list is not None and isinstance(elements_list, list):
            merged_elements = [
                e for e in elements_list
                if isinstance(e, dict) and len(e) > 0
            ]
            if merged_elements:
                inputs["elements"] = merged_elements

        return (inputs,)
