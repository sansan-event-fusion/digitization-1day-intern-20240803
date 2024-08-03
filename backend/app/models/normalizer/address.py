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
        fixed_address = list(address)
        make_hyphon = ["丁目", "番", "地","号"]
        for check in make_hyphon:
            for index, char  in enumerate(fixed_address):
                if check == char:
                    fixed_address[index] = "-"
                    if fixed_address[index-1] == "-":
                        fixed_address.pop(index)
            return "".join(fixed_address)
        return address.strip()
