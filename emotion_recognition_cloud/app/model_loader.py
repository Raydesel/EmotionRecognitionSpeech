"""
Model Loading and Prediction Module
Handles loading of trained models and making predictions
"""

import os
import numpy as np
import joblib
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, LabelEncoder
from .feature_extractor import MelFreqCepsCoef


class EmotionRecognitionModel:
    """Emotion Recognition Model Handler"""
    
    def __init__(self, models_dir="saved_models"):
        """Initialize the model handler with saved models."""
        self.models_dir = models_dir
        self.models = {}
        self.scaler = None
        self.label_encoder = None
        self.load_models()
    
    def load_models(self):
        """Load all trained models and preprocessing objects."""
        try:
            # Load preprocessing objects
            self.scaler = joblib.load(os.path.join(self.models_dir, 'feature_scaler.pkl'))
            self.label_encoder = joblib.load(os.path.join(self.models_dir, 'label_encoder.pkl'))
            
            # Load MLP model
            self.models['MLP'] = tf.keras.models.load_model(
                os.path.join(self.models_dir, 'mlp_emotion_model.h5'),
                compile=False
            )
            
            # Load SVM model
            self.models['SVM'] = joblib.load(
                os.path.join(self.models_dir, 'svm_emotion_model.pkl')
            )
            
            # Load KNN model
            self.models['KNN'] = joblib.load(
                os.path.join(self.models_dir, 'knn_emotion_model.pkl')
            )
            
            print("✅ All models loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            raise e
    
    def predict_emotion(self, file_path, model_name='MLP'):
        """
        Predict emotion from an audio file using the specified model.
        
        Args:
            file_path (str): Path to the audio file
            model_name (str): Name of the model to use ('MLP', 'SVM', 'KNN')
        
        Returns:
            dict: Prediction results with probabilities
        """
        try:
            # Extract features from the audio file
            mfcc_extractor = MelFreqCepsCoef(file_path)
            features = mfcc_extractor.mfccsscalade.reshape(1, -1)
            
            # Clean any NaN or Inf values
            features = np.nan_to_num(features, nan=0.0, posinf=0.0, neginf=0.0)
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Get model
            model = self.models[model_name]
            
            # Make prediction
            if model_name == 'MLP':
                # For MLP, get probabilities
                probabilities = model.predict(features_scaled, verbose=0)[0]
                predicted_class_idx = np.argmax(probabilities)
            else:
                # For SVM and KNN
                predicted_class_idx = model.predict(features_scaled)[0]
                if hasattr(model, 'predict_proba'):
                    probabilities = model.predict_proba(features_scaled)[0]
                else:
                    probabilities = np.zeros(len(self.label_encoder.classes_))
                    probabilities[predicted_class_idx] = 1.0
            
            # Get class name
            predicted_class = self.label_encoder.classes_[predicted_class_idx]
            
            # Create results dictionary
            results_dict = {
                'predicted_class': predicted_class,
                'confidence': float(probabilities[predicted_class_idx]),
                'all_probabilities': {}
            }
            
            # Add probabilities for all classes
            for i, class_name in enumerate(self.label_encoder.classes_):
                results_dict['all_probabilities'][class_name] = float(probabilities[i])
            
            return results_dict
            
        except Exception as e:
            return {'error': f'Prediction failed: {str(e)}'}
    
    def get_available_models(self):
        """Get list of available models."""
        return list(self.models.keys())
    
    def get_emotion_classes(self):
        """Get list of emotion classes."""
        return list(self.label_encoder.classes_)

