from .utils import runwareUtils as rwUtils


class imageInferenceInputs:
    """Image Inference Inputs node for configuring image generation inputs"""
    
    MAX_REFERENCE_IMAGES = 14
    MAX_SUPER_RESOLUTION_REFERENCE_IMAGES = 5
    
    @classmethod
    def INPUT_TYPES(cls):
        optionalInputs = {
            "image": ("IMAGE", {
                "tooltip": "Specifies an image input for the inference process."
            }),
            "mask": ("IMAGE", {
                "tooltip": "Optional mask image for the inference process."
            }),
        }
        
        for i in range(1, cls.MAX_REFERENCE_IMAGES + 1):
            ordinal = rwUtils.getOrdinal(i)
            optionalInputs[f"Reference Image {i}"] = ("IMAGE", {
                "tooltip": f"Specifies {ordinal.capitalize()} Reference Image for the inputs. These reference images help guide the image generation process."
            })
            optionalInputs[f"Reference Tag {i}"] = ("STRING", {
                "tooltip": f"Optional tag describing {ordinal.capitalize()} Reference Image. Leave empty to omit.",
                "default": "",
            })
        
        for i in range(1, cls.MAX_SUPER_RESOLUTION_REFERENCE_IMAGES + 1):
            ordinal = rwUtils.getOrdinal(i)
            optionalInputs[f"Super Resolution Reference Image {i}"] = ("IMAGE", {
                "tooltip": f"Specifies {ordinal.capitalize()} Super Resolution Reference Image for the inputs.",
            })
        
        return {
            "required": {},
            "optional": optionalInputs
        }

    DESCRIPTION = "Configure custom inputs for Runware Image Inference, including reference images that can be passed to the inference node."
    FUNCTION = "createInputs"
    RETURN_TYPES = ("RUNWAREIMAGEINFERENCEINPUTS",)
    RETURN_NAMES = ("Inference Inputs",)
    CATEGORY = "Runware"

    def createInputs(self, **kwargs):
        """Create image inference inputs from provided parameters"""
        image = kwargs.get("image", None)
        mask = kwargs.get("mask", None)

        inputs = {}
        
        if image is not None:
            inputs["image"] = rwUtils.convertTensor2IMG(image)
        if mask is not None:
            inputs["mask"] = rwUtils.convertTensor2IMG(mask)

        references = self._collectReferences(kwargs)
        if len(references) > 0:
            inputs["referenceImages"] = references

        super_resolution_refs = self._collectSuperResolutionReferences(kwargs)
        if len(super_resolution_refs) > 0:
            inputs["superResolutionReferenceImages"] = super_resolution_refs

        return (inputs,)

    def _collectReferences(self, kwargs):
        """Collect and convert reference images to list"""
        referencePairs = []
        
        # Collect all reference image and tag pairs
        for i in range(1, self.MAX_REFERENCE_IMAGES + 1):
            image = kwargs.get(f"Reference Image {i}", None)
            tag = kwargs.get(f"Reference Tag {i}", "")
            if image is not None:
                referencePairs.append((image, tag))
        
        if not referencePairs:
            return []
        
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
            ]

        references = []
        for image, tag in referencePairs:
            entry = {"image": rwUtils.convertTensor2IMG(image)}
            if isinstance(tag, str) and tag.strip() != "":
                entry["tag"] = tag.strip()
            references.append(entry)

        return references

    def _collectSuperResolutionReferences(self, kwargs):
        """Collect and convert super resolution reference images to list (same pattern as referenceImages)"""
        images = []
        for i in range(1, self.MAX_SUPER_RESOLUTION_REFERENCE_IMAGES + 1):
            image = kwargs.get(f"Super Resolution Reference Image {i}", None)
            if image is not None:
                images.append(rwUtils.convertTensor2IMG(image))
        return images
