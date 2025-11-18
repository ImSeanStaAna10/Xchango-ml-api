from pydantic import BaseModel
from typing import List, Optional

class OCRResponse(BaseModel):
    text_lines: List[str]
    extracted_name: Optional[str] = None
    extracted_birthdate: Optional[str] = None
    extracted_id_number: Optional[str] = None
