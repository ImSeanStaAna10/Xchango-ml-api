from fastapi import APIRouter, UploadFile, File, HTTPException
from core.utils import safe_open_image, get_face_embedding, cosine_similarity
from schemas.verify_schema import FaceVerifyResponse
from core.config import log

router = APIRouter(tags=["verification"])

@router.post("/face-verify", response_model=FaceVerifyResponse)
async def face_verify(id_front: UploadFile = File(...), selfie: UploadFile = File(...), id_back: UploadFile = File(None)):
    id_img = safe_open_image(id_front)
    selfie_img = safe_open_image(selfie)
    if not id_img or not selfie_img:
        raise HTTPException(status_code=400, detail="Invalid image input")

    id_emb = get_face_embedding(id_img)
    self_emb = get_face_embedding(selfie_img)
    if id_emb is None or self_emb is None:
        raise HTTPException(status_code=400, detail="No face detected")

    sim = cosine_similarity(id_emb, self_emb)
    match = sim >= 0.6
    log.info(f"Face similarity: {sim:.3f} | Match: {match}")

    return FaceVerifyResponse(face_match=match, similarity=round(sim * 100, 2), back_image_received=bool(id_back))
