# main.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import logging
import io

import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

from categories import CATEGORIES, CATEGORY_PROMPTS, KEYWORDS_BY_CATEGORY
from translator import translate_to_english
from settings import (
    TEXT_WEIGHT, IMAGE_WEIGHT,
    CONF_LOW, CONF_HIGH,
    ENABLE_TRANSLATION, LOG_LEVEL
)

# ---------- Logging ----------
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)s | %(message)s",
)
log = logging.getLogger("xchango-ml")


# ---------- FastAPI ----------
app = FastAPI(title="Xchango ML API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod (frontend/backend origins)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Load CLIP ----------
log.info("🔄 Loading CLIP model... please wait...")
MODEL_NAME = "openai/clip-vit-base-patch32"
device = "cpu"  # keep CPU for your environment
model = CLIPModel.from_pretrained(MODEL_NAME).to(device)
processor = CLIPProcessor.from_pretrained(MODEL_NAME)
log.info("✅ CLIP model loaded successfully!")

# Pre-encode category text prompts once
with torch.no_grad():
    cat_text_inputs = processor(
        text=CATEGORY_PROMPTS,
        return_tensors="pt",
        padding=True,
        truncation=True
    ).to(device)
    CATEGORY_TEXT_FEATS = model.get_text_features(**cat_text_inputs)
    CATEGORY_TEXT_FEATS = CATEGORY_TEXT_FEATS / CATEGORY_TEXT_FEATS.norm(dim=-1, keepdim=True)


# ---------- Schemas ----------
class ClassifyResponse(BaseModel):
    original_title: str
    translated_title: Optional[str] = None
    predicted_category: str
    confidence_score: float  # 0-100
    confidence_level: str    # "low" | "medium" | "high"
    used_text: bool
    used_image: bool
    top3: List[str]


# ---------- Helpers ----------
def confidence_level_from(score: float) -> str:
    """Map 0..1 → low/medium/high."""
    if score >= CONF_HIGH:
        return "high"
    if score >= CONF_LOW:
        return "medium"
    return "low"

def keyword_boost_vector(title_lower: str) -> torch.Tensor:
    """Return a boost vector per category (same shape as CATEGORIES)."""
    boosts = torch.zeros(len(CATEGORIES), dtype=torch.float32)
    for idx, cat in enumerate(CATEGORIES):
        words = KEYWORDS_BY_CATEGORY.get(cat, [])
        for w in words:
            if w in title_lower:
                # small additive boost; tune as needed
                boosts[idx] += 0.15
    return boosts

def softmax_probs(logits: torch.Tensor) -> torch.Tensor:
    return torch.softmax(logits, dim=-1)

def safe_open_image(file: UploadFile) -> Optional[Image.Image]:
    try:
        content = file.file.read()
        img = Image.open(io.BytesIO(content)).convert("RGB")
        return img
    except Exception:
        return None


# ---------- Routes ----------
@app.get("/", tags=["meta"])
def root():
    return {"message": "Xchango AI API is running 🚀", "version": "1.0.0"}

@app.get("/healthz", tags=["meta"])
def healthz():
    return {"status": "ok"}

@app.get("/readyz", tags=["meta"])
def readyz():
    # optionally check if CATEGORY_TEXT_FEATS on device, etc.
    return {"ready": True}


@app.post("/classify", response_model=ClassifyResponse, tags=["classify"])
async def classify_item(
    title: str = Form(..., description="Short item title/name"),
    image: UploadFile = File(None, description="Optional product image"),
):
    """
    Categorize item using **title** (+ optional image).
    - Uses CLIP text+image, plus Tagalog/Taglish translation (optional) and keyword boosts.
    """
    title = (title or "").strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title is required.")

    log.debug(f"Incoming title: {title}")

    # Translate (optional via env)
    translated_title = translate_to_english(title) if ENABLE_TRANSLATION else title
    log.debug(f"Translated title: {translated_title}")

    used_image = False
    img = None
    if image and image.filename:
        img = safe_open_image(image)
        if img is not None:
            used_image = True
        else:
            log.warning("Failed to decode image; ignoring image signal.")

    with torch.no_grad():
        # Text → features
        text_inputs = processor(
            text=[translated_title],
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(device)
        text_feat = model.get_text_features(**text_inputs)
        text_feat = text_feat / text_feat.norm(dim=-1, keepdim=True)  # [1, d]

        # Similarity vs categories (text → categories_text)
        sim_text = (text_feat @ CATEGORY_TEXT_FEATS.T).squeeze(0)  # [num_cats]

        # Image (optional) → features → similarity vs categories_text
        if used_image:
            image_inputs = processor(images=img, return_tensors="pt").to(device)
            image_feat = model.get_image_features(**image_inputs)
            image_feat = image_feat / image_feat.norm(dim=-1, keepdim=True)  # [1, d]
            sim_image = (image_feat @ CATEGORY_TEXT_FEATS.T).squeeze(0)      # [num_cats]
        else:
            sim_image = torch.zeros_like(sim_text)

        # Keyword boosts
        boosts = keyword_boost_vector(translated_title.lower())

        # Combine
        logits = TEXT_WEIGHT * sim_text + IMAGE_WEIGHT * sim_image + boosts

        # Softmax → probs
        probs = softmax_probs(logits)
        best_idx = int(torch.argmax(probs).item())
        best_cat = CATEGORIES[best_idx]
        best_prob = float(probs[best_idx].item())  # 0..1

        # Get top3 category names
        topk = torch.topk(probs, k=min(3, len(CATEGORIES)))
        top3_idx = topk.indices.tolist()
        top3 = [CATEGORIES[i] for i in top3_idx]

    response = ClassifyResponse(
        original_title=title,
        translated_title=(translated_title if ENABLE_TRANSLATION else None),
        predicted_category=best_cat,
        confidence_score=round(best_prob * 100, 2),
        confidence_level=confidence_level_from(best_prob),
        used_text=True,
        used_image=used_image,
        top3=top3,
    )
    return response
