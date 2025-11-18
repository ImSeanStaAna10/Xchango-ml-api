from fastapi import APIRouter, UploadFile, File, HTTPException
from core.utils import safe_open_image
from schemas.ocr_schema import OCRResponse
from core.models_loader import ocr_reader
from core.config import log
import io

router = APIRouter(tags=["ocr"])
@router.post("/ocr-extract", response_model=OCRResponse)
async def ocr_extract(
    id_front: UploadFile = File(...),
    id_back: UploadFile = File(None)
):
    """
    🔍 Extracts text from uploaded ID images using EasyOCR.
    Automatically handles front & back images.
    If OCR is disabled in .env (ENABLE_OCR=false), returns a clear 503 message.
    """

    # ✅ Check if OCR is enabled
    if ocr_reader is None:
        log.warning("⚠️ OCR is disabled via .env — skipping extraction.")
        raise HTTPException(
            status_code=503,
            detail="OCR temporarily disabled by server configuration."
        )

    # ✅ Validate front image
    front = safe_open_image(id_front)
    back = safe_open_image(id_back) if id_back else None
    if not front:
        raise HTTPException(status_code=400, detail="Front image invalid or unreadable.")

    # ✅ Run OCR on image
    def run_ocr(img):
        with io.BytesIO() as buf:
            img.save(buf, format="JPEG")
            buf.seek(0)
            return ocr_reader.readtext(buf.read(), detail=0)

    text = run_ocr(front)
    if back:
        text += run_ocr(back)

    log.info(f"🧾 OCR extracted {len(text)} lines.")

    # ✅ Basic extraction logic
    name = next((l for l in text if "NAME" in l.upper()), None)
    bday = next((l for l in text if any(x in l for x in ["19", "20", "/"])), None)
    idnum = next((l for l in text if "ID" in l.upper() or "NO" in l.upper()), None)

    return OCRResponse(
        text_lines=text,
        extracted_name=name,
        extracted_birthdate=bday,
        extracted_id_number=idnum,
    )