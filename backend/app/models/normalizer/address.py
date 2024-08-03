"""app.models.normalizer.address
住所のノーマライズを行うクラスを提供するモジュール。
"""
import re
kanji_to_num = {'一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9', '十': '10'}
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

        # Address:は削除
        address = address.replace('Address:', '')

        # 、を・に変換
        address = address.replace('、', '・')

        # 住所を1-1-1の形にする
        # 丁目、番地、号を-に変換
        address = address.replace('丁目', '-')
        address = address.replace('番地', '-')
        address = address.replace('番', '-')
        address = address.replace('号', '')

        # かっこで囲まれたところは削除
        address = re.sub(r'\(.*\)', '', address)
        
        # 漢数字をアラビア数字に変換

        


        return address.strip()
