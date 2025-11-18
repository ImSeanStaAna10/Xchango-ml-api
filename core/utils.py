import torch
from PIL import Image
import io
from core.models_loader import mtcnn, facenet_model

def safe_open_image(file):
    if file is None:
        return None
    try:
        content = file.file.read()
        return Image.open(io.BytesIO(content)).convert("RGB")
    except Exception:
        return None

def get_face_embedding(img):
    face = mtcnn(img)
    if face is None:
        return None
    with torch.no_grad():
        emb = facenet_model(face.unsqueeze(0)).detach()
        return emb / emb.norm(dim=-1, keepdim=True)

def cosine_similarity(t1, t2):
    return float(torch.nn.functional.cosine_similarity(t1, t2).item())
