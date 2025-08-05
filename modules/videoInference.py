from .utils import runwareUtils as rwUtils
from .videoModelSearch import videoModelSearch



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
                "fps": ("INT", {
                    "tooltip": "Frames per second for the generated video.",
                    "default": 24,
                    "min": 8,
                    "max": 60,
                }),
                "outputFormat": (["mp4", "webm", "mov"], {
                    "default": "mp4",
                    "tooltip": "Choose the output video format.",
                }),
                "batchSize": ("INT", {
                    "tooltip": "The number of videos to generate in a single request.",
                    "default": 1,
                    "min": 1,
                    "max": 4,
                }),
                "includeCost": ("BOOLEAN", {
                    "tooltip": "Include cost information in the response.",
                    "default": True,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "seed": ("INT", {
                    "tooltip": "A value used to randomize the video generation. If you want to make videos reproducible (generate the same video multiple times), you can use the same seed value. Note: Only supported by Wan models.",
                    "default": rwUtils.genRandSeed(),
                    "min": 1,
                    "max": 9223372036854776000,
                }),
            },
            "optional": {
                "firstImage": ("IMAGE", {
                    "tooltip": "Image to use as the first frame of the video.",
                }),
                "lastImage": ("IMAGE", {
                    "tooltip": "Image to use as the last frame of the video.",
                }),
                "providerSettings": ("DICT", {
                    "tooltip": "Provider-specific settings for video generation.",
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
        firstImage = kwargs.get("firstImage", None)
        lastImage = kwargs.get("lastImage", None)
        useCustomDimensions = kwargs.get("useCustomDimensions", False)
        customWidth = kwargs.get("width", 864)
        customHeight = kwargs.get("height", 480)
        duration = kwargs.get("duration", 5)
        fps = kwargs.get("fps", 24)
        outputFormat = kwargs.get("outputFormat", "mp4")
        batchSize = kwargs.get("batchSize", 1)
        includeCost = kwargs.get("includeCost", True)
        seed = kwargs.get("seed", 1)
        
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
                "fps": fps,
                "outputFormat": outputFormat,
                "numberResults": batchSize,
                "includeCost": includeCost,
            }
        ]
        
        # Add duration parameter - unified for all models
        genConfig[0]["duration"] = duration
        
        # Add seed parameter only for supported models
        
        if model in videoModelSearch.SEED_SUPPORTED_MODELS:
            genConfig[0]["seed"] = seed

        if (negativePrompt is not None and negativePrompt != ""):
            genConfig[0]["negativePrompt"] = negativePrompt
        if (promptWeighting != "Disabled"):
            if (promptWeighting == "sdEmbeds"):
                genConfig[0]["promptWeighting"] = "sdEmbeds"
            else:
                genConfig[0]["promptWeighting"] = "compel"
        # Build frameImages array from firstImage and lastImage parameters
        frameImages = []
        if (firstImage is not None):
            # Force upload to get UUID for video frame images
            firstImageUUID = rwUtils.convertTensor2IMGForVideo(firstImage)
            # Construct full URL with PNG extension
            firstImageURL = f"https://im.runware.ai/image/ii/{firstImageUUID}.webp"
            print(f"[Debugging] First image URL: {firstImageURL}")
            frameImages.append({
                "inputImage": firstImageURL
            })
            
        if (lastImage is not None):
            # Force upload to get UUID for video frame images
            lastImageUUID = rwUtils.convertTensor2IMGForVideo(lastImage)
            # Construct full URL with PNG extension
            lastImageURL = f"https://im.runware.ai/image/ii/{lastImageUUID}.webp"
            print(f"[Debugging] Last image URL: {lastImageURL}")
            frameImages.append({
                "inputImage": lastImageURL
            })
            
        if frameImages:
            genConfig[0]["frameImages"] = frameImages
            print(f"[Debugging] Frame images array: {frameImages}")
        if (providerSettings is not None):
            genConfig[0]["providerSettings"] = providerSettings

        if (multiInferenceMode):
            return (None, genConfig)
        else:
            try:
                genResult = rwUtils.inferenecRequest(genConfig)
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
                
                # Poll for video result
                pollResult = rwUtils.pollVideoResult(taskUUID)
                print(f"[Debugging] Poll result: {pollResult}")
                
                if pollResult and "data" in pollResult and len(pollResult["data"]) > 0:
                    video_data = pollResult["data"][0]
                    
                    # Check status directly
                    if "status" in video_data:
                        status = video_data["status"]
                        
                        if status == "success":
                            if "videoURL" in video_data or "videoBase64Data" in video_data:
                                videos = rwUtils.convertVideoB64List(pollResult, width, height)
                                return videos
                        elif status != "processing":
                            raise Exception(f"Video generation failed: {video_data.get('error', 'Unknown error')}")
                        # If status is "processing", continue polling
                
                # Wait before next poll
                rwUtils.time.sleep(1) 