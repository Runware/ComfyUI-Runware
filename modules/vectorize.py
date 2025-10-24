from .utils import runwareUtils as rwUtils
import json
import base64
import io

class SVGData:
    """Wrapper class to match RecraftIO.SVG format for SaveSVGNode"""
    def __init__(self, svg_content):
        # Convert SVG string to BytesIO
        svg_bytes = io.BytesIO(svg_content.encode('utf-8'))
        self.data = [svg_bytes]

class vectorize:
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
        image = kwargs.get("Image")
        modelName = kwargs.get("Model", "recraft:1@1")
        
        # Get the model AIR code
        model = self.RUNWARE_VECTORIZE_MODELS.get(modelName, "recraft:1@1")
        
        # Convert image to UUID
        image_uuid = rwUtils.convertTensor2IMG(image)
        
        # Build the API request
        genConfig = [
            {
                "taskType": "vectorize",
                "taskUUID": rwUtils.genRandUUID(),
                "model": model,
                "inputs": {
                    "image": image_uuid
                },
                "outputType": "base64Data",
                "outputFormat": "svg",
            }
        ]
        
        try:
            # Debug: Print the request being sent
            print(f"[DEBUG] Sending Vectorize Request:")
            print(f"[DEBUG] Request Payload: {json.dumps(genConfig, indent=2)}")
            
            genResult = rwUtils.inferenecRequest(genConfig)
            
            # Debug: Print the response received
            print(f"[DEBUG] Received Vectorize Response:")
            print(f"[DEBUG] Response: {json.dumps(genResult, indent=2)}")
            
            # Check for errors
            if "errors" in genResult:
                error_message = genResult["errors"][0]["message"]
                raise Exception(f"Vectorization failed: {error_message}")
            
            # Extract the result
            if "data" in genResult and len(genResult["data"]) > 0:
                result_data = genResult["data"][0]
                
                # Check for base64 SVG data
                if "imageBase64Data" in result_data:
                    base64_svg = result_data["imageBase64Data"]
                    
                    # Decode base64 SVG to get the actual SVG content for SaveSVGNode
                    svg_content = base64.b64decode(base64_svg).decode('utf-8')
                    
                    # Wrap SVG content in SVGData for SaveSVGNode compatibility
                    svg_data = SVGData(svg_content)
                    
                    # Return only SVG data
                    return (svg_data,)
                else:
                    raise Exception("imageBase64Data not found in response")
            else:
                raise Exception("No data returned from vectorization API")
                
        except Exception as e:
            print(f"[Error] Vectorization failed: {str(e)}")
            raise e

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RunwareVectorize": vectorize,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVectorize": "Runware Vectorize",
}

