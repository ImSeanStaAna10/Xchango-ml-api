FROM python:3.11-slim

ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# system libs needed by OpenCV, Pillow, and EasyOCR
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libopencv-core-dev \
    libopencv-imgproc-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
