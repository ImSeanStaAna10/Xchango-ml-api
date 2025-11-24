from transformers import CLIPProcessor, CLIPModel
from facenet_pytorch import InceptionResnetV1, MTCNN
import torch
import os
from categories import CATEGORY_PROMPTS
from core.config import log, device

# =========================================================
# CLIP MODEL (Item Categorization)
# =========================================================
log.info("Loading CLIP model...")
MODEL_NAME = "openai/clip-vit-base-patch32"
clip_model = CLIPModel.from_pretrained(
    MODEL_NAME,
    use_safetensors=True,
    torch_dtype=torch.float32
).to(device)

clip_processor = CLIPProcessor.from_pretrained(MODEL_NAME)

with torch.no_grad():
    cat_text_inputs = clip_processor(
        text=CATEGORY_PROMPTS,
        return_tensors="pt",
        padding=True,
        truncation=True
    ).to(device)
    CATEGORY_TEXT_FEATS = clip_model.get_text_features(**cat_text_inputs)
    CATEGORY_TEXT_FEATS = CATEGORY_TEXT_FEATS / CATEGORY_TEXT_FEATS.norm(dim=-1, keepdim=True)

log.info("✅ CLIP loaded successfully!")

# =========================================================
# FACENET MODEL (Face Verification)
# =========================================================
log.info("Loading FaceNet model...")
mtcnn = MTCNN(image_size=160, margin=0)
facenet_model = InceptionResnetV1(pretrained="vggface2").eval().to(device)
log.info("✅ FaceNet loaded successfully!")

# =========================================================
# OCR DISABLED
# =========================================================
ENABLE_OCR = False
ocr_reader = None
log.warning("🚫 OCR disabled (EasyOCR removed from dependencies)")
