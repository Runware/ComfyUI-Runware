from .utils import runwareUtils as rwUtils
import comfy.model_management


class videoTranscription:
    RUNWARE_VIDEO_TRANSCRIPTION_MODELS = {
        "Memories Video Captioning": "memories:1@1",
        "Memories Age Detection": "memories:2@1",
    }

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Video transcription will appear here automatically.",
                    "tooltip": "The video transcription will be loaded here automatically."
                }),
                "video": ("STRING", {
                    "default": "",
                    "placeholder": "Enter video URL, file path, or Runware video UUID",
                    "tooltip": "The video to transcribe. Can be a URL, file path, or Runware video UUID."
                }),
                "model": (list(cls.RUNWARE_VIDEO_TRANSCRIPTION_MODELS.keys()), {
                    "default": "Memories Video Captioning",
                    "tooltip": "Choose the model to use for video transcription."
                }),
            },
            "hidden": { "node_id": "UNIQUE_ID" }
        }

    DESCRIPTION = "Transcribe spoken audio and visual context from videos into accurate text with speaker labeling and optional chapter summaries."

    FUNCTION = "transcribeVideo"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Video Caption",)
    CATEGORY = "Runware"
    OUTPUT_NODE = True

    def transcribeVideo(self, **kwargs):
        video = kwargs.get("video", "")
        modelKey = kwargs.get("model", "Memories Video Captioning")
        model = self.RUNWARE_VIDEO_TRANSCRIPTION_MODELS.get(modelKey, modelKey)
        
        if not video or not video.strip():
            raise Exception("Video URL, file path, or UUID is required")
        
        # Create task parameters with correct structure
        task_params = {
            "taskType": "caption",
            "taskUUID": rwUtils.genRandUUID(),
            "model": model,
            "inputs": {
                "video": video
            }
        }

        # Send the task
        genConfig = [task_params]
        
        # Debug: Print the request being sent
        print(f"[DEBUG] Sending Video Transcription Request:")
        print(f"[DEBUG] Request Payload: {rwUtils.safe_json_dumps(genConfig, indent=2)}")
        
        try:
            genResult = rwUtils.inferenecRequest(genConfig)
            
            # Debug: Print the response received
            print(f"[DEBUG] Received Video Transcription Response:")
            print(f"[DEBUG] Response: {rwUtils.safe_json_dumps(genResult, indent=2)}")
        except Exception as e:
            raise e
        
        # Get task UUID for polling
        taskUUID = task_params["taskUUID"]
        
        # Poll for result
        while True:
            # Check for interrupt before each poll
            comfy.model_management.throw_exception_if_processing_interrupted()
            
            # Poll for result
            pollResult = rwUtils.pollVideoResult(taskUUID)
            print(f"[Debugging] Poll result: {pollResult}")
            
            # Check for errors first
            if pollResult and "errors" in pollResult and len(pollResult["errors"]) > 0:
                error_info = pollResult["errors"][0]
                error_message = error_info.get("message", "Unknown error")
                raise Exception(f"Video transcription failed: {error_message}")
            
            # Check if we have data
            if pollResult and "data" in pollResult and len(pollResult["data"]) > 0:
                data = pollResult["data"][0]
                
                # Check status
                if "status" in data:
                    status = data["status"]
                    
                    if status == "success":
                        # Handle both text (video captioning) and structuredData (age detection) outputs
                        outputText = None
                        
                        if "text" in data:
                            # Video captioning result
                            outputText = data["text"]
                        elif "structuredData" in data:
                            # Age detection result - format as readable text
                            structuredData = data["structuredData"]
                            ageGroup = structuredData.get("ageGroup", "Unknown")
                            confidence = structuredData.get("confidence", 0.0)
                            outputText = f"Age Group: {ageGroup}\nConfidence: {confidence:.2%}"
                        
                        if outputText:
                            # Send transcription result
                            rwUtils.sendVideoTranscription(outputText, kwargs.get("node_id"))
                            return (outputText,)
                        else:
                            raise Exception("No valid output (text or structuredData) in successful response")
                    elif status == "processing":
                        # Continue polling
                        pass
                    else:
                        # Error or other status
                        raise Exception(f"Unexpected status: {status}")
            
            # Check for interrupt before waiting
            comfy.model_management.throw_exception_if_processing_interrupted()
            
            # Wait before next poll
            for _ in range(10):  # 10 x 0.1 second = 1 second total
                comfy.model_management.throw_exception_if_processing_interrupted()
                rwUtils.time.sleep(0.1)

