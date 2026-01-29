from .utils import runwareUtils as rwUtils
import comfy.model_management


class videoBgRemoval:
    """Video Background Removal node for removing video backgrounds"""
    
    RUNWARE_VRMBG_MODELS = {
        "bria:51@1": "bria:51@1",
    }
    
    BACKGROUND_COLORS = {
        "Black [0, 0, 0, 1]": [0, 0, 0, 1],
        "White [255, 255, 255, 0]": [255, 255, 255, 0],
        "Gray [128, 128, 128, 0]": [128, 128, 128, 0],
        "Red [255, 0, 0, 0]": [255, 0, 0, 0],
        "Green [0, 255, 0, 0]": [0, 255, 0, 0],
        "Blue [0, 0, 255, 0]": [0, 0, 255, 0],
        "Yellow [255, 255, 0, 0]": [255, 255, 0, 0],
        "Cyan [0, 255, 255, 0]": [0, 255, 255, 0],
        "Magenta [255, 0, 255, 0]": [255, 0, 255, 0],
        "Orange [255, 165, 0, 0]": [255, 165, 0, 0],
    }
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Video": ("STRING", {
                    "tooltip": "MediaUUID from Runware Media Upload node for the video to process (max 30 seconds). Supports resolution up to 16000x16000 (16K)."
                }),
                "Model": (list(cls.RUNWARE_VRMBG_MODELS.keys()), {
                    "tooltip": "Select the video background removal model to use.",
                    "default": "Bria Video Background Removal",
                }),
            },
            "optional": {
                "Background Color": (list(cls.BACKGROUND_COLORS.keys()), {
                    "default": "White",
                    "tooltip": "Background color preset to use. Hex values are not supported.",
                }),
                "Output Format": (["mp4", "webm", "mov"], {
                    "default": "mp4",
                    "tooltip": "Choose the output video format.",
                }),
            }
        }

    DESCRIPTION = "Remove complex or moving video backgrounds in real time, isolating subjects with clean alpha channels for seamless compositing."
    FUNCTION = "removeBackground"
    RETURN_TYPES = ("VIDEO",)
    RETURN_NAMES = ("VIDEO",)
    CATEGORY = "Runware"

    def removeBackground(self, **kwargs):
        """Remove background from video"""
        videoUuid = kwargs.get("Video")
        modelName = kwargs.get("Model", "Bria Video Background Removal")
        backgroundColor = kwargs.get("Background Color", "Transparent")
        outputFormat = kwargs.get("Output Format", "mp4")
        
        if not videoUuid or videoUuid.strip() == "":
            raise ValueError("Video mediaUUID is required")
        
        modelAir = self.RUNWARE_VRMBG_MODELS.get(modelName, "bria:51@1")
        rgbaColor = self.BACKGROUND_COLORS.get(backgroundColor, [255, 255, 255, 0])
        
        genConfig = self._buildGenConfig(videoUuid, modelAir, outputFormat, rgbaColor)
        
        print(f"[DEBUG] Sending Video Background Removal Request:")
        print(f"[DEBUG] Request Payload: {rwUtils.safe_json_dumps(genConfig, indent=2)}")
        
        genResult = rwUtils.inferenecRequest(genConfig)
        
        print(f"[DEBUG] Received Video Background Removal Response:")
        print(f"[DEBUG] Response: {rwUtils.safe_json_dumps(genResult, indent=2)}")
        
        self._validateResponse(genResult)
        
        taskUuid = genConfig[0]["taskUUID"]
        videos = self._pollForVideoResult(taskUuid)
        
        return videos

    def _buildGenConfig(self, videoUuid, modelAir, outputFormat, rgbaColor):
        """Build generation configuration for API request"""
        return [{
            "taskType": "removeBackground",
            "taskUUID": rwUtils.genRandUUID(),
            "inputs": {
                "video": videoUuid
            },
            "model": modelAir,
            "outputFormat": outputFormat,
            "settings": {
                "rgba": rgbaColor
            }
        }]

    def _validateResponse(self, genResult):
        """Validate API response"""
        if "errors" in genResult:
            errorMessage = genResult["errors"][0]["message"]
            raise Exception(f"Video background removal failed: {errorMessage}")

    def _pollForVideoResult(self, taskUuid):
        """Poll for video result"""
        while True:
            comfy.model_management.throw_exception_if_processing_interrupted()
            
            pollResult = rwUtils.pollVideoResult(taskUuid)
            print(f"[Debugging] Poll result: {pollResult}")
            
            if pollResult and "errors" in pollResult and len(pollResult["errors"]) > 0:
                errorInfo = pollResult["errors"][0]
                errorMessage = errorInfo.get("message", "Unknown error")
                raise Exception(f"Video background removal failed: {errorMessage}")
            
            if pollResult and "data" in pollResult and len(pollResult["data"]) > 0:
                videoData = pollResult["data"][0]
                
                if "status" in videoData:
                    status = videoData["status"]
                    
                    if status == "success":
                        if "videoURL" in videoData or "videoBase64Data" in videoData:
                            videos = rwUtils.convertVideoB64List(pollResult, 1920, 1080)
                            # SaveVideo expects a single video object, not a tuple
                            return (videos[0],) if len(videos) > 0 else (None,)
            
            comfy.model_management.throw_exception_if_processing_interrupted()
            
            for _ in range(10):
                comfy.model_management.throw_exception_if_processing_interrupted()
                rwUtils.time.sleep(0.1)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareVideoBgRemoval": videoBgRemoval,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVideoBgRemoval": "Runware Video Background Removal",
}
