from .utils import runwareUtils as rwUtils
import json
import comfy.model_management

class videoBgRemoval:
    RUNWARE_VRMBG_MODELS = {
        "bria:51@1": "bria:51@1",
    }
    
    BACKGROUND_COLORS = {
        "Transparent": [0, 0, 0, 0],
        "Black": [0, 0, 0, 1],
        "White": [255, 255, 255, 0],
        "Gray": [128, 128, 128, 0],
        "Red": [255, 0, 0, 0],
        "Green": [0, 255, 0, 0],
        "Blue": [0, 0, 255, 0],
        "Yellow": [255, 255, 0, 0],
        "Cyan": [0, 255, 255, 0],
        "Magenta": [255, 0, 255, 0],
        "Orange": [255, 165, 0, 0],
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
                    "default": "Transparent",
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
        video_uuid = kwargs.get("Video")
        modelName = kwargs.get("Model", "Bria Video Background Removal")
        backgroundColor = kwargs.get("Background Color", "Transparent")
        outputFormat = kwargs.get("Output Format", "mp4")
        
        # Validate mediaUUID
        if not video_uuid or video_uuid.strip() == "":
            raise ValueError("Video mediaUUID is required")
        
        # Get the model AIR code
        modelAIR = self.RUNWARE_VRMBG_MODELS.get(modelName, "bria:51@1")
        
        # Get background color RGBA
        rgba_color = self.BACKGROUND_COLORS.get(backgroundColor, [0, 0, 0, 0])
        
        # Build the API request
        genConfig = [
            {
                "taskType": "removeBackground",
                "taskUUID": rwUtils.genRandUUID(),
                "inputs": {
                    "video": video_uuid
                },
                "model": modelAIR,
                "outputFormat": outputFormat,
                "settings": {
                    "rgba": rgba_color
                }
            }
        ]
        
        try:
            # Debug: Print the request being sent
            print(f"[DEBUG] Sending Video Background Removal Request:")
            print(f"[DEBUG] Request Payload: {json.dumps(genConfig, indent=2)}")
            
            genResult = rwUtils.inferenecRequest(genConfig)
            
            # Debug: Print the response received
            print(f"[DEBUG] Received Video Background Removal Response:")
            print(f"[DEBUG] Response: {json.dumps(genResult, indent=2)}")
            
            # Check for errors
            if "errors" in genResult:
                error_message = genResult["errors"][0]["message"]
                raise Exception(f"Video background removal failed: {error_message}")
            
            # Extract task UUID for polling
            taskUUID = genConfig[0]["taskUUID"]
            
            # Poll for video completion
            while True:
                # Check for interrupt before each poll
                comfy.model_management.throw_exception_if_processing_interrupted()
                
                # Poll for video result
                pollResult = rwUtils.pollVideoResult(taskUUID)
                print(f"[Debugging] Poll result: {pollResult}")
                
                # Check for errors first
                if pollResult and "errors" in pollResult and len(pollResult["errors"]) > 0:
                    error_info = pollResult["errors"][0]
                    error_message = error_info.get("message", "Unknown error")
                    raise Exception(f"Video background removal failed: {error_message}")
                
                if pollResult and "data" in pollResult and len(pollResult["data"]) > 0:
                    video_data = pollResult["data"][0]
                    
                    # Check status directly
                    if "status" in video_data:
                        status = video_data["status"]
                        
                        if status == "success":
                            if "videoURL" in video_data or "videoBase64Data" in video_data:
                                videos = rwUtils.convertVideoB64List(pollResult, 1920, 1080)
                                return videos
                        
                        # If status is "processing", continue polling
                
                # Check for interrupt before waiting
                comfy.model_management.throw_exception_if_processing_interrupted()
                
                # Wait before next poll
                for _ in range(10):  # 10 x 0.1 second = 1 second total
                    comfy.model_management.throw_exception_if_processing_interrupted()
                    rwUtils.time.sleep(0.1)
                        
        except Exception as e:
            print(f"[Error] Video background removal failed: {str(e)}")
            raise e

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareVideoBgRemoval": videoBgRemoval,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVideoBgRemoval": "Runware Video Background Removal",
}

