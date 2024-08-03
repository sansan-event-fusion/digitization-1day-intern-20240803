from typing import Callable, Optional

from app.models.entry import EntryModel
from app.models.normalizer.address import AddressNormalizer
from app.models.normalizer.company_name import CompanyNameNormalizer
from app.models.normalizer.email import EmailNormalizer
from app.models.normalizer.full_name import FullNameNormalizer
from app.models.normalizer.position_name import PositionNameNormalizer


class NormalizerEntryPoint:
    def __init__(
        self,
        full_name_normalizer: Optional[Callable[[str], str]] = None,
        email_normalizer: Optional[Callable[[str], str]] = None,
        company_name_normalizer: Optional[Callable[[str], str]] = None,
        position_name_normalizer: Optional[Callable[[str], str]] = None,
        address_normalizer: Optional[Callable[[str], str]] = None,
    ):
        self.full_name_normalizer = full_name_normalizer or FullNameNormalizer()
        self.email_normalizer = email_normalizer or EmailNormalizer()
        self.company_name_normalizer = (
            company_name_normalizer or CompanyNameNormalizer()
        )
        self.position_name_normalizer = (
            position_name_normalizer or PositionNameNormalizer()
        )
        self.address_normalizer = address_normalizer or AddressNormalizer()

    def normalize_all(self, entry: EntryModel) -> EntryModel:
        """normalize
        入力をノーマライズする。
        Args:
                entry (EntryModel): ノーマライズ対象の入力。
        Returns:
                EntryModel: ノーマライズ後の入力。
        Raises:
                ValueError: entry が EntryModel でない場合。
        Example:
                >>> EntryNormalizer().normalize(EntryModel())
                EntryModel()
        """
        if not isinstance(entry, EntryModel):
            raise ValueError("入力が不正です")
        entry.full_name = self.full_name_normalizer(entry.full_name)
        entry.email = self.email_normalizer(entry.email)
        entry.company_name = self.company_name_normalizer(entry.company_name)
        entry.position_name = self.position_name_normalizer(entry.position_name)
        entry.address = self.address_normalizer(entry.address)
        return entry
