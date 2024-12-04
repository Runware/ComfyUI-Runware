class refiner:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Model": ("RUNWAREMODEL", {
                    "tooltip": "Connect a Runware Model From Model Search Node.",
                }),
                "startStep": ("INT", {
                    "tooltip": "Represents the step number at which the refinement process begins. The initial model will generate the image up to this step, after which the refiner model takes over to enhance the result.",
                    "min": 0,
                    "max": 99,
                    "default": 0,
                }),
                "startStepPercentage": ("INT", {
                    "tooltip": "Represents the percentage of total steps at which the refinement process begins. The initial model will generate the image up to this percentage of steps before the refiner takes over.",
                    "min": 0,
                    "max": 99,
                    "default": 0
                }),
            },
        }

    DESCRIPTION = "Refiner models help create higher quality image outputs by incorporating specialized models designed to enhance image details and overall coherence. This can be particularly useful when you need results with superior quality, photorealism, or specific aesthetic refinements. (Note that refiner models are only SDXL based)"
    FUNCTION = "refiner"
    RETURN_TYPES = ("RUNWAREREFINER",)
    CATEGORY = "Runware"

    @classmethod
    def VALIDATE_INPUTS(cls, startStep, startStepPercentage):
        if(startStep != 0 and startStepPercentage != 0):
            raise Exception("Please provide either startStep or startStepPercentage, not both.")
        elif(startStep == 0 and startStepPercentage == 0):
            raise Exception("Please provide either startStep or startStepPercentage.")
        else:
            return True

    def refiner(self, **kwargs):
        runwareModel = kwargs.get("Model")
        startStep = kwargs.get("startStep")
        startStepPercentage = kwargs.get("startStepPercentage")
        refinerResult = {
            "model": runwareModel,
        }
        if(startStep != 0):
            refinerResult["startStep"] = startStep
        else:
            refinerResult["startStepPercentage"] = startStepPercentage
        return (refinerResult,)