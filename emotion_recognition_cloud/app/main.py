"""
FastAPI Application for Emotion Recognition from Speech
Based on the Complete Emotion Recognition Pipeline notebook
"""

import os
import io
import tempfile
import uvicorn
import numpy as np
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import logging

from .model_loader import EmotionRecognitionModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Emotion Recognition API",
    description="API for emotion recognition from speech using MLP, SVM, and KNN models",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the emotion recognition model
try:
    emotion_model = EmotionRecognitionModel()
    logger.info("✅ Emotion recognition model loaded successfully!")
except Exception as e:
    logger.error(f"❌ Failed to load emotion recognition model: {e}")
    logger.info("🔄 API will run in limited mode without models")
    emotion_model = None


@app.get("/")
def home():
    """Home endpoint with API information."""
    return {
        "message": "Emotion Recognition API is working!",
        "docs": "/docs",
        "available_models": emotion_model.get_available_models() if emotion_model else [],
        "emotion_classes": emotion_model.get_emotion_classes() if emotion_model else []
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    if emotion_model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "status": "healthy",
        "models_loaded": len(emotion_model.models),
        "available_models": emotion_model.get_available_models()
    }


@app.get("/models")
def get_models():
    """Get available models and emotion classes."""
    if emotion_model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "available_models": emotion_model.get_available_models(),
        "emotion_classes": emotion_model.get_emotion_classes()
    }


@app.post("/predict")
def predict_emotion(
    file: UploadFile = File(...),
    model: str = Query(default="MLP", description="Model to use: MLP, SVM, or KNN")
):
    """
    Predict emotion from an uploaded audio file.
    
    Args:
        file: Audio file (WAV format recommended)
        model: Model to use (MLP, SVM, or KNN)
    
    Returns:
        JSON response with prediction results
    """
    if emotion_model is None:
        # Return a mock prediction for testing when models aren't loaded
        logger.info("🔄 Models not loaded - returning mock prediction for testing")
        
        # Validate file type
        if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
            raise HTTPException(
                status_code=415, 
                detail="Unsupported file format. Please upload a WAV, MP3, M4A, or FLAC file."
            )
        
        # Mock prediction for testing
        mock_emotions = [
            "A angustia", "E disgusto", "F alegria", "L Sorpresa", 
            "L aburrimiento", "N neutral", "T tristeza", "W ira"
        ]
        
        import random
        predicted_emotion = random.choice(mock_emotions)
        confidence = round(random.uniform(0.6, 0.95), 4)
        
        # Create mock probabilities
        all_probabilities = {}
        for emotion in mock_emotions:
            if emotion == predicted_emotion:
                all_probabilities[emotion] = confidence
            else:
                remaining_prob = (1.0 - confidence) / (len(mock_emotions) - 1)
                all_probabilities[emotion] = round(remaining_prob, 4)
        
        return JSONResponse(content={
            "success": True,
            "model_used": model,
            "predicted_emotion": predicted_emotion,
            "confidence": confidence,
            "all_probabilities": all_probabilities,
            "filename": file.filename,
            "note": "This is a mock prediction - models not loaded. Retrain models for real predictions."
        })
    
    # Validate model parameter
    available_models = emotion_model.get_available_models()
    if model not in available_models:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid model. Available models: {available_models}"
        )
    
    # Validate file type
    if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        raise HTTPException(
            status_code=415, 
            detail="Unsupported file format. Please upload a WAV, MP3, M4A, or FLAC file."
        )
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            content = file.file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Make prediction
        result = emotion_model.predict_emotion(temp_file_path, model)
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        
        if 'error' in result:
            raise HTTPException(status_code=500, detail=result['error'])
        
        # Format response
        response = {
            "success": True,
            "model_used": model,
            "predicted_emotion": result['predicted_class'],
            "confidence": result['confidence'],
            "all_probabilities": result['all_probabilities'],
            "filename": file.filename
        }
        
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/predict-batch")
def predict_emotion_batch(
    files: List[UploadFile] = File(...),
    model: str = Query(default="MLP", description="Model to use: MLP, SVM, or KNN")
):
    """
    Predict emotions from multiple uploaded audio files.
    
    Args:
        files: List of audio files
        model: Model to use (MLP, SVM, or KNN)
    
    Returns:
        JSON response with batch prediction results
    """
    if emotion_model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Validate model parameter
    available_models = emotion_model.get_available_models()
    if model not in available_models:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid model. Available models: {available_models}"
        )
    
    if len(files) > 10:  # Limit batch size
        raise HTTPException(
            status_code=400, 
            detail="Too many files. Maximum 10 files per batch."
        )
    
    results = []
    
    for file in files:
        try:
            # Validate file type
            if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
                results.append({
                    "filename": file.filename,
                    "success": False,
                    "error": "Unsupported file format"
                })
                continue
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                content = file.file.read()
                temp_file.write(content)
                temp_file_path = temp_file.name
            
            # Make prediction
            result = emotion_model.predict_emotion(temp_file_path, model)
            
            # Clean up temporary file
            os.unlink(temp_file_path)
            
            if 'error' in result:
                results.append({
                    "filename": file.filename,
                    "success": False,
                    "error": result['error']
                })
            else:
                results.append({
                    "filename": file.filename,
                    "success": True,
                    "predicted_emotion": result['predicted_class'],
                    "confidence": result['confidence'],
                    "all_probabilities": result['all_probabilities']
                })
                
        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e)
            })
    
    return JSONResponse(content={
        "model_used": model,
        "total_files": len(files),
        "results": results
    })


@app.get("/emotion-classes")
def get_emotion_classes():
    """Get all available emotion classes."""
    if emotion_model is None:
        # Return default emotion classes if models aren't loaded
        default_classes = [
            "A angustia", "E disgusto", "F alegria", "L Sorpresa", 
            "L aburrimiento", "N neutral", "T tristeza", "W ira"
        ]
        return {
            "emotion_classes": default_classes,
            "total_classes": len(default_classes),
            "note": "Models not loaded - showing default classes"
        }
    
    return {
        "emotion_classes": emotion_model.get_emotion_classes(),
        "total_classes": len(emotion_model.get_emotion_classes())
    }


@app.get("/test")
def test_endpoint():
    """Simple test endpoint that doesn't require models."""
    return {
        "status": "API is working!",
        "timestamp": datetime.now().isoformat(),
        "models_loaded": emotion_model is not None
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
