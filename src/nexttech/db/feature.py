from pydantic import BaseModel
import uuid
import time
from .variation import Variation


class Feature(BaseModel):
    name: str
    last_editor: str | None
    last_checked: int | None
    desc: str

    last_modified: int = int(time.time())
    id: str = str(uuid.uuid4())
    active: bool = True
    bucket_by_user_id: bool = False
    deprecated: bool = False
    rollout: bool = False
    from_office: bool = False
    is_staff: bool = True
    is_authenticated: bool = True
    is_anonymous: bool = True
    countries: list[str] = []
    ratio: int = 100

    date_start: int | None = None
    date_end: int | None = None

    variations: list[Variation] = []
    history: list["Feature"] = []

    def __repr__(self):
        return f"Feature({self.model_dump()})"

    def __eq__(self, other):
        return self.model_dump() == other.model_dump()
