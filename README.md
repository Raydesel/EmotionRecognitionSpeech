# 🎭 Emotion Recognition from Speech

A comprehensive machine learning project for emotion recognition in speech using MFCC (Mel-Frequency Cepstral Coefficients) and Multi-band Spectral Entropy Signatures (MSES). This project implements multiple classification algorithms and provides a production-ready API for real-time emotion detection.

## 🚀 Quick Start

This project has **two main deliverables**:

### Option 1: The Notebook 📓

To see the full training and evaluation process, run `Complete_Emotion_Recognition_Pipeline.ipynb`. This self-contained notebook includes:
- Data loading and exploration
- Feature extraction (MFCC)
- Model training (MLP, SVM, KNN)
- Model evaluation and comparison
- Prediction on new audio files

**Setup:**
```bash
pip install -r requirements.txt
jupyter notebook Complete_Emotion_Recognition_Pipeline.ipynb
```

### Option 2: The API 🌐

To run the pre-trained production API, go to the `emotion_recognition_cloud/` folder and follow the Docker instructions in its own README (or build from the Dockerfile).

**Quick start:**
```bash
cd emotion_recognition_cloud
docker build -t emotion-recognition-api .
docker run -p 80:80 emotion-recognition-api
```

### 📦 Archive

All other notebooks and scripts from the original thesis research are archived in the `_legacy_experiments/` folder for reference. These include experimental feature extraction methods, individual classifier implementations, and visualization notebooks.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Methodology](#methodology)
- [Models](#models)
- [Datasets](#datasets)
- [API Deployment](#api-deployment)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project implements a complete pipeline for emotion recognition from speech signals, developed as part of a thesis research. The system extracts acoustic features from audio files and uses machine learning models to classify emotions into eight categories: **anguish, disgust, joy, surprise, boredom, neutral, sadness, and anger**.

### Key Technologies

- **Feature Extraction**: MFCC, RASTA-MFCC, Multi-band Spectral Entropy Signatures (MSES)
- **Machine Learning**: MLP (Deep Learning), SVM, KNN
- **Frameworks**: TensorFlow/Keras, scikit-learn, librosa
- **Deployment**: FastAPI, Docker
- **GPU Support**: CUDA-accelerated processing

## ✨ Features

- **Multiple Feature Extraction Methods**
  - Standard MFCC features
  - RASTA-MFCC (Relatively SpecTrAl) for noise robustness
  - Multi-band Spectral Entropy Signatures (MSES)
  
- **Three Classification Algorithms**
  - **MLP (Multi-Layer Perceptron)**: Deep neural network for high accuracy
  - **SVM (Support Vector Machine)**: Traditional ML approach with good generalization
  - **KNN (K-Nearest Neighbors)**: Instance-based learning for interpretability

- **Production-Ready API**
  - RESTful API with FastAPI
  - Docker containerization
  - Batch processing support
  - Multiple model selection

## 📁 Project Structure

```
EmotionRecognitionSpeech/
├── Complete_Emotion_Recognition_Pipeline.ipynb  # Main notebook (self-contained)
├── emotion_recognition_cloud/                   # Production API
│   ├── app/                                     # FastAPI application
│   │   ├── __init__.py
│   │   ├── main.py                              # API endpoints
│   │   ├── feature_extractor.py                 # MFCC feature extraction
│   │   └── model_loader.py                     # Model loading & prediction
│   ├── saved_models/                            # Pre-trained models (not in git)
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt                         # API dependencies
│   └── README.md                                # API documentation
├── _legacy_experiments/                         # Archived experimental notebooks
│   ├── caracteristicas/                         # Feature extraction experiments
│   ├── clacificadores/                          # Individual classifier notebooks
│   ├── experimentos/                            # Experimental analysis
│   ├── visualizacion/                           # Data visualization
│   └── helpers/                                 # Utility functions
├── metadatos/                                   # Dataset metadata
│   ├── EMODB - testSize 0.3.csv
│   └── emovo - testSize 0.3.csv
├── articulos/                                   # Research papers (reference)
├── documento/                                   # Thesis documentation
├── requirements.txt                             # Notebook dependencies
└── README.md                                    # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- CUDA-capable GPU (optional, for GPU acceleration)
- Docker (for API deployment)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/EmotionRecognitionSpeech.git
   cd EmotionRecognitionSpeech
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### GPU Setup (Optional)

For GPU acceleration, ensure you have:
- NVIDIA GPU with CUDA support
- CUDA Toolkit 11.x or higher
- cuDNN library

The project will automatically detect and use GPU if available.

## 💻 Usage

### Running the Complete Pipeline

1. **Open the main pipeline notebook**
   ```bash
   jupyter notebook Complete_Emotion_Recognition_Pipeline.ipynb
   ```

2. **For GPU-accelerated processing**
   ```bash
   jupyter notebook Complete_Emotion_Recognition_Pipeline_GPU.ipynb
   ```

The notebook is self-contained and includes all necessary code for:
- Loading audio data from `data/EMODB/` and `data/EMOVO/` directories
- Extracting MFCC features
- Training MLP, SVM, and KNN models
- Evaluating model performance
- Making predictions on new audio files

### API Deployment

See the [emotion_recognition_cloud/README.md](emotion_recognition_cloud/README.md) for detailed API deployment instructions.

**Quick start:**
```bash
cd emotion_recognition_cloud
docker build -t emotion-recognition-api .
docker run -p 80:80 emotion-recognition-api
```

**Test the API:**
```bash
curl -X POST "http://localhost/predict?model=MLP" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@audio_file.wav"
```

## 🔬 Methodology

### Feature Extraction

1. **MFCC Features**
   - Standard 13-dimensional MFCC coefficients
   - Delta and delta-delta features for temporal information
   - Frame-level features aggregated to utterance-level

2. **RASTA-MFCC**
   - Relatively SpecTrAl processing for noise robustness
   - Band-pass filtering in the log spectral domain
   - Improved performance in noisy environments

3. **Multi-band Spectral Entropy Signatures (MSES)**
   - Spectral entropy computed across multiple frequency bands
   - Captures emotional characteristics in different frequency ranges
   - Provides complementary information to MFCC features

### Classification Pipeline

1. **Data Preprocessing**
   - Audio normalization
   - Silence removal
   - Feature standardization

2. **Model Training**
   - Train-test split (70-30 or custom)
   - Cross-validation for hyperparameter tuning
   - Model evaluation with multiple metrics

3. **Evaluation Metrics**
   - Accuracy
   - Precision, Recall, F1-score
   - Confusion matrices
   - Classification reports

## 🤖 Models

### MLP (Multi-Layer Perceptron)

- **Architecture**: Deep neural network with multiple hidden layers
- **Activation**: ReLU for hidden layers, softmax for output
- **Optimizer**: Adam
- **Regularization**: Dropout layers to prevent overfitting
- **Best Use Case**: High accuracy requirements, large datasets

### SVM (Support Vector Machine)

- **Kernel**: RBF (Radial Basis Function)
- **Regularization**: C parameter tuning
- **Best Use Case**: Good generalization, interpretable results

### KNN (K-Nearest Neighbors)

- **Distance Metric**: Euclidean distance
- **K Value**: Optimized through cross-validation
- **Best Use Case**: Interpretability, small to medium datasets

## 📊 Datasets

The project uses two primary datasets:

1. **EMODB** (Berlin Database of Emotional Speech)
   - German emotional speech database
   - 535 utterances
   - 10 speakers, 7 emotions

2. **EMOVO** (Italian Emotional Speech Database)
   - Italian emotional speech database
   - 1,176 utterances
   - 6 speakers, 7 emotions

Both datasets are preprocessed and split into training and testing sets. Metadata files are available in `metadatos/`.

**Note**: Audio data files are not included in the repository due to size limitations. Please obtain the datasets separately or use your own audio files for testing.

## 🌐 API Deployment

The project includes a production-ready FastAPI application. See [emotion_recognition_cloud/README.md](emotion_recognition_cloud/README.md) for:
- API endpoints documentation
- Docker deployment instructions
- Usage examples
- Response formats

## 📈 Results

Model performance varies based on feature extraction method and dataset. Key findings:

- **MLP** typically achieves the highest accuracy with MFCC features
- **RASTA-MFCC** provides better noise robustness
- **MSES** features offer complementary information for emotion classification

For detailed results, refer to the `Complete_Emotion_Recognition_Pipeline.ipynb` notebook or archived experiments in `_legacy_experiments/`.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Code style and standards
- Pull request process
- Issue reporting
- Development workflow

## 📄 License

This project is part of a thesis research. Please cite appropriately if used in academic work.

## 📚 References

Research papers and references are available in the `articulos/` directory. Key references include:
- Computational Paralinguistics (Schuller & Batliner, 2013)
- RASTA-MFCC for noise-robust speech recognition
- Multi-band spectral entropy features for robust ASR

## 👤 Author

**Raydesel Ariel Sánchez Montes** - Thesis: "Emotion recognition in speech using MFCC and multi-band spectral entropy signatures"

## 🙏 Acknowledgments

- EMODB database creators
- EMOVO database creators
- Open-source community for libraries and tools
