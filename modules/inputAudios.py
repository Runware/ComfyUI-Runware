from .utils import runwareUtils as rwUtils

class inputAudios:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "Audio 1": ("STRING", {
                    "tooltip": "Connect the mediaUUID output from Runware Media Upload node with audio file.",
                }),
                "Audio 2": ("STRING", {
                    "tooltip": "Connect the mediaUUID output from Runware Media Upload node with audio file.",
                }),
                "Audio 3": ("STRING", {
                    "tooltip": "Connect the mediaUUID output from Runware Media Upload node with audio file.",
                }),
                "Audio 4": ("STRING", {
                    "tooltip": "Connect the mediaUUID output from Runware Media Upload node with audio file.",
                }),
            }
        }

    DESCRIPTION = "Configure custom input audios for Runware Video Inference by connecting mediaUUID outputs from Runware Media Upload nodes."
    FUNCTION = "createInputAudios"
    RETURN_TYPES = ("RUNWAREINPUTAUDIOS",)
    RETURN_NAMES = ("Input Audios",)
    CATEGORY = "Runware"

    def createInputAudios(self, **kwargs):
        audio1 = kwargs.get("Audio 1", None)
        audio2 = kwargs.get("Audio 2", None)
        audio3 = kwargs.get("Audio 3", None)
        audio4 = kwargs.get("Audio 4", None)

        # Build the input audios list
        input_audios = []
        
        # Handle each audio input
        if audio1 is not None and audio1.strip() != "":
            input_audios.append(audio1.strip())
        if audio2 is not None and audio2.strip() != "":
            input_audios.append(audio2.strip())
        if audio3 is not None and audio3.strip() != "":
            input_audios.append(audio3.strip())
        if audio4 is not None and audio4.strip() != "":
            input_audios.append(audio4.strip())

        return (input_audios, )
