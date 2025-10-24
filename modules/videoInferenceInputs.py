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
                "Mask": ("IMAGE", {
                    "tooltip": "Mask image to specify a specific subject in the image to speak. Use white/black mask format."
                }),
            }
        }

    DESCRIPTION = "Configure custom inputs for Runware Video Inference with OmniHuman 1.5 support, including image, audio, and mask inputs."
    FUNCTION = "createInputs"
    RETURN_TYPES = ("RUNWAREVIDEOINFERENCEINPUTS",)
    RETURN_NAMES = ("Video Inference Inputs",)
    CATEGORY = "Runware"

    def createInputs(self, **kwargs):
        image = kwargs.get("Image", None)
        audio = kwargs.get("Audio", None)
        mask = kwargs.get("Mask", None)

        # Build the inputs structure
        inputs = {}
        
        # Handle image input
        if image is not None:
            image_uuid = rwUtils.convertTensor2IMGForVideo(image)
            inputs["image"] = f"https://im.runware.ai/image/ii/{image_uuid}.webp"
        
        # Handle audio input (mediaUUID from media upload node)
        if audio is not None and audio.strip() != "":
            inputs["audio"] = audio.strip()
        
        # Handle mask input
        if mask is not None:
            mask_uuid = rwUtils.convertTensor2IMGForVideo(mask)
            inputs["mask"] = f"https://im.runware.ai/image/ii/{mask_uuid}.webp"

        return (inputs, )
