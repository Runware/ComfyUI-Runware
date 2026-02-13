import base64
import os


class RunwareLoadMesh:
    """Runware Load Mesh node for loading 3D model files (uses same logic as Load Image)"""

    MESH_EXTENSIONS = {".glb", ".ply"}

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "/path/to/model.glb or .ply",
                    "tooltip": "Full path to .glb or .ply file. Use this to load from any directory.",
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Base64",)
    FUNCTION = "load_mesh"
    CATEGORY = "Runware"
    DESCRIPTION = "Load a 3D model file from a path or via upload. Base64 encodes and outputs as data URI. Connect to Runware 3D Inference Inputs meshFile."

    def load_mesh(self, file_path):
        if not file_path or not isinstance(file_path, str) or not file_path.strip():
            return ("",)
        full_path = os.path.expanduser(file_path.strip())
        if not os.path.isfile(full_path) or os.path.splitext(full_path)[1].lower() not in self.MESH_EXTENSIONS:
            return ("",)
        with open(full_path, 'rb') as f:
            mesh_bytes = f.read()
        mesh_base64 = base64.b64encode(mesh_bytes).decode('utf-8')
        return (f"data:application/octet-stream;base64,{mesh_base64}",)


NODE_CLASS_MAPPINGS = {
    "RunwareLoadMesh": RunwareLoadMesh,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareLoadMesh": "Runware Load Mesh",
}
