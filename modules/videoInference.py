from .utils import runwareUtils as rwUtils
from .videoModelSearch import videoModelSearch
import json
import comfy.model_management


class RunwareFrameImages:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "image1": ("IMAGE", {
                    "tooltip": "First frame image. When only one image is provided, it becomes the first frame automatically.",
                }),
                "frame1_position": (["auto", "first", "last"], {
                    "default": "auto",
                    "tooltip": "Position for the first image. 'auto' uses automatic distribution rules.",
                }),
                "image2": ("IMAGE", {
                    "tooltip": "Second frame image. With two images, they become first and last frames automatically.",
                }),
                "frame2_position": (["auto", "first", "last"], {
                    "default": "auto", 
                    "tooltip": "Position for the second image. 'auto' uses automatic distribution rules.",
                }),
                "image3": ("IMAGE", {
                    "tooltip": "Third frame image. Will be distributed between first and last frames.",
                }),
                "frame3_position": (["auto", "first", "last"], {
                    "default": "auto",
                    "tooltip": "Position for the third image. 'auto' uses automatic distribution rules.",
                }),
                "image4": ("IMAGE", {
                    "tooltip": "Fourth frame image. Will be distributed between first and last frames.",
                }),
                "frame4_position": (["auto", "first", "last"], {
                    "default": "auto",
                    "tooltip": "Position for the fourth image. 'auto' uses automatic distribution rules.",
                }),
            }
        }
    
    DESCRIPTION = "Configure frame images for video generation with precise positioning control. Supports automatic distribution or manual positioning."
    FUNCTION = "create_frame_images"
    RETURN_TYPES = ("RUNWAREFRAMEIMAGES",)
    RETURN_NAMES = ("Frame Images",)
    CATEGORY = "Runware"
    
    def create_frame_images(self, **kwargs):
        frame_images = []
        
        # Process each image input
        for i in range(1, 5):  # Support up to 4 images
            image_key = f"image{i}"
            position_key = f"frame{i}_position"
            
            image = kwargs.get(image_key)
            position = kwargs.get(position_key, "auto")
            
            if image is not None:
                # Upload image and get UUID
                image_uuid = rwUtils.convertTensor2IMGForVideo(image)
                image_url = f"https://im.runware.ai/image/ii/{image_uuid}.webp"
                
                frame_data = {
                    "inputImage": image_url
                }
                
                # Only add frame position if not auto
                if position != "auto":
                    frame_data["frame"] = position
                
                frame_images.append(frame_data)
        
        return (frame_images,)


class txt2vid:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Model": ("RUNWAREVIDEOMODEL", {
                    "tooltip": "Connect a Runware Video Model From Runware Video Model Search Node.",
                }),
                "positivePrompt": ("STRING", {
                    "multiline": True,
                    "placeholder": "Positive Prompt: a text instruction to guide the model on generating the video. It is usually a sentence or a paragraph that provides positive guidance for the task. This parameter is essential to shape the desired results.\n\nYou Can Press (Ctrl + Alt + E) To Enhance The Prompt!",
                    "tooltip": "Positive Prompt: a text instruction to guide the model on generating the video. You Can Also Press (Ctrl + Alt + E) To Enhance The Prompt!"
                }),
                "negativePrompt": ("STRING", {
                    "multiline": True,
                    "placeholder": "Negative Prompt: a text instruction to guide the model on generating the video. It is usually a sentence or a paragraph that provides negative guidance for the task. This parameter helps to avoid certain undesired results.",
                    "tooltip": "Negative Prompt: a text instruction to guide the model on generating the video."
                }),
                "Multi Inference Mode": ("BOOLEAN", {
                    "tooltip": "If Enabled the node will skip the video generation process and will only return the Runware Task Object to be used in the Multi Inference Node.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "Prompt Weighting": (["Disabled", "sdEmbeds", "Compel"], {
                    "default": "Disabled",
                    "tooltip": "Prompt weighting allows you to adjust how strongly different parts of your prompt influence the generated video.\n\nChoose between \"compel\" notation with advanced weighting operations or \"sdEmbeds\" for simple emphasis adjustments.\n\nCompel Example: \"small+ dog, pixar style\"\n\nsdEmbeds Example: \"(small:2.5) dog, pixar style\"",
                }),
                "useCustomDimensions": ("BOOLEAN", {
                    "tooltip": "Model Default: Uses optimal dimensions for selected model. Custom: Uses width/height values below.",
                    "default": False,
                    "label_on": "Custom",
                    "label_off": "Model Default",
                }),
                "width": ("INT", {
                    "tooltip": "Width in pixels. Only used when 'Custom' is selected above.",
                    "default": 1024,
                    "min": 256,
                    "max": 1920,
                    "step": 1,
                }),
                "height": ("INT", {
                    "tooltip": "Height in pixels. Only used when 'Custom' is selected above.",
                    "default": 576,
                    "min": 256,
                    "max": 1920,
                    "step": 1,
                }),
                "duration": ("INT", {
                    "tooltip": "The duration of the video in seconds.",
                    "default": 5,
                    "min": 1,
                    "max": 30,
                }),
                "useFps": ("BOOLEAN", {
                    "tooltip": "Enable to include fps parameter in API request. Disable if your model doesn't support fps.",
                    "default": True,
                }),
                "fps": ("INT", {
                    "tooltip": "Frames per second for the generated video. Only used when 'Use FPS' is enabled.",
                    "default": 24,
                    "min": 8,
                    "max": 60,
                }),
                "outputFormat": (["mp4", "webm", "mov"], {
                    "default": "mp4",
                    "tooltip": "Choose the output video format.",
                }),
                "useSeed": ("BOOLEAN", {
                    "tooltip": "Enable to include seed parameter in API request. Disable if your model doesn't support seed.",
                    "default": True,
                }),
                "seed": ("INT", {
                    "tooltip": "A value used to randomize the video generation. If you want to make videos reproducible (generate the same video multiple times), you can use the same seed value. Leave empty or 0 to auto-generate.",
                    "default": 1,
                    "min": 1,
                    "max": 9223372036854776000,
                }),
                "batchSize": ("INT", {
                    "tooltip": "The number of videos to generate in a single request.",
                    "default": 1,
                    "min": 1,
                    "max": 4,
                }),
            },
            "optional": {
                "frameImages": ("RUNWAREFRAMEIMAGES", {
                    "tooltip": "Frame images configuration from Runware Frame Images node. Allows precise control over frame positioning.",
                }),
                "referenceImages": ("RUNWAREREFERENCEIMAGES", {
                    "tooltip": "Connect a Runware Reference Images node to provide reference images for the subject. These reference images help the AI maintain identity consistency during the video generation process.",
                }),
                "providerSettings": ("RUNWAREPROVIDERSETTINGS", {
                    "tooltip": "Connect a Runware Provider Settings node to configure provider-specific parameters.",
                }),
                "inputAudios": ("RUNWAREINPUTAUDIOS", {
                    "tooltip": "Connect input audio files for video generation with audio synchronization.",
                }),
            }
        }

    @classmethod
    def VALIDATE_INPUTS(cls, positivePrompt, negativePrompt):
        if (positivePrompt is not None and (positivePrompt == "" or len(positivePrompt) < 3 or len(positivePrompt) > 2000)):
            raise Exception(
                "Positive Prompt Must Be Between 3 And 2000 characters!")
        if (negativePrompt is not None and negativePrompt != "" and (len(negativePrompt) < 3 or len(negativePrompt) > 2000)):
            raise Exception(
                "Negative Prompt Must Be Between 3 And 2000 characters!")
        return True

    DESCRIPTION = "Generates Videos Lightning Fast With Runware Video Inference Engine."
    FUNCTION = "generateVideo"
    RETURN_TYPES = ("VIDEO", "RUNWARETASK")
    RETURN_NAMES = ("VIDEO", "RW-Task")
    CATEGORY = "Runware"

    def generateVideo(self, **kwargs):
        runwareVideoModel = kwargs.get("Model")
        positivePrompt = kwargs.get("positivePrompt")
        negativePrompt = kwargs.get("negativePrompt", None)
        multiInferenceMode = kwargs.get("Multi Inference Mode", False)
        promptWeighting = kwargs.get("Prompt Weighting", "Disabled")
        providerSettings = kwargs.get("providerSettings", None)
        frameImages = kwargs.get("frameImages", None)
        referenceImages = kwargs.get("referenceImages", None)
        inputAudios = kwargs.get("inputAudios", None)
        useCustomDimensions = kwargs.get("useCustomDimensions", False)
        customWidth = kwargs.get("width", 864)
        customHeight = kwargs.get("height", 480)
        duration = kwargs.get("duration", 5)
        fps = kwargs.get("fps", 24)
        useFps = kwargs.get("useFps", True)
        outputFormat = kwargs.get("outputFormat", "mp4")
        batchSize = kwargs.get("batchSize", 1)
        seed = kwargs.get("seed", 1)
        useSeed = kwargs.get("useSeed", True)
        
        # Handle model input - could be dict or string
        if isinstance(runwareVideoModel, dict):
            model = runwareVideoModel.get("model", "")
        else:
            model = runwareVideoModel
        
        # Determine dimensions based on custom setting
        if useCustomDimensions:
            width = customWidth
            height = customHeight
        else:
            

            model_dimensions = videoModelSearch.MODEL_DIMENSIONS.get(model, {"width": 1024, "height": 576})
            width = model_dimensions["width"]
            height = model_dimensions["height"]
        
        genConfig = [
            {
                "taskType": "videoInference",
                "taskUUID": rwUtils.genRandUUID(),
                "positivePrompt": positivePrompt,
                "height": height,
                "width": width,
                "model": model,
                "outputFormat": outputFormat,
                "numberResults": batchSize,
                "includeCost": True,
            }
        ]
        
        # Add fps parameter only if enabled
        if useFps:
            genConfig[0]["fps"] = fps
        
        # Add duration parameter - unified for all models
        genConfig[0]["duration"] = duration
        
        # Add seed parameter only if enabled
        
        if useSeed:
            genConfig[0]["seed"] = seed

        if (negativePrompt is not None and negativePrompt != ""):
            genConfig[0]["negativePrompt"] = negativePrompt
        if (promptWeighting != "Disabled"):
            if (promptWeighting == "sdEmbeds"):
                genConfig[0]["promptWeighting"] = "sdEmbeds"
            else:
                genConfig[0]["promptWeighting"] = "compel"
        # Add frameImages if provided from Runware Frame Images node
        if frameImages is not None and len(frameImages) > 0:
            genConfig[0]["frameImages"] = frameImages
            print(f"[Debugging] Frame images array: {frameImages}")
        # Add referenceImages if provided from Runware Reference Images node
        if referenceImages is not None and len(referenceImages) > 0:
            genConfig[0]["referenceImages"] = referenceImages
            print(f"[Debugging] Reference images array: {referenceImages}")
        # Add inputAudios if provided
        if inputAudios is not None and len(inputAudios) > 0:
            genConfig[0]["inputAudios"] = inputAudios
            print(f"[Debugging] Input audios array: {inputAudios}")
        # Handle providerSettings - extract provider name from model and merge with custom settings
        if providerSettings is not None:
            # Extract provider name from model (e.g., "pixverse:1@1" -> "pixverse")
            provider_name = model.split(":")[0] if ":" in model else model
            
            # If providerSettings is a dictionary, create the correct API format
            if isinstance(providerSettings, dict):
                # Create the providerSettings object with provider name as key
                final_provider_settings = {
                    provider_name: providerSettings
                }
                genConfig[0]["providerSettings"] = final_provider_settings
                print(f"[Debugging] Provider settings: {final_provider_settings}")
            else:
                # If it's just a string, use it directly
                genConfig[0]["providerSettings"] = providerSettings

        if (multiInferenceMode):
            return (None, genConfig)
        else:
            try:
                # Debug: Print the request being sent
                print(f"[DEBUG] Sending Video Inference Request:")
                print(f"[DEBUG] Request Payload: {json.dumps(genConfig, indent=2)}")
                
                genResult = rwUtils.inferenecRequest(genConfig)
                
                # Debug: Print the response received
                print(f"[DEBUG] Received Video Inference Response:")
                print(f"[DEBUG] Response: {json.dumps(genResult, indent=2)}")
                
                print(f"[Debugging] Generation config: {genConfig}")
            except Exception as e:
                # Check if it's a dimension error and provide helpful information
                error_msg = str(e)
                if ("unsupported width" in error_msg.lower() or 
                    "unsupported height" in error_msg.lower() or 
                    "invalid width" in error_msg.lower() or 
                    "invalid height" in error_msg.lower() or
                    "dimension not supported" in error_msg.lower()):
                    # Get model default dimensions for comparison
                    model_dimensions = videoModelSearch.MODEL_DIMENSIONS.get(model, {"width": 1024, "height": 576})
                    expected_width = model_dimensions["width"]
                    expected_height = model_dimensions["height"]
                    
                    raise Exception(f"Error: Unsupported width/height combination for this model architecture. You used {width}x{height}, but {model} expects {expected_width}x{expected_height}. Please use 'Model Default' or set custom dimensions to {expected_width}x{expected_height}.")
                else:
                    # Re-raise the original error
                    raise e
            
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
                    
                    # Extract more detailed error info if available
                    if "responseContent" in error_info:
                        response_content = error_info["responseContent"]
                        # Handle both string and dict response content
                        if isinstance(response_content, str):
                            detailed_message = response_content
                        elif isinstance(response_content, dict):
                            detailed_message = response_content.get("message", str(response_content))
                        else:
                            detailed_message = str(response_content)
                        
                        if detailed_message:
                            error_message = f"{error_message}\nProvider Error: {detailed_message}"
                    
                    # Include taskUUID for debugging
                    task_uuid = error_info.get("taskUUID", "unknown")
                    raise Exception(f"Video generation failed (Task: {task_uuid}): {error_message}")
                
                if pollResult and "data" in pollResult and len(pollResult["data"]) > 0:
                    video_data = pollResult["data"][0]
                    
                    # Check status directly
                    if "status" in video_data:
                        status = video_data["status"]
                        
                        if status == "success":
                            if "videoURL" in video_data or "videoBase64Data" in video_data:
                                videos = rwUtils.convertVideoB64List(pollResult, width, height)
                                return videos
                        
                        # If status is "processing", continue polling
                
                # Check for interrupt before waiting
                comfy.model_management.throw_exception_if_processing_interrupted()
                
                # Wait before next poll (split into smaller chunks to allow more frequent interrupt checks)
                for _ in range(10):  # 10 x 0.1 second = 1 second total
                    comfy.model_management.throw_exception_if_processing_interrupted()
                    rwUtils.time.sleep(0.1) 


# Node class mappings for ComfyUI registration
NODE_CLASS_MAPPINGS = {
    "RunwareFrameImages": RunwareFrameImages,
    "txt2vid": txt2vid,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareFrameImages": "Runware Frame Images",
    "txt2vid": "Runware Video Inference",
}