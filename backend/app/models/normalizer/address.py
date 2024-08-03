"""app.models.normalizer.address
住所のノーマライズを行うクラスを提供するモジュール。
"""


class AddressNormalizer:
    """AddressNormalizer
    住所のノーマライズを行う。
    """

    def normalize(self, address: str):
        """normalize
        住所をノーマライズする。
        Args:
                address (str): ノーマライズ対象の住所。
        Returns:
                str: ノーマライズ後の住所。
        Example:
                >>> AddressNormalizer().normalize("  東京都渋谷区渋谷1-2-3  ")
                "東京都渋谷区渋谷1-2-3"
        """
        # [work] ラベルの削除
        address = address.replace("住所：", "")
        address = address.replace("Address:", "")
        address = address.replace("address:", "")

        address = address.strip()
        return address
