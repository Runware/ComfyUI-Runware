from .utils import runwareUtils as rwUtils
import json

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
    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("IMAGE", "Vector Data")
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
                
                # Return the vectorized image URL
                if "imageURL" in result_data:
                    vector_url = result_data["imageURL"]
                    return (image, vector_url)
                else:
                    raise Exception("imageURL not found in response")
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

