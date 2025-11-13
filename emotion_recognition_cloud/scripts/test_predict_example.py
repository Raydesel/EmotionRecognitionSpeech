#!/usr/bin/env python3
"""
Test script to demonstrate the /predict endpoint usage
This script shows how to use the API even when models aren't loaded
"""

import requests
import json
import os
from pathlib import Path

def test_predict_endpoint():
    """Test the /predict endpoint with a sample audio file."""
    
    print("🧪 Testing /predict endpoint...")
    print("=" * 50)
    
    # Check if API is running
    try:
        response = requests.get("http://localhost:8080/test", timeout=5)
        if response.status_code == 200:
            print("✅ API is running")
        else:
            print("❌ API is not responding correctly")
            return
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API: {e}")
        print("Make sure the Docker container is running:")
        print("  docker run -d -p 8080:80 --name emotion-api emotion-recognition-api")
        return
    
    # Look for sample audio files
    sample_files = []
    
    # Check for audio files in the data directory
    data_dir = Path("../data")
    if data_dir.exists():
        for dataset in ["EMODB", "EMOVO"]:
            dataset_dir = data_dir / dataset
            if dataset_dir.exists():
                wav_files = list(dataset_dir.glob("*.wav"))
                if wav_files:
                    sample_files.extend(wav_files[:2])
                    break
    
    if not sample_files:
        print("❌ No sample audio files found")
        print("📁 Looking for audio files in: ../data/EMODB/ or ../data/EMOVO/")
        print("💡 You can create a test audio file or use any WAV file")
        return
    
    print(f"📁 Found {len(sample_files)} sample files")
    
    # Test with the first available file
    test_file = sample_files[0]
    print(f"🎵 Testing with: {test_file.name}")
    
    # Test different models
    models = ["MLP", "SVM", "KNN"]
    
    for model in models:
        print(f"\n🤖 Testing with {model} model:")
        print("-" * 30)
        
        try:
            # Prepare the request
            url = f"http://localhost:8080/predict?model={model}"
            
            with open(test_file, 'rb') as f:
                files = {'file': (test_file.name, f, 'audio/wav')}
                response = requests.post(url, files=files, timeout=30)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Prediction successful!")
                print(f"   Predicted emotion: {result.get('predicted_emotion', 'N/A')}")
                print(f"   Confidence: {result.get('confidence', 'N/A')}")
                print(f"   Model used: {result.get('model_used', 'N/A')}")
            else:
                print("❌ Prediction failed")
                try:
                    error_detail = response.json()
                    print(f"   Error: {error_detail.get('detail', 'Unknown error')}")
                except:
                    print(f"   Error: {response.text}")
                    
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

def test_with_curl_example():
    """Show how to test with curl command."""
    
    print("\n" + "=" * 50)
    print("🔧 CURL Command Examples:")
    print("=" * 50)
    
    print("1. Basic prediction:")
    print('   curl -X POST "http://localhost:8080/predict?model=MLP" \\')
    print('        -H "Content-Type: multipart/form-data" \\')
    print('        -F "file=@your_audio_file.wav"')
    print()
    
    print("2. Test with different models:")
    print('   curl -X POST "http://localhost:8080/predict?model=SVM" \\')
    print('        -H "Content-Type: multipart/form-data" \\')
    print('        -F "file=@your_audio_file.wav"')
    print()
    
    print("3. Batch prediction:")
    print('   curl -X POST "http://localhost:8080/predict-batch?model=KNN" \\')
    print('        -H "Content-Type: multipart/form-data" \\')
    print('        -F "files=@audio1.wav" \\')
    print('        -F "files=@audio2.wav"')

def show_api_status():
    """Show current API status."""
    
    print("\n" + "=" * 50)
    print("📊 API Status:")
    print("=" * 50)
    
    try:
        # Test basic endpoints
        endpoints = [
            ("/", "Home"),
            ("/test", "Test"),
            ("/health", "Health"),
            ("/emotion-classes", "Emotion Classes"),
            ("/models", "Models")
        ]
        
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"http://localhost:8080{endpoint}", timeout=5)
                if response.status_code == 200:
                    print(f"✅ {name}: Working")
                else:
                    print(f"❌ {name}: Error {response.status_code}")
            except:
                print(f"❌ {name}: Connection failed")
                
    except Exception as e:
        print(f"❌ Error checking API status: {e}")

if __name__ == "__main__":
    print("🎭 Emotion Recognition API Test")
    print("=" * 50)
    
    show_api_status()
    test_predict_endpoint()
    test_with_curl_example()
    
    print("\n" + "=" * 50)
    print("💡 Next Steps:")
    print("=" * 50)
    print("1. If models aren't loading, you need to retrain them")
    print("2. Use the interactive docs at: http://localhost:8080/docs")
    print("3. Check the container logs: docker logs emotion-api")
    print("4. The API structure is working - just need compatible models!")
