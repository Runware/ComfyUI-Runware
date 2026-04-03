from typing import Optional, Dict, Any


class safetyInputs:
    """Runware Safety Inputs Node for configuring safety and content moderation settings"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useMode": ("BOOLEAN", {
                    "tooltip": "Enable to include mode in payload.",
                    "default": False,
                }),
                "mode": (["none", "fast", "full"], {
                    "tooltip": "Safety moderation mode: none (disable), fast (quick check), or full (comprehensive check).",
                    "default": "none",
                }),
                "useTolerance": ("BOOLEAN", {
                    "tooltip": "Enable to include tolerance in payload.",
                    "default": False,
                }),
                "tolerance": ("BOOLEAN", {
                    "tooltip": "Safety tolerance setting for content moderation.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useCheckInputs": ("BOOLEAN", {
                    "tooltip": "Enable to include checkInputs in payload.",
                    "default": False,
                }),
                "checkInputs": ("BOOLEAN", {
                    "tooltip": "Enable checking of input content for safety violations.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "useCheckContent": ("BOOLEAN", {
                    "tooltip": "Enable to include checkContent in payload.",
                    "default": False,
                }),
                "checkContent": ("BOOLEAN", {
                    "tooltip": "Enable checking of generated content for safety violations.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
            }
        }
    
    RETURN_TYPES = ("RUNWARESAFETYINPUTS",)
    RETURN_NAMES = ("Safety Inputs",)
    FUNCTION = "createSafetyInputs"
    CATEGORY = "Runware"
    DESCRIPTION = "Configure safety and content moderation settings for Runware tasks."
    
    def createSafetyInputs(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create safety inputs dictionary"""
        useMode = kwargs.get("useMode", False)
        mode = kwargs.get("mode", None)
        useTolerance = kwargs.get("useTolerance", False)
        tolerance = kwargs.get("tolerance", None)
        useCheckInputs = kwargs.get("useCheckInputs", False)
        checkInputs = kwargs.get("checkInputs", None)
        useCheckContent = kwargs.get("useCheckContent", False)
        checkContent = kwargs.get("checkContent", None)
        
        safetyInputs = {}
        
        if useMode and mode is not None:
            safetyInputs["mode"] = mode
        if useTolerance and tolerance is not None:
            safetyInputs["tolerance"] = tolerance
        if useCheckInputs and checkInputs is not None:
            safetyInputs["checkInputs"] = checkInputs
        if useCheckContent and checkContent is not None:
            safetyInputs["checkContent"] = checkContent
        
        return (safetyInputs,)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareSafetyInputs": safetyInputs,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareSafetyInputs": "Runware Safety Inputs",
}
