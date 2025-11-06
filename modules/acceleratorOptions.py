class acceleratorOptions:
    """Accelerator Options node for configuring caching options for faster generation"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "fbcache": ("BOOLEAN", {
                    "tooltip": "Enable Frame Buffer Cache for faster generation",
                    "default": None,
                }),
                "useCacheDistance": ("BOOLEAN", {
                    "tooltip": "Enable to include cacheDistance parameter in API request.",
                    "default": False,
                }),
                "cacheDistance": ("FLOAT", {
                    "tooltip": "Cache distance parameter for FBCache",
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
                "teaCache": ("BOOLEAN", {
                    "tooltip": "Enable TeaCache for transformer-based models (Flux, SD3). Does not work with UNet models like SDXL or SD1.5. Particularly effective for iterative editing workflows.",
                    "default": None,
                }),
                "useTeaCacheDistance": ("BOOLEAN", {
                    "tooltip": "Enable to include teaCacheDistance parameter in API request.",
                    "default": False,
                }),
                "teaCacheDistance": ("FLOAT", {
                    "tooltip": "Controls TeaCache aggressiveness: 0.0 (conservative/quality) to 1.0 (aggressive/speed). Lower values maintain quality, higher values prioritize speed.",
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
                "deepCache": ("BOOLEAN", {
                    "tooltip": "Enable DeepCache for UNet-based models (SDXL, SD1.5). Not applicable to transformer models. Provides performance improvements for high-throughput scenarios.",
                    "default": None,
                }),
                "useDeepCacheOptions": ("BOOLEAN", {
                    "tooltip": "Enable to include DeepCache options (deepCacheInterval and deepCacheBranchId) in API request.",
                    "default": False,
                }),
                "deepCacheInterval": ("INT", {
                    "tooltip": "Frequency of feature caching - steps between cache operations. Larger values = faster but may impact quality. Smaller values = better quality but slower.",
                    "default": 1,
                    "min": 1,
                    "max": 20,
                }),
                "deepCacheBranchId": ("INT", {
                    "tooltip": "Network branch for caching (0=shallowest, deeper=more conservative). Lower IDs = aggressive caching/faster, higher IDs = conservative caching/better quality.",
                    "default": 0,
                    "min": 0,
                    "max": 10,
                }),
                "useCacheSteps": ("BOOLEAN", {
                    "tooltip": "Enable to include cache step control parameters (step numbers) in API request.",
                    "default": False,
                }),
                "cacheStartStep": ("INT", {
                    "tooltip": "Inference step number where caching begins (0 to total steps). Only included when useCacheSteps is enabled and value > 0.",
                    "default": 0,
                    "min": 0,
                    "max": 200,
                }),
                "cacheEndStep": ("INT", {
                    "tooltip": "Inference step number where caching stops (must be > cacheStartStep). Only included when useCacheSteps is enabled.",
                    "default": 1,
                    "min": 1,
                    "max": 200,
                }),
                "useCachePercentageSteps": ("BOOLEAN", {
                    "tooltip": "Enable to include cache step control parameters (percentages) in API request.",
                    "default": False,
                }),
                "cacheStartStepPercentage": ("INT", {
                    "tooltip": "Percentage of total steps where caching begins (0-99). Only included when useCachePercentageSteps is enabled and value > 0.",
                    "default": 0,
                    "min": 0,
                    "max": 99,
                }),
                "cacheEndStepPercentage": ("INT", {
                    "tooltip": "Percentage of total steps where caching stops (must be > cacheStartStepPercentage). Only included when useCachePercentageSteps is enabled.",
                    "default": 1,
                    "min": 1,
                    "max": 100,
                }),
                "useCacheMaxConsecutiveSteps": ("BOOLEAN", {
                    "tooltip": "Enable to include cacheMaxConsecutiveSteps parameter in API request.",
                    "default": False,
                }),
                "cacheMaxConsecutiveSteps": ("INT", {
                    "tooltip": "Max consecutive steps using cached computations before forcing fresh computation. Prevents quality degradation from extended cache reuse.",
                    "default": 1,
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
        """Build accelerator options dictionary"""
        params = self._extractParameters(kwargs)
        acceleratorOptions = self._buildAcceleratorOptions(params)
        return (acceleratorOptions,)

    def _extractParameters(self, kwargs):
        """Extract all parameters from kwargs"""
        return {
            "fbcache": kwargs.get("fbcache"),
            "useCacheDistance": kwargs.get("useCacheDistance", False),
            "cacheDistance": kwargs.get("cacheDistance", 0.0),
            "teaCache": kwargs.get("teaCache"),
            "useTeaCacheDistance": kwargs.get("useTeaCacheDistance", False),
            "teaCacheDistance": kwargs.get("teaCacheDistance", 0.0),
            "deepCache": kwargs.get("deepCache"),
            "useDeepCacheOptions": kwargs.get("useDeepCacheOptions", False),
            "deepCacheInterval": kwargs.get("deepCacheInterval", 1),
            "deepCacheBranchId": kwargs.get("deepCacheBranchId", 0),
            "useCacheSteps": kwargs.get("useCacheSteps", False),
            "cacheStartStep": kwargs.get("cacheStartStep", 0),
            "cacheEndStep": kwargs.get("cacheEndStep", 1),
            "useCachePercentageSteps": kwargs.get("useCachePercentageSteps", False),
            "cacheStartStepPercentage": kwargs.get("cacheStartStepPercentage", 0),
            "cacheEndStepPercentage": kwargs.get("cacheEndStepPercentage", 1),
            "useCacheMaxConsecutiveSteps": kwargs.get("useCacheMaxConsecutiveSteps", False),
            "cacheMaxConsecutiveSteps": kwargs.get("cacheMaxConsecutiveSteps", 1),
        }

    def _buildAcceleratorOptions(self, params):
        """Build accelerator options dictionary from parameters"""
        acceleratorOptions = {}
        
        if params["fbcache"] is True:
            acceleratorOptions["fbcache"] = params["fbcache"]
        if params["useCacheDistance"]:
            acceleratorOptions["cacheDistance"] = params["cacheDistance"]
        
        if params["teaCache"] is True:
            acceleratorOptions["teaCache"] = params["teaCache"]
        if params["useTeaCacheDistance"]:
            acceleratorOptions["teaCacheDistance"] = params["teaCacheDistance"]
            
        if params["deepCache"] is True:
            acceleratorOptions["deepCache"] = params["deepCache"]
        if params["useDeepCacheOptions"]:
            acceleratorOptions["deepCacheInterval"] = params["deepCacheInterval"]
            acceleratorOptions["deepCacheBranchId"] = params["deepCacheBranchId"]
            
        if params["useCacheSteps"]:
            if params["cacheStartStep"] > 0:
                acceleratorOptions["cacheStartStep"] = params["cacheStartStep"]
            acceleratorOptions["cacheEndStep"] = params["cacheEndStep"]
        
        if params["useCachePercentageSteps"]:
            if params["cacheStartStepPercentage"] > 0:
                acceleratorOptions["cacheStartStepPercentage"] = params["cacheStartStepPercentage"]
            acceleratorOptions["cacheEndStepPercentage"] = params["cacheEndStepPercentage"]
        
        if params["useCacheMaxConsecutiveSteps"]:
            acceleratorOptions["cacheMaxConsecutiveSteps"] = params["cacheMaxConsecutiveSteps"]

        return acceleratorOptions
