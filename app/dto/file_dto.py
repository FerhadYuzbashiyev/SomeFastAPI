from dataclasses import dataclass
from fastapi import UploadFile

@dataclass
class FileCreateDTO:
    file: UploadFile