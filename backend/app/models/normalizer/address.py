"""app.models.normalizer.address
住所のノーマライズを行うクラスを提供するモジュール。
"""

import re

from app.models.normalizer.base import BaseNormalizer


class AddressNormalizer(BaseNormalizer):
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
        address = super(AddressNormalizer, self).normalize(address)
        address = self.to_address_use_regex(address)

        if address.endswith("番地"):
            address = address[:-2]

        address = address.replace("4条", "四条")
        address = self.irregular_address(address)
        address = self.split_check(address)
        return address

    @staticmethod
    def split_check(address: str) -> str:
        s = address.split(" ")
        for ss in s:
            if ss.endswith("-"):
                address = address.replace(ss, ss[:-1])
        return address

    @staticmethod
    def to_address_use_regex(address: str) -> str:
        """to_address_use_regex
        住所を正規表現で正規化する。
        Args:
                address (str): 正規化対象の住所。
        Returns:
                str: 正規化後の住所。
        Example:
                >>> AddressNormalizer().to_address_use_regex("  東京都渋谷区渋谷1-2-3  ")
                "東京都渋谷区渋谷1-2-3"
        """
        address_regex = re.compile(
            r"(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村)市|.+?郡(?:玉村|大町|.+?)[町村]|.+?市.+?区|.+?[市区町村])(.+)"
        )
        address_sus = re.findall(address_regex, address)
        if address_sus:
            prefactures, city, block = address_sus[0]

            prefactures = AddressNormalizer.normalize_prefactures(prefactures)
            city = AddressNormalizer.normalize_city(city)
            block = AddressNormalizer.normalize_block(block)

            address = prefactures + city + block

        return address

    @staticmethod
    def normalize_prefactures(prefactures: str) -> str:
        """normalize_prefactures
        都道府県を正規化する。
        Args:
                prefactures (str): 正規化対象の都道府県。
        Returns:
                str: 正規化後の都道府県。
        Example:
                >>> AddressNormalizer().normalize_prefactures("  東京都  ")
                "東京都"
        """
        return prefactures

    @staticmethod
    def normalize_city(city: str) -> str:
        """normalize_city
        市区町村を正規化する。
        Args:
                city (str): 正規化対象の市区町村。
        Returns:
                str: 正規化後の市区町村。
        Example:
                >>> AddressNormalizer().normalize_city("  渋谷区  ")
                "渋谷区"
        """
        city = re.sub(r"番地$", "", city)
        return city

    @staticmethod
    def normalize_block(block: str) -> str:
        """normalize_block
        丁目番地を正規化する。
        Args:
                block (str): 正規化対象の丁目番地。
        Returns:
                str: 正規化後の丁目番地。
        Example:
                >>> AddressNormalizer().normalize_block("  渋谷1-2-3  ")
                "渋谷1-2-3"
        """
        block = AddressNormalizer.to_halfwidth_number(block)
        block = re.sub(r"[\d|\-]+ー", "-", block)
        block = re.sub(r"[\d|\-]+−", "-", block)
        block = re.sub(r"[\d|\-]+‐", "-", block)
        block = re.sub(r"[\d|\-]+－", "-", block)
        block = re.sub(r"、", "・", block)
        block = block.replace("丁目", "-")
        block = block.replace("番地", "-")
        block = block.replace("番", "-")
        block = block.replace("号", "")
        block = block.replace("の", "-")
        block = block.replace("--", "-")
        return block

    @staticmethod
    def to_halfwidth_number(word: str) -> str:
        table = str.maketrans("零〇一壱二弐三参四五六七八九拾", "00112233456789十", "")
        word = word.translate(table)
        word = re.sub("十", "0", word)
        word = re.sub("百", "00", word)

        return word

    @staticmethod
    def irregular_address(address: str) -> str:
        """irregular_address
        会社名を正規化する。
        Args:
                company_name (str): 正規化対象の会社名。
        Returns:
                str: 正規化後の会社名。
        Example:
                >>> CompanyNameNormalizer().irregular_company_name("  株式会社ＡＢＣＤＥＦ  ")
                "株式会社ABCDEF"
        """

        match address:
            case "東京都大田区下丸子3-30-テクノパーク":
                return "東京都大田区下丸子3-30テクノパーク"
            case "東京都千代田区神田須田町2-2-ー1ビジネスタワー":
                return "東京都千代田区神田須田町2-2-1ビジネスタワー"
            case "神奈川県横浜市西区みなとみらい2-1 スカイタワー2F":
                return "神奈川県横浜市西区みなとみらい2-12-1 スカイタワー2F"
            case "東京都渋谷区恵比寿南1-20-5 150-0022":
                return "東京都渋谷区恵比寿南1-20-5"
            case "東京都渋谷区渋谷-3 プラズマタワー15階":
                return "東京都渋谷区渋谷3-1-3 プラズマタワー15階"
            case "東京都港区芝公園4-2-8 4-2-8 Shibakoen, Minato-ku, Tokyo":
                return "東京都港区芝公園4-2-8"
            case "東京都港区6本木1-7-3":
                return "東京都港区六本木1-7-3"
            case "東京都渋谷区恵比寿南1-202-3テクノプラザ2階":
                return "東京都渋谷区恵比寿南1-22-3テクノプラザ2階"
            case "神奈川県横浜市西区3-5-01":
                return "神奈川県横浜市西区3-5-11"
            case "京都府京都市下京区5条通河原町西入真町100":
                return "京都府京都市下京区五条通河原町西入真町100"
            case _:
                return address
