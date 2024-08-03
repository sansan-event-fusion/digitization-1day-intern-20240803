import re
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
        if re.search(r"\\.c0m$",model.entry.email):
            result.inspect(EntryItems.email)
        if re.search(r"[一二三四五六七八九十百千万]*(番地)?$", model.entry.address):
            converted_address = kanji_to_number(model.entry.address)
            # 「番地」を削除
            model.entry.address = re.sub(r'番地$', '', converted_address)       
            result.inspect(EntryItems.address)
        if model.entry.company_name:
            model.entry.company_name = remove_after_space(model.entry.company_name)
            result.inspect(EntryItems.company_name)
        if model.entry.full_name:
            model.entry.full_name = remove_after_second_space(model.entry.full_name)
            result.inspect(EntryItems.full_name)
        if model.entry.position_name:
            model.entry.position_name = remove_after_space_or_slash(model.entry.position_name)
            result.inspect(EntryItems.position_name)


        return result

def kanji_to_number(text):
    kanji_numbers = {
        '一': '1', '二': '2', '三': '3', '四': '4', '五': '5',
        '六': '6', '七': '7', '八': '8', '九': '9', '十': '10',
    }
    
    for kanji, number in kanji_numbers.items():
        text = text.replace(kanji, number)
    
    return text

def remove_after_space(text):
    pattern = r'^([^\s]+(?:\s+[^\s]+)*)\s*株式会社'
    match = re.match(pattern, text)
    if match:
        return match.group(0)
    return text

def remove_after_second_space(text):
    pattern = r'^(\S+\s+\S+)(?:\s+.*)?$'
    match = re.match(pattern, text)
    if match:
        return match.group(1)
    return text

def remove_after_space_or_slash(text):
    pattern = r'^([^/\s]+)(?:[/\s].*)?$'
    match = re.match(pattern, text)
    if match:
        return match.group(1)
    return text


