import unicodedata
import re

from app.models.entry import EntryItems
from app.models.inspector.base import BaseInspector, InspectedVirtualCardModel
from app.models.virtual_card import VirtualCardModel


## メモ
# class EntryModel(BaseModel):
#  full_name: str = Field(description=
#  email: str = Field(description=
#  company_name: str = Field(description=
#  position_name: str = Field(description=
#  address: str = Field(description=


class Inspector(BaseInspector):
    def inspect(self, model: VirtualCardModel) -> InspectedVirtualCardModel:
        # 最初になにも検知されていない結果を作成しておく
        result = InspectedVirtualCardModel(**model.model_dump())

        # 条件に合致したら EntryItems.company_name を渡して実行
        # inspected_items を更新してくれる
        ## 会社名に全角英数字が含まれている場合に会社名（company_name）
        ## をリセットする場合だと以下䛾ような実装になります
        for char in model.entry.company_name:
            if unicodedata.east_asian_width(char) == "F":
                result.inspect(EntryItems.company_name)
                break

        # データだけ取り出し
        full_name = model.entry.full_name
        email = model.entry.email
        company_name = model.entry.company_name
        position_name = model.entry.position_name
        address = model.entry.address

        # TODO: ここにロジックを追加する

        if re.search(r"\.c0m$", email):
            result.inspect(EntryItems.email)

        # 会社名にカッコが含まれている場合に検出
        if re.search(r"\(", company_name):
            result.inspect(EntryItems.company_name)

        # 名前にカッコが含まれている場合に検出
        if re.search(r"\(", full_name):
            result.inspect(EntryItems.full_name)

        # addressの中に(が含まれている場合に抽出
        if re.search(r"\(", address):
            result.inspect(EntryItems.address)

        # position_nameを空白区切りにした時に、単語が2つ以上ある場合に検出
        if len(position_name.split()) >= 1:
            result.inspect(EntryItems.position_name)

        # 番地変換 例：「一丁目二番地三号 ->  東京都渋谷区神南1-2-3」
        if "丁目" in address or "番地" in address or "号" in address:
            result.inspect(EntryItems.address)

        # 名前を空白分割したときに長さが2より大きい時検知
        if len(full_name.split()) >= 2:
            result.inspect(EntryItems.full_name)

        # emailに//が含まれていたら検知
        if "//" in email:
            result.inspect(EntryItems.email)

        # 会社名を空白分割したときに長さが1より大きいときに検知
        if len(company_name.split()) > 1:
            result.inspect(EntryItems.company_name)

        # emailに”,”が含まれていたら検知
        if "," in email:
            result.inspect(EntryItems.email)

        # emailに":"が含まれていたら検知
        if ":" in email:
            result.inspect(EntryItems.email)
        # addressに":"が含まれていたら検知
        if ":" in address:
            result.inspect(EntryItems.address)

        # 生成させた正規表現で検査
        # patterns = {
        #     "full_name": r"[^\w\-]",  # 英数字、ハイフン、スペース以外の文字
        #     "email": r"[^a-zA-Z0-9@\._\-]",  # 英数字、@._-以外の文字
        #     "company_name": r"[^\p{L}\p{M}\p{N}\p{P}\p{Zs}]",  # 記号、スペース以外の文字
        #     "position_name": r"[^\p{L}\p{M}\p{N}\p{P}\p{Zs}]",  # 記号、スペース以外の文字
        #     "address": r"[^\p{L}\p{M}\p{N}\p{P}\p{Zs}\d\-]",  # 記号、数字、ハイフン、スペース以外の文字
        # }
        # # full_nameの検知
        # if re.search(patterns["full_name"], full_name):
        #     result.inspect(EntryItems.full_name)
        # # emailの検知
        # if re.search(patterns["email"], email):
        #     result.inspect(EntryItems.email)
        # # company_nameの検知
        # if re.search(patterns["company_name"], company_name):
        #     result.inspect(EntryItems.company_name)
        # # position_nameの検知
        # if re.search(patterns["position_name"], position_name):
        #     result.inspect(EntryItems.position_name)
        # # addressの検知
        # if re.search(patterns["address"], address):
        #     result.inspect(EntryItems.address)

        return result
