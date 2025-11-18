FROM python:3.11-slim

WORKDIR /app

ENV PIP_NO_CACHE_DIR=1

# System dependencies for EasyOCR + OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# HuggingFace Spaces runs on port 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
