class ipAdapterCombine:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "IPAdapter 1": ("RUNWAREIPAdapter", {
                    "tooltip": "Connect an IPAdapter from Runware IPAdapter node.",
                }),
            },
            "optional": {
                "IPAdapter 2": ("RUNWAREIPAdapter", {
                    "tooltip": "Connect an IPAdapter from Runware IPAdapter node.",
                }),
                "IPAdapter 3": ("RUNWAREIPAdapter", {
                    "tooltip": "Connect an IPAdapter from Runware IPAdapter node.",
                }),
            },
        }

    DESCRIPTION = "Combine multiple IPAdapters to connect with Runware Image Inference."
    FUNCTION = "ipAdapterCombine"
    RETURN_TYPES = ("RUNWAREIPAdapter",)
    RETURN_NAMES = ("IPAdapters",)
    CATEGORY = "Runware"

    def ipAdapterCombine(self, **kwargs):
        ipAdapter1 = kwargs.get("IPAdapter 1")
        ipAdapter2 = kwargs.get("IPAdapter 2", None)
        ipAdapter3 = kwargs.get("IPAdapter 3", None)

        ipAdapterArray = []
        ipAdapterArray.append(ipAdapter1)
        if(ipAdapter2):
            ipAdapterArray.append(ipAdapter2)
        if(ipAdapter3):
            ipAdapterArray.append(ipAdapter3)
        return (ipAdapterArray,)