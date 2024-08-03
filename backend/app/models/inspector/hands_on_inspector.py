import unicodedata

from app.models.entry import EntryItems
from app.models.inspector.base import BaseInspector, InspectedVirtualCardModel
from app.models.virtual_card import VirtualCardModel

import re

NUMBER_CHARACTER_PATTERN = r'[一二三四五六七八九十百千万億兆]+ー'

def is_japanese(text):
    for char in text:
        # ひらがな、カタカナ、漢字の Unicode 範囲をチェック
        if ('\u3040' <= char <= '\u309F') or ('\u30A0' <= char <= '\u30FF') or ('\u4E00' <= char <= '\u9FFF'):
            return True
    return False

def has_invalid_delimiter(text):
    return bool(re.search(NUMBER_CHARACTER_PATTERN, text))

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
        if model.entry.company_name == "キャノン株式会社":
            result.inspect(EntryItems.company_name)
        if model.entry.company_name == "ブリジストン株式会社":
            result.inspect(EntryItems.company_name)
        if "事業所" in model.entry.company_name:
            result.inspect(EntryItems.company_name)
            result.inspect(EntryItems.position_name)
        if "店" in model.entry.company_name:
            result.inspect(EntryItems.company_name)
            result.inspect(EntryItems.position_name)
        if "/" in model.entry.company_name:
            result.inspect(EntryItems.company_name)
        if model.entry.company_name.endswith(" "):
            result.inspect(EntryItems.company_name)
        if "(" in model.entry.company_name:
            result.inspect(EntryItems.company_name)
        if "営業所" in model.entry.company_name:
            result.inspect(EntryItems.company_name)
            result.inspect(EntryItems.position_name)
        if "研究所" in model.entry.company_name:
            result.inspect(EntryItems.company_name)
            result.inspect(EntryItems.position_name)
        if '"' in model.entry.company_name:
            result.inspect(EntryItems.company_name)
        if is_japanese(model.entry.company_name):
            if len(model.entry.company_name.split()) >= 2:
                result.inspect(EntryItems.company_name)
        if "部" in model.entry.company_name:
            result.inspect(EntryItems.position_name)


        if model.entry.email.endswith("c0m"):
            result.inspect(EntryItems.email)
        if "http" in model.entry.email:
            result.inspect(EntryItems.email)
        if "Email" in model.entry.email:
            result.inspect(EntryItems.email)
        if "," in model.entry.email:
            result.inspect(EntryItems.email)

        if "Address" in model.entry.address:
            result.inspect(EntryItems.address)
        if "丁目" in model.entry.address:
            result.inspect(EntryItems.address)
        if "番地" in model.entry.address:
            result.inspect(EntryItems.address)
        if "(" in model.entry.address:
            result.inspect(EntryItems.address)
        if "、" in model.entry.address:
            result.inspect(EntryItems.address)
        if "の" in model.entry.address:
            result.inspect(EntryItems.address)
        if has_invalid_delimiter(model.entry.address):
            result.inspect(EntryItems.address)

        if "仁" in model.entry.full_name:
            result.inspect(EntryItems.full_name)
        if "崎" in model.entry.full_name:
            result.inspect(EntryItems.full_name)
        if "Mr." in model.entry.full_name:
            result.inspect(EntryItems.full_name)
        if "Dr." in model.entry.full_name:
            result.inspect(EntryItems.full_name)
        if "/" in model.entry.full_name:
            result.inspect(EntryItems.full_name)
        if "(" in model.entry.full_name:
            result.inspect(EntryItems.full_name)
        if "（" in model.entry.full_name:
            result.inspect(EntryItems.full_name)
        if len(model.entry.full_name.split()) >= 3:
            result.inspect(EntryItems.full_name)
        if model.entry.full_name.replace(" ", "") in model.entry.company_name:
            result.inspect(EntryItems.full_name)

        if "/" in model.entry.position_name:
            result.inspect(EntryItems.position_name)
        if "(" in model.entry.position_name:
            result.inspect(EntryItems.position_name)
        if "部" in model.entry.position_name:
            if "Department" in model.entry.position_name:
                result.inspect(EntryItems.position_name)
            if "Div" in model.entry.position_name:
                result.inspect(EntryItems.position_name)
        if "最高経営責任者" in model.entry.position_name and "CEO" in model.entry.position_name:
            result.inspect(EntryItems.position_name)
        if "エンジニア" in model.entry.position_name and "Engineer" in model.entry.position_name:
            result.inspect(EntryItems.position_name)

        return result
