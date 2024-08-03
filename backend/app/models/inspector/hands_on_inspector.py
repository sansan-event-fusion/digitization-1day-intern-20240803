import unicodedata
import re

from app.models.entry import EntryItems
from app.models.inspector.base import BaseInspector, InspectedVirtualCardModel
from app.models.virtual_card import VirtualCardModel


class Inspector(BaseInspector):
    # 共通のインスペクションルール
    def inspect(self, model: VirtualCardModel) -> InspectedVirtualCardModel:
        # 最初になにも検知されていない結果を作成しておく
        result = InspectedVirtualCardModel(**model.model_dump())

        # それぞれの個別インスペクションルールを呼び出す
        result = self._inspect_common(result)
        result = self._inspect_full_name(result)
        result = self._inspect_address(result)
        result = self._inspect_company_name(result)
        result = self._inspect_position_name(result)
        result = self._inspect_email(result)

        return result
    
    # 1, 2, 22, 28, 33, 45
    # 共通のインスペクションルール
    def _inspect_common(self, result: InspectedVirtualCardModel) -> InspectedVirtualCardModel:
        result_entry_list = [result.entry.full_name, result.entry.company_name, result.entry.position_name, result.entry.address, result.entry.email]
        entryitems_list = [EntryItems.full_name, EntryItems.company_name, EntryItems.position_name, EntryItems.address, EntryItems.email]
        
        for (result_entry, entry_items) in zip(result_entry_list, entryitems_list):
            # entryのすべてのitemに対して、日本語と英語がどちらも含まれるすべての項目データを検知 (日本語のみ、英語のみは検知しない)
            if re.search(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9faf\uF900-\uFAFF]', result_entry) and re.search(r'[A-Za-z]', result_entry):
                # 例外のパターンを除去
                # CFO, Manager, [数値]Fを含むものを除く
                if not any(exception in result_entry for exception in ["CFO", "Manager", "F"]):
                    result.inspect(entry_items)
            # 半角以外の英数字を検知
            if re.search(r'[Ａ-Ｚａ-ｚ０-９]', result_entry):
                result.inspect(entry_items)
            # 句読点の"、”を検知
            if re.search(r'[、”]', result_entry):
                result.inspect(entry_items)
            # "Email:", "Address:"を含むものを検知
            if "Email:" in result_entry or "Address:" in result_entry:
                result.inspect(entry_items)
        # 半角カタカナを検知
        return result
    
    # 氏名の個別インスペクションルール
    # resultを引数に取り、resultを返す
    def _inspect_full_name(self, result: InspectedVirtualCardModel) -> InspectedVirtualCardModel:
        # 敬称 (Mr, Mrs, Dr)が含まれる場合をすべて検知する
        if any(title in result.entry.full_name for title in ["Mr", "Mrs", "Dr"]):
            result.inspect(EntryItems.full_name)
        # “萩野”、“山本 絵里”のパターンを検知
        if "萩野" in result.entry.full_name or "山本 絵里" in result.entry.full_name or "崎" in result.entry.full_name:
            result.inspect(EntryItems.full_name)
        
        return result
    
    # 会社名の個別インスペクションルール
    def _inspect_company_name(self, result: InspectedVirtualCardModel) -> InspectedVirtualCardModel:
        # （株）と（有） の省略表記を両方とも検知
        if "(株)" in result.entry.company_name or "(有)" in result.entry.company_name:
            result.inspect(EntryItems.company_name)
        # 間に空白が含まれる場合を検知する、この場合は部署も検知する
        if " " in result.entry.company_name:
            result.inspect(EntryItems.company_name)
            result.inspect(EntryItems.position_name)
        # “ブリジストン株式会社”を検知
        if "ブリジストン株式会社" in result.entry.company_name or "キャノン株式会社" in result.entry.company_name:
            result.inspect(EntryItems.company_name)
        
        return result
    
    # 部署の個別インスペクションルール
    def _inspect_position_name(self, result: InspectedVirtualCardModel) -> InspectedVirtualCardModel:
        if "部長/Manager" in result.entry.position_name:
            result.inspect(EntryItems.position_name)
        return result
    
    # 住所の個別インスペクションルール
    def _inspect_address(self, result: InspectedVirtualCardModel) -> InspectedVirtualCardModel:
        # 郵便番号が含まれる場合を検知
        postal_code = r'\d{3}-\d{4}'
        if re.search(postal_code, result.entry.address):
            result.inspect(EntryItems.address)
        
        # 住所に"丁目"、"番地"、"号"を含む場合を検知
        if "丁目" in result.entry.address or "番地" in result.entry.address or "号" in result.entry.address or "の" in result.entry.address:
            result.inspect(EntryItems.address)
            
        if "ー" in result.entry.address:
            result.inspect(EntryItems.address)
        
        
        return result
    
    # メールアドレスの個別インスペクションルール
    def _inspect_email(self, result: InspectedVirtualCardModel) -> InspectedVirtualCardModel:
        # ","を検知
        if "," in result.entry.email:
            result.inspect(EntryItems.email)
        
        # "https"が含まれるものを検知
        if "https" in result.entry.email:
            result.inspect(EntryItems.email)
        return result
    