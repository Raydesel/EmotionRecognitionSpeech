#!/bin/bash

# Build script for Emotion Recognition API Docker container

echo "🐳 Building Emotion Recognition API Docker container..."

# Build the Docker image
docker build -t emotion-recognition-api .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    echo ""
    echo "🚀 To run the container:"
    echo "   docker run -p 80:80 emotion-recognition-api"
    echo ""
    echo "📖 Or use docker-compose:"
    echo "   docker-compose up"
    echo ""
    echo "🧪 To test the API:"
    echo "   python scripts/test_api.py"
else
    echo "❌ Docker build failed!"
    exit 1
fi

