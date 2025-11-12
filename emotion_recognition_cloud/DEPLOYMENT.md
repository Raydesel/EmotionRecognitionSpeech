# Emotion Recognition API - Deployment Guide

## Quick Start

### 1. Build the Docker Image

```bash
# Make the build script executable and run it
chmod +x build.sh
./build.sh

# Or build manually
docker build -t emotion-recognition-api .
```

### 2. Run the Container

#### Option A: Using Docker Run
```bash
docker run -p 80:80 emotion-recognition-api
```

#### Option B: Using Docker Compose
```bash
docker-compose up
```

### 3. Test the API

```bash
# Test the API endpoints
python test_api.py

# Or visit the interactive docs
open http://localhost/docs
```

## API Endpoints

Once running, the API will be available at `http://localhost` with the following endpoints:

- `GET /` - API information
- `GET /health` - Health check
- `GET /models` - Available models
- `GET /emotion-classes` - Emotion classes
- `POST /predict` - Single file prediction
- `POST /predict-batch` - Batch prediction

## Usage Examples

### Single File Prediction

```bash
curl -X POST "http://localhost/predict?model=MLP" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@audio_file.wav"
```

### Batch Prediction

```bash
curl -X POST "http://localhost/predict-batch?model=SVM" \
     -H "Content-Type: multipart/form-data" \
     -F "files=@audio1.wav" \
     -F "files=@audio2.wav"
```

### Python Example

```python
import requests

# Single file prediction
with open('audio_file.wav', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost/predict?model=MLP', files=files)
    result = response.json()
    print(f"Predicted emotion: {result['predicted_emotion']}")
    print(f"Confidence: {result['confidence']}")
```

## Production Deployment

### Environment Variables

```bash
# Set production environment
export PYTHONUNBUFFERED=1
export WORKERS=4
```

### Docker Compose for Production

```yaml
version: '3.8'
services:
  emotion-recognition-api:
    build: .
    ports:
      - "80:80"
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Scaling

```bash
# Scale to multiple instances
docker-compose up --scale emotion-recognition-api=3
```

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port mapping
   ```bash
   docker run -p 8080:80 emotion-recognition-api
   ```

2. **Model loading errors**: Ensure saved_models directory exists and contains all required files

3. **Audio format issues**: Supported formats are WAV, MP3, M4A, FLAC

### Logs

```bash
# View container logs
docker logs <container_id>

# Follow logs in real-time
docker logs -f <container_id>
```

### Health Check

```bash
# Check API health
curl http://localhost/health

# Check available models
curl http://localhost/models
```

## Performance Optimization

### GPU Support (Optional)

For GPU acceleration, modify the Dockerfile:

```dockerfile
FROM tensorflow/tensorflow:2.15.0-gpu
# ... rest of the Dockerfile
```

### Memory Optimization

```bash
# Limit container memory
docker run -m 2g -p 80:80 emotion-recognition-api
```

## Security Considerations

1. **Input Validation**: The API validates file types and sizes
2. **Rate Limiting**: Consider adding rate limiting for production
3. **Authentication**: Add authentication for production deployments
4. **HTTPS**: Use reverse proxy with SSL for production

## Monitoring

### Health Checks

```bash
# Automated health check
curl -f http://localhost/health || exit 1
```

### Metrics

The API provides basic metrics through the `/health` endpoint:
- Model loading status
- Available models
- System health

## Support

For issues or questions:
1. Check the logs: `docker logs <container_id>`
2. Test with the provided test script: `python test_api.py`
3. Verify model files are present in `saved_models/` directory

