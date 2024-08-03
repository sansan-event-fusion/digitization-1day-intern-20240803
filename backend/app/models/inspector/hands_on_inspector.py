import unicodedata
import re
import string

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

        if re.search(r"\.c0m$", model.entry.email):
            result.inspect(EntryItems.email)
        # address
        if self.is_inspecting_word("address",model.entry.address):
            result.inspect(EntryItems.address)
        #full_nameに対するインスペクタ
        if self.is_inspecting_word("full_name",model.entry.full_name) or self.is_separate_en_or_other(model.entry.full_name):
            result.inspect(EntryItems.full_name)
        #positionに対するインスペクタ
        if self.is_inspecting_word("position_name",model.entry.position_name):
            result.inspect(EntryItems.position_name)
        #emailに対するインスペクタ
        if self.is_inspecting_word("email",model.entry.email):
            result.inspect(EntryItems.email)
        #companyに対するインスペクタ
        if self.is_inspecting_word("company_name",model.entry.company_name) or self.is_separate_en_or_other(model.entry.company_name):
            result.inspect(EntryItems.company_name)
            
        return result
    
    def is_inspecting_word(self, target, string):
        inspect_words_of_address = ["、","(",")","150-0222","Address",
                                    "丁目","番地","号",
                                    "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
        inspect_words_of_full_name = ["/","(",")",
                                      "山本 絵里","萩野 仁","Mr.","Dr.","店","髙","高","崎","﨑"]
        inspect_words_of_position_name = ["店","部","CEO","ソーシャルエコノミクス","主任"]
        inspect_words_of_email = ["Email:","https:",","]
        inspect_words_of_company_name = ["/","\"",
                                         "(株)","(有)","営業所","事業所","総務部",
                                         "ブリジストン","キャノン","日本エネルギー協会"
                                         "明日のエネルギーを、今",]
        inspect_words = None
        if target == "address":
            inspect_words = inspect_words_of_address
        elif target == "full_name":
            inspect_words = inspect_words_of_full_name
        elif target == "position_name":
            inspect_words = inspect_words_of_position_name
        elif target == "email":
            inspect_words = inspect_words_of_email
        elif target == "company_name":
            inspect_words = inspect_words_of_company_name

        for inspect_word in inspect_words:
            if inspect_word in string:
                return True
        return False
    
    def is_separate_en_or_other(self,string):
        is_en = string[0].isalpha()
        change_once = False
        for index, char in enumerate(string):
            if index == 0 or char.isdigit() or self.is_punctuation(char) or char == "（" or char == " ":
                continue
            if char.isalpha() != is_en:
                if change_once:
                    return False
                else:
                    change_once = True
        return True
    
    def is_punctuation(self, char):
        return char in string.punctuation