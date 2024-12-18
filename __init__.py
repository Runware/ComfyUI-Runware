from .modules.imageInference import txt2img
from .modules.bgremoval import bgremoval
from .modules.photoMaker import photoMaker
from .modules.upscaler import upscaler
from .modules.modelSearch import modelSearch
from .modules.bridges import mainRoute
from .modules.controlNet import controlNet
from .modules.loraSearch import loraSearch
from .modules.loraCombine import loraCombine
from .modules.refiner import refiner
from .modules.imageMasking import imageMasking
from .modules.controlNetPreprocessor import controlNetPreprocessor
from .modules.apiManager import apiManager
from .modules.imageCaptioning import imageCaptioning
from .modules.controlNetCombine import controlNetCombine
from .modules.embeddingSearch import embeddingSearch
from .modules.embeddingsCombine import embeddingsCombine
from .modules.vaeSearch import vaeSearch

RUNWARE_COMFYUI_VERSION = "0.9.4 Beta"

RESET_COLOR = "\033[0m"
BLUE_COLOR = "\033[94m"
GREEN_COLOR = "\033[92m"
print(BLUE_COLOR + "##############################################################" + RESET_COLOR)
print(GREEN_COLOR + "  Runware ComfyUI Inference Services Are Loaded Successfully" + RESET_COLOR)
print(GREEN_COLOR + "  Version: " + RUNWARE_COMFYUI_VERSION + " | Maintained by: Runware Inc" + RESET_COLOR)
print(GREEN_COLOR + "  Official Website: https://my.runware.ai" + RESET_COLOR)
print(BLUE_COLOR + "##############################################################" + RESET_COLOR)

NODE_CLASS_MAPPINGS = {
    "Runware Image Inference": txt2img,
    "Runware Background Removal": bgremoval,
    "Runware PhotoMaker V2": photoMaker,
    "Runware Image Upscaler": upscaler,
    "Runware Model Search": modelSearch,
    "Runware Lora Search": loraSearch,
    "Runware Embedding Search": embeddingSearch,
    "Runware VAE Search": vaeSearch,
    "Runware Embeddings Combine": embeddingsCombine,
    "Runware ControlNet": controlNet,
    "Runware Lora Combine": loraCombine,
    "Runware Refiner": refiner,
    "Runware Image Masking": imageMasking,
    "Runware ControlNet PreProcessor": controlNetPreprocessor,
    "Runware API Manager": apiManager,
    "Runware Image Caption": imageCaptioning,
    "Runware ControlNet Combine": controlNetCombine,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Runware Model Search": "Runware Model",
    "Runware Lora Search": "Runware Lora",
    "Runware Embedding Search": "Runware Embedding",
    "Runware VAE Search": "Runware VAE",
}

WEB_DIRECTORY = "./clientlibs"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]