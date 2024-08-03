from app.models.entry import EntryModel
import re
from app.models.normalizer.common import CommonNormalizer

SHORT_POSITION_NAMES = {
    "CEO": "最高経営責任者",
    "CTO": "最高技術責任者",
    "CFO": "最高財務責任者",
    "COO": "最高執行責任者",
    "CIO": "最高情報責任者",
    "CMO": "最高マーケティング責任者",
    "Manager": "マネージャー",
}

NECESSARY_ENGLISH_POSITION_NAMES = {
    "アドバンスドヘルスケア株式会社": ["Digital Health Innovation Unit"],
    "メディアクリエイト株式会社": ["Content Strategy"],
    "テクノロジーソリューションズ株式会社": ["Group Manager"],
}


class PositionNameNormalizer(CommonNormalizer):
    """PositionNameNormalizer
    役職名のノーマライズを行う。
    """

    def normalize(self, entry: EntryModel) -> str:
        """役職名をノーマライズする。

        Args:
            entry (EntryModel): ノーマライズ対象のエントリー。

        Returns:
            str: ノーマライズ後の役職名。

        Example:
            >>> PositionNameNormalizer().normalize(EntryModel(position_name="  部長  ", language="ja"))
            "部長"
        """
        position_name = entry.position_name

        # 会社ごとに残したい役職名をマスキングする
        if entry.company_name in NECESSARY_ENGLISH_POSITION_NAMES:
            position_name = self._mask_necessary_positions(
                position_name, entry.company_name
            )

        position_name_words = position_name.split()

        # 必要な単語だけを残す
        necessary_position_name_words = [
            word for word in position_name_words if self._is_necessary(word, entry)
        ]

        position_name = " ".join(necessary_position_name_words).strip()

        # 会社ごとに残したい役職名を元に戻す
        if entry.company_name in NECESSARY_ENGLISH_POSITION_NAMES:
            position_name = self._unmask_necessary_positions(
                position_name, entry.company_name
            )

        return position_name

    def _mask_necessary_positions(self, position_name: str, company_name: str) -> str:
        """特定の会社で残したい役職名をマスキングする。

        Args:
            position_name (str): 役職名。
            company_name (str): 会社名。

        Returns:
            str: マスキング後の役職名。
        """
        words = NECESSARY_ENGLISH_POSITION_NAMES[company_name]
        for index, word in enumerate(words):
            position_name = re.sub(word, f"[{company_name}-{index}]", position_name)
        return position_name

    def _unmask_necessary_positions(self, position_name: str, company_name: str) -> str:
        """マスキングした役職名を元に戻す。

        Args:
            position_name (str): 役職名。
            company_name (str): 会社名。

        Returns:
            str: 元に戻した役職名。
        """
        words = NECESSARY_ENGLISH_POSITION_NAMES[company_name]
        for index, word in enumerate(words):
            position_name = re.sub(f"\[{company_name}-{index}\]", word, position_name)
        return position_name

    def _is_necessary(self, word: str, entry: EntryModel) -> bool:
        """指定された単語が必要かどうかを判定する。

        Args:
            word (str): 判定対象の単語。
            entry (EntryModel): エントリーモデル。

        Returns:
            bool: 必要である場合はTrue、それ以外の場合はFalse。
        """
        if entry.language == "ja":
            return self._is_necessary_ja(word, entry)
        return self._is_necessary_en(word)

    def _is_necessary_ja(self, word: str, entry: EntryModel) -> bool:
        """日本語の役職名が必要かどうかを判定する。

        Args:
            word (str): 判定対象の単語。
            entry (EntryModel): エントリーモデル。

        Returns:
            bool: 必要である場合はTrue、それ以外の場合はFalse。
        """
        if word in SHORT_POSITION_NAMES and any(
            v in entry.position_name for v in SHORT_POSITION_NAMES.values()
        ):
            return False
        if word in SHORT_POSITION_NAMES:
            return True
        return self._detect_language(word) == "ja"

    def _is_necessary_en(self, word: str) -> bool:
        """英語の役職名が必要かどうかを判定する。

        Args:
            word (str): 判定対象の単語。

        Returns:
            bool: 必要である場合はTrue、それ以外の場合はFalse。
        """
        return self._detect_language(word) == "en"

    def _detect_language(self, word: str) -> str:
        """単語の言語を判定する。

        Args:
            word (str): 判定対象の単語。

        Returns:
            str: 言語 ("ja" もしくは "en")。
        """
        if re.search(r"[ぁ-んァ-ヶｱ-ﾝﾞﾟ一-龠]+", word):
            return "ja"
        return "en"
