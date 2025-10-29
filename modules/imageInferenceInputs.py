from .utils import runwareUtils as rwUtils

class imageInferenceInputs:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "image": ("IMAGE", {
                    "tooltip": "Specifies an image input for the inference process."
                }),
                "Reference Image 1": ("IMAGE", {
                    "tooltip": "Specifies Reference Image 1 for the inputs. These reference images help guide the image generation process."
                }),
                "Reference Image 2": ("IMAGE", {
                    "tooltip": "Specifies Reference Image 2 for the inputs. These reference images help guide the image generation process."
                }),
                "Reference Image 3": ("IMAGE", {
                    "tooltip": "Specifies Reference Image 3 for the inputs. These reference images help guide the image generation process."
                }),
                "Reference Image 4": ("IMAGE", {
                    "tooltip": "Specifies Reference Image 4 for the inputs. These reference images help guide the image generation process."
                }),
            }
        }

    DESCRIPTION = "Configure custom inputs for Runware Image Inference, including reference images that can be passed to the inference node."
    FUNCTION = "createInputs"
    RETURN_TYPES = ("RUNWAREIMAGEINFERENCEINPUTS",)
    RETURN_NAMES = ("Inference Inputs",)
    CATEGORY = "Runware"

    def createInputs(self, **kwargs):
        image = kwargs.get("image", None)
        refImage1 = kwargs.get("Reference Image 1", None)
        refImage2 = kwargs.get("Reference Image 2", None)
        refImage3 = kwargs.get("Reference Image 3", None)
        refImage4 = kwargs.get("Reference Image 4", None)

        # Build the inputs structure
        inputs = {}
        
        # Handle image if provided
        if image is not None:
            inputs["image"] = rwUtils.convertTensor2IMG(image)
        
        # Handle references if any are provided
        references = []
        if refImage1 is not None:
            references.append(rwUtils.convertTensor2IMG(refImage1))
        if refImage2 is not None:
            references.append(rwUtils.convertTensor2IMG(refImage2))
        if refImage3 is not None:
            references.append(rwUtils.convertTensor2IMG(refImage3))
        if refImage4 is not None:
            references.append(rwUtils.convertTensor2IMG(refImage4))
        
        if len(references) > 0:
            inputs["references"] = references

        return (inputs, )

