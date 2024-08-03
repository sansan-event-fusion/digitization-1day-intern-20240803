from app.models.entry import EntryModel
from app.models.normalizer.common import CommonNormalizer
from app.models.normalizer.address import AddressNormalizer
from app.models.normalizer.company_name import CompanyNameNormalizer
from app.models.normalizer.email import EmailNormalizer
from app.models.normalizer.full_name import FullNameNormalizer
from app.models.normalizer.position_name import PositionNameNormalizer


class EntryNormalizer:
    def normalize(self, entry: EntryModel):
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
        for entry_item in [entry.full_name, entry.email, entry.company_name, entry.company_name, entry.address]:
                entry_item = CommonNormalizer().normalize(entry_item)
        entry.full_name = FullNameNormalizer().normalize(entry.full_name)
        entry.email = EmailNormalizer().normalize(entry.email)
        entry.company_name = CompanyNameNormalizer().normalize(entry.company_name)
        entry.position_name = PositionNameNormalizer().normalize(entry.position_name)
        entry.address = AddressNormalizer().normalize(entry.address)
        return entry
