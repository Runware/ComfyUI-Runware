from .utils import runwareUtils as rwUtils


class RunwareVideoInputsFrameImages:
    """Video Inputs Frame node for adapting frame images structure for video inference"""
    
    MAX_FRAMES = 4
    
    @classmethod
    def INPUT_TYPES(cls):
        optionalInputs = {}
        
        for i in range(1, cls.MAX_FRAMES + 1):
            optionalInputs[f"image{i}"] = ("IMAGE", {
                "tooltip": "Frame image to include in video inference inputs."
            })
            optionalInputs[f"frame{i} position"] = ("STRING", {
                "default": "",
                "tooltip": "Optional frame label (e.g., 'first', 'last', specific frame number). Leave blank for provider defaults."
            })
        
        return {
            "required": {},
            "optional": optionalInputs
        }
    
    DESCRIPTION = "Convert Runware Frame Images into the expected structure for video inference inputs."
    FUNCTION = "createFrameInputs"
    RETURN_TYPES = ("RUNWAREVIDEOINPUTSFRAMEIMAGES",)
    RETURN_NAMES = ("Video Inputs Frame Images",)
    CATEGORY = "Runware"
    
    def createFrameInputs(self, **kwargs):
        frameImages = []
        
        for i in range(1, self.MAX_FRAMES + 1):
            imageKey = f"image{i}"
            frameKey = f"frame{i} position"
            
            image = kwargs.get(imageKey)
            frame = kwargs.get(frameKey, "")
            
            if image is None:
                continue
            
            frameData = self._createFrameEntry(image, frame)
            frameImages.append(frameData)
        
        return (frameImages,)
    
    def _createFrameEntry(self, image, frameLabel):
        imageData = rwUtils.convertTensor2IMGBase64Only(image)
        entry = {"image": imageData}
        
        if isinstance(frameLabel, str) and frameLabel.strip() != "":
            if frameLabel.strip().isdigit():
                entry["frame"] = int(frameLabel.strip())
            else:
                entry["frame"] = frameLabel.strip()
        
        return entry


NODE_CLASS_MAPPINGS = {
    "RunwareVideoInputsFrameImages": RunwareVideoInputsFrameImages,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVideoInputsFrameImages": "Runware Video Inputs Frame Images",
}
