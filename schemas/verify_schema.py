from pydantic import BaseModel
from typing import Optional

class FaceVerifyResponse(BaseModel):
    face_match: bool
    similarity: float
    back_image_received: Optional[bool] = None
