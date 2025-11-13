# Emotion Recognition API

A Docker containerized FastAPI application for emotion recognition from speech using machine learning models.

## Features

- **Multiple ML Models**: MLP (Deep Learning), SVM (Support Vector Machine), and KNN (K-Nearest Neighbors)
- **Custom MFCC Feature Extraction**: Advanced audio feature extraction
- **RESTful API**: Easy-to-use HTTP endpoints
- **Batch Processing**: Support for multiple file uploads
- **Docker Ready**: Fully containerized application

## API Endpoints

### Core Endpoints

- `GET /` - API information and status
- `GET /health` - Health check
- `GET /models` - Available models and emotion classes
- `GET /emotion-classes` - List of emotion classes

### Prediction Endpoints

- `POST /predict` - Predict emotion from single audio file
- `POST /predict-batch` - Predict emotions from multiple audio files

## Usage

### Building the Docker Image

```bash
docker build -t emotion-recognition-api .
```

### Running the Container

```bash
docker run -p 80:80 emotion-recognition-api
```

### Web Interface

The API includes a web-based user interface for easy interaction:

- **Main Web App**: `http://localhost/` (or `http://localhost:80/`)
- **Direct Access**: `http://localhost/static/web_app.html`

The web interface allows you to:
- Upload audio files via drag-and-drop or file picker
- Select between MLP, SVM, and KNN models
- View emotion predictions with confidence scores
- See probability distributions for all emotion classes
- Preview uploaded audio files

**Note**: If running on a different port (e.g., `docker run -p 8080:80`), access the web app at `http://localhost:8080/` and update the API URL in the web interface if needed.

### API Usage Examples

#### Single File Prediction

```bash
curl -X POST "http://localhost/predict?model=MLP" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@audio_file.wav"
```

#### Batch Prediction

```bash
curl -X POST "http://localhost/predict-batch?model=SVM" \
     -H "Content-Type: multipart/form-data" \
     -F "files=@audio1.wav" \
     -F "files=@audio2.wav"
```

## Supported Audio Formats

- WAV
- MP3
- M4A
- FLAC

## Available Models

- **MLP**: Multi-Layer Perceptron (Deep Learning)
- **SVM**: Support Vector Machine
- **KNN**: K-Nearest Neighbors

## Emotion Classes

The API recognizes the following emotions:
- A angustia (Anguish)
- E disgusto (Disgust)
- F alegria (Joy)
- L Sorpresa (Surprise)
- L aburrimiento (Boredom)
- N neutral (Neutral)
- T tristeza (Sadness)
- W ira (Anger)

## Response Format

```json
{
  "success": true,
  "model_used": "MLP",
  "predicted_emotion": "F alegria",
  "confidence": 0.8542,
  "all_probabilities": {
    "A angustia": 0.0234,
    "E disgusto": 0.0123,
    "F alegria": 0.8542,
    "L Sorpresa": 0.0456,
    "L aburrimiento": 0.0123,
    "N neutral": 0.0234,
    "T tristeza": 0.0123,
    "W ira": 0.0169
  },
  "filename": "audio_file.wav"
}
```

## Development

The application is built from the Complete Emotion Recognition Pipeline notebook and includes:

- Custom MFCC feature extraction
- Pre-trained models (MLP, SVM, KNN)
- FastAPI web framework
- Docker containerization

## Requirements

- Docker
- Python 3.11
- TensorFlow 2.15.0
- scikit-learn
- FastAPI
- Audio processing libraries (librosa, soundfile)

## Scripts Folder

The `scripts/` folder contains utility and testing scripts that are not part of the Docker application but are useful for development and maintenance:

- **`fix_model_compatibility.py`** - Fixes TensorFlow model compatibility issues. Run this before building the Docker image if you encounter model loading errors.
- **`test_api.py`** - Comprehensive test script for all API endpoints
- **`test_predict_example.py`** - Example script demonstrating how to use the `/predict` endpoint
- **`working_examples.py`** - Working examples showing various API usage patterns

These scripts are not included in the Docker container and should be run from your local machine when testing or maintaining the API.

