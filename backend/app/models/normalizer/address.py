import re
from app.models.normalizer.common import CommonNormalizer
from app.models.entry import EntryModel
from app.utils.kanji_number_converter import KanjiNumberConverter

STREETS_WITH_KANJI_NUMBER = ["六本木", "西三坊", "南一条", "四条", "千代田", "五条"]
STREET_EXPRESSIONS = ["丁目", "番地", "番", "号", "の"]
LABEL_EXPRESSIONS = ["住所", "Address", "address"]


class AddressNormalizer(CommonNormalizer):
    """AddressNormalizer
    住所のノーマライズを行う。
    """

    def normalize(self, entry: EntryModel):
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

        address = entry.address

        address = self._trim_bracket(address)
        address = self._trim_label(address, LABEL_EXPRESSIONS)
        address = self._trim_post_code(address)
        address = self._normalize_street(address)

        address = re.sub(r"\s+", " ", address)

        return address.strip()

    def _trim_post_code(self, text):
        """
        郵便番号をトリムする
        """
        return re.sub(r"\d{3}-\d{4}", "", text)

    def _normalize_street(self, address: str):
        """normalize_street
        住所の街路番号をノーマライズする。
        Args:
                street (str): ノーマライズ対象の街路番号。
        Returns:
                str: ノーマライズ後の街路番号。
        Example:
                >>> AddressNormalizer().normalize_street("  渋谷1-2-3  ")
                "渋谷1-2-3"
        """

        normalized = address

        # 漢数字の入った地名をマスキングする
        normalized = self._mask_kanji_streets(normalized)

        # 漢数字をアラビア数字に変換する
        normalized = KanjiNumberConverter.kanji_to_arabic(normalized)

        # 漢数字の地名を元に戻す
        normalized = self._unmask_kanji_streets(normalized)

        # 数字に挟まれている丁目、番地、番、号をハイフンに変換する
        normalized = re.sub(
            rf"(?<=\d)({'|'.join(STREET_EXPRESSIONS)})(?=\d)", "-", normalized
        )
        # 丁目、番地、番、号を削除する
        normalized = re.sub(rf"({'|'.join(STREET_EXPRESSIONS)})", "", normalized)

        # 数字に挟まれている長音をハイフンに変換する
        normalized = re.sub(r"(?<=\d)ー(?=\d)", "-", normalized)

        # 句読点を中点に変換する
        normalized = self._replace_comma(normalized)

        # スペースをトリムする
        normalized = re.sub(r"\s+", " ", normalized)

        return normalized.strip()

    def _mask_kanji_streets(self, text: str) -> str:
        """漢数字の入った地名をマスキングする。

        Args:
            text (str): 入力テキスト。

        Returns:
            str: マスキング後のテキスト。
        """
        for index, street in enumerate(STREETS_WITH_KANJI_NUMBER):
            text = re.sub(street, f"[{index}]", text)
        return text

    def _unmask_kanji_streets(self, text: str) -> str:
        """マスキングされた漢数字の地名を元に戻す。

        Args:
            text (str): 入力テキスト。

        Returns:
            str: 元に戻した後のテキスト。
        """
        for index, street in enumerate(STREETS_WITH_KANJI_NUMBER):
            text = re.sub(rf"\[{index}\]", street, text)
        return text

    def _replace_comma(self, text):
        """
        句読点を中点に変換する
        """
        return text.replace("、", "・")
