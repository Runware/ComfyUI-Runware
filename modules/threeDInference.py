from .utils import runwareUtils as rwUtils
import comfy.model_management


class threeDInference:
    """Runware 3D Inference node for generating 3D models from images"""

    # Available 3D models
    THREED_MODELS = {
        "Meta SAM 3D": "meta:sam@3d",
    }

    # Output formats
    OUTPUT_FORMATS = ["GLB", "PLY"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Model": (list(cls.THREED_MODELS.keys()), {
                    "tooltip": "Select the 3D generation model to use.",
                    "default": "Meta SAM 3D",
                }),
                "positivePrompt": ("STRING", {
                    "multiline": True,
                    "placeholder": "Describe the 3D object you want to generate...",
                    "tooltip": "A text prompt describing the 3D object to generate."
                }),
                "seed": ("INT", {
                    "tooltip": "Seed for reproducibility. Use the same seed to get the same result.",
                    "default": 1,
                    "min": 1,
                    "max": 2147483647,
                }),
                "outputFormat": (cls.OUTPUT_FORMATS, {
                    "tooltip": "Output format for the 3D model file.",
                    "default": "GLB",
                }),
            },
            "optional": {
                "inputs": ("RUNWARE3DINFERENCEINPUTS", {
                    "tooltip": "Connect a Runware 3D Inference Inputs node to provide image and mask inputs.",
                }),
            },
        }

    DESCRIPTION = "Generate 3D models from images using Runware's 3D Inference API. Connect the output to 'Runware Save 3D' node to save the file."
    FUNCTION = "generate3D"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("3dObject",)
    CATEGORY = "Runware"

    def generate3D(self, **kwargs):
        """Generate 3D model from inputs"""
        modelName = kwargs.get("Model", "Meta SAM 3D")
        positivePrompt = kwargs.get("positivePrompt", "")
        seed = kwargs.get("seed", 1)
        outputFormat = kwargs.get("outputFormat", "GLB")
        inputs = kwargs.get("inputs", None)

        # Get model AIR code
        model = self.THREED_MODELS.get(modelName, "meta:sam@3d")

        # Build generation config
        genConfig = [
            {
                "taskType": "3dInference",
                "taskUUID": rwUtils.genRandUUID(),
                "model": model,
                "numberResults": 1,
                "outputType": "URL",
                "includeCost": True,
                "deliveryMethod": "async",
                "outputFormat": outputFormat,
            }
        ]

        # Add positivePrompt if provided
        if positivePrompt and positivePrompt.strip() != "":
            genConfig[0]["positivePrompt"] = positivePrompt.strip()

        # Add seed
        genConfig[0]["seed"] = seed

        # Handle inputs from 3D Inference Inputs node
        if inputs is not None and isinstance(inputs, dict) and len(inputs) > 0:
            genConfig[0]["inputs"] = inputs

        try:
            print(f"[DEBUG] Sending 3D Inference Request:")
            print(f"[DEBUG] Request Payload: {rwUtils.safe_json_dumps(genConfig, indent=2)}")

            # Send initial request
            genResult = rwUtils.inferenecRequest(genConfig)

            print(f"[DEBUG] Received 3D Inference Response:")
            print(f"[DEBUG] Response: {rwUtils.safe_json_dumps(genResult, indent=2)}")

        except Exception as e:
            raise

        # Extract task UUID for polling
        taskUUID = genConfig[0]["taskUUID"]

        # Poll for 3D generation completion
        while True:
            # Check for interrupt before each poll
            comfy.model_management.throw_exception_if_processing_interrupted()

            # Poll for result
            pollResult = rwUtils.pollVideoResult(taskUUID)  # Reuse existing poll function
            print(f"[Debugging] Poll result: {rwUtils.safe_json_dumps(pollResult, indent=2) if isinstance(pollResult, (dict, list)) else pollResult}")

            # Check for errors
            if pollResult and "errors" in pollResult and len(pollResult["errors"]) > 0:
                error_info = pollResult["errors"][0]
                error_message = error_info.get("message", "Unknown error")

                if "responseContent" in error_info:
                    response_content = error_info["responseContent"]
                    if isinstance(response_content, str):
                        detailed_message = response_content
                    elif isinstance(response_content, dict):
                        detailed_message = response_content.get("message", str(response_content))
                    else:
                        detailed_message = str(response_content)

                    if detailed_message:
                        error_message = f"{error_message}\nProvider Error: {detailed_message}"

                task_uuid = error_info.get("taskUUID", "unknown")
                raise Exception(f"3D generation failed (Task: {task_uuid}): {error_message}")

            # Check for successful completion
            if pollResult and "data" in pollResult and len(pollResult["data"]) > 0:
                data = pollResult["data"][0]

                # Check if outputs.files exists (3D inference response format)
                outputs = data.get("outputs", {})
                files = outputs.get("files", [])

                if len(files) > 0:
                    file_info = files[0]
                    file_url = file_info.get("url", "")

                    if file_url:
                        print(f"[3D Inference] Generated 3D file URL: {file_url}")
                        return (file_url,)

                # Check status if available
                if "status" in data:
                    status = data["status"]
                    if status == "success":
                        # Try alternative response format
                        if "outputs" in data and "files" in data["outputs"]:
                            files = data["outputs"]["files"]
                            if len(files) > 0:
                                file_url = files[0].get("url", "")
                                if file_url:
                                    print(f"[3D Inference] Generated 3D file URL: {file_url}")
                                    return (file_url,)

            # Check for interrupt before waiting
            comfy.model_management.throw_exception_if_processing_interrupted()

            # Wait before next poll
            for _ in range(10):  # 10 x 0.1 second = 1 second total
                comfy.model_management.throw_exception_if_processing_interrupted()
                rwUtils.time.sleep(0.1)


NODE_CLASS_MAPPINGS = {
    "Runware3DInference": threeDInference,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Runware3DInference": "Runware 3D Inference",
}
