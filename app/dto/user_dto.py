from dataclasses import dataclass

@dataclass
class UserCreateDTO:
    name: str
    email: str
    password: str

@dataclass
class UserLoginDTO:
    email: str
    password: str
    