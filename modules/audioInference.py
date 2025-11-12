import uuid
import requests
import torch
import numpy as np
import librosa
import tempfile
import os
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
                    "default": True,
                    "tooltip": "Enable/disable sampleRate parameter in API request"
                }),
                "sampleRate": ("INT", {
                    "default": 22050,
                    "min": 8000,
                    "max": 48000,
                    "step": 1,
                    "tooltip": "Sample rate of the generated audio in Hz (8000-48000)"
                }),
                "useBitrate": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Enable/disable bitrate parameter in API request"
                }),
                "bitrate": ("INT", {
                    "default": 32,
                    "min": 32,
                    "max": 320,
                    "step": 32,
                    "tooltip": "Bitrate of the generated audio in kbps (32-320)"
                }),
                "outputType": (["URL", "dataURI", "base64Data"], {
                    "default": "URL",
                    "tooltip": "Output type for the generated audio"
                }),
                "outputFormat": (["MP3"], {
                    "default": "MP3",
                    "tooltip": "Format of the output audio"
                }),
                "numberResults": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 3,
                    "tooltip": "Number of audio files to generate"
                }),
            },
            "optional": {
                "inputs": ("RUNWAREAUDIOINFERENCEINPUTS", {
                    "tooltip": "Custom inputs for audio generation (e.g., video URL for audio extraction)"
                }),
                "providerSettings": ("RUNWAREPROVIDERSETTINGS", {
                    "tooltip": "Provider-specific configuration settings"
                }),
            }
        }

    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)
    FUNCTION = "generateAudio"
    CATEGORY = "Runware/Audio"

    def generateAudio(self, **kwargs):
        """Main function to generate audio using Runware API"""
        params = self._extractParameters(kwargs)
        genConfig = self._buildGenConfig(params)
        genResult = rwUtils.inferenecRequest(genConfig)
        
        self._logResponse(genResult)
        self._validateResponse(genResult)
        
        audioUrl = self._extractAudioUrl(genResult)
        audioObj = self._downloadAndProcessAudio(audioUrl, params["sampleRate"])
        
        return (audioObj,)

    def _extractParameters(self, kwargs):
        """Extract and validate parameters from kwargs"""
        return {
            "positivePrompt": kwargs.get("positivePrompt", ""),
            "usePositivePrompt": kwargs.get("usePositivePrompt", True),
            "model": kwargs.get("model", ""),
            "duration": kwargs.get("duration", 30),
            "useDuration": kwargs.get("useDuration", True),
            "sampleRate": kwargs.get("sampleRate", 22050),
            "useSampleRate": kwargs.get("useSampleRate", True),
            "bitrate": kwargs.get("bitrate", 32),
            "useBitrate": kwargs.get("useBitrate", True),
            "outputType": kwargs.get("outputType", "URL"),
            "outputFormat": kwargs.get("outputFormat", "MP3"),
            "negativePrompt": kwargs.get("negativePrompt", ""),
            "numberResults": kwargs.get("numberResults", 1),
            "inputs": kwargs.get("inputs", None),
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
            "deliveryMethod": "sync",
            "includeCost": True,
            "numberResults": params["numberResults"],
        }]
        
        # Build audioSettings conditionally based on use flags
        audioSettings = {}
        if params["useSampleRate"]:
            audioSettings["sampleRate"] = params["sampleRate"]
        if params["useBitrate"]:
            audioSettings["bitrate"] = params["bitrate"]
        
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
        
        # Add optional parameters
        if params["negativePrompt"]:
            genConfig[0]["negativePrompt"] = params["negativePrompt"]
        
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
            raise Exception("No audio data received from API")

    def _extractAudioUrl(self, genResult):
        """Extract audio URL from API response"""
        audioData = genResult["data"][0]
        
        audioUrl = audioData.get("audioURL", "")
        if not audioUrl:
            audioUrl = audioData.get("audioDataURI", "")
        if not audioUrl:
            audioUrl = audioData.get("audioBase64Data", "")
        
        if not audioUrl:
            raise Exception("No audio URL received from API")
        
        return audioUrl

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
