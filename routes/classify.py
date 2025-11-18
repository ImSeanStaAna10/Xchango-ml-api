from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import torch
from core.models_loader import clip_model, clip_processor, CATEGORY_TEXT_FEATS
from core.config import log, device
from categories import CATEGORIES, KEYWORDS_BY_CATEGORY
from schemas.classify_schema import ClassifyResponse
from translator import translate_to_english
from settings import TEXT_WEIGHT, IMAGE_WEIGHT, CONF_LOW, CONF_HIGH, ENABLE_TRANSLATION
from core.utils import safe_open_image

router = APIRouter(tags=["classify"])

def confidence_level(score):
    if score >= CONF_HIGH:
        return "high"
    elif score >= CONF_LOW:
        return "medium"
    return "low"

def keyword_boost_vector(title_lower):
    boosts = torch.zeros(len(CATEGORIES), dtype=torch.float32)
    for idx, cat in enumerate(CATEGORIES):
        for w in KEYWORDS_BY_CATEGORY.get(cat, []):
            if w in title_lower:
                boosts[idx] += 0.15
    return boosts

@router.post("/classify", response_model=ClassifyResponse)
async def classify_item(title: str = Form(...), image: UploadFile = File(None)):
    title = title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")

    translated = translate_to_english(title) if ENABLE_TRANSLATION else title
    img = safe_open_image(image) if image else None

    with torch.no_grad():
        text_inputs = clip_processor(text=[translated], return_tensors="pt", padding=True, truncation=True).to(device)
        text_feat = clip_model.get_text_features(**text_inputs)
        text_feat = text_feat / text_feat.norm(dim=-1, keepdim=True)
        sim_text = (text_feat @ CATEGORY_TEXT_FEATS.T).squeeze(0)

        if img:
            image_inputs = clip_processor(images=img, return_tensors="pt").to(device)
            image_feat = clip_model.get_image_features(**image_inputs)
            image_feat = image_feat / image_feat.norm(dim=-1, keepdim=True)
            sim_image = (image_feat @ CATEGORY_TEXT_FEATS.T).squeeze(0)
        else:
            sim_image = torch.zeros_like(sim_text)

        boosts = keyword_boost_vector(translated.lower())
        logits = TEXT_WEIGHT * sim_text + IMAGE_WEIGHT * sim_image + boosts
        probs = torch.softmax(logits, dim=-1)
        idx = int(torch.argmax(probs))
        top3 = [CATEGORIES[i] for i in torch.topk(probs, k=3).indices.tolist()]

    return ClassifyResponse(
        original_title=title,
        translated_title=(translated if ENABLE_TRANSLATION else None),
        predicted_category=CATEGORIES[idx],
        confidence_score=round(probs[idx].item() * 100, 2),
        confidence_level=confidence_level(probs[idx]),
        used_text=True,
        used_image=bool(img),
        top3=top3
    )
