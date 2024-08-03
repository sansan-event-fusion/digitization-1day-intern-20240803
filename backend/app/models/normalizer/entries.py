from app.models.entry import EntryModel
from app.models.normalizer.address import AddressNormalizer
from app.models.normalizer.company_name import CompanyNameNormalizer
from app.models.normalizer.email import EmailNormalizer
from app.models.normalizer.full_name import FullNameNormalizer
from app.models.normalizer.position_name import PositionNameNormalizer


class EntryNormalizer:
    def __init__(self):
        self.normalizers = {
            "full_name": FullNameNormalizer(),
            "email": EmailNormalizer(),
            "company_name": CompanyNameNormalizer(),
            "position_name": PositionNameNormalizer(),
            "address": AddressNormalizer(),
        }

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

        for item_type, normalizer in self.normalizers.items():
            setattr(entry, item_type, normalizer.normalize(entry))

        return entry
