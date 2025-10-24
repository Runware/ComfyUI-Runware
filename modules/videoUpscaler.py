from .utils import runwareUtils as rwUtils
import json
import comfy.model_management

class videoUpscaler:
    RUNWARE_VUPSCALER_MODELS = {
        "Bria Video Upscaler": "bria:50@1",
    }
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Video": ("STRING", {
                    "tooltip": "MediaUUID from Runware Media Upload node for the video to upscale."
                }),
                "upscaleFactor": ([2, 4], {
                    "tooltip": "Integer scale factor for upscaling (2x or 4x).",
                    "default": 2,
                }),
                "Model": (list(cls.RUNWARE_VUPSCALER_MODELS.keys()), {
                    "tooltip": "Select the video upscaler model to use.",
                    "default": "Bria Video Upscaler",
                }),
            },
            "optional": {
                "Output Format": (["mp4", "webm"], {
                    "default": "mp4",
                    "tooltip": "Choose the output video format.",
                }),
            }
        }

    DESCRIPTION = "Enhance the resolution and quality of your videos using Runware's advanced upscaling API."
    FUNCTION = "upscale"
    RETURN_TYPES = ("VIDEO",)
    RETURN_NAMES = ("VIDEO",)
    CATEGORY = "Runware"

    def upscale(self, **kwargs):
        video_uuid = kwargs.get("Video")
        upscaleFactor = kwargs.get("upscaleFactor", 2)
        modelName = kwargs.get("Model", "Bria Video Upscaler")
        outputFormat = kwargs.get("Output Format", "mp4")
        
        # Validate mediaUUID
        if not video_uuid or video_uuid.strip() == "":
            raise ValueError("Video mediaUUID is required")
        
        # Get the model AIR code
        modelAIR = self.RUNWARE_VUPSCALER_MODELS.get(modelName, "bria:50@1")
        
        # Build the API request
        genConfig = [
            {
                "taskType": "upscale",
                "taskUUID": rwUtils.genRandUUID(),
                "upscaleFactor": upscaleFactor,
                "inputs": {
                    "video": video_uuid
                },
                "outputType": "URL",
                "outputFormat": outputFormat.upper(),
                "model": modelAIR,
                "includeCost": True
            }
        ]
        
        try:
            # Debug: Print the request being sent
            print(f"[DEBUG] Sending Video Upscale Request:")
            print(f"[DEBUG] Request Payload: {json.dumps(genConfig, indent=2)}")
            
            genResult = rwUtils.inferenecRequest(genConfig)
            
            # Debug: Print the response received
            print(f"[DEBUG] Received Video Upscale Response:")
            print(f"[DEBUG] Response: {json.dumps(genResult, indent=2)}")
            
            # Check for errors
            if "errors" in genResult:
                error_message = genResult["errors"][0]["message"]
                raise Exception(f"Video upscale failed: {error_message}")
            
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
                    raise Exception(f"Video upscale failed: {error_message}")
                
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
            print(f"[Error] Video upscale failed: {str(e)}")
            raise e

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareVideoUpscaler": videoUpscaler,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVideoUpscaler": "Runware Video Upscaler",
}

