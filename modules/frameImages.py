from .utils import runwareUtils as rwUtils


class RunwareFrameImages:
    """Frame Images node for defining keyframes that constrain video timeline"""
    
    FRAME_POSITIONS = ["auto", "first", "last", "0", "12", "24", "36", "48", "60", "72", "84", "96", "108", "120"]
    MAX_FRAMES = 4
    
    @classmethod
    def INPUT_TYPES(cls):
        optionalInputs = {}
        
        for i in range(1, cls.MAX_FRAMES + 1):
            optionalInputs[f"image{i}"] = ("IMAGE", {
                "tooltip": "Frame image that will constrain video content at a specific timeline position. Used for keyframe control.",
            })
            optionalInputs[f"frame{i}_position"] = (cls.FRAME_POSITIONS, {
                "default": "auto",
                "tooltip": "Frame position: 'auto' (automatic distribution), 'first' (beginning), 'last' (end), or specific frame number (0-120).",
            })
        
        return {
            "required": {},
            "optional": optionalInputs
        }
    
    DESCRIPTION = "Define keyframes that constrain specific frames within the video timeline. Different from reference images - these control WHEN specific visual content appears, not overall style consistency."
    FUNCTION = "createFrameImages"
    RETURN_TYPES = ("RUNWAREFRAMEIMAGES",)
    RETURN_NAMES = ("Frame Images",)
    CATEGORY = "Runware"
    
    def createFrameImages(self, **kwargs):
        """Create frame images list from provided parameters"""
        frameImages = []
        
        for i in range(1, self.MAX_FRAMES + 1):
            imageKey = f"image{i}"
            positionKey = f"frame{i}_position"
            
            image = kwargs.get(imageKey)
            position = kwargs.get(positionKey, "auto")
            
            if image is not None:
                frameData = self._createFrameData(image, position)
                frameImages.append(frameData)
        
        return (frameImages,)

    def _createFrameData(self, image, position):
        """Create frame data object from image and position"""
        imageData = rwUtils.convertTensor2IMGBase64Only(image)
        frameData = {"inputImage": imageData}
        
        if position != "auto":
            if position.isdigit():
                frameData["frame"] = int(position)
            else:
                frameData["frame"] = position  # "first" or "last"
        
        return frameData


# Node class mappings for ComfyUI registration
NODE_CLASS_MAPPINGS = {
    "RunwareFrameImages": RunwareFrameImages,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareFrameImages": "Runware Frame Images",
}
