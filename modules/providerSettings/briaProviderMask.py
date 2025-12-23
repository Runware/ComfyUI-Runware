"""
Runware Bria Provider Mask Node
Creates mask configuration for Bria video eraser settings
"""

from typing import Optional, Dict, Any, List


class RunwareBriaProviderMask:
    """Runware Bria Provider Mask Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useForeground": ("BOOLEAN", {
                    "tooltip": "Enable to include mask.foreground parameter in API request.",
                    "default": False,
                }),
                "foreground": ("BOOLEAN", {
                    "tooltip": "Triggers the foreground mask endpoint. Only used when 'Use Foreground' is enabled.",
                    "default": True,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "usePrompt": ("BOOLEAN", {
                    "tooltip": "Enable to include mask.prompt parameter in API request.",
                    "default": False,
                }),
                "prompt": ("STRING", {
                    "tooltip": "Text instruction describing the object to be masked. Only used when 'Use Prompt' is enabled.",
                    "default": "",
                    "multiline": True,
                }),
                "useFrameIndex": ("BOOLEAN", {
                    "tooltip": "Enable to include mask.frameIndex parameter in API request.",
                    "default": False,
                }),
                "frameIndex": ("INT", {
                    "tooltip": "The frame number to apply key points to. Specifies which frame in the video to use for masking. Only used when 'Use Frame Index' is enabled.",
                    "default": 0,
                    "min": 0,
                }),
                "use_1": ("BOOLEAN", {
                    "tooltip": "Enable to include the first key point in the mask configuration.",
                    "default": False,
                }),
                "X1": ("INT", {
                    "tooltip": "X-coordinate of the first key point on the frame",
                    "default": 0,
                    "min": 0,
                }),
                "Y1": ("INT", {
                    "tooltip": "Y-coordinate of the first key point on the frame",
                    "default": 0,
                    "min": 0,
                }),
                "Type1": (["positive", "negative"], {
                    "tooltip": "Type of mask hint for first key point. 'positive' includes area, 'negative' excludes area.",
                    "default": "positive",
                }),
                "use_2": ("BOOLEAN", {
                    "tooltip": "Enable to include the second key point in the mask configuration.",
                    "default": False,
                }),
                "X2": ("INT", {
                    "tooltip": "X-coordinate of the second key point on the frame",
                    "default": 0,
                    "min": 0,
                }),
                "Y2": ("INT", {
                    "tooltip": "Y-coordinate of the second key point on the frame",
                    "default": 0,
                    "min": 0,
                }),
                "Type2": (["positive", "negative"], {
                    "tooltip": "Type of mask hint for second key point. 'positive' includes area, 'negative' excludes area.",
                    "default": "positive",
                }),
                "use_3": ("BOOLEAN", {
                    "tooltip": "Enable to include the third key point in the mask configuration.",
                    "default": False,
                }),
                "X3": ("INT", {
                    "tooltip": "X-coordinate of the third key point on the frame",
                    "default": 0,
                    "min": 0,
                }),
                "Y3": ("INT", {
                    "tooltip": "Y-coordinate of the third key point on the frame",
                    "default": 0,
                    "min": 0,
                }),
                "Type3": (["positive", "negative"], {
                    "tooltip": "Type of mask hint for third key point. 'positive' includes area, 'negative' excludes area.",
                    "default": "positive",
                }),
                "use_4": ("BOOLEAN", {
                    "tooltip": "Enable to include the fourth key point in the mask configuration.",
                    "default": False,
                }),
                "X4": ("INT", {
                    "tooltip": "X-coordinate of the fourth key point on the frame",
                    "default": 0,
                    "min": 0,
                }),
                "Y4": ("INT", {
                    "tooltip": "Y-coordinate of the fourth key point on the frame",
                    "default": 0,
                    "min": 0,
                }),
                "Type4": (["positive", "negative"], {
                    "tooltip": "Type of mask hint for fourth key point. 'positive' includes area, 'negative' excludes area.",
                    "default": "positive",
                }),
                "use_5": ("BOOLEAN", {
                    "tooltip": "Enable to include the fifth key point in the mask configuration.",
                    "default": False,
                }),
                "X5": ("INT", {
                    "tooltip": "X-coordinate of the fifth key point on the frame",
                    "default": 0,
                    "min": 0,
                }),
                "Y5": ("INT", {
                    "tooltip": "Y-coordinate of the fifth key point on the frame",
                    "default": 0,
                    "min": 0,
                }),
                "Type5": (["positive", "negative"], {
                    "tooltip": "Type of mask hint for fifth key point. 'positive' includes area, 'negative' excludes area.",
                    "default": "positive",
                }),
                "use_6": ("BOOLEAN", {
                    "tooltip": "Enable to include the sixth key point in the mask configuration.",
                    "default": False,
                }),
                "X6": ("INT", {
                    "tooltip": "X-coordinate of the sixth key point on the frame",
                    "default": 0,
                    "min": 0,
                }),
                "Y6": ("INT", {
                    "tooltip": "Y-coordinate of the sixth key point on the frame",
                    "default": 0,
                    "min": 0,
                }),
                "Type6": (["positive", "negative"], {
                    "tooltip": "Type of mask hint for sixth key point. 'positive' includes area, 'negative' excludes area.",
                    "default": "positive",
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREBRIAPROVIDERMASK",)
    RETURN_NAMES = ("Bria Provider Setting Mask",)
    FUNCTION = "createMask"
    CATEGORY = "Runware/Provider Settings"
    DESCRIPTION = "Create mask configuration for Bria video eraser settings. Supports foreground mask, text-based masking, and coordinate-based key points for precise object removal."

    def createMask(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create mask configuration from provided parameters"""
        
        mask: Dict[str, Any] = {}
        maskEnabled = False
        
        # Handle foreground
        useForeground = kwargs.get("useForeground", False)
        if useForeground:
            foreground = kwargs.get("foreground", True)
            mask["foreground"] = foreground
            maskEnabled = True
        
        # Handle prompt
        usePrompt = kwargs.get("usePrompt", False)
        if usePrompt:
            prompt = kwargs.get("prompt", "").strip()
            if prompt:
                mask["prompt"] = prompt
                maskEnabled = True
        
        # Handle frameIndex
        useFrameIndex = kwargs.get("useFrameIndex", False)
        if useFrameIndex:
            frameIndex = kwargs.get("frameIndex", 0)
            mask["frameIndex"] = frameIndex
            maskEnabled = True
        
        # Process key points
        keyPoints: List[Dict[str, Any]] = []
        for i in range(1, 7):
            use_key = kwargs.get(f"use_{i}", False)
            
            # Only process key point if use toggle is enabled
            if use_key:
                x = kwargs.get(f"X{i}", 0)
                y = kwargs.get(f"Y{i}", 0)
                point_type = kwargs.get(f"Type{i}", "positive")
                
                # Only add key point if both x and y are provided and at least one is non-zero
                if x > 0 or y > 0:
                    keyPoints.append({
                        "x": x,
                        "y": y,
                        "type": point_type
                    })
        
        # Add keyPoints if any were provided
        if len(keyPoints) > 0:
            mask["keyPoints"] = keyPoints
            maskEnabled = True
        
        # Only return mask if it has at least one property
        if maskEnabled:
            return (mask,)
        else:
            return ({},)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareBriaProviderMask": RunwareBriaProviderMask,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareBriaProviderMask": "Runware Bria Provider Mask",
}
