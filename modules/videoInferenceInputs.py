from .utils import runwareUtils as rwUtils

class videoInferenceInputs:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "Image": ("IMAGE", {
                    "tooltip": "Portrait image for video generation. This will be the main subject that will speak and move in the generated video."
                }),
                "Audio": ("STRING", {
                    "tooltip": "Connect the mediaUUID output from Runware Media Upload node with audio file. This audio will be synchronized with the generated video."
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
                "References": ("RUNWAREVIDEOINPUTSREFERENCES", {
                    "tooltip": "Connect the Video Inputs References node to provide reference images."
                }),
            }
        }

    DESCRIPTION = "Configure custom inputs for Runware Video Inference with OmniHuman 1.5 support, including image, audio, video, and mask inputs."
    FUNCTION = "createInputs"
    RETURN_TYPES = ("RUNWAREVIDEOINFERENCEINPUTS",)
    RETURN_NAMES = ("Video Inference Inputs",)
    CATEGORY = "Runware"

    def createInputs(self, **kwargs):
        image = kwargs.get("Image", None)
        audio = kwargs.get("Audio", None)
        video = kwargs.get("Video", None)
        mask = kwargs.get("Mask", None)
        frame = kwargs.get("Frame", None)
        references = kwargs.get("References", None)

        inputs = {}

        if image is not None:
            image_uuid = rwUtils.convertTensor2IMG(image)
            inputs["image"] = image_uuid

        if audio is not None and audio.strip() != "":
            inputs["audio"] = audio.strip()

        if video is not None and video.strip() != "":
            inputs["video"] = video.strip()

        if mask is not None:
            mask_uuid = rwUtils.convertTensor2IMG(mask)
            inputs["mask"] = mask_uuid

        if frame is not None:
            frame_uuid = rwUtils.convertTensor2IMG(frame)
            inputs["frame"] = frame_uuid

        if references is not None and len(references) > 0:
            inputs["references"] = references

        return (inputs,)

