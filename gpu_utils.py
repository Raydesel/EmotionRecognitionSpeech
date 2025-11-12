#!/usr/bin/env python3
"""
GPU Utility Functions for Emotion Recognition Speech Project
"""

import tensorflow as tf
import numpy as np
import pynvml
from contextlib import contextmanager

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

@contextmanager
def gpu_device():
    """Context manager for GPU operations."""
    with tf.device('/GPU:0'):
        yield

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

def gpu_audio_processing(audio_data, sample_rate=22050):
    """GPU-accelerated audio processing."""
    with gpu_device():
        # Convert to TensorFlow tensor
        audio_tensor = tf.constant(audio_data, dtype=tf.float32)
        
        # Apply windowing
        windowed = tf.signal.hann_window(tf.shape(audio_tensor)[-1])
        windowed_audio = audio_tensor * windowed
        
        # Compute FFT
        fft = tf.signal.fft(tf.cast(windowed_audio, tf.complex64))
        magnitude = tf.abs(fft)
        
        # Compute MFCC-like features
        log_magnitude = tf.math.log(magnitude + 1e-8)
        
        return log_magnitude

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

def create_optimization_recommendations():
    """Create GPU optimization recommendations."""
    print("\n⚡ GPU Optimization Recommendations")
    print("=" * 50)
    
    recommendations = [
        "1. Use tf.device('/GPU:0') for explicit GPU placement",
        "2. Enable mixed precision: tf.keras.mixed_precision.set_global_policy('mixed_float16')",
        "3. Use tf.data.Dataset for efficient data loading",
        "4. Enable XLA compilation: tf.config.optimizer.set_jit(True)",
        "5. Use tf.function decorator for graph compilation",
        "6. Batch operations to maximize GPU utilization",
        "7. Use tf.signal for GPU-accelerated audio processing",
        "8. Monitor memory usage with tf.config.experimental.set_memory_growth",
        "9. Use tf.keras.utils.plot_model to visualize your model",
        "10. Consider using TensorRT for inference optimization"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        print(f"✓ {rec}")
    
    return recommendations

def main():
    """Main GPU utility test."""
    print("🚀 GPU Utilities for Emotion Recognition Speech Project")
    print("=" * 60)
    
    # Setup GPU environment
    if not setup_gpu_environment():
        print("❌ GPU setup failed")
        return False
    
    # Print GPU info
    print_gpu_info()
    
    # Run benchmark
    try:
        benchmark_gpu_vs_cpu()
    except Exception as e:
        print(f"⚠️  Benchmark failed: {e}")
    
    # Create recommendations
    create_optimization_recommendations()
    
    print("\n🎉 GPU utilities are ready!")
    print("Use these functions in your emotion recognition notebooks.")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

