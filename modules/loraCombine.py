class loraCombine:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Lora 1": ("RUNWARELORA", {
                    "tooltip": "Connect a Runware Lora From Lora Search Node.",
                }),
            },
            "optional": {
                "Lora 2": ("RUNWARELORA", {
                    "tooltip": "Connect a Runware Lora From Lora Search Node.",
                }),
                "Lora 3": ("RUNWARELORA", {
                    "tooltip": "Connect a Runware Lora From Lora Search Node.",
                }),
            },
        }

    DESCRIPTION = "Combine One or More Lora's To Connect It With Runware Image Inference."
    FUNCTION = "loraCombine"
    RETURN_TYPES = ("RUNWARELORA",)
    RETURN_NAMES = ("Runware Lora's",)
    CATEGORY = "Runware"

    def loraCombine(self, **kwargs):
        runwareLora1 = kwargs.get("Lora 1")
        runwareLora2 = kwargs.get("Lora 2", None)
        runwareLora3 = kwargs.get("Lora 3", None)

        loraObjectArray = []
        loraObjectArray.append(runwareLora1)
        if(runwareLora2):
            loraObjectArray.append(runwareLora2)
        if(runwareLora3):
            loraObjectArray.append(runwareLora3)
        return (loraObjectArray,)