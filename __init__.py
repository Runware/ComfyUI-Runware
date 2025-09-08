from .modules.imageInference import txt2img
from .modules.outpaintSettings import outpaintSettings
from .modules.bgremoval import bgremoval
from .modules.photoMaker import photoMaker
from .modules.upscaler import upscaler
from .modules.modelSearch import modelSearch
from .modules.bridges import mainRoute
from .modules.controlNet import controlNet
from .modules.multiInference import multiInference
from .modules.runwareBFL import runwareKontext
from .modules.runwareImagen import runwareImagen
from .modules.teaCache import teaCache
from .modules.deepCache import deepCache
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
from .modules.ipAdapter import ipAdapter
from .modules.ipAdapterCombine import ipAdapterCombine
from .modules.vaeSearch import vaeSearch
from .modules.referenceImages import referenceImages
from .modules.videoInference import txt2vid
from .modules.videoModelSearch import videoModelSearch
from .modules.frameImages import RunwareFrameImages
from .modules.providerSettings import RunwareProviderSettings
from .modules.pixverseProviderSettings import RunwarePixverseProviderSettings
from .modules.openaiProviderSettings import RunwareOpenAIProviderSettings

RUNWARE_COMFYUI_VERSION = "1.3.0 Beta"

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
    "Runware Outpaint": outpaintSettings,
    "Runware Background Removal": bgremoval,
    "Runware PhotoMaker V2": photoMaker,
    "Runware Image Upscaler": upscaler,
    "Runware Model Search": modelSearch,
    "Runware Kontext Inference": runwareKontext,
    "Runware Imagen Inference": runwareImagen,
    "Runware Multi Inference": multiInference,
    "Runware TeaCache": teaCache,
    "Runware DeepCache": deepCache,
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
    "Runware IPAdapter": ipAdapter,
    "Runware IPAdapters Combine": ipAdapterCombine,
    "Runware Reference Images": referenceImages,
    "Runware Video Inference": txt2vid,
    "Runware Video Model Search": videoModelSearch,
    "Runware Frame Images": RunwareFrameImages,
    "Runware Provider Settings": RunwareProviderSettings,
    "Runware Pixverse Provider Settings": RunwarePixverseProviderSettings,
    "Runware OpenAI Provider Settings": RunwareOpenAIProviderSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Runware Model Search": "Runware Model",
    "Runware Lora Search": "Runware Lora",
    "Runware Embedding Search": "Runware Embedding",
    "Runware VAE Search": "Runware VAE",
    "Runware Multi Inference": "Runware Multi Inference [BETA]",
    "Runware Video Model Search": "Runware Video Model",
}

WEB_DIRECTORY = "./clientlibs"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]