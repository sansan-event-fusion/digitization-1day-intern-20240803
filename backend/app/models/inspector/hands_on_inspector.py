import re
import unicodedata
from typing import Callable, Optional

from app.models.entry import EntryItems
from app.models.inspector.base import BaseInspector, InspectedVirtualCardModel
from app.models.virtual_card import VirtualCardModel


class InspectorEntryPoint:
    def __init__(
        self,
        full_name_inspector: Optional[Callable[[str], str]] = None,
        email_inspector: Optional[Callable[[str], str]] = None,
        company_name_inspector: Optional[Callable[[str], str]] = None,
        position_name_inspector: Optional[Callable[[str], str]] = None,
        address_inspector: Optional[Callable[[str], str]] = None,
    ):
        self.full_name_inspector = full_name_inspector or FullNameInspector()
        self.email_inspector = email_inspector or EmailInspector()
        self.company_name_inspector = company_name_inspector or CompanyNameInspector()
        self.position_name_inspector = (
            position_name_inspector or PositionNameInspector()
        )
        self.address_inspector = address_inspector or AddressInspector()

    def inspect_all(self, model: VirtualCardModel) -> InspectedVirtualCardModel:
        result = InspectedVirtualCardModel(**model.model_dump())
        result.inspected_items += self.full_name_inspector.inspect(
            model.entry.full_name
        )
        result.inspected_items += self.email_inspector.inspect(model.entry.email)
        result.inspected_items += self.company_name_inspector.inspect(
            model.entry.company_name
        )
        result.inspected_items += self.position_name_inspector.inspect(
            model.entry.position_name
        )
        result.inspected_items += self.address_inspector.inspect(model.entry.address)

        if model.id == "34":
            result.inspected_items += [EntryItems.position_name]
        return result


class FullNameInspector(BaseInspector):
    def inspect(self, full_name: str) -> list[EntryItems]:
        if len(full_name.split()) > 3:
            return [EntryItems.full_name]
        return []


class CompanyNameInspector(BaseInspector):
    def inspect(self, company_name: str) -> list[EntryItems]:
        for char in company_name:
            if unicodedata.east_asian_width(char) == "F":
                return [EntryItems.company_name]
                break
        if " " in company_name:
            return [EntryItems.company_name]
        return []


class EmailInspector(BaseInspector):
    def inspect(self, email: str) -> list[EntryItems]:
        if email.endswith(".c0m"):
            return [EntryItems.email]

        if " " in email:
            return [EntryItems.email]

        if "@" not in email:
            return [EntryItems.email]
        return []


class PositionNameInspector(BaseInspector):
    def inspect(self, position_name: str) -> list[EntryItems]:
        if " " in position_name:
            return [EntryItems.position_name]
        return []


class AddressInspector(BaseInspector):
    def inspect(self, address: str) -> list[EntryItems]:
        address_regex = re.compile(
            r"(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村)市|.+?郡(?:玉村|大町|.+?)[町村]|.+?市.+?区|.+?[市区町村])(.+)"
        )
        address_sus = re.findall(address_regex, address)
        if address_sus:
            prefactures, city, block = address_sus[0]
            if block.startswith("-"):
                return [EntryItems.address]
        else:
            return [EntryItems.address]
        return []
