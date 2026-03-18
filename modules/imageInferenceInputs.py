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
            optionalInputs[f"Reference Type {i}"] = ("STRING", {
                "tooltip": f"Optional type for {ordinal} reference, e.g. 'sketch' for illustrious style models. Leave empty to omit.",
                "default": "",
            })
            optionalInputs[f"Reference Strength {i}"] = ("FLOAT", {
                "tooltip": f"Strength (0-1) for sketch reference. Only used when Reference Type is 'sketch'.",
                "default": 0.0,
                "min": 0.0,
                "max": 1.0,
                "step": 0.1,
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

    DESCRIPTION = "Configure custom inputs for Runware Image Inference, including reference images (with optional type e.g. 'sketch' for illustrious style models, and strength 0-1 for sketch) that can be passed to the inference node."
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
        """Collect and convert reference images to list. Each entry may include type (e.g. 'sketch') and strength (0-1, only for sketch)."""
        referenceSlots = []

        for i in range(1, self.MAX_REFERENCE_IMAGES + 1):
            image = kwargs.get(f"Reference Image {i}", None)
            tag = kwargs.get(f"Reference Tag {i}", "")
            ref_type = kwargs.get(f"Reference Type {i}", "")
            strength = kwargs.get(f"Reference Strength {i}", 0.0)
            if image is not None:
                referenceSlots.append((image, tag, ref_type, strength))

        if not referenceSlots:
            return []

        has_tags = any(
            isinstance(tag, str) and tag.strip() != ""
            for _, tag, _, _ in referenceSlots
        )
        has_type = any(
            isinstance(rt, str) and rt.strip() != ""
            for _, _, rt, _ in referenceSlots
        )

        if not has_tags and not has_type:
            return [
                rwUtils.convertTensor2IMG(image)
                for image, _, _, _ in referenceSlots
            ]

        references = []
        for image, tag, ref_type, strength in referenceSlots:
            entry = {"image": rwUtils.convertTensor2IMG(image)}
            if isinstance(tag, str) and tag.strip() != "":
                entry["tag"] = tag.strip()
            if isinstance(ref_type, str) and ref_type.strip() != "":
                entry["type"] = ref_type.strip()
                if ref_type.strip().lower() == "sketch":
                    entry["strength"] = max(0.0, min(1.0, float(strength)))
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
