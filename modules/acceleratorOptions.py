from .utils import runwareUtils as rwUtils

class acceleratorOptions:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                # FBCache parameters
                "fbcache": ("BOOLEAN", {
                    "tooltip": "Enable Frame Buffer Cache for faster generation",
                    "default": None,
                }),
                "cacheDistance": ("FLOAT", {
                    "tooltip": "Cache distance parameter for FBCache",
                    "default": None,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
                
                # TeaCache parameters
                "teaCache": ("BOOLEAN", {
                    "tooltip": "Enable TeaCache for transformer-based models (Flux, SD3). Does not work with UNet models like SDXL or SD1.5. Particularly effective for iterative editing workflows.",
                    "default": None,
                }),
                "teaCacheDistance": ("FLOAT", {
                    "tooltip": "Controls TeaCache aggressiveness: 0.0 (conservative/quality) to 1.0 (aggressive/speed). Lower values maintain quality, higher values prioritize speed.",
                    "default": None,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
                
                # DeepCache parameters
                "deepCache": ("BOOLEAN", {
                    "tooltip": "Enable DeepCache for UNet-based models (SDXL, SD1.5). Not applicable to transformer models. Provides performance improvements for high-throughput scenarios.",
                    "default": None,
                }),
                "deepCacheInterval": ("INT", {
                    "tooltip": "Frequency of feature caching - steps between cache operations. Larger values = faster but may impact quality. Smaller values = better quality but slower.",
                    "default": None,
                    "min": 1,
                    "max": 20,
                }),
                "deepCacheBranchId": ("INT", {
                    "tooltip": "Network branch for caching (0=shallowest, deeper=more conservative). Lower IDs = aggressive caching/faster, higher IDs = conservative caching/better quality.",
                    "default": None,
                    "min": 0,
                    "max": 10,
                }),
                
                # Cache step control parameters
                "cacheStartStep": ("INT", {
                    "tooltip": "Inference step number where caching begins (0 to total steps). Alternative to cacheStartStepPercentage.",
                    "default": None,
                    "min": 0,
                    "max": 200,
                }),
                "cacheStartStepPercentage": ("INT", {
                    "tooltip": "Percentage of total steps where caching begins (0-99). Alternative to cacheStartStep.",
                    "default": None,
                    "min": 0,
                    "max": 99,
                }),
                "cacheEndStep": ("INT", {
                    "tooltip": "Inference step number where caching stops (must be > cacheStartStep). Alternative to cacheEndStepPercentage.",
                    "default": None,
                    "min": 1,
                    "max": 200,
                }),
                "cacheEndStepPercentage": ("INT", {
                    "tooltip": "Percentage of total steps where caching stops (must be > cacheStartStepPercentage). Alternative to cacheEndStep.",
                    "default": None,
                    "min": 1,
                    "max": 100,
                }),
                "cacheMaxConsecutiveSteps": ("INT", {
                    "tooltip": "Max consecutive steps using cached computations before forcing fresh computation. Prevents quality degradation from extended cache reuse.",
                    "default": None,
                    "min": 1,
                    "max": 5,
                }),
            },
        }

    DESCRIPTION = "Configure Runware accelerator options for faster image generation. Supports TeaCache (transformer models like Flux/SD3) and DeepCache (UNet models like SDXL/SD1.5) with fine-grained control over caching parameters and step ranges. Note: These caching methods work best with deterministic schedulers (Euler, DDIM) rather than stochastic schedulers."
    FUNCTION = "acceleratorOptions"
    RETURN_TYPES = ("RUNWAREACCELERATOR",)
    RETURN_NAMES = ("Runware Accelerator",)
    CATEGORY = "Runware"

    def acceleratorOptions(self, **kwargs):
        # Get all optional parameters
        fbcache = kwargs.get("fbcache")
        cacheDistance = kwargs.get("cacheDistance")
        teaCache = kwargs.get("teaCache")
        teaCacheDistance = kwargs.get("teaCacheDistance")
        deepCache = kwargs.get("deepCache")
        deepCacheInterval = kwargs.get("deepCacheInterval")
        deepCacheBranchId = kwargs.get("deepCacheBranchId")
        cacheStartStep = kwargs.get("cacheStartStep")
        cacheStartStepPercentage = kwargs.get("cacheStartStepPercentage")
        cacheEndStep = kwargs.get("cacheEndStep")
        cacheEndStepPercentage = kwargs.get("cacheEndStepPercentage")
        cacheMaxConsecutiveSteps = kwargs.get("cacheMaxConsecutiveSteps")

        # Build accelerator options dictionary
        acceleratorOptions = {}
        
        # FBCache options
        if fbcache is not None:
            acceleratorOptions["fbcache"] = fbcache
        if cacheDistance is not None:
            acceleratorOptions["cacheDistance"] = cacheDistance
        
        # TeaCache options
        if teaCache is not None:
            acceleratorOptions["teaCache"] = teaCache
        if teaCacheDistance is not None:
            acceleratorOptions["teaCacheDistance"] = teaCacheDistance
            
        # DeepCache options
        if deepCache is not None:
            acceleratorOptions["deepCache"] = deepCache
        if deepCacheInterval is not None:
            acceleratorOptions["deepCacheInterval"] = deepCacheInterval
        if deepCacheBranchId is not None:
            acceleratorOptions["deepCacheBranchId"] = deepCacheBranchId
            
        # Cache step control options
        if cacheStartStep is not None:
            acceleratorOptions["cacheStartStep"] = cacheStartStep
        if cacheStartStepPercentage is not None:
            acceleratorOptions["cacheStartStepPercentage"] = cacheStartStepPercentage
        if cacheEndStep is not None:
            acceleratorOptions["cacheEndStep"] = cacheEndStep
        if cacheEndStepPercentage is not None:
            acceleratorOptions["cacheEndStepPercentage"] = cacheEndStepPercentage
        if cacheMaxConsecutiveSteps is not None:
            acceleratorOptions["cacheMaxConsecutiveSteps"] = cacheMaxConsecutiveSteps

        return (acceleratorOptions,)
