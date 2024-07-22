"""app.models.normalizer.position_name
役職名のノーマライズを行うクラスを提供するモジュール。
"""


class PositionNameNormalizer:
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
        return position_name.strip()
