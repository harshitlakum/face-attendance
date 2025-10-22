from pydantic import BaseModel
class EnrollResp(BaseModel):
    enrolled: int
class IdentifyResp(BaseModel):
    label: str
    distance: float
