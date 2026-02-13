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
    DESCRIPTION = "Load a 3D model file from a path or entering a path. Base64 encodes and outputs as data URI. Connect to Runware 3D Inference Inputs meshFile."

    def load_mesh(self, file_path):
        path = (file_path or "").strip() if isinstance(file_path, str) else ""
        if not path:
            return ("",)
        full_path = os.path.expanduser(path)
        ext = os.path.splitext(full_path)[1].lower()
        if ext not in self.MESH_EXTENSIONS:
            raise ValueError(
                f"Runware Load Mesh: unsupported extension '{ext}'. Expected .glb or .ply."
            )
        if not os.path.isfile(full_path):
            raise FileNotFoundError(
                f"Runware Load Mesh: file not found: {full_path}"
            )
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
