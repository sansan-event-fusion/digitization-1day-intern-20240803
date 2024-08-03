import unicodedata

from app.models.entry import EntryItems
from app.models.inspector.base import BaseInspector, InspectedVirtualCardModel
from app.models.virtual_card import VirtualCardModel


class Inspector(BaseInspector):
    def inspect(self, model: VirtualCardModel) -> InspectedVirtualCardModel:
        # 最初になにも検知されていない結果を作成しておく
        result = InspectedVirtualCardModel(**model.model_dump())

        # 条件に合致したら EntryItems.company_name を渡して実行
        # inspected_items を更新してくれる
        for char in model.entry.company_name:
            if unicodedata.east_asian_width(char) == "F": # 会社名が大文字になっているか検知
                result.inspect(EntryItems.company_name)
                break

        # TODO: ここにロジックを追加する
        # emailの最後がcomかどうかを検知する
        if model.entry.email.split('.')[-1] == 'c0m':
            result.inspect(EntryItems.email)

        
    


        return result
