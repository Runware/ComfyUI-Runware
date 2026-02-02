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
from .modules.loraSearch import loraSearch
from .modules.loraCombine import loraCombine
from .modules.refiner import refiner
from .modules.imageMasking import imageMasking
from .modules.controlNetPreprocessor import controlNetPreprocessor
from .modules.apiManager import apiManager
from .modules.imageCaptioning import imageCaptioning
from .modules.videoTranscription import videoTranscription
from .modules.controlNetCombine import controlNetCombine
from .modules.embeddingSearch import embeddingSearch
from .modules.embeddingsCombine import embeddingsCombine
from .modules.ipAdapter import ipAdapter
from .modules.ipAdapterCombine import ipAdapterCombine
from .modules.vaeSearch import vaeSearch
from .modules.referenceImages import referenceImages
from .modules.imageInferenceInputs import imageInferenceInputs
from .modules.videoInference import txt2vid
from .modules.videoModelSearch import videoModelSearch
from .modules.frameImages import RunwareFrameImages
from .modules.providerSettings.pixverseProviderSettings import RunwarePixverseProviderSettings
from .modules.providerSettings.openaiProviderSettings import RunwareOpenAIProviderSettings
from .modules.providerSettings.bytedanceImageProviderSettings import RunwareBytedanceProviderSettings
from .modules.providerSettings.briaImageProviderSettings import RunwareBriaProviderSettings
from .modules.providerSettings.briaProviderMask import RunwareBriaProviderMask
from .modules.audioInference import RunwareAudioInference
from .modules.audioModelSearch import RunwareAudioModelSearch
from .modules.audioSections import RunwareAudioSections
from .modules.audioInferenceInputs import audioInferenceInputs
from .modules.providerSettings.elevenlabsProviderSettings import RunwareElevenLabsProviderSettings
from .modules.providerSettings.elevenlabsProviderSettingsSections import RunwareElevenLabsProviderSettingsSections
from .modules.acceleratorOptions import acceleratorOptions
from .modules.providerSettings.viduProviderSettings import RunwareViduProviderSettings
from .modules.mediaUpload import runwareMediaUpload
from .modules.inputAudios import inputAudios
from .modules.audioInput import RunwareAudioInput
from .modules.audioInputCombine import RunwareAudioInputCombine
from .modules.speechInput import RunwareSpeechInput
from .modules.speechInputCombine import RunwareSpeechInputCombine
from .modules.referenceVideos import referenceVideos
from .modules.referenceVoices import referenceVoices
from .modules.videoInferenceInputs import videoInferenceInputs
from .modules.providerSettings.lightricksProviderSettings import RunwareLightricksProviderSettings
from .modules.providerSettings.minimaxProviderSettings import RunwareMiniMaxProviderSettings
from .modules.providerSettings.klingProviderSettings import RunwareKlingProviderSettings
from .modules.providerSettings.runwayProviderSettings import RunwareRunwayProviderSettings
from .modules.providerSettings.lumaProviderSettings import RunwareLumaProviderSettings
from .modules.providerSettings.midjourneyProviderSettings import RunwareMidjourneyProviderSettings
from .modules.providerSettings.mireloProviderSettings import RunwareMireloProviderSettings
from .modules.providerSettings.alibabaProviderSettings import RunwareAlibabaProviderSettings
from .modules.providerSettings.googleProviderSettings import RunwareGoogleProviderSettings
from .modules.providerSettings.blackForestProviderSettings import RunwareBlackForestProviderSettings
from .modules.providerSettings.syncSegment import RunwareSyncSegment
from .modules.providerSettings.syncProviderSettings import RunwareSyncProviderSettings
from .modules.vectorize import vectorize
from .modules.videoBgRemoval import videoBgRemoval
from .modules.videoUpscaler import videoUpscaler
from .modules.videoInputsReferences import videoInputsReferences
from .modules.videoInputsFrame import RunwareVideoInputsFrameImages
from .modules.safetyInputs import safetyInputs
from .modules.settings import RunwareSettings
from .modules.videoAdvancedFeatureInputs import videoAdvancedFeatureInputs
from .modules.advancedFeatureSettings.wanAnimateAdvancedFeatureSettings import RunwareWanAnimateAdvancedFeatureSettings
from .modules.saveImage import RunwareSaveImage
from .modules.videoOutputs import RunwareVideoInferenceOutputs
from .modules.threeDInference import threeDInference
from .modules.threeDInferenceInputs import threeDInferenceInputs
from .modules.save3D import RunwareSave3D

RUNWARE_COMFYUI_VERSION = "1.4.0 Beta"

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
    "Runware Video Transcription": videoTranscription,
    "Runware ControlNet Combine": controlNetCombine,
    "Runware IPAdapter": ipAdapter,
    "Runware IPAdapters Combine": ipAdapterCombine,
    "Runware Reference Images": referenceImages,
    "Runware Image Inference Inputs": imageInferenceInputs,
    "Runware Video Inference": txt2vid,
    "Runware Video Model Search": videoModelSearch,
    "Runware Frame Images": RunwareFrameImages,
    "Runware Pixverse Provider Settings": RunwarePixverseProviderSettings,
    "Runware OpenAI Provider Settings": RunwareOpenAIProviderSettings,
    "Runware Bytedance Provider Settings": RunwareBytedanceProviderSettings,
    "Runware Bria Provider Settings": RunwareBriaProviderSettings,
    "Runware Bria Provider Mask": RunwareBriaProviderMask,
    "Runware Audio Inference": RunwareAudioInference,
    "Runware Audio Model Search": RunwareAudioModelSearch,
    "Runware Audio Sections": RunwareAudioSections,
    "Runware Audio Inference Inputs": audioInferenceInputs,
    "Runware ElevenLabs Provider Settings": RunwareElevenLabsProviderSettings,
    "Runware ElevenLabs Provider Settings Sections": RunwareElevenLabsProviderSettingsSections,
    "Runware Accelerator Options": acceleratorOptions,
    "Runware Vidu Provider Settings": RunwareViduProviderSettings,
    "Runware Media Upload": runwareMediaUpload,
    "Runware Input Audios": inputAudios,
    "Runware Video Audio Input": RunwareAudioInput,
    "Runware Audio Inputs Combine": RunwareAudioInputCombine,
    "Runware Video Speech Input": RunwareSpeechInput,
    "Runware Speech Inputs Combine": RunwareSpeechInputCombine,
    "Runware Reference Videos": referenceVideos,
    "Runware Reference Voices": referenceVoices,
    "Runware Video Inference Inputs": videoInferenceInputs,
    "Runware Lightricks Provider Settings": RunwareLightricksProviderSettings,
    "Runware MiniMax Provider Settings": RunwareMiniMaxProviderSettings,
    "Runware Luma Provider Settings": RunwareLumaProviderSettings,
    "Runware KlingAI Provider Settings": RunwareKlingProviderSettings,
    "Runware Runway Provider Settings": RunwareRunwayProviderSettings,
    "Runware Midjourney Provider Settings": RunwareMidjourneyProviderSettings,
    "Runware Mirelo Provider Settings": RunwareMireloProviderSettings,
    "Runware Alibaba Provider Settings": RunwareAlibabaProviderSettings,
    "Runware Google Provider Settings": RunwareGoogleProviderSettings,
    "Runware BlackForest Labs Provider Settings": RunwareBlackForestProviderSettings,
    "Runware Sync Segment": RunwareSyncSegment,
    "Runware Sync Provider Settings": RunwareSyncProviderSettings,
    "Runware Vectorize": vectorize,
    "Runware Video Background Removal": videoBgRemoval,
    "Runware Video Upscaler": videoUpscaler,
    "Runware Video Inputs References": videoInputsReferences,
    "Runware Video Inputs Frame Images": RunwareVideoInputsFrameImages,
    "Runware Safety Inputs": safetyInputs,
    "Runware Settings": RunwareSettings,
    "Runware Video Advanced Feature Inputs": videoAdvancedFeatureInputs,
    "Runware Wan Animate Advanced Feature Settings": RunwareWanAnimateAdvancedFeatureSettings,
    "Runware Save Image": RunwareSaveImage,
    "Runware Video Inference Outputs": RunwareVideoInferenceOutputs,
    "Runware 3D Inference": threeDInference,
    "Runware 3D Inference Inputs": threeDInferenceInputs,
    "Runware Save 3D": RunwareSave3D,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Runware Model Search": "Runware Model",
    "Runware Lora Search": "Runware Lora",
    "Runware Embedding Search": "Runware Embedding",
    "Runware VAE Search": "Runware VAE",
    "Runware Multi Inference": "Runware Multi Inference [BETA]",
    "Runware Video Model Search": "Runware Video Model",
    "Runware Audio Model Search": "Runware Audio Model",
    "Runware Video Transcription": "Runware Video Caption",
}

WEB_DIRECTORY = "./clientlibs"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]