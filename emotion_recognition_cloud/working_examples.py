#!/usr/bin/env python3
"""
Working Examples for Emotion Recognition API
This script demonstrates how to use the /predict endpoint with real examples
"""

import requests
import json
import os
from pathlib import Path

def example_1_basic_prediction():
    """Example 1: Basic prediction with a single audio file."""
    
    print("🎵 Example 1: Basic Prediction")
    print("=" * 40)
    
    # Find a sample audio file
    sample_file = None
    data_dir = Path("../data")
    
    if data_dir.exists():
        for dataset in ["EMODB", "EMOVO"]:
            dataset_dir = data_dir / dataset
            if dataset_dir.exists():
                wav_files = list(dataset_dir.glob("*.wav"))
                if wav_files:
                    sample_file = wav_files[0]
                    break
    
    if not sample_file:
        print("❌ No sample audio file found")
        return
    
    print(f"📁 Using file: {sample_file.name}")
    
    # Make prediction
    url = "http://localhost:8080/predict?model=MLP"
    
    with open(sample_file, 'rb') as f:
        files = {'file': (sample_file.name, f, 'audio/wav')}
        response = requests.post(url, files=files)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Prediction successful!")
        print(f"   🎭 Predicted emotion: {result['predicted_emotion']}")
        print(f"   📊 Confidence: {result['confidence']:.4f}")
        print(f"   🤖 Model used: {result['model_used']}")
        print(f"   📝 Note: {result.get('note', '')}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

def example_2_different_models():
    """Example 2: Testing different models."""
    
    print("\n🤖 Example 2: Different Models")
    print("=" * 40)
    
    # Find a sample audio file
    sample_file = None
    data_dir = Path("../data")
    
    if data_dir.exists():
        for dataset in ["EMODB", "EMOVO"]:
            dataset_dir = data_dir / dataset
            if dataset_dir.exists():
                wav_files = list(dataset_dir.glob("*.wav"))
                if wav_files:
                    sample_file = wav_files[0]
                    break
    
    if not sample_file:
        print("❌ No sample audio file found")
        return
    
    models = ["MLP", "SVM", "KNN"]
    
    for model in models:
        print(f"\n🧠 Testing {model} model:")
        url = f"http://localhost:8080/predict?model={model}"
        
        with open(sample_file, 'rb') as f:
            files = {'file': (sample_file.name, f, 'audio/wav')}
            response = requests.post(url, files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"   🎭 Emotion: {result['predicted_emotion']}")
            print(f"   📊 Confidence: {result['confidence']:.4f}")
        else:
            print(f"   ❌ Error: {response.status_code}")

def example_3_batch_prediction():
    """Example 3: Batch prediction with multiple files."""
    
    print("\n📦 Example 3: Batch Prediction")
    print("=" * 40)
    
    # Find multiple sample files
    sample_files = []
    data_dir = Path("../data")
    
    if data_dir.exists():
        for dataset in ["EMODB", "EMOVO"]:
            dataset_dir = data_dir / dataset
            if dataset_dir.exists():
                wav_files = list(dataset_dir.glob("*.wav"))
                if wav_files:
                    sample_files.extend(wav_files[:2])  # Take first 2 files
                    break
    
    if len(sample_files) < 2:
        print("❌ Need at least 2 audio files for batch prediction")
        return
    
    print(f"📁 Using {len(sample_files)} files for batch prediction")
    
    # Prepare files for batch prediction
    files = []
    for file_path in sample_files:
        files.append(('files', (file_path.name, open(file_path, 'rb'), 'audio/wav')))
    
    # Make batch prediction
    url = "http://localhost:8080/predict-batch?model=SVM"
    response = requests.post(url, files=files)
    
    # Close all files
    for _, (_, file_obj, _) in files:
        file_obj.close()
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Batch prediction successful!")
        print(f"   🤖 Model used: {result['model_used']}")
        print(f"   📊 Total files: {result['total_files']}")
        
        for i, file_result in enumerate(result['results']):
            print(f"\n   📁 File {i+1}: {file_result['filename']}")
            if file_result['success']:
                print(f"      🎭 Emotion: {file_result['predicted_emotion']}")
                print(f"      📊 Confidence: {file_result['confidence']:.4f}")
            else:
                print(f"      ❌ Error: {file_result['error']}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

def example_4_curl_commands():
    """Example 4: Show equivalent cURL commands."""
    
    print("\n🔧 Example 4: cURL Commands")
    print("=" * 40)
    
    print("Here are the equivalent cURL commands:")
    print()
    
    print("1. Basic prediction:")
    print('   curl -X POST "http://localhost:8080/predict?model=MLP" \\')
    print('        -H "Content-Type: multipart/form-data" \\')
    print('        -F "file=@your_audio_file.wav"')
    print()
    
    print("2. Different models:")
    print('   curl -X POST "http://localhost:8080/predict?model=SVM" \\')
    print('        -H "Content-Type: multipart/form-data" \\')
    print('        -F "file=@your_audio_file.wav"')
    print()
    
    print('   curl -X POST "http://localhost:8080/predict?model=KNN" \\')
    print('        -H "Content-Type: multipart/form-data" \\')
    print('        -F "file=@your_audio_file.wav"')
    print()
    
    print("3. Batch prediction:")
    print('   curl -X POST "http://localhost:8080/predict-batch?model=MLP" \\')
    print('        -H "Content-Type: multipart/form-data" \\')
    print('        -F "files=@audio1.wav" \\')
    print('        -F "files=@audio2.wav"')

def example_5_api_documentation():
    """Example 5: Show how to use the interactive API docs."""
    
    print("\n📚 Example 5: Interactive API Documentation")
    print("=" * 40)
    
    print("🌐 Open your browser and go to:")
    print("   http://localhost:8080/docs")
    print()
    print("📋 Available endpoints:")
    print("   • GET  /              - API information")
    print("   • GET  /test          - Simple test")
    print("   • GET  /health        - Health check")
    print("   • GET  /models        - Available models")
    print("   • GET  /emotion-classes - Emotion classes")
    print("   • POST /predict       - Single file prediction")
    print("   • POST /predict-batch - Batch prediction")
    print()
    print("🎯 To test /predict:")
    print("   1. Click on 'POST /predict'")
    print("   2. Click 'Try it out'")
    print("   3. Upload an audio file")
    print("   4. Select model (MLP, SVM, or KNN)")
    print("   5. Click 'Execute'")

def show_api_info():
    """Show current API information."""
    
    print("🎭 Emotion Recognition API - Working Examples")
    print("=" * 50)
    
    try:
        # Test API connection
        response = requests.get("http://localhost:8080/test", timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API Status: {result['status']}")
            print(f"📅 Timestamp: {result['timestamp']}")
            print(f"🤖 Models loaded: {result['models_loaded']}")
        else:
            print("❌ API not responding correctly")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API: {e}")
        print("💡 Make sure the Docker container is running:")
        print("   docker run -d -p 8080:80 --name emotion-api emotion-recognition-api")
        return False
    
    return True

if __name__ == "__main__":
    if show_api_info():
        example_1_basic_prediction()
        example_2_different_models()
        example_3_batch_prediction()
        example_4_curl_commands()
        example_5_api_documentation()
        
        print("\n" + "=" * 50)
        print("🎉 All examples completed!")
        print("💡 The API is working with mock predictions.")
        print("🔧 To get real predictions, retrain the models with current TensorFlow.")
        print("📖 Visit http://localhost:8080/docs for interactive testing!")
    else:
        print("\n❌ Please start the API first and try again.")
