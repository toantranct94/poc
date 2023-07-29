from pydantic import BaseModel
from typing import Optional


class Cache(BaseModel):
    key: str
    value: Optional[dict] = None
    ttl: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "value": self.value,
            "ttl": self.ttl,
        }
