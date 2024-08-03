import re

from app.models.entry import EntryItems
from app.models.inspector.base import (
    BaseInspector,
    InspectedVirtualCardModel,
    InspectionResetRule,
    InspectionRule,
)
from app.models.virtual_card import VirtualCardModel


class Inspector(BaseInspector):
    def __inspection_rules(self) -> list[InspectionRule]:
        return [
            InspectionRule(
                rules=[
                    InspectionResetRule(item=EntryItems.email, value=r"\.c0m$"),
                ],
                inspected_items=[EntryItems.email],
            ),
            InspectionRule(
                rules=[
                    InspectionResetRule(
                        item=EntryItems.company_name, value=r"Sansan株式会社"
                    ),
                    InspectionResetRule(
                        item=EntryItems.position_name, value=r"個人情報保護士"
                    ),
                ],
                inspected_items=[EntryItems.position_name],
            ),
        ]

    def __inspection_by_single_rule(
        self, model: InspectedVirtualCardModel, rule: InspectionRule
    ) -> InspectedVirtualCardModel:
        if all(
            re.search(rule.value, getattr(model.entry, rule.item.value))
            for rule in rule.rules
        ):
            model.inspect(*rule.inspected_items)
        return model

    def inspect(self, model: VirtualCardModel) -> InspectedVirtualCardModel:
        result = InspectedVirtualCardModel(**model.model_dump())
        for rule in self.__inspection_rules():
            result = self.__inspection_by_single_rule(result, rule)

        return result
