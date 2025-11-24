from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from routes.classify import router as classify_router
from routes.verification import router as verify_router

app = FastAPI(title="Xchango ML API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load main routes
app.include_router(classify_router)
app.include_router(verify_router)

# Conditional OCR route
ENABLE_OCR = os.getenv("ENABLE_OCR", "false").lower() == "true"
if ENABLE_OCR:
    from routes.ocr import router as ocr_router
    app.include_router(ocr_router)
    print("🟢 OCR Enabled and Route Loaded")
else:
    print("🟡 OCR Disabled — Route Not Loaded")

@app.get("/")
def root():
    return {"message": "Xchango AI API running 🚀"}
