import re
from app.models.entry import EntryModel
from app.models.normalizer.common import CommonNormalizer

"""app.models.normalizer.name
氏名のノーマライズを行うクラスを提供するモジュール。
"""

PREFIX_EXPRESSIONS = ["Mr.", "Ms.", "Dr.", "Prof."]


class FullNameNormalizer(CommonNormalizer):
    """FullNameNormalizer
    氏名のノーマライズを行う。
    """

    def normalize(self, entry: EntryModel) -> str:
        """氏名をノーマライズする。

        Args:
            entry (EntryModel): ノーマライズ対象のエントリ。

        Returns:
            str: ノーマライズ後の氏名。

        Example:
            >>> FullNameNormalizer().normalize(EntryModel(full_name=" 田中　太郎 "))
            "田中　太郎"
        """

        # 括弧書きをトリムする
        full_name = self._trim_bracket(entry.full_name)

        # 敬称をトリムする
        full_name = self._trim_prefix(full_name)

        # 言語に合わせて氏名をトリムする
        full_name = self._trim_by_language(full_name, entry.language)

        return full_name.strip()

    def _trim_prefix(self, full_name: str) -> str:
        """氏名から敬称をトリムする。

        Args:
            full_name (str): 敬称をトリムする氏名。

        Returns:
            str: 敬称をトリムした氏名。

        Example:
            >>> FullNameNormalizer()._trim_prefix("Mr. 田中　太郎")
            "田中　太郎"
        """
        for prefix in PREFIX_EXPRESSIONS:
            full_name = full_name.replace(prefix, "")
        return full_name

    def _trim_by_language(self, full_name: str, language: str) -> str:
        """日英併記の場合、言語に合わせて氏名をトリムする。

        Args:
            full_name (str): トリムする氏名。
            language (str): 言語コード（jaまたはen）。

        Returns:
            str: トリム後の氏名。
        """
        if language == "ja":
            return self._extract_japanese_name(full_name)
        elif language == "en":
            return self._extract_english_name(full_name)

        return full_name

    def _extract_japanese_name(self, full_name: str) -> str:
        """氏名から日本語の部分を抽出する。

        Args:
            full_name (str): 抽出対象の氏名。

        Returns:
            str: 日本語の部分のみを含む氏名。
        """
        japanese_name_words = re.findall(r"[ぁ-んァ-ヶｱ-ﾝﾞﾟ一-龠々]+", full_name)
        return " ".join(japanese_name_words)

    def _extract_english_name(self, full_name: str) -> str:
        """氏名から英語の部分を抽出する。

        Args:
            full_name (str): 抽出対象の氏名。

        Returns:
            str: 英語の部分のみを含む氏名。
        """
        english_name_words = re.findall(r"[a-zA-Z]+", full_name)
        return " ".join(english_name_words)
