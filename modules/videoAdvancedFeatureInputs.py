from typing import Optional, Dict, Any

class videoAdvancedFeatureInputs:
    """Runware Video Advanced Feature Inputs Node"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useVideoCFGScale": ("BOOLEAN", {
                    "tooltip": "Enable to include videoCFGScale parameter in API request.",
                    "default": False,
                }),
                "videoCFGScale": ("FLOAT", {
                    "tooltip": "CFG scale for video generation. Only used when 'Use Video CFG Scale' is enabled.",
                    "default": None,
                    "min": 0.0,
                    "max": 30.0,
                    "step": 0.1,
                }),
                "useAudioCFGScale": ("BOOLEAN", {
                    "tooltip": "Enable to include audioCFGScale parameter in API request.",
                    "default": False,
                }),
                "audioCFGScale": ("FLOAT", {
                    "tooltip": "CFG scale for audio generation. Only used when 'Use Audio CFG Scale' is enabled.",
                    "default": None,
                    "min": 0.0,
                    "max": 30.0,
                    "step": 0.1,
                }),
                "useVideoNegativePrompt": ("BOOLEAN", {
                    "tooltip": "Enable to include videoNegativePrompt parameter in API request.",
                    "default": False,
                }),
                "videoNegativePrompt": ("STRING", {
                    "tooltip": "Negative prompt for video generation. Only used when 'Use Video Negative Prompt' is enabled.",
                    "multiline": True,
                    "default": "",
                }),
                "useAudioNegativePrompt": ("BOOLEAN", {
                    "tooltip": "Enable to include audioNegativePrompt parameter in API request.",
                    "default": False,
                }),
                "audioNegativePrompt": ("STRING", {
                    "tooltip": "Negative prompt for audio generation. Only used when 'Use Audio Negative Prompt' is enabled.",
                    "multiline": True,
                    "default": "",
                }),
                "useSlgLayer": ("BOOLEAN", {
                    "tooltip": "Enable to include slgLayer parameter in API request.",
                    "default": False,
                }),
                "slgLayer": ("INT", {
                    "tooltip": "SLG layer setting. Only used when 'Use SLG Layer' is enabled.",
                    "default": None,
                    "min": 0,
                    "max": 100,
                }),
                "Advanced Feature Settings": ("RUNWAREWANANIMATEADVANCEDFEATURESETTINGS", {
                    "tooltip": "Connect Runware Wan Animate Advanced Feature Settings node to provide Wan Animate configuration for character animation and replacement.",
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
        
        # Get use parameters
        useVideoCFGScale = kwargs.get("useVideoCFGScale", False)
        useAudioCFGScale = kwargs.get("useAudioCFGScale", False)
        useVideoNegativePrompt = kwargs.get("useVideoNegativePrompt", False)
        useAudioNegativePrompt = kwargs.get("useAudioNegativePrompt", False)
        useSlgLayer = kwargs.get("useSlgLayer", False)
        
        # Get actual parameters
        videoCFGScale = kwargs.get("videoCFGScale", None)
        audioCFGScale = kwargs.get("audioCFGScale", None)
        videoNegativePrompt = kwargs.get("videoNegativePrompt", None)
        audioNegativePrompt = kwargs.get("audioNegativePrompt", None)
        slgLayer = kwargs.get("slgLayer", None)
        wanAnimateSettings = kwargs.get("Advanced Feature Settings", None)
        
        # Build advanced feature inputs dictionary - only include when use* is enabled
        advanced_inputs = {}
        
        if useVideoCFGScale and videoCFGScale is not None:
            advanced_inputs["videoCFGScale"] = videoCFGScale
        if useAudioCFGScale and audioCFGScale is not None:
            advanced_inputs["audioCFGScale"] = audioCFGScale
        if useVideoNegativePrompt and videoNegativePrompt is not None and videoNegativePrompt.strip() != "":
            advanced_inputs["videoNegativePrompt"] = videoNegativePrompt.strip()
        if useAudioNegativePrompt and audioNegativePrompt is not None and audioNegativePrompt.strip() != "":
            advanced_inputs["audioNegativePrompt"] = audioNegativePrompt.strip()
        if useSlgLayer and slgLayer is not None:
            advanced_inputs["slgLayer"] = slgLayer
        
        # Merge advanced feature settings if provided (similar to how providerSettings are merged)
        if wanAnimateSettings is not None and isinstance(wanAnimateSettings, dict) and len(wanAnimateSettings) > 0:
            # Merge the settings dictionary directly into advanced_inputs
            # The settings dict should already contain the correct structure (e.g., {"wanAnimate": {...}})
            advanced_inputs.update(wanAnimateSettings)
        
        return (advanced_inputs,)

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareVideoAdvancedFeatureInputs": videoAdvancedFeatureInputs,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVideoAdvancedFeatureInputs": "Runware Video Advanced Feature Inputs",
}

