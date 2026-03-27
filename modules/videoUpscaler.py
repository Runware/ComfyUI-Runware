from .utils import runwareUtils as rwUtils
import comfy.model_management

class videoUpscaler:
    RUNWARE_VUPSCALER_MODELS = {
        "Bria Video Upscaler": "bria:50@1",
        "Bytedance Video Upscaler": "bytedance:50@1",
        "Topaz Labs Starlight Precise 2.5": "topazlabs:starlight-precise@2.5",
    }
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Video": ("STRING", {
                    "tooltip": "MediaUUID from Runware Media Upload node for the video to upscale."
                }),
                "Model": (list(cls.RUNWARE_VUPSCALER_MODELS.keys()), {
                    "tooltip": "Select the video upscaler model to use.",
                    "default": "Bria Video Upscaler",
                }),
                "useUpscaleFactor": ("BOOLEAN", {
                    "label_on": "Yes",
                    "label_off": "No",
                    "tooltip": "Enable to explicitly set the upscale factor for the request.",
                    "default": False,
                }),
                "useFps": ("BOOLEAN", {
                    "label_on": "Yes",
                    "label_off": "No",
                    "tooltip": "Enable to explicitly set FPS for the output video.",
                    "default": False,
                }),
                "useDimension": (["none", "custom"], {
                    "tooltip": "Choose whether to send custom width and height.",
                    "default": "none",
                }),
            },
            "optional": {
                "upscaleFactor": ([2, 4], {
                    "tooltip": "Integer scale factor for upscaling (2x or 4x).",
                    "default": 2,
                }),
                "fps": ("INT", {
                    "default": 24,
                    "min": 1,
                    "max": 240,
                    "step": 1,
                    "tooltip": "Output frames per second (1-240). Used when useFps is enabled.",
                }),
                "width": ("INT", {
                    "default": 1920,
                    "min": 1,
                    "max": 8192,
                    "step": 1,
                    "tooltip": "Custom output width in pixels. Used when useDimension is custom.",
                }),
                "height": ("INT", {
                    "default": 1080,
                    "min": 1,
                    "max": 8192,
                    "step": 1,
                    "tooltip": "Custom output height in pixels. Used when useDimension is custom.",
                }),
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
        useUpscaleFactor = kwargs.get("useUpscaleFactor", False)
        upscaleFactor = kwargs.get("upscaleFactor")
        useFps = kwargs.get("useFps", False)
        fps = kwargs.get("fps", 24)
        useDimension = kwargs.get("useDimension", "none")
        width = kwargs.get("width", 1920)
        height = kwargs.get("height", 1080)
        modelName = kwargs.get("Model", "Bria Video Upscaler")
        outputFormat = kwargs.get("Output Format", "mp4")
        
        # Validate mediaUUID
        if not video_uuid or video_uuid.strip() == "":
            raise ValueError("Video mediaUUID is required")
        
        # Get the model AIR code
        modelAIR = self.RUNWARE_VUPSCALER_MODELS.get(modelName, "bria:50@1")
        
        # Build the API request
        task_payload = {
            "taskType": "upscale",
            "taskUUID": rwUtils.genRandUUID(),
            "inputs": {
                "video": video_uuid
            },
            "outputFormat": outputFormat.upper(),
            "model": modelAIR,
            "includeCost": True
        }

        if useUpscaleFactor:
            if upscaleFactor in (2, 4):
                task_payload["upscaleFactor"] = upscaleFactor
            else:
                raise ValueError("upscaleFactor must be 2 or 4 when useUpscaleFactor is enabled.")

        if useFps:
            if isinstance(fps, int) and 1 <= fps <= 240:
                task_payload["fps"] = fps
            else:
                raise ValueError("fps must be an integer between 1 and 240 when useFps is enabled.")

        if useDimension == "custom":
            if isinstance(width, int) and isinstance(height, int) and width > 0 and height > 0:
                task_payload["width"] = width
                task_payload["height"] = height
            else:
                raise ValueError("width and height must be positive integers when useDimension is custom.")
        elif useDimension != "none":
            raise ValueError("useDimension must be either 'none' or 'custom'.")

        genConfig = [task_payload]
        
        try:
            # Debug: Print the request being sent
            print(f"[DEBUG] Sending Video Upscale Request:")
            print(f"[DEBUG] Request Payload: {rwUtils.safe_json_dumps(genConfig, indent=2)}")
            
            genResult = rwUtils.inferenecRequest(genConfig)
            
            # Debug: Print the response received
            print(f"[DEBUG] Received Video Upscale Response:")
            print(f"[DEBUG] Response: {rwUtils.safe_json_dumps(genResult, indent=2)}")
            
            # Check for errors
            if "errors" in genResult:
                error_message = genResult["errors"][0]["message"]
                raise Exception(f"Video upscale failed: {error_message}")
            
            # Extract task UUID for polling
            taskUUID = genConfig[0]["taskUUID"]
            max_poll_seconds = 2400  # 40 minutes
            started_at = rwUtils.time.time()
            
            # Poll for video completion
            while True:
                if rwUtils.time.time() - started_at > max_poll_seconds:
                    raise TimeoutError(
                        f"Video upscale timed out after {max_poll_seconds} seconds. "
                        f"Task UUID: {taskUUID}"
                    )

                # Check for interrupt before each poll
                comfy.model_management.throw_exception_if_processing_interrupted()
                
                # Poll for video result
                pollResult = rwUtils.pollVideoResult(taskUUID)
                print(f"[Debugging] Poll result: {pollResult}")

                if not isinstance(pollResult, dict):
                    # Keep polling if transport layer returned empty/invalid payload.
                    for _ in range(10):
                        comfy.model_management.throw_exception_if_processing_interrupted()
                        rwUtils.time.sleep(0.1)
                    continue
                
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
                            if "mediaURL" in video_data or "videoURL" in video_data or "videoBase64Data" in video_data:
                                out_width = width if useDimension == "custom" else video_data.get("width", 1920)
                                out_height = height if useDimension == "custom" else video_data.get("height", 1080)
                                videos = rwUtils.convertVideoB64List(pollResult, out_width, out_height)
                                # SaveVideo expects a single video object, not a tuple
                                return (videos[0],) if len(videos) > 0 else (None,)
                            raise Exception(
                                "Video upscale returned success without mediaURL/videoURL/videoBase64Data. "
                                f"Response: {rwUtils.safe_json_dumps(video_data, indent=2)}"
                            )
                        if status in ("failed", "error", "cancelled", "canceled"):
                            raise Exception(
                                "Video upscale failed with terminal status "
                                f"'{status}'. Response: {rwUtils.safe_json_dumps(video_data, indent=2)}"
                            )
                        
                        # If status is "processing" (or unknown transient), continue polling
                
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

