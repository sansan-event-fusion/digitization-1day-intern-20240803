import unicodedata

from app.models.entry import EntryItems
from app.models.inspector.base import BaseInspector, InspectedVirtualCardModel
from app.models.virtual_card import VirtualCardModel


class Inspector(BaseInspector):
    def inspect(self, model: VirtualCardModel) -> InspectedVirtualCardModel:
        # 最初になにも検知されていない結果を作成しておく
        result = InspectedVirtualCardModel(**model.model_dump())

        # 名前の検査
        self.inspect_name(model, result)

        # メアドの検査
        self.inspect_email(model, result)

        # 会社名の検査
        self.inspect_company_name(model, result)

        # 住所の検査
        self.inspect_address(model, result)

        return result

    def inspect_name(self, model: VirtualCardModel, result: InspectedVirtualCardModel)-> None:
        # 特定のエラーケースに対して個別に処理を行う
        if model.entry.full_name[0] in ["D", "M"]:
            result.inspect(EntryItems.full_name)

        if model.entry.full_name[-1] == ")":
            result.inspect(EntryItems.full_name)

        if model.entry.full_name[0] == "萩" and model.entry.full_name[1] == "野":
            result.inspect(EntryItems.full_name)

        if model.entry.full_name[0] == "大" and model.entry.full_name[1] == "崎":
            result.inspect(EntryItems.full_name)

    def inspect_email(self, model: VirtualCardModel, result: InspectedVirtualCardModel)-> None:
        # 特定のエラーケースに対して個別に処理を行う
        if any(char in model.entry.email for char in [",", ":"]):
            result.inspect(EntryItems.address)

    def inspect_company_name(self, model: VirtualCardModel, result: InspectedVirtualCardModel)-> None:
        # 特定のエラーケースに対して個別に処理を行う
        if model.entry.company_name[-1] == "所":
            result.inspect(EntryItems.full_name)

    def inspect_address(self, model: VirtualCardModel, result: InspectedVirtualCardModel)-> None:
        # 不適切な表記の住所を検知する
        error_address_wards: list[str] = [
            "一",
            "二",
            "三",
            "四",
            "五",
            "六",
            "七",
            "八",
            "九",
            "十,",
            "丁目",
            "番地",
            "号",
        ]

        if any(char in model.entry.address for char in error_address_wards):
            result.inspect(EntryItems.address)
