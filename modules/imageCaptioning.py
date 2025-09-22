from .utils import runwareUtils as rwUtils

class imageCaptioning:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Always Recaption": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Enable this option to always recaption the image each time you run the workflow.",
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "Describe this image in detail",
                    "placeholder": "Enter the prompt for image captioning. You can provide multiple prompts separated by newlines.",
                    "tooltip": "The prompt(s) to guide the image captioning. Multiple prompts can be provided, each on a new line."
                }),
            },
            "optional": {
                "inputImages": ("IMAGE", {
                    "tooltip": "Connect multiple Load Image nodes here to caption multiple images at once."
                }),
                "inputImage": ("IMAGE", {
                    "tooltip": "Connect a single Load Image node here for convenience. If inputImages is provided, this will be ignored."
                }),
                "model": ("STRING", {
                    "default": "",
                    "placeholder": "Leave empty for default model (runware:150@1)",
                    "tooltip": "Optional: Specify the AIR model ID (e.g., runware:150@1, runware:150@2). Leave empty to use the default model."
                }),
                "template": ("STRING", {
                    "default": "",
                    "placeholder": "Optional template for structured output",
                    "tooltip": "Optional template to structure the caption output."
                }),
                "imageCaption": ("STRING", {
                    "multiline": True,
                    "placeholder": "Generated image caption will appear here automatically.",
                    "tooltip": "This field will be automatically populated with the generated image caption."
                }),
            },
            "hidden": { "node_id": "UNIQUE_ID" }
        }

    DESCRIPTION = "Advanced image captioning with support for multiple images, custom prompts, and model selection. Generate descriptive text from single or multiple images using customizable prompts and optional AIR models. Perfect for batch processing and structured output generation."

    FUNCTION = "imageCaptioning"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("IMAGE PROMPT",)
    CATEGORY = "Runware"
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(s, **kwargs):
        alwaysRecaption = kwargs.get("Always Recaption")
        if(alwaysRecaption):
            return float("NAN")
        return True

    def imageCaptioning(self, **kwargs):
        inputImages = kwargs.get("inputImages", None)
        inputImage = kwargs.get("inputImage", None)
        prompt = kwargs.get("prompt", "Describe this image in detail")
        model = kwargs.get("model", "")
        template = kwargs.get("template", "")
        
        # Handle multiple prompts - split by newlines
        prompt_list = [p.strip() for p in prompt.split('\n') if p.strip()]
        if not prompt_list:
            prompt_list = ["Describe this image in detail"]
        
        # Determine which images to use (following SDK logic)
        if inputImages is not None:
            images_to_process = inputImages
        elif inputImage is not None:
            # Single image provided via inputImage - convert to array
            images_to_process = [inputImage]
        else:
            raise Exception("Either inputImages or inputImage must be provided")
        
        # Set inputImage to inputImages[0] if not already provided
        actual_input_image = inputImage
        if actual_input_image is None and len(images_to_process) > 0:
            actual_input_image = images_to_process[0]
        
        # Convert images to base64 format
        converted_images = []
        for img in images_to_process:
            converted_images.append(rwUtils.convertTensor2IMG(img))
        
        # Create a dictionary with mandatory parameters
        task_params = {
            "taskType": "imageCaption",
            "taskUUID": rwUtils.genRandUUID(),
        }
        
        # Add either inputImage or inputImages, but not both (API requirement)
        if len(converted_images) == 1:
            # Single image - use inputImage parameter
            task_params["inputImage"] = converted_images[0]
        else:
            # Multiple images - use inputImages parameter
            task_params["inputImages"] = converted_images

        # Add model parameter only if specified - backend handles default
        if model and model.strip():
            task_params["model"] = model.strip()

        # Add template parameter if specified
        if template and template.strip():
            task_params["template"] = template.strip()
            # When using template, do NOT include prompt parameter
        else:
            # Use the provided prompt when no template
            task_params["prompt"] = prompt_list

        # Send the task with all applicable parameters
        genConfig = [task_params]
        genResult = rwUtils.inferenecRequest(genConfig)
        print(genResult)
        
        # Handle multiple results if multiple images were processed
        if len(genResult["data"]) > 1:
            # Multiple images - combine results
            combined_text = "\n\n".join([item["text"] for item in genResult["data"]])
            genText = combined_text
        else:
            # Single image
            genText = genResult["data"][0]["text"]
        
        rwUtils.sendImageCaption(genText, kwargs.get("node_id"))
        return (genText, )