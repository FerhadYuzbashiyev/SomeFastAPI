from dataclasses import dataclass

@dataclass
class FileCreateDTO:
    filename: str
    content_type: str
    size: int
    path: str
    user_id: int
