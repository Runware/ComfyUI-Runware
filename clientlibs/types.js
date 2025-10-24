const DEFAULT_BGCOLOR = "#5345bf";

const DEFAULT_DIMENSIONS_LIST = {
    "Square (512x512)": "512x512",
    "Square HD (1024x1024)": "1024x1024",
    "Portrait 3:4 (768x1024)": "768x1024",
    "Portrait 9:16 (576x1024)": "576x1024",
    "Landscape 4:3 (1024x768)": "1024x768",
    "Landscape 16:9 (1024x576)": "1024x576"
};

const DEFAULT_MODELS_ARCH_LIST = {
    "All": "all",
    "FLUX.1-Schnell": "flux1s",
    "FLUX.1-Dev": "flux1d",
    "FLUX.1-Krea": "flux1d",
    "Pony": "pony",
    "SD 1.5": "sd1x",
    "SD 1.5 Hyper": "sdhyper",
    "SD 1.5 LCM": "sd1xlcm",
    "SD 3": "sd3",
    "SDXL 1.0": "sdxl",
    "SDXL 1.0 LCM": "sdxllcm",
    "SDXL Distilled": "sdxldistilled",
    "SDXL Hyper": "sdxlhyper",
    "SDXL Lightning": "sdxllightning",
    "SDXL Turbo": "sdxlturbo",
};

const DEFAULT_CONTROLNET_CONDITIONING_LIST = {
    "All": "all",
    "Canny": "canny",
    "Depth": "depth",
    "MLSD": "mlsd",
    "Normal BAE": "normalbae",
    "Open Pose": "openpose",
    "Tile": "tile",
    "Seg": "seg",
    "Line Art": "lineart",
    "Line Art Anime": "lineart_anime",
    "Shuffle": "shuffle",
    "Scribble": "scribble",
    "Soft Edge": "softedge",
};

const SEARCH_TERMS = ["Model Search", "Lora Search", "ControlNet Search", "Embedding Search", "VAE Search"];
const MODEL_TYPES_TERMS = ["ModelType", "LoraType", "ControlNetType"];
const MODEL_LIST_TERMS = ["ModelList", "LoraList", "ControlNetList", "EmbeddingList", "VAEList"];

const RUNWARE_NODE_TYPES = {
    IMAGEINFERENCE: "Runware Image Inference",
    KONTEXTINFERENCE: "Runware Kontext Inference",
    IMAGENINFERENCE: "Runware Imagen Inference",
    OUTPAINT: "Runware Outpaint",
    PHOTOMAKER: "Runware PhotoMaker V2",
    MODELSEARCH: "Runware Model Search",
    MULTIINFERENCE: "Runware Multi Inference",
    TEACACHE: "Runware TeaCache",
    DEEPCACHE: "Runware DeepCache",
    LORASEARCH: "Runware Lora Search",
    CONTROLNET: "Runware ControlNet",
    BGREMOVAL: "Runware Background Removal",
    UPSCALER: "Runware Image Upscaler",
    REFINER: "Runware Refiner",
    LORACOMBINE: "Runware Lora Combine",
    CONTROLNETCOMBINE: "Runware ControlNet Combine",
    IPADAPTER: "Runware IPAdapter",
    IPADAPTERSCOMBINE: "Runware IPAdapters Combine",
    IMAGEMASKING: "Runware Image Masking",
    CONTROLNETPREPROCESSING: "Runware ControlNet PreProcessor",
    APIMANAGER: "Runware API Manager",
    IMAGECAPTION: "Runware Image Caption",
    EMBEDDING: "Runware Embedding Search",
    EMBEDDINGCOMBINE: "Runware Embedding Combine",
    VAE: "Runware VAE Search",
    REFERENCEIMAGES: "Runware Reference Images",
    IMAGEINFERENCEINPUTS: "Runware Image Inference Inputs",
    VIDEOINFERENCE: "Runware Video Inference",
    VIDEOMODELSEARCH: "Runware Video Model Search",
    FRAMEIMAGES: "Runware Frame Images",
    AUDIOINFERENCE: "Runware Audio Inference",
    AUDIOMODELSEARCH: "Runware Audio Model Search",
    AUDIOSECTIONS: "Runware Audio Sections",
    PROVIDERSETTINGS: "Runware Provider Settings",
    PIXVERSEPROVIDERSETTINGS: "Runware Pixverse Provider Settings",
    OPENAIPROVIDERSETTINGS: "Runware OpenAI Provider Settings",
    BYTEDANCEPROVIDERSETTINGS: "Runware Bytedance Provider Settings",
    ELEVENLABSPROVIDERSETTINGS: "Runware ElevenLabs Provider Settings",
    ELEVENLABSPROVIDERSETTINGSSECTIONS: "Runware ElevenLabs Provider Settings Sections",
    VIDUPROVIDERSETTINGS: "Runware Vidu Provider Settings",
    MEDIAUPLOAD: "Runware Media Upload",
    INPUTAUDIOS: "Runware Input Audios",
    REFERENCEVIDEOS: "Runware Reference Videos",
    VIDEOINFERENCEINPUTS: "Runware Video Inference Inputs",
    LIGHTRICKSPROVIDERSETTINGS: "Runware Lightricks Provider Settings",
    VECTORIZE: "Runware Vectorize",
    VIDEOBGREMOVAL: "Runware Video Background Removal",
    VIDEOUPSCALER: "Runware Video Upscaler",
    VIDEOINPUTSREFERENCES: "Runware Video Inputs References",
};

const RUNWARE_NODE_PROPS = {
    [RUNWARE_NODE_TYPES.IMAGEINFERENCE]: {
        bgColor: DEFAULT_BGCOLOR,
        liveDimensions: true,
        promptEnhancer: true,
    },
    [RUNWARE_NODE_TYPES.KONTEXTINFERENCE]: {
        bgColor: DEFAULT_BGCOLOR,
        promptEnhancer: true,
    },
    [RUNWARE_NODE_TYPES.IMAGENINFERENCE]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.REFERENCEIMAGES]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.OUTPAINT]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.PHOTOMAKER]: {
        bgColor: DEFAULT_BGCOLOR,
        liveDimensions: true,
        promptEnhancer: true,
    },
    [RUNWARE_NODE_TYPES.MODELSEARCH]: {
        bgColor: DEFAULT_BGCOLOR,
        liveSearch: true,
    },
    [RUNWARE_NODE_TYPES.MULTIINFERENCE]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.TEACACHE]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.DEEPCACHE]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.LORASEARCH]: {
        bgColor: DEFAULT_BGCOLOR,
        liveSearch: true,
    },
    [RUNWARE_NODE_TYPES.EMBEDDING]: {
        bgColor: DEFAULT_BGCOLOR,
        liveSearch: true,
    },
    [RUNWARE_NODE_TYPES.CONTROLNET]: {
        bgColor: DEFAULT_BGCOLOR,
        liveSearch: true,
    },
    [RUNWARE_NODE_TYPES.VAE]: {
        bgColor: DEFAULT_BGCOLOR,
        liveSearch: true,
    },
    [RUNWARE_NODE_TYPES.EMBEDDINGCOMBINE]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.CONTROLNETCONDITIONING]: {
        bgColor: DEFAULT_BGCOLOR,
        liveSearch: true,
    },
    [RUNWARE_NODE_TYPES.BGREMOVAL]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.UPSCALER]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.REFINER]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.LORACOMBINE]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.IPADAPTER]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.IPADAPTERSCOMBINE]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.CONTROLNETCOMBINE]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.IMAGEMASKING]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.CONTROLNETPREPROCESSING]: {
        bgColor: DEFAULT_BGCOLOR,
        liveDimensions: true,
    },
    [RUNWARE_NODE_TYPES.APIMANAGER]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.IMAGECAPTION]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.VIDEOINFERENCE]: {
        bgColor: DEFAULT_BGCOLOR,
        liveDimensions: true,
        promptEnhancer: true,
    },
    [RUNWARE_NODE_TYPES.VIDEOMODELSEARCH]: {
        bgColor: DEFAULT_BGCOLOR,
        liveSearch: true,
    },
    [RUNWARE_NODE_TYPES.FRAMEIMAGES]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.AUDIOINFERENCE]: {
        bgColor: DEFAULT_BGCOLOR,
        promptEnhancer: true,
    },
    [RUNWARE_NODE_TYPES.AUDIOMODELSEARCH]: {
        bgColor: DEFAULT_BGCOLOR,
        liveSearch: true,
    },
    [RUNWARE_NODE_TYPES.AUDIOSECTIONS]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.PROVIDERSETTINGS]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.PIXVERSEPROVIDERSETTINGS]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.OPENAIPROVIDERSETTINGS]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.BYTEDANCEPROVIDERSETTINGS]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.ELEVENLABSPROVIDERSETTINGS]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.ELEVENLABSPROVIDERSETTINGSSECTIONS]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.VIDUPROVIDERSETTINGS]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.MEDIAUPLOAD]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.INPUTAUDIOS]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.REFERENCEVIDEOS]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.VIDEOINFERENCEINPUTS]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.LIGHTRICKSPROVIDERSETTINGS]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
    [RUNWARE_NODE_TYPES.VECTORIZE]: {
        bgColor: DEFAULT_BGCOLOR,
    },
    [RUNWARE_NODE_TYPES.VIDEOBGREMOVAL]: {
        bgColor: DEFAULT_BGCOLOR,
    },
    [RUNWARE_NODE_TYPES.VIDEOUPSCALER]: {
        bgColor: DEFAULT_BGCOLOR,
    },
    [RUNWARE_NODE_TYPES.VIDEOINPUTSREFERENCES]: {
        bgColor: DEFAULT_BGCOLOR,
        colorModeOnly: true,
    },
};

export {
    DEFAULT_BGCOLOR,
    DEFAULT_DIMENSIONS_LIST,
    DEFAULT_MODELS_ARCH_LIST,
    DEFAULT_CONTROLNET_CONDITIONING_LIST,
    SEARCH_TERMS,
    MODEL_TYPES_TERMS,
    MODEL_LIST_TERMS,
    RUNWARE_NODE_TYPES,
    RUNWARE_NODE_PROPS
}