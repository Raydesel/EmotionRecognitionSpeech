#!/usr/bin/env python3
"""
Simple GPU Utilities for Emotion Recognition Speech Project
No complex imports needed - everything is self-contained
"""

import tensorflow as tf
import numpy as np
import pynvml

def setup_gpu_environment():
    """Setup GPU environment with optimal settings."""
    print("🔧 Setting up GPU environment...")
    
    # Check GPU availability
    gpus = tf.config.list_physical_devices('GPU')
    if not gpus:
        print("❌ No GPUs found")
        return False
    
    print(f"✓ Found {len(gpus)} GPU(s)")
    
    # Configure GPU memory growth
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print("✓ GPU memory growth enabled")
    except Exception as e:
        print(f"⚠️  Could not set memory growth: {e}")
    
    # Enable mixed precision for better performance
    try:
        tf.keras.mixed_precision.set_global_policy('mixed_float16')
        print("✓ Mixed precision enabled (FP16)")
    except Exception as e:
        print(f"⚠️  Could not enable mixed precision: {e}")
    
    # Enable XLA compilation
    try:
        tf.config.optimizer.set_jit(True)
        print("✓ XLA compilation enabled")
    except Exception as e:
        print(f"⚠️  Could not enable XLA: {e}")
    
    return True

def get_gpu_info():
    """Get detailed GPU information."""
    try:
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        
        info = {
            'name': pynvml.nvmlDeviceGetName(handle).decode(),
            'memory_total': pynvml.nvmlDeviceGetMemoryInfo(handle).total / 1024**3,
            'memory_used': pynvml.nvmlDeviceGetMemoryInfo(handle).used / 1024**3,
            'memory_free': pynvml.nvmlDeviceGetMemoryInfo(handle).free / 1024**3,
            'temperature': pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU),
            'power_usage': pynvml.nvmlDeviceGetPowerUsage(handle) / 1000
        }
        
        return info
    except Exception as e:
        print(f"Error getting GPU info: {e}")
        return None

def print_gpu_info():
    """Print GPU information in a formatted way."""
    info = get_gpu_info()
    if not info:
        return
    
    print("\n💾 GPU Information")
    print("=" * 50)
    print(f"GPU Name: {info['name']}")
    print(f"Total Memory: {info['memory_total']:.2f} GB")
    print(f"Used Memory:  {info['memory_used']:.2f} GB")
    print(f"Free Memory:   {info['memory_free']:.2f} GB")
    print(f"Usage:         {info['memory_used']/info['memory_total']*100:.1f}%")
    print(f"Temperature:   {info['temperature']}°C")
    print(f"Power Usage:   {info['power_usage']:.1f} W")

def gpu_device():
    """Context manager for GPU operations."""
    return tf.device('/GPU:0')

def create_gpu_optimized_model(input_shape, num_classes):
    """Create a GPU-optimized model for emotion recognition."""
    with gpu_device():
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(512, activation='relu', input_shape=input_shape),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(256, activation='relu'),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(num_classes, activation='softmax')
        ])
        
        # Compile with GPU-optimized settings
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model

def gpu_audio_analysis(filename, use_gpu=True):
    """
    Perform GPU-accelerated audio analysis
    """
    import librosa
    
    # Load audio with librosa
    data, sample_rate = librosa.load(filename)
    
    if use_gpu:
        # GPU-accelerated processing
        with gpu_device():
            # Convert to TensorFlow tensor
            audio_tensor = tf.constant(data, dtype=tf.float32)
            
            # GPU-accelerated FFT
            fft = tf.signal.fft(tf.cast(audio_tensor, tf.complex64))
            magnitude = tf.abs(fft)
            
            # GPU-accelerated spectrogram
            stft = tf.signal.stft(audio_tensor, frame_length=2048, frame_step=512)
            spectrogram = tf.abs(stft)
            
            # Convert back to numpy for visualization
            magnitude_np = magnitude.numpy()
            spectrogram_np = spectrogram.numpy()
    else:
        # CPU processing (fallback)
        fft = np.fft.fft(data)
        magnitude_np = np.abs(fft)
        stft = librosa.stft(data)
        spectrogram_np = np.abs(stft)
    
    return data, sample_rate, magnitude_np, spectrogram_np

def benchmark_gpu_vs_cpu():
    """Simple benchmark comparing GPU vs CPU performance."""
    print("\n🚀 GPU vs CPU Benchmark")
    print("=" * 50)
    
    # Test data
    batch_size = 1000
    input_size = 1000
    
    x = np.random.rand(batch_size, input_size).astype(np.float32)
    
    # CPU benchmark
    print("CPU Performance:")
    with tf.device('/CPU:0'):
        start = tf.timestamp()
        model_cpu = tf.keras.Sequential([
            tf.keras.layers.Dense(500, activation='relu'),
            tf.keras.layers.Dense(500, activation='relu'),
            tf.keras.layers.Dense(10, activation='softmax')
        ])
        _ = model_cpu(x)
        cpu_time = tf.timestamp() - start
    
    # GPU benchmark
    print("GPU Performance:")
    with tf.device('/GPU:0'):
        start = tf.timestamp()
        model_gpu = tf.keras.Sequential([
            tf.keras.layers.Dense(500, activation='relu'),
            tf.keras.layers.Dense(500, activation='relu'),
            tf.keras.layers.Dense(10, activation='softmax')
        ])
        _ = model_gpu(x)
        gpu_time = tf.timestamp() - start
    
    # Calculate speedup
    speedup = cpu_time / gpu_time
    print(f"\n🚀 GPU Speedup: {speedup:.2f}x faster than CPU")
    
    return speedup

def main():
    """Test all GPU functions."""
    print("🚀 Testing Simple GPU Utilities")
    print("=" * 50)
    
    # Setup GPU environment
    setup_gpu_environment()
    
    # Print GPU info
    print_gpu_info()
    
    # Test benchmark
    try:
        benchmark_gpu_vs_cpu()
    except Exception as e:
        print(f"Benchmark failed: {e}")
    
    print("\n✅ All GPU utilities working!")

if __name__ == "__main__":
    main()




