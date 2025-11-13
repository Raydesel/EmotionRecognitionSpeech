# Base image with Python 3.11
FROM python:3.11-slim

# Set working directory
WORKDIR /code

# Install system dependencies for audio processing
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy application code
COPY ./app /code/app

# Copy saved models (if they exist)
COPY ./saved_models /code/saved_models

# Create static directory and copy web app
RUN mkdir -p /code/static
COPY ./web_app.html /code/static/web_app.html

# Create directory for temporary files
RUN mkdir -p /tmp/audio_uploads

# Expose port
EXPOSE 80

# Run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

