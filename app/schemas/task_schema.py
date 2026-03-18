from pydantic import BaseModel
from datetime import datetime

class ConvertRequest(BaseModel):
    target_format: str