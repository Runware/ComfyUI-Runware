from typing import Optional, Dict, Any

class safetyInputs:
    """Runware Safety Inputs Node"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "mode": (["none", "fast", "full"], {
                    "tooltip": "Safety moderation mode: none (disable), fast (quick check), or full (comprehensive check).",
                    "default": "none",
                }),
                "tolerance": ("BOOLEAN", {
                    "tooltip": "Safety tolerance setting for content moderation.",
                    "default": None,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "checkInputs": ("BOOLEAN", {
                    "tooltip": "Enable checking of input content for safety violations.",
                    "default": None,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "checkContent": ("BOOLEAN", {
                    "tooltip": "Enable checking of generated content for safety violations.",
                    "default": None,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
            }
        }
    
    RETURN_TYPES = ("RUNWARESAFETYINPUTS",)
    RETURN_NAMES = ("Safety Inputs",)
    FUNCTION = "create_safety_inputs"
    CATEGORY = "Runware"
    DESCRIPTION = "Configure safety and content moderation settings for Runware tasks."
    
    def create_safety_inputs(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create safety inputs dictionary"""
        
        # Get parameters
        mode = kwargs.get("mode", None)
        tolerance = kwargs.get("tolerance", None)
        checkInputs = kwargs.get("checkInputs", None)
        checkContent = kwargs.get("checkContent", None)
        
        # Build safety inputs dictionary - only include non-None values
        safety_inputs = {}
        
        if mode is not None:
            safety_inputs["mode"] = mode
        if tolerance is not None:
            safety_inputs["tolerance"] = tolerance
        if checkInputs is not None:
            safety_inputs["checkInputs"] = checkInputs
        if checkContent is not None:
            safety_inputs["checkContent"] = checkContent
        
        return (safety_inputs,)

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareSafetyInputs": safetyInputs,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareSafetyInputs": "Runware Safety Inputs",
}

