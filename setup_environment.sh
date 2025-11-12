#!/bin/bash

# Emotion Recognition Speech Project - Environment Setup Script
# This script activates the conda environment and verifies all dependencies

echo "🎤 Emotion Recognition Speech Project - Environment Setup"
echo "========================================================="

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Conda is not installed or not in PATH"
    echo "Please install Anaconda or Miniconda first"
    exit 1
fi

# Activate the emotion_rec environment
echo "🔄 Activating conda environment: emotion_rec"
source $(conda info --base)/etc/profile.d/conda.sh
conda activate emotion_rec

if [ $? -ne 0 ]; then
    echo "❌ Failed to activate emotion_rec environment"
    echo "Please create the environment first with: conda create -n emotion_rec python=3.9"
    exit 1
fi

echo "✅ Environment activated successfully"

# Test the installation
echo "🧪 Testing library installation..."
python test_installation.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Setup complete! Your environment is ready."
    echo ""
    echo "To start working with the project:"
    echo "1. Activate the environment: conda activate emotion_rec"
    echo "2. Start Jupyter: jupyter notebook"
    echo "3. Open the notebooks in the visualizacion/ folder"
    echo ""
    echo "Available notebooks:"
    echo "- visualizacion/1 Data Exploration and Visualisation.ipynb"
    echo "- visualizacion/2 Data Preprocessing and Data Splitting.ipynb"
    echo "- caracteristicas/Features_emovo_EMODB.ipynb"
    echo "- experimentos/experimentos_EMODB_MSES.ipynb"
    echo "- clacificadores/3.2.0.0 Model Training and Evaluation.ipynb"
else
    echo "❌ Some libraries failed to import. Please check the error messages above."
    exit 1
fi

