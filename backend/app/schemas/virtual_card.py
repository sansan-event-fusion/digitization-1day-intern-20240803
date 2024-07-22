import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.entry import EntryModel
from app.models.virtual_card import VirtualCardModel


class VirtualCardBase(BaseModel):
    image_path: str | None
    entry: EntryModel = Field(...)


class VirtualCardCreate(VirtualCardBase):
    pass


class VirtualCardCreateBulk(BaseModel):
    entries: list[VirtualCardCreate]


class VirtualCard(VirtualCardBase):
    id: str = Field(uuid.uuid4().hex)
    created_at: str = Field(datetime.now().isoformat())
    delivered_at: str | None = Field(None)

    @classmethod
    def from_model(cls, model: VirtualCardModel) -> "VirtualCard":
        return VirtualCard(
            id=model.id,
            image_path=model.image_path,
            entry=model.entry,
            created_at=model.created_at,
            delivered_at=model.delivered_at,
        )
