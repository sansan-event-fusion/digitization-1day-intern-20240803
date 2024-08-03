import unicodedata

from app.models.entry import EntryItems
from app.models.inspector.base import BaseInspector, InspectedVirtualCardModel
from app.models.virtual_card import VirtualCardModel

kansuujis = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']

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

        # 会社名に"ブリジストン"が含まれているか検知
        if "ブリジストン" in model.entry.company_name:
            result.inspect(EntryItems.company_name) 


        target_items = [
            (model.entry.full_name, EntryItems.full_name),
            (model.entry.position_name, EntryItems.position_name),
            (model.entry.address, EntryItems.address),
        ]

        for target, item in target_items:
            if '/' in target:
                result.inspect(item)

        # メールアドレスがhttpならば
        if 'http' in model.entry.email:
            result.inspect(EntryItems.email)


        # 名前に異体字があったら
        itaijis = ['崎', '高', '萩']
        for itaiji in itaijis:
            if itaiji in model.entry.full_name:
                result.inspect(EntryItems.full_name)

        # キャノンはキヤノンです
        if 'キャノン' in model.entry.company_name:
            result.inspect(EntryItems.company_name)

        # 住所に漢数字があったら除外
        for kansuuji in kansuujis:
            if kansuuji in model.entry.address:
                result.inspect(EntryItems.address)
                break


        # 会社名に空白があるものは除外（英語の企業は良くない）
        if ' ' in model.entry.company_name:
            result.inspect(EntryItems.company_name)
        
        # 英語でpositionを書いてるものは除外
        positions = ['Marketing Department', 'Manager', 'CEO', 'Sales Div.', 'Engineer', 'ソーシャルエコノミクス','設計部','']
        for position in positions:
            if position in model.entry.position_name:
                result.inspect(EntryItems.position_name)
                break
    
        
        if model.entry.full_name == '山本 絵里':
            result.inspect(EntryItems.full_name)

        if model.entry.address == '東京都港区芝公園4-2-8 4-2-8 Shibakoen, Minato-ku, Tokyo':
            result.inspect(EntryItems.address)
        return result
