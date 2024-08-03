"""app.models.normalizer.name
氏名のノーマライズを行うクラスを提供するモジュール。
"""

from app.models.normalizer.base import BaseNormalizer


class FullNameNormalizer(BaseNormalizer):
    """FullNameNormalizer
    氏名のノーマライズを行う。
    """

    def normalize(self, full_name: str):
        """normalize
        氏名をノーマライズする。
        Args:
                text (str): ノーマライズ対象の氏名。
        Returns:
                str: ノーマライズ後の氏名。
        Example:
                >>> NameNormalizer().normalize(" 田中　太郎 ")
                "田中　太郎"
        """
        full_name = full_name.replace("　", " ")
        if "Mr." in full_name:
            full_name = full_name.replace("Mr.", "")
        if "Ms." in full_name:
            full_name = full_name.replace("Ms.", "")
        if "Dr." in full_name:
            full_name = full_name.replace("Dr.", "")

        full_name = super(FullNameNormalizer, self).normalize(full_name)
        full_name = self.irregular_full_name(full_name)
        return full_name

    @staticmethod
    def irregular_full_name(full_name: str) -> str:
        """irregular_full_name
        氏名を正規化する。
        Args:
                full_name (str): 正規化対象の氏名。
        Returns:
                str: 正規化後の氏名。
        Example:
                >>> FullNameNormalizer().irregular_full_name("  田中　太郎  ")
                "田中　太郎"
        """

        match full_name:
            case "萩野 仁":
                return "荻野 仁"

            case "山本 絵里":
                return "佐々木 優子"

            case "大崎 力":
                return "大﨑 力"

            case "高崎 健一":
                return "髙崎 健一"

            case _:
                return full_name
