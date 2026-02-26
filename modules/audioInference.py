import uuid
import requests
import torch
import numpy as np
import librosa
import tempfile
import os
import comfy.model_management
from .utils import runwareUtils as rwUtils


class RunwareAudioInference:
    """Runware Audio Inference node for generating audio using Runware API"""
    
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("RUNWAREAUDIOMODEL", {
                    "tooltip": "AI model to use for audio generation"
                }),
                "usePositivePrompt": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Enable/disable positivePrompt parameter in API request"
                }),
                "positivePrompt": ("STRING", {
                    "multiline": True,
                    "default": "classical piano piece, gentle and melodic",
                    "tooltip": "Text description that guides the audio generation process"
                }),
                "negativePrompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Text description of what you don't want in the audio"
                }),
                "useDuration": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Enable/disable duration parameter in API request"
                }),
                "duration": ("INT", {
                    "default": 10,
                    "min": 10,
                    "max": 300,
                    "step": 1,
                    "tooltip": "Length of generated audio in seconds (10-300)"
                }),
                "useSampleRate": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Enable/disable sampleRate parameter in API request"
                }),
                "sampleRate": ([8000, 16000, 22050, 24000, 32000, 44100], {
                    "default": 32000,
                    "tooltip": "Audio sample rate in Hz. Supported: 8000, 16000, 22050, 24000, 32000, 44100."
                }),
                "useBitrate": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Enable/disable bitrate parameter in API request (MP3 only)"
                }),
                "bitrate": ([32, 64, 128, 256], {
                    "default": 128,
                    "tooltip": "Audio bitrate in kbps. Allowed: 32, 64, 128, 256. Only applies to MP3 format."
                }),
                "useChannels": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Enable/disable channels parameter in API request"
                }),
                "channels": ("INT", {
                    "default": 2,
                    "min": 1,
                    "max": 2,
                    "step": 1,
                    "tooltip": "Number of audio channels (1=mono, 2=stereo)"
                }),
                "outputType": (["URL", "dataURI", "base64Data"], {
                    "default": "URL",
                    "tooltip": "Output type for the generated audio"
                }),
                "outputFormat": (["MP3", "MP4"], {
                    "default": "MP3",
                    "tooltip": "Format of the output audio"
                }),
                "numberResults": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 3,
                    "tooltip": "Number of audio files to generate"
                }),
                "useSeed": ("BOOLEAN", {
                    "tooltip": "Enable to include seed parameter in API request for reproducible generation.",
                    "default": False,
                }),
                "seed": ("INT", {
                    "tooltip": "Seed for reproducible audio generation. Only used when 'Use Seed' is enabled.",
                    "default": 1,
                    "min": 1,
                    "max": 2147483647,
                }),
                "useSteps": ("BOOLEAN", {
                    "tooltip": "Enable to include steps parameter in API request. Disable if your model doesn't support steps.",
                    "default": False,
                }),
                "steps": ("INT", {
                    "tooltip": "Number of inference steps for audio generation. More steps generally result in higher quality but longer generation time.",
                    "default": 20,
                    "min": 1,
                    "max": 100,
                }),
                "useStrength": ("BOOLEAN", {
                    "tooltip": "Enable to include strength parameter in API request. Used for audio-to-audio generation.",
                    "default": False,
                }),
                "strength": ("FLOAT", {
                    "tooltip": "Influence of the input audio in audio-to-audio generation. Lower = more original, higher = more variation. Only used when 'Use Strength' is enabled.",
                    "default": 0.8,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
                "useCFGScale": ("BOOLEAN", {
                    "tooltip": "Enable to include CFGScale parameter in API request. Disable if your model doesn't support CFG scale.",
                    "default": False,
                }),
                "CFGScale": ("FLOAT", {
                    "tooltip": "Classifier-free guidance scale. Higher values adhere more closely to the prompt. Only used when 'Use CFG Scale' is enabled.",
                    "default": 12.0,
                    "min": 1.0,
                    "max": 50.0,
                    "step": 0.5,
                }),
            },
            "optional": {
                "inputs": ("RUNWAREAUDIOINFERENCEINPUTS", {
                    "tooltip": "Custom inputs for audio generation (e.g., video URL for audio extraction)"
                }),
                "settings": ("RUNWAREAUDIOSETTINGS", {
                    "tooltip": "Connect Runware Audio Inference Settings for lyrics, guidanceType, etc."
                }),
                "speech": ("RUNWARESPEECH", {
                    "tooltip": "Connect Runware Audio Inference Speech for speech synthesis (e.g. Minimax)"
                }),
                "voiceModify": ("RUNWAREVOICEMODIFY", {
                    "tooltip": "Connect Runware Audio Inference Settings Voice Modify for pitch, intensity, timbre, sound effects"
                }),
                "providerSettings": ("RUNWAREPROVIDERSETTINGS", {
                    "tooltip": "Provider-specific configuration settings"
                }),
            }
        }

    RETURN_TYPES = ("AUDIO", "VIDEO")
    RETURN_NAMES = ("audio", "video")
    FUNCTION = "generateAudio"
    CATEGORY = "Runware/Audio"

    def generateAudio(self, **kwargs):
        """Main function to generate audio using Runware API"""
        params = self._extractParameters(kwargs)
        genConfig = self._buildGenConfig(params)
        
        try:
            # Debug: Print the request being sent
            print(f"[DEBUG] Sending Audio Inference Request:")
            print(f"[DEBUG] Request Payload: {rwUtils.safe_json_dumps(genConfig, indent=2)}")
            
            genResult = rwUtils.inferenecRequest(genConfig)
            
            # Debug: Print the response received
            print(f"[DEBUG] Received Audio Inference Response:")
            print(f"[DEBUG] Response: {rwUtils.safe_json_dumps(genResult, indent=2)}")
            
            print(f"[Debugging] Generation config: {rwUtils.safe_json_dumps(genConfig, indent=2)}")
        except Exception as e:
            # Re-raise the original error without modification
            raise e
        
        # Extract task UUID for polling
        taskUUID = genConfig[0]["taskUUID"]
        
        # Poll for audio completion
        while True:
            # Check for interrupt before each poll
            comfy.model_management.throw_exception_if_processing_interrupted()
            
            # Poll for audio result
            pollResult = rwUtils.pollVideoResult(taskUUID)
            print(f"[Debugging] Poll result: {rwUtils.safe_json_dumps(pollResult, indent=2) if isinstance(pollResult, (dict, list)) else pollResult}")
            
            # Check for errors first
            if pollResult and "errors" in pollResult and len(pollResult["errors"]) > 0:
                error_info = pollResult["errors"][0]
                error_message = error_info.get("message", "Unknown error")
                
                # Extract more detailed error info if available
                if "responseContent" in error_info:
                    response_content = error_info["responseContent"]
                    # Handle both string and dict response content
                    if isinstance(response_content, str):
                        detailed_message = response_content
                    elif isinstance(response_content, dict):
                        detailed_message = response_content.get("message", str(response_content))
                    else:
                        detailed_message = str(response_content)
                    
                    if detailed_message:
                        error_message = f"{error_message}\nProvider Error: {detailed_message}"
                
                # Include taskUUID for debugging
                task_uuid = error_info.get("taskUUID", "unknown")
                raise Exception(f"Audio generation failed (Task: {task_uuid}): {error_message}")
            
            if pollResult and "data" in pollResult and len(pollResult["data"]) > 0:
                audioData = pollResult["data"][0]
                
                # Check status directly
                if "status" in audioData:
                    status = audioData["status"]
                    
                    if status == "success":
                        audioUrl = self._extractAudioUrl(pollResult)
                        hasAudio = audioUrl is not None
                        hasVideo = bool(audioData.get("videoURL") or audioData.get("videoBase64Data", False))
                        
                        if hasAudio:
                            audioObj = self._downloadAndProcessAudio(audioUrl, params["sampleRate"])
                            print(f"[DEBUG] Audio URL found, returning audio. Audio URL: {audioUrl}")
                            # Return empty video object when only audio is present (prevents errors in downstream nodes)
                            emptyVideoObj = rwUtils.VideoObject("", width=0, height=0)
                            return (audioObj, emptyVideoObj)
                        
                        if hasVideo:
                            videos = rwUtils.convertVideoB64List(pollResult, width=None, height=None)
                            print(f"[DEBUG] No audio URL in response, but video is present. Returning video.")
                            # Extract first video object from tuple (ComfyUI expects single VideoObject, not tuple)
                            if len(videos) > 0:
                                # Return empty audio object when only video is present (prevents errors in downstream nodes)
                                emptyAudioObj = {
                                    "waveform": torch.zeros((1, 1, 1)),  # [batch, channels, samples]
                                    "sample_rate": params["sampleRate"]
                                }
                                return (emptyAudioObj, videos[0])
                            else:
                                raise Exception("No video object found in response")
                        
                        raise Exception("No audio or video data received from API")
                    
                    # If status is "processing", continue polling
            
            # Check for interrupt before waiting
            comfy.model_management.throw_exception_if_processing_interrupted()
            
            # Wait before next poll (split into smaller chunks to allow more frequent interrupt checks)
            for _ in range(10):  # 10 x 0.1 second = 1 second total
                comfy.model_management.throw_exception_if_processing_interrupted()
                rwUtils.time.sleep(0.1)

    def _extractParameters(self, kwargs):
        """Extract and validate parameters from kwargs"""
        return {
            "positivePrompt": kwargs.get("positivePrompt", ""),
            "usePositivePrompt": kwargs.get("usePositivePrompt", True),
            "model": kwargs.get("model", ""),
            "duration": kwargs.get("duration", 30),
            "useDuration": kwargs.get("useDuration", True),
            "sampleRate": int(kwargs.get("sampleRate", 32000)),
            "useSampleRate": kwargs.get("useSampleRate", False),
            "bitrate": kwargs.get("bitrate", 128),
            "useBitrate": kwargs.get("useBitrate", False),
            "channels": kwargs.get("channels", 2),
            "useChannels": kwargs.get("useChannels", False),
            "outputType": kwargs.get("outputType", "URL"),
            "outputFormat": kwargs.get("outputFormat", "MP3"),
            "negativePrompt": kwargs.get("negativePrompt", ""),
            "numberResults": kwargs.get("numberResults", 1),
            "seed": kwargs.get("seed", 1),
            "useSeed": kwargs.get("useSeed", False),
            "steps": kwargs.get("steps", 20),
            "useSteps": kwargs.get("useSteps", False),
            "strength": kwargs.get("strength", 0.8),
            "useStrength": kwargs.get("useStrength", False),
            "CFGScale": kwargs.get("CFGScale", 12.0),
            "useCFGScale": kwargs.get("useCFGScale", False),
            "inputs": kwargs.get("inputs", None),
            "settings": kwargs.get("settings", None),
            "speech": kwargs.get("speech", None),
            "voiceModify": kwargs.get("voiceModify", None),
            "providerSettings": kwargs.get("providerSettings", None),
        }

    def _hasSections(self, providerSettings):
        """Check if provider settings contain sections"""
        if not providerSettings or not isinstance(providerSettings, dict):
            return False
        
        # Provider settings is now flat (e.g., {"music": {...}})
        # Check if it has music.compositionPlan.sections
        musicSettings = providerSettings.get("music", {})
        compositionPlan = musicSettings.get("compositionPlan", {})
        sections = compositionPlan.get("sections", [])
        
        return len(sections) > 0

    def _buildGenConfig(self, params):
        """Build the generation configuration for API request"""
        taskUuid = str(uuid.uuid4())
        
        genConfig = [{
            "taskType": "audioInference",
            "taskUUID": taskUuid,
            "model": params["model"],
            "outputType": params["outputType"],
            "outputFormat": params["outputFormat"],
            "deliveryMethod": "async",
            "includeCost": True,
            "numberResults": params["numberResults"],
        }]
        
        # Build audioSettings conditionally based on use flags
        audioSettings = {}
        if params["useSampleRate"]:
            audioSettings["sampleRate"] = int(params["sampleRate"])
        if params["useBitrate"]:
            _br = int(params["bitrate"])
            _allowed_bitrates = (32, 64, 128, 256)
            audioSettings["bitrate"] = _br if _br in _allowed_bitrates else min(_allowed_bitrates, key=lambda x: abs(x - _br))
        if params["useChannels"]:
            audioSettings["channels"] = params["channels"]
        
        # Only add audioSettings if at least one setting is enabled
        if audioSettings:
            genConfig[0]["audioSettings"] = audioSettings
        
        # Handle sections - disable duration if sections are provided
        hasSections = self._hasSections(params["providerSettings"])
        if hasSections:
            params["useDuration"] = False
            print(f"[DEBUG] Disabled duration because sections are provided")
        
        # Add prompts conditionally
        if params["usePositivePrompt"]:
            genConfig[0]["positivePrompt"] = params["positivePrompt"]
            print(f"[DEBUG] Added positivePrompt: '{params['positivePrompt']}'")
        else:
            print(f"[DEBUG] Skipped positivePrompt")
        
        if params["useDuration"]:
            genConfig[0]["duration"] = params["duration"]
            print(f"[DEBUG] Added duration: {params['duration']}")
        else:
            print(f"[DEBUG] Skipped duration")
        
        # Add seed parameter only if enabled
        if params["useSeed"]:
            genConfig[0]["seed"] = params["seed"]

        # Add steps parameter only if enabled
        if params["useSteps"]:
            genConfig[0]["steps"] = params["steps"]

        # Add strength parameter only if enabled
        if params["useStrength"]:
            genConfig[0]["strength"] = params["strength"]

        # Add CFGScale parameter only if enabled
        if params["useCFGScale"]:
            genConfig[0]["CFGScale"] = params["CFGScale"]

        # Add optional parameters
        if params["negativePrompt"]:
            genConfig[0]["negativePrompt"] = params["negativePrompt"]
        
        # Handle audio settings (lyrics, guidance_type)
        if params["settings"] is not None and isinstance(params["settings"], dict) and len(params["settings"]) > 0:
            genConfig[0]["settings"] = params["settings"]
            print(f"[DEBUG] Audio settings merged: {rwUtils.sanitize_for_logging(params['settings'])}")

        # Handle speech (from Runware Audio Inference Speech node)
        if params["speech"] is not None and isinstance(params["speech"], dict) and len(params["speech"]) > 0:
            genConfig[0]["speech"] = params["speech"]
            print(f"[DEBUG] Speech merged: {rwUtils.sanitize_for_logging(params['speech'])}")

        # Handle voiceModify (from Runware Audio Inference Settings Voice Modify node) -> settings.voiceModify
        if params["voiceModify"] is not None and isinstance(params["voiceModify"], dict) and len(params["voiceModify"]) > 0:
            if "settings" not in genConfig[0]:
                genConfig[0]["settings"] = {}
            vm = dict(params["voiceModify"])

            genConfig[0]["settings"]["voiceModify"] = vm
            print(f"[DEBUG] Voice modify merged: {rwUtils.sanitize_for_logging(vm)}")
        
        # Handle inputs - merge custom inputs from Audio Inference Inputs node
        if params["inputs"] is not None:
            # Merge inputs from audio inference inputs node
            if "inputs" not in genConfig[0]:
                genConfig[0]["inputs"] = {}
            
            # Merge each input from inputs
            for key, value in params["inputs"].items():
                genConfig[0]["inputs"][key] = value
            
            print(f"[DEBUG] Audio inference inputs merged: {rwUtils.sanitize_for_logging(params['inputs'])}")
            print(f"[DEBUG] Final genConfig inputs: {rwUtils.sanitize_for_logging(genConfig[0].get('inputs', {}))}")
        
        # Handle providerSettings - extract provider name from model and wrap with provider name (same pattern as video inference)
        if params["providerSettings"] is not None:
            # Extract provider name from model (e.g., "klingai:8@1" -> "klingai", "elevenlabs:1@1" -> "elevenlabs")
            provider_name = params["model"].split(":")[0] if ":" in params["model"] else params["model"]
            
            # If providerSettings is a dictionary, create the correct API format
            if isinstance(params["providerSettings"], dict):
                # Create the providerSettings object with provider name as key
                final_provider_settings = {
                    provider_name: params["providerSettings"]
                }
                genConfig[0]["providerSettings"] = final_provider_settings
                print(f"[DEBUG] Provider settings wrapped with provider name: {rwUtils.sanitize_for_logging(final_provider_settings)}")
            else:
                # If it's just a string, use it directly
                genConfig[0]["providerSettings"] = params["providerSettings"]
        
        print(f"[DEBUG] Sending Audio Inference Request:")
        print(f"[DEBUG] Request Payload: {rwUtils.safe_json_dumps(genConfig, indent=2)}")
        
        return genConfig

    def _logResponse(self, genResult):
        """Log the API response for debugging"""
        print(f"[DEBUG] Received Audio Inference Response:")
        print(f"[DEBUG] Response: {rwUtils.safe_json_dumps(genResult, indent=2)}")

    def _validateResponse(self, genResult):
        """Validate API response and raise errors if needed"""
        if "errors" in genResult:
            errorMessage = genResult["errors"][0]["message"]
            raise Exception(f"Audio generation failed: {errorMessage}")
        
        if "data" not in genResult or len(genResult["data"]) == 0:
            raise Exception("No data received from API")
        
        
        audioData = genResult["data"][0]
        hasAudio = bool(audioData.get("audioURL") or audioData.get("audioDataURI") or audioData.get("audioBase64Data"))
        hasVideo = bool(audioData.get("videoURL") or audioData.get("videoBase64Data") or audioData.get("videoUUID"))
        
        if not hasAudio and not hasVideo:
            raise Exception("No audio or video data received from API")

    def _extractAudioUrl(self, genResult):
        """Extract audio URL from API response. Returns None if no audio URL is present (e.g., when only video is returned)."""
        audioData = genResult["data"][0]
        
        audioUrl = audioData.get("audioURL", "")
        if not audioUrl:
            audioUrl = audioData.get("audioDataURI", "")
        if not audioUrl:
            audioUrl = audioData.get("audioBase64Data", "")
        

        return audioUrl if audioUrl else None

    def _downloadAndProcessAudio(self, audioUrl, targetSampleRate):
        """Download audio file and process it for ComfyUI"""
        try:
            response = requests.get(audioUrl, timeout=30)
            response.raise_for_status()
            
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tempFile:
                tempFile.write(response.content)
                tempFilePath = tempFile.name
            
            try:
                waveformNp, originalSampleRate = self._loadAudioFile(tempFilePath)
                waveformNp = self._resampleAudio(waveformNp, originalSampleRate, targetSampleRate)
                waveformTensor = self._convertToTensor(waveformNp)
                
                return {
                    "waveform": waveformTensor,
                    "sample_rate": targetSampleRate
                }
            finally:
                if os.path.exists(tempFilePath):
                    os.unlink(tempFilePath)
        except Exception as e:
            raise Exception(f"Failed to download audio: {e}")

    def _loadAudioFile(self, filePath):
        """Load audio file using librosa"""
        waveformNp, originalSampleRate = librosa.load(filePath, sr=None, mono=False)
        
        # Convert to [samples, channels] format
        if waveformNp.ndim == 1:
            waveformNp = waveformNp.reshape(-1, 1)
        else:
            waveformNp = waveformNp.T  # [channels, samples] -> [samples, channels]
        
        return waveformNp, originalSampleRate

    def _resampleAudio(self, waveformNp, originalSampleRate, targetSampleRate):
        """Resample audio to target sample rate"""
        if originalSampleRate == targetSampleRate:
            return waveformNp
        
        if waveformNp.ndim == 1:
            return librosa.resample(waveformNp, orig_sr=originalSampleRate, target_sr=targetSampleRate)
        else:
            # Multi-channel: resample each channel
            return librosa.resample(waveformNp.T, orig_sr=originalSampleRate, target_sr=targetSampleRate).T

    def _convertToTensor(self, waveformNp):
        """Convert numpy array to PyTorch tensor with correct format"""
        # Ensure 2D shape [samples, channels]
        if waveformNp.ndim == 1:
            waveformNp = waveformNp.reshape(-1, 1)
        
        # Convert to [channels, samples] for ComfyUI
        waveformTensor = torch.from_numpy(waveformNp.T).float()
        
        # Add batch dimension if needed: [batch, channels, samples]
        if waveformTensor.dim() == 2:
            waveformTensor = waveformTensor.unsqueeze(0)
        
        return waveformTensor
