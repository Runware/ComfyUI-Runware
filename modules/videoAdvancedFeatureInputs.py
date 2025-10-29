from typing import Optional, Dict, Any

class videoAdvancedFeatureInputs:
    """Runware Video Advanced Feature Inputs Node"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "videoCFGScale": ("FLOAT", {
                    "tooltip": "CFG scale for video generation.",
                    "default": None,
                    "min": 0.0,
                    "max": 30.0,
                    "step": 0.1,
                }),
                "audioCFGScale": ("FLOAT", {
                    "tooltip": "CFG scale for audio generation.",
                    "default": None,
                    "min": 0.0,
                    "max": 30.0,
                    "step": 0.1,
                }),
                "videoNegativePrompt": ("STRING", {
                    "tooltip": "Negative prompt for video generation.",
                    "multiline": True,
                    "default": "",
                }),
                "audioNegativePrompt": ("STRING", {
                    "tooltip": "Negative prompt for audio generation.",
                    "multiline": True,
                    "default": "",
                }),
                "slgLayer": ("INT", {
                    "tooltip": "SLG layer setting.",
                    "default": None,
                    "min": 0,
                    "max": 100,
                }),
            }
        }
    
    RETURN_TYPES = ("RUNWAREVIDEOADVANCEDFEATUREINPUTS",)
    RETURN_NAMES = ("Video Advanced Feature Inputs",)
    FUNCTION = "create_advanced_feature_inputs"
    CATEGORY = "Runware"
    DESCRIPTION = "Configure advanced video feature inputs including CFG scales, negative prompts, and SLG layer settings."
    
    def create_advanced_feature_inputs(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create video advanced feature inputs dictionary"""
        
        # Get parameters
        videoCFGScale = kwargs.get("videoCFGScale", None)
        audioCFGScale = kwargs.get("audioCFGScale", None)
        videoNegativePrompt = kwargs.get("videoNegativePrompt", None)
        audioNegativePrompt = kwargs.get("audioNegativePrompt", None)
        slgLayer = kwargs.get("slgLayer", None)
        
        # Build advanced feature inputs dictionary - only include non-None values
        advanced_inputs = {}
        
        if videoCFGScale is not None:
            advanced_inputs["videoCFGScale"] = videoCFGScale
        if audioCFGScale is not None:
            advanced_inputs["audioCFGScale"] = audioCFGScale
        if videoNegativePrompt is not None and videoNegativePrompt.strip() != "":
            advanced_inputs["videoNegativePrompt"] = videoNegativePrompt.strip()
        if audioNegativePrompt is not None and audioNegativePrompt.strip() != "":
            advanced_inputs["audioNegativePrompt"] = audioNegativePrompt.strip()
        if slgLayer is not None:
            advanced_inputs["slgLayer"] = slgLayer
        
        return (advanced_inputs,)

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareVideoAdvancedFeatureInputs": videoAdvancedFeatureInputs,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVideoAdvancedFeatureInputs": "Runware Video Advanced Feature Inputs",
}

