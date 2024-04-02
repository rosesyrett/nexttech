from pydantic import BaseModel
import uuid

class Variation(BaseModel):
    name: str
    ratio: int
    id: str = str(uuid.uuid4())