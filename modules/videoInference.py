from .utils import runwareUtils as rwUtils
from .videoModelSearch import videoModelSearch
import comfy.model_management


class txt2vid:
    @staticmethod
    def _format_reference_images(referenceImages, model):
        """
        Shape referenceImages based on model requirements:
        - skywork:skyreels@v4 -> grouped objects [{type, tag, images, audio?}]
        - others -> flat list[str] (legacy behavior)
        """
        if referenceImages is None:
            return []

        if not isinstance(referenceImages, list):
            referenceImages = [referenceImages]

        is_skyreels = isinstance(model, str) and model.strip().lower() == "skywork:skyreels@v4"

        if is_skyreels:
            grouped = []
            for idx, ref in enumerate(referenceImages, start=1):
                images = []
                ref_type = "image"
                ref_tag = f"@image{idx}"
                ref_audio = ""

                if isinstance(ref, str):
                    if ref.strip():
                        images = [ref.strip()]
                elif isinstance(ref, dict):
                    ref_type = (str(ref.get("type", "image")).strip() or "image")
                    raw_tag = str(ref.get("tag", "")).strip()
                    ref_tag = raw_tag if raw_tag else ref_tag
                    if not ref_tag.startswith("@"):
                        ref_tag = f"@{ref_tag}"

                    raw_audio = ref.get("audio", "")
                    if isinstance(raw_audio, str) and raw_audio.strip():
                        ref_audio = raw_audio.strip()

                    image_value = ref.get("image")
                    if isinstance(image_value, str) and image_value.strip():
                        images.append(image_value.strip())

                    image_group = ref.get("images")
                    if isinstance(image_group, list):
                        for item in image_group:
                            if isinstance(item, str) and item.strip():
                                images.append(item.strip())

                if not images:
                    continue

                group = {
                    "type": ref_type,
                    "tag": ref_tag,
                    "images": images[:5],  # provider limit: max 5
                }
                if ref_audio:
                    group["audio"] = ref_audio
                grouped.append(group)

            return grouped

        # Legacy/default path: flatten to list of image strings
        flattened = []
        for ref in referenceImages:
            if isinstance(ref, str):
                if ref.strip():
                    flattened.append(ref.strip())
            elif isinstance(ref, dict):
                image_value = ref.get("image")
                if isinstance(image_value, str) and image_value.strip():
                    flattened.append(image_value.strip())

                image_group = ref.get("images")
                if isinstance(image_group, list):
                    for item in image_group:
                        if isinstance(item, str) and item.strip():
                            flattened.append(item.strip())
        return flattened

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Model": ("RUNWAREVIDEOMODEL", {
                    "tooltip": "Connect a Runware Video Model From Runware Video Model Search Node.",
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
                "useDuration": ("BOOLEAN", {
                    "tooltip": "Enable to include duration parameter in API request. Disable if your model doesn't support duration.",
                    "default": True,
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
                    "tooltip": "A value used to randomize the video generation. If you want to make videos reproducible (generate the same video multiple times), you can use the same seed value.",
                    "default": 1,
                    "min": 1,
                    "max": 2147483647,
                }),
                "useSteps": ("BOOLEAN", {
                    "tooltip": "Enable to include steps parameter in API request. Disable if your model doesn't support steps.",
                    "default": False,
                }),
                "steps": ("INT", {
                    "tooltip": "Number of inference steps for video generation. More steps generally result in higher quality but longer generation time.",
                    "default": 20,
                    "min": 1,
                    "max": 100,
                }),
                "useBatchSize": ("BOOLEAN", {
                    "tooltip": "Enable to include batchSize parameter in API request. Disable if your model doesn't support batch size.",
                    "default": False,
                }),
                "batchSize": ("INT", {
                    "tooltip": "The number of videos to generate in a single request. Only used when 'Use Batch Size' is enabled.",
                    "default": 1,
                    "min": 1,
                    "max": 4,
                }),
                "useSchedulers": ("BOOLEAN", {
                    "tooltip": "Enable to include scheduler parameter in API request. Disable if your model doesn't support scheduler.",
                    "default": False,
                }),
                "scheduler": (["euler", "dpm", "adams", "unipc"], {
                    "default": "euler",
                    "tooltip": "High-level scheduler name for video generation. Only used when 'Use Schedulers' is enabled.",
                }),
                "useCFGScale": ("BOOLEAN", {
                    "tooltip": "Enable to include guidance_scale (CFG) parameter in API request. Disable for No-CFG models.",
                    "default": False,
                }),
                "cfgScale": ("FLOAT", {
                    "tooltip": "Classifier-free guidance strength. Set to 1 for No-CFG models. For Duration 5 use 1; for Duration 10, 1-7 is valid. Default 5.",
                    "default": 5.0,
                    "min": 1.0,
                    "max": 7.0,
                    "step": 0.1,
                }),
                "acceleration": (["none", "low", "medium", "high"], {
                    "tooltip": "Applies optimized acceleration presets that automatically configure multiple generation parameters for the best speed and quality balance. This parameter serves as an abstraction layer that intelligently adjusts acceleratorOptions, steps, scheduler, and other underlying settings.\n\nAvailable values:\n- none: No acceleration applied, uses default parameter values.\n- low: Minimal acceleration with optimized settings for lowest quality loss.\n- medium: Balanced acceleration preset with moderate speed improvements.\n- high: Maximum acceleration with caching and aggressive optimizations for fastest generation.",
                    "default": "none",
                }),
            },
            "optional": {
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
                "referenceVideos": ("RUNWAREREFERENCEVIDEOS", {
                    "tooltip": "Connect reference video files for video generation.",
                }),
                "speech": ("RUNWAREVIDEOINFERENCESPEECHINPUT", {
                    "tooltip": "Connect a Runware Video Inference Speech Input node to set voice and text for speech synthesis.",
                }),
                "inputs": ("RUNWAREVIDEOINFERENCEINPUTS", {
                    "tooltip": "Connect a Runware Video Inference Inputs node to provide custom inputs like image, audio, mask, and parameters for OmniHuman 1.5 and other video models.",
                }),
                "safetyInputs": ("RUNWARESAFETYINPUTS", {
                    "tooltip": "Connect Runware Safety Inputs node to configure safety and content moderation settings.",
                }),
                "videoAdvancedFeatureInputs": ("RUNWAREVIDEOADVANCEDFEATUREINPUTS", {
                    "tooltip": "Connect Runware Video Advanced Feature Inputs node to configure advanced video features like CFG scales, FPS, negative prompts, and SLG layer settings.",
                }),
                "Accelerator": ("RUNWAREACCELERATOR", {
                    "tooltip": "Connect a Runware Accelerator Options Node to configure caching and acceleration settings.",
                }),
                "settings": ("RUNWAREVIDEOSETTINGS", {
                    "tooltip": "Connect a Runware Video Inference Settings node to configure draft, audio, promptUpsampling, voiceDescription, style, thinking, multiClip, shotType, promptExtend, syncMode, mode, emotion, temperature, occlusionDetection, tts, activeSpeakerDetection, segments, etc.",
                }),
            }
        }

    @classmethod
    def VALIDATE_INPUTS(cls, positivePrompt=None, negativePrompt=None):
        # Only validate if prompts are provided and not empty
        if positivePrompt is not None and positivePrompt.strip() != "":
            if len(positivePrompt) < 3 or len(positivePrompt) > 2000:
                raise Exception("Positive Prompt Must Be Between 3 And 2000 characters!")
        if negativePrompt is not None and negativePrompt.strip() != "":
            if len(negativePrompt) < 3 or len(negativePrompt) > 2000:
                raise Exception("Negative Prompt Must Be Between 3 And 2000 characters!")
        return True

    DESCRIPTION = "Generates Videos Lightning Fast With Runware Video Inference Engine."
    FUNCTION = "generateVideo"
    RETURN_TYPES = ("VIDEO", "RUNWARETASK", "RUNWARETASK")
    RETURN_NAMES = ("VIDEO", "RW-Task", "OUTPUT")
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
        referenceVideos = kwargs.get("referenceVideos", None)
        speech = kwargs.get("speech", None)
        inputs = kwargs.get("inputs", None)
        safetyInputs = kwargs.get("safetyInputs", None)
        videoAdvancedFeatureInputs = kwargs.get("videoAdvancedFeatureInputs", None)
        runwareAccelerator = kwargs.get("Accelerator", None)
        settings = kwargs.get("settings", None)
        useDuration = kwargs.get("useDuration", True)
        duration = kwargs.get("duration", 5)
        fps = kwargs.get("fps", 24)
        useFps = kwargs.get("useFps", True)
        outputFormat = kwargs.get("outputFormat", "mp4")
        seed = kwargs.get("seed", 1)
        useSeed = kwargs.get("useSeed", True)
        steps = kwargs.get("steps", 20)
        useSteps = kwargs.get("useSteps", False)
        useBatchSize = kwargs.get("useBatchSize", False)
        batchSize = kwargs.get("batchSize", 1)
        useSchedulers = kwargs.get("useSchedulers", False)
        scheduler = kwargs.get("scheduler", "euler")
        useCFGScale = kwargs.get("useCFGScale", False)
        cfgScale = kwargs.get("cfgScale", 5.0)
        acceleration = kwargs.get("acceleration", "none")
        
        # Handle model input - could be dict or string
        if isinstance(runwareVideoModel, dict):
            model = runwareVideoModel.get("model", "")
            width = runwareVideoModel.get("width")
            height = runwareVideoModel.get("height")
            useResolution = runwareVideoModel.get("useResolution", False)
            resolution = runwareVideoModel.get("resolution", None)
        else:
            model = runwareVideoModel
            width = None
            height = None
            useResolution = False
            resolution = None

        genConfig = [
            {
                "taskType": "videoInference",
                "taskUUID": rwUtils.genRandUUID(),
                "model": model,
                "outputFormat": outputFormat,
                "includeCost": True,
            }
        ]
        
        # Add batchSize (numberResults) only if enabled
        if useBatchSize:
            genConfig[0]["numberResults"] = batchSize
        
        # Add resolution if enabled
        if useResolution and resolution:
            genConfig[0]["resolution"] = resolution
        
        # Add width/height if not using resolution (or if resolution is not provided)
        if (
            width is not None and height is not None
            and width > 0 and height > 0
        ):
            genConfig[0]['height'] = height
            genConfig[0]['width'] = width
        
        # Only add positivePrompt if it's not empty
        if positivePrompt and positivePrompt.strip() != "":
            genConfig[0]["positivePrompt"] = positivePrompt
        
        # Add fps parameter only if enabled
        if useFps:
            genConfig[0]["fps"] = fps
        
        # Add duration parameter - unified for all models
        if useDuration:
            genConfig[0]["duration"] = duration
        
        # Add seed parameter only if enabled
        if useSeed:
            genConfig[0]["seed"] = seed
        
        # Add steps parameter only if enabled
        if useSteps:
            genConfig[0]["steps"] = steps

        # Add scheduler parameter only if enabled
        if useSchedulers:
            genConfig[0]["scheduler"] = scheduler

        # Add CFGScale parameter only if enabled
        if useCFGScale:
            genConfig[0]["CFGScale"] = cfgScale

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
            print(f"[Debugging] Frame images array: {rwUtils.sanitize_for_logging(frameImages)}")
        # Add referenceImages if provided from Runware Reference Images node
        if referenceImages is not None and len(referenceImages) > 0:
            formattedReferenceImages = self._format_reference_images(referenceImages, model)
            if len(formattedReferenceImages) > 0:
                genConfig[0]["referenceImages"] = formattedReferenceImages
                print(f"[Debugging] Reference images array: {rwUtils.sanitize_for_logging(formattedReferenceImages)}")
        # Add inputAudios if provided
        if inputAudios is not None and len(inputAudios) > 0:
            genConfig[0]["inputAudios"] = inputAudios
            print(f"[Debugging] Input audios array: {rwUtils.sanitize_for_logging(inputAudios)}")
        
        # Add referenceVideos if provided and not empty
        if referenceVideos is not None:
            # Handle both single mediaUUID (string) and multiple mediaUUIDs (list)
            if isinstance(referenceVideos, str) and referenceVideos.strip() != "":
                genConfig[0]["referenceVideos"] = [referenceVideos.strip()]
                print(f"[Debugging] Reference videos: {rwUtils.sanitize_for_logging(genConfig[0].get('referenceVideos', []))}")
            elif isinstance(referenceVideos, list) and len(referenceVideos) > 0:
                genConfig[0]["referenceVideos"] = referenceVideos
                print(f"[Debugging] Reference videos: {rwUtils.sanitize_for_logging(genConfig[0].get('referenceVideos', []))}")
        
        # Add speech parameters if provided from Runware Video Inference Speech Input node
        if speech is not None and isinstance(speech, dict) and speech:
            genConfig[0]["speech"] = speech
            print(f"[Debugging] Speech parameters: {rwUtils.sanitize_for_logging(speech)}")

        # Handle inputs - merge custom inputs from Video Inference Inputs node
        if inputs is not None:
            # Merge inputs from video inference inputs node
            if "inputs" not in genConfig[0]:
                genConfig[0]["inputs"] = {}
            
            # Merge each input from inputs (only actual input data, not provider settings)
            for key, value in inputs.items():
                # Normalize referenceImages:
                # - skyreels -> grouped objects
                # - others -> flat string[] payload
                if key == "referenceImages":
                    formatted_input_refs = self._format_reference_images(value, model)
                    if len(formatted_input_refs) > 0:
                        genConfig[0]["inputs"][key] = formatted_input_refs
                    continue
                genConfig[0]["inputs"][key] = value
            
            print(f"[Debugging] Video inference inputs merged: {rwUtils.sanitize_for_logging(inputs)}")
            print(f"[Debugging] Final genConfig inputs: {rwUtils.sanitize_for_logging(genConfig[0].get('inputs', {}))}")
        
        # Handle providerSettings - extract provider name from model and merge with custom settings
        if providerSettings is not None:
            provider_name = model.split(":")[0] if ":" in model else model

            if isinstance(providerSettings, dict):
                if provider_name in providerSettings:
                    final_provider_settings = providerSettings
                else:
                    final_provider_settings = {provider_name: providerSettings}

                if final_provider_settings:
                    genConfig[0]["providerSettings"] = final_provider_settings
                    print(f"[Debugging] Provider settings: {rwUtils.sanitize_for_logging(final_provider_settings)}")
            else:
                genConfig[0]["providerSettings"] = providerSettings
        
        # Add safety inputs if provided
        # Note: Video inference API only supports 'mode' key for safety
        if safetyInputs is not None and isinstance(safetyInputs, dict) and len(safetyInputs) > 0:
            # Filter to only include 'mode' (only allowed key for video inference)
            filtered_safety = {}
            if "mode" in safetyInputs:
                filtered_safety["mode"] = safetyInputs["mode"]
            if filtered_safety:
                genConfig[0]["safety"] = filtered_safety
        
        # Add video advanced feature inputs if provided
        if videoAdvancedFeatureInputs is not None and isinstance(videoAdvancedFeatureInputs, dict) and len(videoAdvancedFeatureInputs) > 0:
            genConfig[0]["advancedFeatures"] = videoAdvancedFeatureInputs
        
        # Add accelerator options if provided
        if runwareAccelerator is not None and isinstance(runwareAccelerator, dict) and len(runwareAccelerator) > 0:
            genConfig[0]["acceleratorOptions"] = runwareAccelerator

        # Add settings if provided (draft, audio, promptUpsampling, voiceDescription, ...)
        if settings is not None and isinstance(settings, dict) and len(settings) > 0:
            genConfig[0]["settings"] = settings
        
        # Add acceleration if not "none"
        if acceleration and acceleration != "none":
            genConfig[0]["acceleration"] = acceleration

        if (multiInferenceMode):
            return (None, genConfig, None)
        else:
            try:
                # Debug: Print the request being sent
                print(f"[DEBUG] Sending Video Inference Request:")
                print(f"[DEBUG] Request Payload: {rwUtils.safe_json_dumps(genConfig, indent=2)}")
                
                genResult = rwUtils.inferenecRequest(genConfig)
                
                # Debug: Print the response received
                print(f"[DEBUG] Received Video Inference Response:")
                print(f"[DEBUG] Response: {rwUtils.safe_json_dumps(genResult, indent=2)}")
                
                print(f"[Debugging] Generation config: {rwUtils.safe_json_dumps(genConfig, indent=2)}")
            except Exception as e:
                # Re-raise the original error without modification
                raise e
            
            # Extract task UUID for polling
            taskUUID = genConfig[0]["taskUUID"]
            
            # Poll for video completion
            while True:
                # Check for interrupt before each poll
                comfy.model_management.throw_exception_if_processing_interrupted()
                
                # Poll for video result
                pollResult = rwUtils.pollVideoResult(taskUUID)
                print(f"[Debugging] Poll result: {rwUtils.safe_json_dumps(pollResult, indent=2) if isinstance(pollResult, (dict, list)) else pollResult}")
                
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
                                # SaveVideo expects a single video object, not a tuple
                                video_output = videos[0] if len(videos) > 0 else None
                                return (video_output, genConfig, pollResult)
                        
                        # If status is "processing", continue polling
                
                # Check for interrupt before waiting
                comfy.model_management.throw_exception_if_processing_interrupted()
                
                # Wait before next poll (split into smaller chunks to allow more frequent interrupt checks)
                for _ in range(10):  # 10 x 0.1 second = 1 second total
                    comfy.model_management.throw_exception_if_processing_interrupted()
                    rwUtils.time.sleep(0.1) 


# Node class mappings for ComfyUI registration
NODE_CLASS_MAPPINGS = {
    "txt2vid": txt2vid,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "txt2vid": "Runware Video Inference",
}