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

        # [hands-on] c0m を検知する
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

        # [work] 部署名の要素が会社名にふくまれていることを検知
        position_keywords = ["店", "支店", "営業所", "事業所", "研究所", "部"]
        for pos_keyword in position_keywords:
            if pos_keyword in model.entry.company_name:
                result.inspect(EntryItems.company_name)
                result.inspect(EntryItems.position_name)

        # [work] ラベルの検知（email: の部分が要らない）
        target_labels = ["address", "email"]
        for t_label in target_labels:
            lower_data = model.entry.dict().get(t_label).lower()
            if t_label in lower_data:
                result.inspect(eval(f"EntryItems.{t_label}"))

        # [work] invalid mail address の検知
        if model.entry.email.startswith("http://"):
            result.inspect(EntryItems.email)
        if model.entry.email.startswith("https://"):
            result.inspect(EntryItems.email)
        if "," in model.entry.email:
            result.inspect(EntryItems.email)

        # [work] 誤った会社名の検知
        # アドバイス：inspectorはブラックリスト方式で良い
        incorrect_company_names = ["キャノン", "ブリジストン"]
        for incor_c_name in incorrect_company_names:
            if incor_c_name in model.entry.company_name:
                result.inspect(EntryItems.company_name)

        # [work] スローガン？の検知
        # クォートがあればダメ？
        if "\"" in model.entry.company_name:
            result.inspect(EntryItems.company_name)
        if "\'" in model.entry.company_name:
            result.inspect(EntryItems.company_name)
        if "”" in model.entry.company_name:
            result.inspect(EntryItems.company_name)
        if "’" in model.entry.company_name:
            result.inspect(EntryItems.company_name)

        # [work] 街路番号の検知
        ng_words = ["丁目", "番地", "号"]
        for ng_word in ng_words:
            if ng_word in model.entry.address:
                result.inspect(EntryItems.address)

        # [work] 街路番号その２
        # 一の二の三 を検知したい
        kanji_nums = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
        # {}の{}の{} を検知したい
        for i in kanji_nums:
            for j in kanji_nums:
                for k in kanji_nums:
                    ng_word = f"{i}の{j}の{k}"
                    if ng_word in model.entry.address:
                        result.inspect(EntryItems.address)

        # DEBUG:
        # print("# Ln:inspect()")

        return result
