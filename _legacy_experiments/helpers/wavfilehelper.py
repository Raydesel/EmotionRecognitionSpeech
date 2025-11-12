"""
WavFileHelper class for reading audio file properties.

This helper class provides methods to extract audio file properties
like number of channels, sample rate, and bit depth from WAV files.
"""

import wave
import os
import numpy as np
from scipy.io import wavfile


class WavFileHelper:
    """
    Helper class for reading WAV file properties.
    
    This class provides methods to extract audio file metadata
    including channels, sample rate, and bit depth.
    """
    
    def __init__(self):
        """Initialize the WavFileHelper."""
        pass
    
    def read_file_properties(self, filename):
        """
        Read audio file properties from a WAV file.
        
        Args:
            filename (str): Path to the WAV file
            
        Returns:
            tuple: (num_channels, sample_rate, bit_depth)
                - num_channels (int): Number of audio channels
                - sample_rate (int): Sample rate in Hz
                - bit_depth (int): Bit depth in bits
                
        Raises:
            FileNotFoundError: If the file doesn't exist
            Exception: If there's an error reading the file
        """
        try:
            # Check if file exists
            if not os.path.exists(filename):
                raise FileNotFoundError(f"File not found: {filename}")
            
            # Read file using scipy.io.wavfile for basic properties
            sample_rate, data = wavfile.read(filename)
            
            # Get number of channels
            if data.ndim == 1:
                num_channels = 1  # Mono
            else:
                num_channels = data.shape[1]  # Stereo or multi-channel
            
            # Calculate bit depth from data type
            if data.dtype == np.int8:
                bit_depth = 8
            elif data.dtype == np.int16:
                bit_depth = 16
            elif data.dtype == np.int32:
                bit_depth = 32
            elif data.dtype == np.float32:
                bit_depth = 32  # Float32 is equivalent to 32-bit
            elif data.dtype == np.float64:
                bit_depth = 64  # Float64 is equivalent to 64-bit
            else:
                # Try to get bit depth from wave module as fallback
                try:
                    with wave.open(filename, 'rb') as wav_file:
                        bit_depth = wav_file.getsampwidth() * 8
                except:
                    bit_depth = 16  # Default assumption
            
            return num_channels, sample_rate, bit_depth
            
        except Exception as e:
            print(f"Error reading file {filename}: {str(e)}")
            # Return default values if there's an error
            return 1, 22050, 16
    
    def get_audio_info(self, filename):
        """
        Get comprehensive audio file information.
        
        Args:
            filename (str): Path to the WAV file
            
        Returns:
            dict: Dictionary containing audio file information
        """
        try:
            num_channels, sample_rate, bit_depth = self.read_file_properties(filename)
            
            # Get file size
            file_size = os.path.getsize(filename)
            
            # Get duration using librosa if available
            try:
                import librosa
                data, sr = librosa.load(filename, sr=None)
                duration = len(data) / sr
            except ImportError:
                # Fallback calculation
                duration = file_size / (sample_rate * num_channels * (bit_depth / 8))
            
            return {
                'filename': filename,
                'num_channels': num_channels,
                'sample_rate': sample_rate,
                'bit_depth': bit_depth,
                'file_size_bytes': file_size,
                'duration_seconds': duration
            }
            
        except Exception as e:
            print(f"Error getting audio info for {filename}: {str(e)}")
            return None
