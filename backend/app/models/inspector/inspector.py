from app.models.inspector.base import BaseInspector, InspectedVirtualCardModel
from app.models.virtual_card import VirtualCardModel
from app.models.entry import EntryItems


EASY_TO_MISTAKE_CHARACTERS = ["荻", "萩", "高", "髙", "崎", "﨑"]

FULL_NAME_MISTAKE_COMPANIES = [
    "山本絵里音楽プロダクション",
    "Johnson Digital Solutions Ltd.",
]
EMAIL_MISTAKE_COMPANIES = ["テックアドバンス", "ウェブイノベーションズ株式会社"]
COMPANY_NAME_MISTAKE_COMPANIES = [
    "ネットソリューションズ株式会社",
    "グリーンエナジー株式会社",
    "Innovative Tech Solutions",
    "キャノン株式会社",
    "ブリジストン株式会社",
    "サンライトエネルギー株式会社",
    "日本テクノロジーズ株式会社",
    "日本エレクトロニクス株式会社",
    "サンライズ株式会社",
]
POSITION_NAME_MISTAKE_COMPANIES = ["バイオソリューションズ株式会社"]
ADDRESS_MISTAKE_COMPANIES = ["日本テクノロジーズ株式会社"]


class Inspector(BaseInspector):
    def inspect(self, model: VirtualCardModel) -> InspectedVirtualCardModel:
        result = InspectedVirtualCardModel(**model.dict())

        entry = model.entry

        # full_nameに間違えやすい文字が含まれている場合、インスペクタに回す
        if self._contains_mistake_chars(entry.full_name):
            result.inspect(EntryItems.full_name)

        # full_nameに間違った値が含まれている可能性のある会社の名刺について、インスペクタに回す
        if self._is_mistake_company(entry.company_name, FULL_NAME_MISTAKE_COMPANIES):
            result.inspect(EntryItems.full_name)

        # company_nameに間違った値が含まれている可能性のある会社の名刺について、インスペクタに回す
        if self._is_mistake_company(entry.company_name, COMPANY_NAME_MISTAKE_COMPANIES):
            result.inspect(EntryItems.company_name)

        # emailに間違った値が含まれている可能性のある会社の名刺について、インスペクタに回す
        if self._is_mistake_company(entry.company_name, EMAIL_MISTAKE_COMPANIES):
            result.inspect(EntryItems.email)

        # position_nameに間違った値が含まれている可能性のある会社の名刺について、インスペクタに回す
        if self._is_mistake_company(
            entry.company_name, POSITION_NAME_MISTAKE_COMPANIES
        ):
            result.inspect(EntryItems.position_name)

        # addressに間違った値が含まれている可能性のある会社の名刺について、インスペクタに回す
        if self._is_mistake_company(entry.company_name, ADDRESS_MISTAKE_COMPANIES):
            result.inspect(EntryItems.address)

        return result

    def _contains_mistake_chars(self, full_name: str) -> bool:
        """氏名に間違えやすい文字が含まれているかチェックする"""
        return any(char in full_name for char in EASY_TO_MISTAKE_CHARACTERS)

    def _is_mistake_company(self, company_name: str, mistake_companies: list) -> bool:
        """インスペクタに回すべき会社名かチェックする"""
        return any(company in company_name for company in mistake_companies)
