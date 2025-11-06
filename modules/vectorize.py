from .utils import runwareUtils as rwUtils
import json
import base64
import io


class SVGData:
    """Wrapper class to match RecraftIO.SVG format for SaveSVGNode"""
    
    def __init__(self, svgContent):
        svgBytes = io.BytesIO(svgContent.encode('utf-8'))
        self.data = [svgBytes]


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
    RETURN_TYPES = ("SVG",)
    RETURN_NAMES = ("SVG",)
    CATEGORY = "Runware"

    def vectorizeImage(self, **kwargs):
        """Vectorize image and return SVG data"""
        image = kwargs.get("Image")
        modelName = kwargs.get("Model", "recraft:1@1")
        
        model = self.RUNWARE_VECTORIZE_MODELS.get(modelName, "recraft:1@1")
        imageUuid = rwUtils.convertTensor2IMG(image)
        
        genConfig = self._buildGenConfig(model, imageUuid)
        
        print(f"[DEBUG] Sending Vectorize Request:")
        print(f"[DEBUG] Request Payload: {json.dumps(genConfig, indent=2)}")
        
        genResult = rwUtils.inferenecRequest(genConfig)
        
        print(f"[DEBUG] Received Vectorize Response:")
        print(f"[DEBUG] Response: {json.dumps(genResult, indent=2)}")
        
        self._validateResponse(genResult)
        
        svgData = self._extractSvgData(genResult)
        
        return (svgData,)

    def _buildGenConfig(self, model, imageUuid):
        """Build generation configuration for API request"""
        return [{
            "taskType": "vectorize",
            "taskUUID": rwUtils.genRandUUID(),
            "model": model,
            "inputs": {
                "image": imageUuid
            },
            "outputType": "base64Data",
            "outputFormat": "svg",
        }]

    def _validateResponse(self, genResult):
        """Validate API response"""
        if "errors" in genResult:
            errorMessage = genResult["errors"][0]["message"]
            raise Exception(f"Vectorization failed: {errorMessage}")
        
        if "data" not in genResult or len(genResult["data"]) == 0:
            raise Exception("No data returned from vectorization API")

    def _extractSvgData(self, genResult):
        """Extract SVG data from API response"""
        resultData = genResult["data"][0]
        
        if "imageBase64Data" not in resultData:
            raise Exception("imageBase64Data not found in response")
        
        base64Svg = resultData["imageBase64Data"]
        svgContent = base64.b64decode(base64Svg).decode('utf-8')
        svgData = SVGData(svgContent)
        
        return svgData


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareVectorize": vectorize,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVectorize": "Runware Vectorize",
}
