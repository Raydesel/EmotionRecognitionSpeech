# Project Structure Documentation

This document provides a detailed explanation of the project's directory structure and file organization.

## 📁 Directory Overview

```
EmotionRecognitionSpeech/
├── caracteristicas/          # Feature extraction
├── clacificadores/           # Model training and evaluation
├── experimentos/             # Experimental analysis
├── visualizacion/            # Data exploration
├── emotion_recognition_cloud/ # Production API
├── helpers/                  # Utility functions
├── metadatos/                # Dataset metadata
├── articulos/                # Research papers
├── documento/                # Thesis documentation
└── [root files]              # Main pipeline and configuration
```

## 📂 Detailed Directory Descriptions

### `caracteristicas/` - Feature Extraction

Contains Jupyter notebooks for extracting audio features from speech signals.

**Files:**
- `Features_emovo_EMODB.ipynb` - Standard MFCC feature extraction
- `Features_emovo_EMODB(sinVocalizacion).ipynb` - MFCC without vocalization
- `FeaturesMSES_emovo_EMODB.ipynb` - Multi-band Spectral Entropy Signatures
- `FeaturesMSES_emovo_EMODB(sinVocalizacion).ipynb` - MSES without vocalization

**Purpose:** Extract acoustic features (MFCC, RASTA-MFCC, MSES) from audio files for both EMOVO and EMODB datasets.

### `clacificadores/` - Model Training and Evaluation

Contains notebooks for training and evaluating machine learning models.

**Files:**
- `3.2.0.0 Model Training and Evaluation.ipynb` - Complete training pipeline
- `SVM tesis.ipynb` - Support Vector Machine implementation
- `KNN tesis.ipynb` - K-Nearest Neighbors implementation

**Purpose:** Train and evaluate MLP, SVM, and KNN models on extracted features.

### `experimentos/` - Experimental Analysis

Contains notebooks for running experiments with different feature combinations.

**Files:**
- `experimentos_EMODB_MSES.ipynb` - MSES experiments on EMODB
- `experimentos_EMODB_RASTA-MFCC.ipynb` - RASTA-MFCC experiments on EMODB
- `experimentos_emovo_MSES.ipynb` - MSES experiments on EMOVO
- `experimentos_emovo_RASTA-MFCC.ipynb` - RASTA-MFCC experiments on EMOVO
- Variants with `(sinVocalizacion)` - Experiments excluding vocalization

**Purpose:** Compare different feature extraction methods and their performance.

### `visualizacion/` - Data Exploration

Contains notebooks for data visualization and preprocessing.

**Files:**
- `1 Data Exploration and Visualisation.ipynb` - Dataset exploration
- `2 Data Preprocessing and Data Splitting.ipynb` - Data preprocessing and splitting

**Purpose:** Understand the datasets, visualize distributions, and prepare data for training.

### `emotion_recognition_cloud/` - Production API

Production-ready FastAPI application for emotion recognition.

**Structure:**
```
emotion_recognition_cloud/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── feature_extractor.py # Feature extraction module
│   └── model_loader.py      # Model loading and prediction
├── saved_models/            # Pre-trained models (not in git)
│   ├── mlp_emotion_model.h5
│   ├── svm_emotion_model.pkl
│   ├── knn_emotion_model.pkl
│   ├── feature_scaler.pkl
│   └── label_encoder.pkl
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── requirements.txt         # API dependencies
├── README.md                # API documentation
└── test_api.py             # API testing script
```

**Purpose:** Deploy trained models as a RESTful API service.

### `helpers/` - Utility Functions

Python modules with helper functions.

**Files:**
- `wavfilehelper.py` - Audio file reading utilities
- `__init__.py` - Package initialization

**Purpose:** Reusable utility functions for audio processing.

### `metadatos/` - Dataset Metadata

CSV files containing dataset information and splits.

**Files:**
- `EMODB - testSize 0.3.csv` - EMODB dataset metadata with 30% test split
- `emovo - testSize 0.3.csv` - EMOVO dataset metadata with 30% test split

**Purpose:** Track dataset organization, train/test splits, and file metadata.

### `articulos/` - Research Papers

PDF files of research papers and references used in the thesis.

**Purpose:** Store academic references and related research.

### `documento/` - Thesis Documentation

Thesis document and presentation files.

**Files:**
- `TesisAriel.pdf` - Complete thesis document
- `PresentacionTesis.pptx` - Thesis presentation

**Purpose:** Store thesis-related documentation.

## 📄 Root Level Files

### Main Pipeline Notebooks

- `Complete_Emotion_Recognition_Pipeline.ipynb` - Complete end-to-end pipeline (CPU)
- `Complete_Emotion_Recognition_Pipeline_GPU.ipynb` - GPU-accelerated version

**Purpose:** Comprehensive notebooks that combine all steps from data loading to prediction.

### Configuration Files

- `requirements.txt` - Python package dependencies
- `setup_environment.sh` - Environment setup script
- `.gitignore` - Git ignore rules

### Utility Scripts

- `gpu_utils.py` - GPU utility functions
- `simple_gpu_utils.py` - Simplified GPU utilities

### Documentation Files

- `README.md` - Main project documentation
- `CONTRIBUTING.md` - Contribution guidelines
- `PROJECT_STRUCTURE.md` - This file
- `GPU_OPTIMIZATION_GUIDE.md` - GPU setup guide
- Various fix and update documentation files

## 🔄 Workflow Through Directories

### Typical Workflow

1. **Data Exploration** (`visualizacion/`)
   - Explore datasets
   - Understand data distribution

2. **Feature Extraction** (`caracteristicas/`)
   - Extract MFCC, RASTA-MFCC, or MSES features
   - Save features for model training

3. **Model Training** (`clacificadores/`)
   - Train MLP, SVM, or KNN models
   - Evaluate model performance

4. **Experimentation** (`experimentos/`)
   - Compare different feature combinations
   - Analyze results

5. **Deployment** (`emotion_recognition_cloud/`)
   - Deploy trained models as API
   - Test API endpoints

### Complete Pipeline

For a complete end-to-end workflow, use:
- `Complete_Emotion_Recognition_Pipeline.ipynb` (CPU version)
- `Complete_Emotion_Recognition_Pipeline_GPU.ipynb` (GPU version)

## 📦 Files Not in Repository

The following are excluded from Git (see `.gitignore`):

- **Data files**: `data/` directory (too large)
- **Model files**: `*.h5`, `*.pkl` in `saved_models/`
- **Cache files**: `feature_cache/`, `__pycache__/`
- **Jupyter checkpoints**: `.ipynb_checkpoints/`

## 🎯 Best Practices

1. **Keep notebooks focused**: Each notebook should have a clear, single purpose
2. **Use descriptive names**: File names should indicate their purpose
3. **Organize by function**: Group related files in appropriate directories
4. **Document changes**: Update this file when adding new directories
5. **Follow naming conventions**: Use consistent naming patterns

## 📝 Adding New Components

When adding new components:

1. **Choose the right directory**: Place files in the most appropriate existing directory
2. **Create new directory if needed**: If no suitable directory exists, create one with a clear name
3. **Update this document**: Add documentation for new directories or significant changes
4. **Follow existing patterns**: Maintain consistency with existing structure

## 🔍 Finding Files

- **Feature extraction**: Look in `caracteristicas/`
- **Model training**: Check `clacificadores/`
- **Experiments**: See `experimentos/`
- **API code**: Navigate to `emotion_recognition_cloud/app/`
- **Utilities**: Check `helpers/`

---

For questions about the project structure, please open an issue or refer to the main README.md.

