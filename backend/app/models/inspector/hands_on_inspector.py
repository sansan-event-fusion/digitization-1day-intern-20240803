import unicodedata
import re

from app.models.entry import EntryItems
from app.models.inspector.base import BaseInspector, InspectedVirtualCardModel
from app.models.virtual_card import VirtualCardModel


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

        # TODO: ここにロジックを追加する
        if re.search(r"\.c0m$", model.entry.email):
            result.inspect(EntryItems.email)

        return result
