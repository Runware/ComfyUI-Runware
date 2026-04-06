from .utils import runwareUtils as rwUtils

_IMAGE_SLOTS = 4


class threeDInferenceInputs:
    """3D Inference Inputs node for configuring 3D generation inputs"""

    @classmethod
    def INPUT_TYPES(cls):
        optional = {
            "image": ("IMAGE", {
                "tooltip": "Input image for 3D inference. This image will be used as the source for generating the 3D model.",
            }),
            "mask": ("IMAGE", {
                "tooltip": "Optional mask image to specify a region of interest in the input image for 3D generation.",
            }),
            "meshFile": ("STRING", {
                "default": "",
                "tooltip": "Base64 data URI of mesh file (.glb or .ply) from Runware Load Mesh.",
            }),
        }
        for i in range(1, _IMAGE_SLOTS + 1):
            optional[f"images_{i}"] = ("IMAGE", {
                "tooltip": f"Multi-view image slot {i}; merged in order into inputs.images as a list of data URIs.",
            })
        return {
            "required": {},
            "optional": optional,
        }

    DESCRIPTION = (
        "Configure custom inputs for Runware 3D Inference: image, mask, meshFile, and images_1…images_4 "
        "(merged into inputs.images as an array)."
    )
    FUNCTION = "createInputs"
    RETURN_TYPES = ("RUNWARE3DINFERENCEINPUTS",)
    RETURN_NAMES = ("Inputs",)
    CATEGORY = "Runware"

    def createInputs(self, **kwargs):
        """Create 3D inference inputs from provided parameters"""
        image = kwargs.get("image", None)
        mask = kwargs.get("mask", None)
        mesh_file = kwargs.get("meshFile", "")

        inputs = {}

        if image is not None:
            inputs["image"] = rwUtils.convertTensor2IMG(image)

        if mask is not None:
            inputs["mask"] = rwUtils.convertTensor2IMG(mask)

        if mesh_file and isinstance(mesh_file, str) and mesh_file.strip():
            inputs["meshFile"] = mesh_file.strip()

        images_list: list = []
        for i in range(1, _IMAGE_SLOTS + 1):
            slot = kwargs.get(f"images_{i}")
            if slot is not None:
                images_list.append(rwUtils.convertTensor2IMG(slot))
        if images_list:
            inputs["images"] = images_list

        return (inputs,)


NODE_CLASS_MAPPINGS = {
    "Runware3DInferenceInputs": threeDInferenceInputs,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Runware3DInferenceInputs": "Runware 3D Inference Inputs",
}
