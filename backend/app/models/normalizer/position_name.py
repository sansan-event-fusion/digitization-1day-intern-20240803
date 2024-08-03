"""app.models.normalizer.position_name
役職名のノーマライズを行うクラスを提供するモジュール。
"""

from app.models.normalizer.base import BaseNormalizer


class PositionNameNormalizer(BaseNormalizer):
    """PositionNameNormalizer
    役職名のノーマライズを行う。
    """

    def normalize(self, position_name: str):
        """normalize
        役職名をノーマライズする。
        Args:
                position_name (str): ノーマライズ対象の役職名。
        Returns:
                str: ノーマライズ後の役職名。
        Example:
                >>> PositionNameNormalizer().normalize("  部長  ")
                "部長"
        """
        position_name = super(PositionNameNormalizer, self).normalize(position_name)
        position_name = self.irregular_position_name(position_name)
        return position_name

    @staticmethod
    def irregular_position_name(position_name: str) -> str:
        """irregular_position_name
        部署名を正規化する。
        Args:
                full_name (str): 正規化対象の氏名。
        Returns:
                str: 正規化後の氏名。
        Example:
                >>> FullNameNormalizer().irregular_full_name("  田中　太郎  ")
                "田中　太郎"
        """

        match position_name:
            case "ソーシャルエコノミクス":
                return "データサイエンス研究所 ソーシャルエコノミクス"
            case "主任":
                return "東京事務所 主任"
            case "設計部":
                return "大阪営業所 設計部"
            case "店長":
                return "青山店 店長"
            case _:
                return position_name
