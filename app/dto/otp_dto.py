from dataclasses import dataclass

@dataclass
class OTPCreateDTO:
    user_id: int
    otp_code: int
