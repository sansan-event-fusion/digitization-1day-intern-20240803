from app.models.entry import EntryModel
from pydantic import BaseModel, Field


class VirtualCardModel(BaseModel):
    id: str = Field(description="名刺のID")
    image_path: str | None = Field(description="名刺の画像のパス")
    entry: EntryModel = Field(description="名刺のデータ化項目")
    created_at: str = Field(description="作成日時")
    delivered_at: str | None = Field(None, description="納品日時")
