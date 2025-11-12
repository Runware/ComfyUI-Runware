from .utils import runwareUtils as rwUtils


class imageInferenceInputs:
    """Image Inference Inputs node for configuring image generation inputs"""
    
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
                "Reference Tag 1": ("STRING", {
                    "tooltip": "Optional tag describing Reference Image 1. Leave empty to omit.",
                    "default": "",
                }),
                "Reference Image 2": ("IMAGE", {
                    "tooltip": "Specifies Reference Image 2 for the inputs. These reference images help guide the image generation process."
                }),
                "Reference Tag 2": ("STRING", {
                    "tooltip": "Optional tag describing Reference Image 2. Leave empty to omit.",
                    "default": "",
                }),
                "Reference Image 3": ("IMAGE", {
                    "tooltip": "Specifies Reference Image 3 for the inputs. These reference images help guide the image generation process."
                }),
                "Reference Tag 3": ("STRING", {
                    "tooltip": "Optional tag describing Reference Image 3. Leave empty to omit.",
                    "default": "",
                }),
                "Reference Image 4": ("IMAGE", {
                    "tooltip": "Specifies Reference Image 4 for the inputs. These reference images help guide the image generation process."
                }),
                "Reference Tag 4": ("STRING", {
                    "tooltip": "Optional tag describing Reference Image 4. Leave empty to omit.",
                    "default": "",
                }),
            }
        }

    DESCRIPTION = "Configure custom inputs for Runware Image Inference, including reference images that can be passed to the inference node."
    FUNCTION = "createInputs"
    RETURN_TYPES = ("RUNWAREIMAGEINFERENCEINPUTS",)
    RETURN_NAMES = ("Inference Inputs",)
    CATEGORY = "Runware"

    def createInputs(self, **kwargs):
        """Create image inference inputs from provided parameters"""
        image = kwargs.get("image", None)
        refImage1 = kwargs.get("Reference Image 1", None)
        refTag1 = kwargs.get("Reference Tag 1", "")
        refImage2 = kwargs.get("Reference Image 2", None)
        refTag2 = kwargs.get("Reference Tag 2", "")
        refImage3 = kwargs.get("Reference Image 3", None)
        refTag3 = kwargs.get("Reference Tag 3", "")
        refImage4 = kwargs.get("Reference Image 4", None)
        refTag4 = kwargs.get("Reference Tag 4", "")

        inputs = {}
        
        if image is not None:
            inputs["image"] = rwUtils.convertTensor2IMG(image)

        references = self._collectReferences(
            refImage1, refTag1,
            refImage2, refTag2,
            refImage3, refTag3,
            refImage4, refTag4,
        )
        if len(references) > 0:
            inputs["referenceImages"] = references

        return (inputs,)

    def _collectReferences(self, *referenceArgs):
        """Collect and convert reference images to list"""
        # Build list of (image, tag) pairs from the flat arguments
        referencePairs = list(zip(referenceArgs[0::2], referenceArgs[1::2]))

        # Determine if any tag is provided
        hasTags = any(
            isinstance(tag, str) and tag.strip() != ""
            for _, tag in referencePairs
        )

        if not hasTags:
            # Use legacy behavior: simple list of images
            return [
                rwUtils.convertTensor2IMG(image)
                for image, _ in referencePairs
                if image is not None
            ]

        references = []
        for image, tag in referencePairs:
            if image is None:
                continue

            entry = {"image": rwUtils.convertTensor2IMG(image)}
            if isinstance(tag, str) and tag.strip() != "":
                entry["tag"] = tag.strip()
            references.append(entry)

        return references
