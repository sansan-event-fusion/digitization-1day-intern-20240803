from enum import Enum
from pydantic import BaseModel, Field


class EntryItems(Enum):
    full_name = "full_name"
    email = "email"
    company_name = "company_name"
    position_name = "position_name"
    address = "address"


class EntryModel(BaseModel):
    full_name: str = Field(description="名前")
    email: str = Field(description="メールアドレス")
    company_name: str = Field(description="会社名")
    position_name: str = Field(description="部署名")
    address: str = Field(description="住所")

    def __init__(self, /, **data: str) -> None:
        super().__init__(**data)
