from pydantic import BaseModel
from typing import List, Optional

class ClassifyResponse(BaseModel):
    original_title: str
    translated_title: Optional[str] = None
    predicted_category: str
    confidence_score: float
    confidence_level: str
    used_text: bool
    used_image: bool
    top3: List[str]
