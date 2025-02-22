from .utils import runwareUtils as rwUtils

class controlNet:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Guide Image": ("IMAGE", {
                    "tooltip": "Specifies the preprocessed image to be used as guide to control the image generation process."
                }),
                "ControlNet Search": ("STRING", {
                    "tooltip": "Searchg For Specific ControlNet By Name Or Civit AIR Code (eg: Canny).",
                }),
                "Model Architecture": ([
                        "All",
                        "FLUX.1-Schnell",
                        "FLUX.1-Dev",
                        "Pony",
                        "SD 1.5",
                        "SD 1.5 Hyper",
                        "SD 1.5 LCM",
                        "SD 3",
                        "SDXL 1.0",
                        "SDXL 1.0 LCM",
                        "SDXL Distilled",
                        "SDXL Hyper",
                        "SDXL Lightning",
                        "SDXL Turbo",
                    ], {
                    "tooltip": "Choose ControlNet Model Architecture To Filter Results.",
                    "default": "All",
                }),
                "ControlNetType": ([
                        "All",
                        "Canny",
                        "Depth",
                        "MLSD",
                        "Normal BAE",
                        "Open Pose",
                        "Tile",
                        "Seg",
                        "Line Art",
                        "Line Art Anime",
                        "Shuffle",
                        "Scribble",
                        "Soft Edge",
                    ], {
                    "tooltip": "Choose ControlNet Type To Filter Results.",
                    "default": "All",
                }),
                "ControlNetList": ([
                        "civitai:38784@44716 (SD1.5 Canny)",
                        "civitai:38784@44876 (SD1.5 Inpaint)",
                        "civitai:38784@44877 (SD1.5 Lineart)",
                        "civitai:38784@44795 (SD1.5 MLSD)",
                        "civitai:38784@44774 (SD1.5 NormalBAE)",
                        "runware:20@1 (SDXL Canny)",
                        "runware:25@1 (Flux Dev Canny)",
                        "runware:26@1 (Flux Dev Tile)",
                        "runware:28@1 (Flux Dev Blur)",
                        "runware:29@1 (Flux Dev OpenPose)",
                        "runware:30@1 (Flux Dev Gray)",
                        "runware:31@1 (Flux Dev Low Quality)",
                    ], {
                    "tooltip": "ControlNet Results Will Show UP Here So You Could Choose From.",
                    "default": "civitai:38784@44716 (SD1.5 Canny)",
                }),
                "startStep": ("INT", {
                    "tooltip": "Represents the step number at which the ControlNet model starts to control the inference process. (Enter -1 To Disable)",
                    "min": -1,
                    "max": 99,
                    "default": -1,
                }),
                "startStepPercentage": ("INT", {
                    "tooltip": "Represents the percentage of steps at which the ControlNet model starts to control the inference process. (Enter -1 To Disable)",
                    "min": -1,
                    "max": 99,
                    "default": 0,
                }),
                "endStep": ("INT", {
                    "tooltip": "Represents the step number at which the ControlNet preprocessor ends to control the inference process. (Enter -1 To Disable)",
                    "min": -1,
                    "max": 100,
                    "default": -1,
                }),
                "endStepPercentage": ("INT", {
                    "tooltip": "Represents the percentage of steps at which the ControlNet model ends to control the inference process. (Enter -1 To Disable)",
                    "min": -1,
                    "max": 100,
                    "default": 80,
                }),
                "Control Mode": (["prompt", "controlnet", "balanced"], {
                    "tooltip": "Choose Control Mode To Control The Inference Process.",
                    "default": "balanced",
                }),
                "weight": ("FLOAT", {
                    "tooltip": "Represents the weight (strength) of the ControlNet model in the image.",
                    "default": 1.0,
                    "min": 0,
                    "max": 1.0,
                    "step": 0.1,
                }),
                "Use Search Value": ("BOOLEAN", {
                    "tooltip": "When Enabled, the value you've set in the search input will be used instead.\n\nThis is useful in case the model search API is down or you prefer to set the model manually.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
            },
        }

    DESCRIPTION = "Directly Search and Configure ControlNet Guidance to Connect It With Runware Image Inference Nodes In ComfyUI."
    FUNCTION = "controlNet"
    RETURN_TYPES = ("RUNWARECONTROLNET",)
    RETURN_NAMES = ("Runware ControlNet",)
    CATEGORY = "Runware"

    @classmethod
    def VALIDATE_INPUTS(cls, ControlNetList, startStep, startStepPercentage, endStep, endStepPercentage):
        if((startStep == -1 and startStepPercentage == -1) or (startStep != -1 and startStepPercentage != -1)):
            raise Exception("Error: Please Provide Either Start Step or Start Step Percentage!")
        if((endStep == -1 and endStepPercentage == -1) or (endStep != -1 and endStepPercentage != -1)):
            raise Exception("Error: Please Provide Either End Step or End Step Percentage!")
        if((startStep != -1 and endStep != -1) and (startStep > endStep)):
            raise Exception("Error: Start Step Cannot Be Greater Than End Step!")
        elif((startStep != -1 and endStep != -1) and (startStep == endStep)):
            raise Exception("Error: Start Step Cannot Be Equal To End Step!")
        if((startStepPercentage != -1 and endStepPercentage != -1) and (startStepPercentage > endStepPercentage)):
            raise Exception("Error: Start Step Percentage Cannot Be Greater Than End Step Percentage!")
        elif((startStepPercentage != -1 and endStepPercentage != -1) and (startStepPercentage == endStepPercentage)):
            raise Exception("Error: Start Step Percentage Cannot Be Equal To End Step Percentage!")
        return True

    def controlNet(self, **kwargs):
        guideImage = kwargs.get("Guide Image")
        enableSearchValue = kwargs.get("Use Search Value", False)
        searchInput = kwargs.get("ControlNet Search")

        if enableSearchValue:
            modelAIRCode = searchInput
        else:
            CRModel = kwargs.get("ControlNetList")
            modelAIRCode = CRModel.split(" ")[0]

        startStep = kwargs.get("startStep")
        startStepPercentage = kwargs.get("startStepPercentage")
        endStep = kwargs.get("endStep")
        endStepPercentage = kwargs.get("endStepPercentage")
        controlMode = kwargs.get("Control Mode")
        weight = kwargs.get("weight")

        controlNetGuideOBJ = [{
            "model": modelAIRCode,
            "guideImage": rwUtils.convertTensor2IMG(guideImage),
            "weight": round(weight, 2),
            "controlMode": controlMode,
        }]

        if(startStep != -1):
            controlNetGuideOBJ[0]["startStep"] = startStep
        elif(startStepPercentage != -1):
            controlNetGuideOBJ[0]["startStepPercentage"] = startStepPercentage
        if(endStep != -1):
            controlNetGuideOBJ[0]["endStep"] = endStep
        elif(endStepPercentage != -1):
            controlNetGuideOBJ[0]["endStepPercentage"] = endStepPercentage

        return (controlNetGuideOBJ,)