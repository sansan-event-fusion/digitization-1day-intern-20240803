import unicodedata

from app.models.entry import EntryItems
from app.models.inspector.base import BaseInspector, InspectedVirtualCardModel
from app.models.virtual_card import VirtualCardModel


class Inspector(BaseInspector):
    def inspect(self, model: VirtualCardModel) -> InspectedVirtualCardModel:
        # DEBUG:
        # print("# L0:inspect()")

        # 最初になにも検知されていない結果を作成しておく
        result = InspectedVirtualCardModel(**model.model_dump())

        # 条件に合致したら EntryItems.company_name を渡して実行
        # inspected_items を更新してくれる
        for char in model.entry.company_name:
            if unicodedata.east_asian_width(char) == "F":
                result.inspect(EntryItems.company_name)
                break

        # TODO: ここにロジックを追加する

        # c0m を検知する
        if model.entry.email.endswith("c0m"):
            result.inspect(EntryItems.email)
        # 解答例：
        # import re
        # if re.search(r"\.c0m$", model.entry.email):
        #     result.inspect(EntryItems.email)

        # [work] （株）（有）の検知
        short_types = ["（株）", "（有）"]
        for short_type in short_types:
            if short_type in model.entry.company_name:
                result.inspect(EntryItems.company_name)

        # [work] Mr. Dr. の検知
        titles = ["Mr.", "Dr."]
        for title in titles:
            if title in model.entry.full_name:
                result.inspect(EntryItems.full_name)

        # [work] 日英併記の検知
        # 氏名，会社名，部署名，住所 それぞれを確認する
        target_props = ["full_name", "company_name", "position_name", "address"]
        for prop in target_props:
            data = model.entry.dict().get(prop)
            is_combined: bool = len(set([unicodedata.east_asian_width(char) in "WH" for char in data])) > 1
            if is_combined:
                result.inspect(eval(f"EntryItems.{prop}"))

        # DEBUG:
        # print("# Ln:inspect()")

        return result
