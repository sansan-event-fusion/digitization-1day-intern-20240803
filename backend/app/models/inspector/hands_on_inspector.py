import unicodedata

from app.models.entry import EntryItems
from app.models.inspector.base import BaseInspector, InspectedVirtualCardModel
from app.models.virtual_card import VirtualCardModel
import re

class Inspector(BaseInspector):
    def inspect(self, model: VirtualCardModel) -> InspectedVirtualCardModel:
        # 最初になにも検知されていない結果を作成しておく
        result = InspectedVirtualCardModel(**model.model_dump())

        # 条件に合致したら EntryItems.company_name を渡して実行
        # inspected_items を更新してくれる
        # 今回：会社名が全角？
        for char in model.entry.company_name:
            if unicodedata.east_asian_width(char) == "F":
                result.inspect(EntryItems.company_name)
                break

        # TODO: ここにロジックを追加する
        if self.check_email(model):
            result.inspect(EntryItems.email)

        if self.check_full_name(model):
            result.inspect(EntryItems.full_name)

        if self.check_company_name(model):
            result.inspect(EntryItems.company_name)

        if self.check_position_name(model):
            result.inspect(EntryItems.position_name)

        if self.check_address(model):
            result.inspect(EntryItems.address)

        return result

    def contains_english_and_japanese(self, text):
        # 英語の正規表現パターン
        english_pattern = re.compile(r'[A-Za-z]')
        # 日本語の正規表現パターン
        japanese_pattern = re.compile(r'[\u3040-\u30FF\u4E00-\u9FFF]')
        
        # 英語と日本語の両方が含まれているかをチェック
        return bool(english_pattern.search(text)) and bool(japanese_pattern.search(text))
    
    def check_full_name(self, model: VirtualCardModel)-> bool:
        if self.contains_english_and_japanese(model.entry.full_name):
            return True
        
        if model.entry.full_name.replace(" ", "") in model.entry.company_name:
            return True
        
        for word in ["萩野", "荻野"]:
            if word in model.entry.full_name:
                return True
        return False
    
    def check_company_name(self, model: VirtualCardModel)-> bool:

        if self.contains_english_and_japanese(model.entry.company_name):
            return True
        
        office_words = ["店", "所", "部"]
        for office_word in office_words:
            if office_word in model.entry.company_name:
                return True
        
        if "\"" in model.entry.company_name:
            return True
        
        proper_noun_err_lst = ["ブリジストン"]
        for proper_noun_err in proper_noun_err_lst:
            if proper_noun_err in model.entry.company_name:
                return True
            
        pattern = r"株式会社\s+.*"
        if re.search(pattern, model.entry.company_name):
            return True
        return False
    
    def check_position_name(self, model: VirtualCardModel)-> bool:
        if self.contains_english_and_japanese(model.entry.position_name):
            return True
        
        return False
    
    def check_address(self, model: VirtualCardModel)-> bool:
        is_no_digit = not any(char.isdigit() for char in model.entry.address)
        if is_no_digit:
            return True
        
        for word in ["丁目", "番地", "号"]:
            if word in model.entry.address:
                return True
        
        return False
    
    def check_email(self, model: VirtualCardModel)-> bool:
        if model.entry.email.endswith('.c0m'):
            return True
        
        pattern = re.compile(r'^.+@.+$')
        # ~@~ みたいな形になってない
        if not pattern.match(model.entry.email):
            return True

        return False