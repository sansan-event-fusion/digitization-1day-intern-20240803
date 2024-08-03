from enum import Enum
from pydantic import BaseModel, Field
import re


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

    @property
    def language(self):
        """
        名刺の言語を返す
        仮置きで、日本語の文字が一つでも含まれていたら日本語とする
        """

        for item_type in EntryItems:
            if re.search(r"[ぁ-んァ-ヶｱ-ﾝﾞﾟ一-龠]+", getattr(self, item_type.value)):
                return "ja"
        return "en"
