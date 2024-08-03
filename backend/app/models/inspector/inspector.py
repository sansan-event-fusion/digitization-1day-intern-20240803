from typing import List, Tuple, Callable
from functools import reduce
from app.models.inspector.base import BaseInspector, InspectedVirtualCardModel
from app.models.virtual_card import VirtualCardModel
from app.models.entry import EntryItems
import re

class Inspector(BaseInspector):
    rules = [
        ([(EntryItems.email, lambda x: re.match("http", x))], [EntryItems.email]),
        ([(EntryItems.email, lambda x: x.endswith(".c0m"))], [EntryItems.email]),
        ([
            (EntryItems.company_name, lambda x: x == "Sansan株式会社"),
            (EntryItems.position_name, lambda x: x == "個人情報保護士"),
        ], [EntryItems.position_name]),
        ([(EntryItems.company_name, lambda x: re.search(r'"', x))], [EntryItems.company_name]),
        ([(EntryItems.company_name, lambda x: re.search(r"会社.*協会", x))], [EntryItems.company_name]),
        ([(EntryItems.company_name, lambda x: re.search(r"^.*株式会社 .*", x))], [EntryItems.company_name]),
        ([(EntryItems.company_name, lambda x: re.search(r" .*(部|店|事業所|営業所|出張所|研究所)$", x))], [EntryItems.company_name, EntryItems.position_name]),
        ([(EntryItems.full_name, lambda x: "崎" in x)], [EntryItems.full_name]),
        ([(EntryItems.address, lambda x: "丁目" in x)], [EntryItems.address]),
        ([(EntryItems.address, lambda x: "番地" in x)], [EntryItems.address]),
        ([(EntryItems.address, lambda x: "号" in x)], [EntryItems.address]),
        ([(EntryItems.address, lambda x: "の" in x)], [EntryItems.address]),
        ([(EntryItems.address, lambda x: re.search("[()]", x))], [EntryItems.address]),
        ([(EntryItems.address, lambda x: re.search("[、・]", x))], [EntryItems.address]),
        # ([(EntryItems.address, lambda x: re.search("\/? \(?[a-zA-Z0-9., -]*\)?$", x))], [EntryItems.address]),
        # ([(EntryItems.full_name, lambda x: re.search("\/? \(?[a-zA-Z0-9., -]*\)?$", x))], [EntryItems.full_name]),
        # ([(EntryItems.company_name, lambda x: re.search("\/? \(?[a-zA-Z0-9., -]*\)?$", x))], [EntryItems.company_name]),
        # ([(EntryItems.position_name, lambda x: re.search("\/? \(?[a-zA-Z0-9., -]*\)?$", x))], [EntryItems.position_name]),
    ]

    def check(self, result: InspectedVirtualCardModel, rules) -> InspectedVirtualCardModel:
        """
        全てのチェックルールに合致しているかを確認する。チェックルールに合致する→インスペクトを実施する。
        OR 条件は考えない。（別のルールで定義することでカバーができる）
        """
        passed = True
        for (field, checkFunc) in rules:
            if not checkFunc(getattr(result.entry, field.value)):
                passed = False
                break
        return passed

    def apply(self, result: InspectedVirtualCardModel, rule) -> InspectedVirtualCardModel:
        checkRules, resetFields = rule
        if self.check(result, checkRules):
            for field in resetFields:
                result.inspect(field)
        return result


    def inspect(self, model: VirtualCardModel) -> InspectedVirtualCardModel:
        result = InspectedVirtualCardModel(**model.model_dump())
        reduce(self.apply, self.rules, result)
        return result
