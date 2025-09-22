import json
import uuid
import requests
import torch
import torchaudio
import numpy as np
from io import BytesIO
import tempfile
import os
from .utils import runwareUtils as rwUtils

class RunwareAudioInference:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "positivePrompt": ("STRING", {
                    "multiline": True,
                    "default": "classical piano piece, gentle and melodic",
                    "tooltip": "Text description that guides the audio generation process"
                }),
                "usePositivePrompt": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Enable/disable positivePrompt parameter in API request"
                }),
                "negativePrompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Text description of what you don't want in the audio"
                }),
                "model": ("RUNWAREAUDIOMODEL", {
                    "tooltip": "AI model to use for audio generation"
                }),
                "duration": ("INT", {
                    "default": 10,
                    "min": 10,
                    "max": 300,
                    "step": 1,
                    "tooltip": "Length of generated audio in seconds (10-300)"
                }),
                "useDuration": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Enable/disable duration parameter in API request"
                }),
                "sampleRate": ("INT", {
                    "default": 22050,
                    "min": 8000,
                    "max": 48000,
                    "step": 1,
                    "tooltip": "Sample rate of the generated audio in Hz (8000-48000)"
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
        # Get required parameters
        positivePrompt = kwargs.get("positivePrompt", "")
        usePositivePrompt = kwargs.get("usePositivePrompt", True)
        model = kwargs.get("model", "")
        duration = kwargs.get("duration", 30)
        useDuration = kwargs.get("useDuration", True)
        sampleRate = kwargs.get("sampleRate", 44100)
        bitrate = kwargs.get("bitrate", 128)
        outputType = kwargs.get("outputType", "URL")
        outputFormat = kwargs.get("outputFormat", "MP3")
        negativePrompt = kwargs.get("negativePrompt", "")
        numberResults = kwargs.get("numberResults", 1)
        providerSettings = kwargs.get("providerSettings", None)
        
        # Create task UUID
        taskUUID = str(uuid.uuid4())
        
        # Build the generation config
        genConfig = [{
            "taskType": "audioInference",
            "taskUUID": taskUUID,
            "model": model,
            "outputType": outputType,
            "outputFormat": outputFormat,
            "deliveryMethod": "sync",
            "includeCost": True,
            "numberResults": numberResults,
            "audioSettings": {
                "sampleRate": sampleRate,
                "bitrate": bitrate
            }
        }]
        
        # Add positivePrompt only if usePositivePrompt is True AND no sections are provided
        has_sections = False
        if providerSettings is not None:
            # Check if there are sections in the provider settings
            if isinstance(providerSettings, dict):
                elevenlabs_settings = providerSettings.get("elevenlabs", {})
                music_settings = elevenlabs_settings.get("music", {})
                composition_plan = music_settings.get("compositionPlan", {})
                sections = composition_plan.get("sections", [])
                has_sections = len(sections) > 0
        
        # When sections are provided, disable duration but add minimal positivePrompt (ElevenLabs requires it)
        if has_sections:
            useDuration = False
            # ElevenLabs requires positivePrompt even with composition plans
            #genConfig[0]["positivePrompt"] = "Music composition"
            print(f"[DEBUG] Disabled duration and added minimal positivePrompt because sections are provided")
        
        if usePositivePrompt:
            genConfig[0]["positivePrompt"] = positivePrompt
            print(f"[DEBUG] Added positivePrompt: '{positivePrompt}' (usePositivePrompt={usePositivePrompt})")
        else:
            print(f"[DEBUG] Skipped positivePrompt (usePositivePrompt={usePositivePrompt})")
        
        # Add duration only if useDuration is True
        if useDuration:
            genConfig[0]["duration"] = duration
            print(f"[DEBUG] Added duration: {duration} (useDuration={useDuration})")
        else:
            print(f"[DEBUG] Skipped duration (useDuration={useDuration})")
        
        # Add optional parameters if provided
        if negativePrompt:
            genConfig[0]["negativePrompt"] = negativePrompt
            
        if providerSettings is not None:
            genConfig[0]["providerSettings"] = providerSettings
        
        # Debug: Print the request being sent
        print(f"[DEBUG] Sending Audio Inference Request:")
        print(f"[DEBUG] Request Payload: {json.dumps(genConfig, indent=2)}")
        
        # Make the API request
        genResult = rwUtils.inferenecRequest(genConfig)
        
        # Debug: Print the response received
        print(f"[DEBUG] Received Audio Inference Response:")
        print(f"[DEBUG] Response: {json.dumps(genResult, indent=2)}")
        
        # Check for errors
        if "errors" in genResult:
            error_message = genResult["errors"][0]["message"]
            raise Exception(f"Audio generation failed: {error_message}")
        
        # Extract audio data from response
        if "data" in genResult and len(genResult["data"]) > 0:
            audioData = genResult["data"][0]
            
            # Get the audio URL
            audioURL = audioData.get("audioURL", "")
            if not audioURL:
                # Fallback to other audio data formats
                audioURL = audioData.get("audioDataURI", "")
                if not audioURL:
                    audioURL = audioData.get("audioBase64Data", "")
            
            if audioURL:
                # Download the audio and create proper audio data for ComfyUI
                try:
                    # Download the audio file
                    response = requests.get(audioURL, timeout=30)
                    response.raise_for_status()
                    
                    # Save to temporary file and load with torchaudio
                    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                        temp_file.write(response.content)
                        temp_file_path = temp_file.name
                    
                    try:
                        # Load audio with torchaudio
                        waveform, original_sample_rate = torchaudio.load(temp_file_path)
                        
                        # Resample if necessary
                        if original_sample_rate != sampleRate:
                            resampler = torchaudio.transforms.Resample(original_sample_rate, sampleRate)
                            waveform = resampler(waveform)
                        
                        # Ensure correct format: [batch, channels, samples]
                        if waveform.dim() == 2:
                            waveform = waveform.unsqueeze(0)  # Add batch dimension
                        
                        # Create the audio object
                        audio_obj = {
                            "waveform": waveform,
                            "sample_rate": sampleRate
                        }
                        
                    finally:
                        # Clean up temporary file
                        if os.path.exists(temp_file_path):
                            os.unlink(temp_file_path)
                    
                    return (audio_obj,)
                    
                except Exception as e:
                    raise Exception(f"Failed to download audio: {e}")
            else:
                raise Exception("No audio URL received from API")
        else:
            raise Exception("No audio data received from API")
