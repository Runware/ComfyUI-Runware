from .utils import runwareUtils as rwUtils


class vectorize:
    """Vectorize node for converting images to vector format"""
    
    RUNWARE_VECTORIZE_MODELS = {
        "recraft:1@1": "recraft:1@1",
        "picsart:1@1": "picsart:1@1",
    }
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Image": ("IMAGE", {
                    "tooltip": "Input image to be vectorized."
                }),
                "Model": (list(cls.RUNWARE_VECTORIZE_MODELS.keys()), {
                    "tooltip": "Select the vectorization model to use.",
                    "default": "recraft:1@1",
                }),
            },
        }

    DESCRIPTION = "Convert images to vector format using Runware's vectorization service."
    FUNCTION = "vectorizeImage"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("IMAGE",)
    CATEGORY = "Runware"

    def vectorizeImage(self, **kwargs):
        """Vectorize image and return SVG URL"""
        image = kwargs.get("Image")
        modelName = kwargs.get("Model", "recraft:1@1")
        
        model = self.RUNWARE_VECTORIZE_MODELS.get(modelName, "recraft:1@1")
        imageUuid = rwUtils.convertTensor2IMG(image)
        
        genConfig = self._buildGenConfig(model, imageUuid)
        
        print(f"[DEBUG] Sending Vectorize Request:")
        print(f"[DEBUG] Request Payload: {rwUtils.safe_json_dumps(genConfig, indent=2)}")
        
        genResult = rwUtils.inferenecRequest(genConfig)
        
        print(f"[DEBUG] Received Vectorize Response:")
        print(f"[DEBUG] Response: {rwUtils.safe_json_dumps(genResult, indent=2)}")
        
        self._validateResponse(genResult)
        
        svg_url = rwUtils.extractImageURLs(genResult)
        
        return (svg_url,)

    def _buildGenConfig(self, model, imageUuid):
        """Build generation configuration for API request"""
        return [{
            "taskType": "vectorize",
            "taskUUID": rwUtils.genRandUUID(),
            "model": model,
            "inputs": {
                "image": imageUuid
            },
            "outputType": "URL",
            "outputFormat": "svg",
        }]

    def _validateResponse(self, genResult):
        """Validate API response"""
        if "errors" in genResult:
            errorMessage = genResult["errors"][0]["message"]
            raise Exception(f"Vectorization failed: {errorMessage}")


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareVectorize": vectorize,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVectorize": "Runware Vectorize",
}
