"""
Runware Bria Provider Key Points Node
Creates key points configuration for Bria mask settings
"""

from typing import Optional, Dict, Any, List


class RunwareBriaProviderKeyPoints:
    """Runware Bria Provider Key Points Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
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

    RETURN_TYPES = ("RUNWAREBRIAPROVIDERKEYPOINTS",)
    RETURN_NAMES = ("Key Points",)
    FUNCTION = "createKeyPoints"
    CATEGORY = "Runware/Provider Settings"
    DESCRIPTION = "Create key points configuration for Bria mask settings. Each key point defines a coordinate (x, y) and type (positive/negative) to guide mask generation."

    def createKeyPoints(self, **kwargs) -> tuple[List[Dict[str, Any]]]:
        """Create key points array from provided parameters"""
        
        keyPoints: List[Dict[str, Any]] = []
        
        # Process up to 6 key points
        for i in range(1, 7):
            use_key = kwargs.get(f"use_{i}", False)
            
            # Only process key point if use toggle is enabled
            if use_key:
                x = kwargs.get(f"X{i}", 0)
                y = kwargs.get(f"Y{i}", 0)
                point_type = kwargs.get(f"Type{i}", "positive")
                
                # Only add key point if both x and y are provided and at least one is non-zero
                # This allows users to leave unused key points at 0,0
                if x > 0 or y > 0:
                    keyPoints.append({
                        "x": x,
                        "y": y,
                        "type": point_type
                    })
        
        return (keyPoints,)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareBriaProviderKeyPoints": RunwareBriaProviderKeyPoints,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareBriaProviderKeyPoints": "Runware Bria Provider Key Points",
}

