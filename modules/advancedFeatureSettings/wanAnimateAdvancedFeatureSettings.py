"""
Runware Wan Animate Advanced Feature Settings Node
Provides Wan Animate-specific settings for video generation
"""

from typing import Optional, Dict, Any

class RunwareWanAnimateAdvancedFeatureSettings:
    """Runware Wan Animate Advanced Feature Settings Node"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useMode": ("BOOLEAN", {
                    "tooltip": "Enable to include mode parameter in API request.",
                    "default": True,
                }),
                "mode": (["animate", "replace"], {
                    "tooltip": "Animation mode: 'animate' uses pose detector and skeleton retargeting to animate a character from a reference image. 'replace' uses pose detector and segmentation model to replace a character in existing footage. Only used when 'Use Mode' is enabled.",
                    "default": "animate",
                }),
                "useRetargetPose": ("BOOLEAN", {
                    "tooltip": "Enable to include retargetPose parameter in API request. Only available for animate mode.",
                    "default": False,
                }),
                "retargetPose": ("BOOLEAN", {
                    "tooltip": "Retarget the pose of video image to match the reference image initial pose. That is achieved moving the hands' bones according to video. Means if the character from video moves his hands it will take the initial reference image pose and change the position of bones according to video movements. Supported only for animate mode. Only used when 'Use Retarget Pose' is enabled.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "usePrevSegCondFrames": ("BOOLEAN", {
                    "tooltip": "Enable to include prevSegCondFrames parameter in API request.",
                    "default": False,
                }),
                "prevSegCondFrames": ("INT", {
                    "tooltip": "How many frames to take from previous segment to keep temporal consistency. Less -> less consistent between the segments. More -> more time for inference. Only used when 'Use Prev Seg Cond Frames' is enabled.",
                    "default": 1,
                    "min": 1,
                    "max": 5,
                }),
            }
        }
    
    RETURN_TYPES = ("RUNWAREWANANIMATEADVANCEDFEATURESETTINGS",)
    RETURN_NAMES = ("Wan Animate Advanced Feature Settings",)
    FUNCTION = "create_wan_animate_settings"
    CATEGORY = "Runware/Advanced Feature Settings"
    DESCRIPTION = "Configure Wan Animate advanced feature settings including mode (animate/replace), pose retargeting, and previous segment conditioning frames for character animation and replacement."
    
    def create_wan_animate_settings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Create Wan Animate advanced feature settings"""
        
        # Get use parameters
        useMode = kwargs.get("useMode", True)
        useRetargetPose = kwargs.get("useRetargetPose", False)
        usePrevSegCondFrames = kwargs.get("usePrevSegCondFrames", False)
        
        # Get actual parameters
        mode = kwargs.get("mode", "animate")
        retargetPose = kwargs.get("retargetPose", False)
        prevSegCondFrames = kwargs.get("prevSegCondFrames", 1)
        
        # Build settings dictionary
        wanAnimateSettings = {}
        
        # Add mode only if useMode is enabled
        if useMode and mode is not None:
            wanAnimateSettings["mode"] = mode
        
        # Add retargetPose only if useRetargetPose is enabled
        # Note: retargetPose is only supported for animate mode, but we'll let the API handle validation
        if useRetargetPose:
            wanAnimateSettings["retargetPose"] = retargetPose
        
        # Add prevSegCondFrames only if usePrevSegCondFrames is enabled
        if usePrevSegCondFrames:
            wanAnimateSettings["prevSegCondFrames"] = prevSegCondFrames
        
        # Clean up None values
        wanAnimateSettings = {k: v for k, v in wanAnimateSettings.items() if v is not None}
        
        # Return the full structure with the feature name as key (similar to providerSettings pattern)
        if wanAnimateSettings:
            return ({"wanAnimate": wanAnimateSettings},)
        else:
            return ({},)

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareWanAnimateAdvancedFeatureSettings": RunwareWanAnimateAdvancedFeatureSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareWanAnimateAdvancedFeatureSettings": "Runware Wan Animate Advanced Feature Settings",
}

