class controlNetCombine:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "ControlNet 1": ("RUNWARECONTROLNET", {
                    "tooltip": "Connect a Runware ControlNet Node.",
                }),
            },
            "optional": {
                "ControlNet 2": ("RUNWARECONTROLNET", {
                    "tooltip": "Connect a Runware ControlNet Node.",
                }),
                "ControlNet 3": ("RUNWARECONTROLNET", {
                    "tooltip": "Connect a Runware ControlNet Node.",
                }),
            },
        }

    DESCRIPTION = "Combine One or More ControlNet's To Guide Image Generation Process in Runware Image Inference."
    FUNCTION = "controlNetCombine"
    RETURN_TYPES = ("RUNWARECONTROLNET",)
    RETURN_NAMES = ("Runware ControlNet's",)
    CATEGORY = "Runware"

    def controlNetCombine(self, **kwargs):
        controlNet1 = kwargs.get("ControlNet 1")
        controlNet2 = kwargs.get("ControlNet 2", None)
        controlNet3 = kwargs.get("ControlNet 3", None)

        controlNetObjectArray = controlNet1
        if(controlNet2 is not None):
            controlNetObjectArray = controlNetObjectArray + controlNet2
        if(controlNet3 is not None):
            controlNetObjectArray = controlNetObjectArray + controlNet3
        print(controlNetObjectArray)
        return (controlNetObjectArray,)