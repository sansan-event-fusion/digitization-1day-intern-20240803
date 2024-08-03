from typing import Optional

from app.models.entry import EntryModel
from pydantic import BaseModel


class EntryBase(BaseModel):
    full_name: Optional[str]
    email: Optional[str]
    company_name: Optional[str]
    position_name: Optional[str]
    address: Optional[str]


class Entry(EntryBase):
    @classmethod
    def from_model(cls, model: EntryModel) -> "Entry":
        return Entry(
            full_name=model.full_name or "",
            email=model.email or "",
            company_name=model.company_name or "",
            position_name=model.position_name or "",
            address=model.address or "",
        )
