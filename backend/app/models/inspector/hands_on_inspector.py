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
            if unicodedata.east_asian_width(char) == "F":
                result.inspect(EntryItems.company_name)
                break

        # TODO: ここにロジックを追加する
        
        if (model.entry.email.split(".")[-1] == "c0m" or 
          ":" in model.entry.email or 
          "http" in model.entry.email or
          "," in model.entry.email):
            result.inspect(EntryItems.email)

        company_name_miss = ["(", ")",  " ", "ブリヂストン", "キャノン", "店", "営業所","研究所", "\"" ]

        for i in company_name_miss:
            if i in model.entry.company_name:
                result.inspect(EntryItems.company_name)
            elif " " in model.entry.company_name:
                result.inspect(EntryItems.position_name)

        
        
        adress_miss  = ["丁目", "番", "地","号""一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "ー"]

        for i in adress_miss:
            if i in model.entry.address:
                result.inspect(EntryItems.address)
        
        name_miss = ["カ", "力", "高", "髙", "荻", "(", ")", "Mr.", "Ms.", "Mrs.", "Dr"]

        for i in name_miss:
            if i in model.entry.full_name:
                result.inspect(EntryItems.full_name)

        position_miss = ["CEO", "/", "\""]

        for i in position_miss:
            if i in model.entry.position_name:
                result.inspect(EntryItems.position_name)
        

        

        
            

        return result
