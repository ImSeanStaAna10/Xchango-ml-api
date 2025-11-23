from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.classify import router as classify_router
from routes.verification import router as verify_router
from routes.ocr import router as ocr_router

app = FastAPI(title="Xchango ML API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(classify_router)
app.include_router(verify_router)
app.include_router(ocr_router)

@app.get("/")
def root():
    return {"message": "Xchango AI API running 🚀"}
