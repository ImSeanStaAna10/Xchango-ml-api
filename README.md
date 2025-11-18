# 🚀 Xchango ML API  
Machine Learning API for CLIP Item Classification, Face Verification, and OCR  
Built using **FastAPI**, **PyTorch**, **CLIP**, **FaceNet**, and **EasyOCR**.

This API powers the Xchango mobile application for automated image analysis and identity verification.

---

## 🔥 Features

### 🧩 1. CLIP Image Classification  
- Categorizes uploaded images into predefined text prompts  
- Uses `openai/clip-vit-base-patch32`

### 🧑‍🦰 2. Face Verification  
- Detects and extracts face embeddings using **MTCNN**  
- Compares faces using **InceptionResnetV1 (FaceNet)**  
- Returns cosine similarity score

### 📝 3. OCR (Text Extraction)  
- Reads text from IDs using **EasyOCR**  
- Supports English text extraction  
- Completely runs on CPU (no GPU required)

---

## 📦 Tech Stack
- **FastAPI**
- **PyTorch**
- **Torchvision**
- **Transformers**
- **Facenet-Pytorch**
- **EasyOCR**
- **OpenCV (Headless)**

---

## 🚀 Running the API locally

