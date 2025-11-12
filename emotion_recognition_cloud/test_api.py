#!/usr/bin/env python3
"""
Test script for the Emotion Recognition API
"""

import requests
import json
import os
from pathlib import Path

def test_api_endpoints():
    """Test all API endpoints."""
    base_url = "http://localhost:8080"
    
    print("🧪 Testing Emotion Recognition API...")
    print("=" * 50)
    
    # Test home endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Home endpoint: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Home endpoint failed: {e}")
    
    print()
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health endpoint: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")
    
    print()
    
    # Test models endpoint
    try:
        response = requests.get(f"{base_url}/models")
        print(f"✅ Models endpoint: {response.status_code}")
        print(f"   Available models: {response.json()['available_models']}")
        print(f"   Emotion classes: {len(response.json()['emotion_classes'])}")
    except Exception as e:
        print(f"❌ Models endpoint failed: {e}")
    
    print()
    
    # Test emotion classes endpoint
    try:
        response = requests.get(f"{base_url}/emotion-classes")
        print(f"✅ Emotion classes endpoint: {response.status_code}")
        print(f"   Classes: {response.json()['emotion_classes']}")
    except Exception as e:
        print(f"❌ Emotion classes endpoint failed: {e}")

def test_prediction_with_sample():
    """Test prediction with a sample audio file."""
    base_url = "http://localhost:8080"
    
    print("\n🎵 Testing prediction with sample audio...")
    print("=" * 50)
    
    # Look for sample audio files in the data directory
    data_dir = Path("./data")
    sample_files = []
    
    if data_dir.exists():
        for dataset in ["EMODB", "EMOVO"]:
            dataset_dir = data_dir / dataset
            if dataset_dir.exists():
                wav_files = list(dataset_dir.glob("*.wav"))
                if wav_files:
                    sample_files.extend(wav_files[:2])  # Take first 2 files from each dataset
                    break
    
    if not sample_files:
        print("❌ No sample audio files found in ../data directory")
        return
    
    print(f"📁 Found {len(sample_files)} sample files")
    
    # Test prediction with each model
    models = ["MLP", "SVM", "KNN"]
    
    for model in models:
        print(f"\n🤖 Testing with {model} model:")
        for sample_file in sample_files[:1]:  # Test with first file only
            try:
                with open(sample_file, 'rb') as f:
                    files = {'file': (sample_file.name, f, 'audio/wav')}
                    response = requests.post(
                        f"{base_url}/predict?model={model}",
                        files=files
                    )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✅ {sample_file.name}: {result['predicted_emotion']} (confidence: {result['confidence']:.3f})")
                else:
                    print(f"   ❌ {sample_file.name}: {response.status_code} - {response.text}")
                    
            except Exception as e:
                print(f"   ❌ {sample_file.name}: {e}")

def predict_multiple_files(file_paths, model="MLP"):
    url = f"http://localhost:8080/predict-batch?model={model}"
    
    files = []
    for file_path in file_paths:
        files.append(('files', open(file_path, 'rb')))
    
    response = requests.post(url, files=files)
    
    # Close all files
    for _, file_obj in files:
        file_obj.close()
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    print("🚀 Starting API tests...")
    print("Make sure the Docker container is running on localhost:8080")
    print()
    
    test_api_endpoints()
    test_prediction_with_sample()
    
    print("\n✅ API testing completed!")
    print("Visit http://localhost:8080/docs for interactive API documentation")

    # Example usage
    audio_files = ["./data/EMOVO/dis-f2-n4.wav"]
    results = predict_multiple_files(audio_files, model="SVM")