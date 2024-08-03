"""app.modules.normalizer.company_name
会社名のノーマライズを行うクラスを提供するモジュール。
"""

import unicodedata
from typing import Callable, Optional


class CompanyNameNormalizer:
    """CompanyNameNormalizer
    会社名の正規化を行う。
    """

    def normalize(
        self,
        company_name: str,
        normalize_funcs: Optional[list[Callable[[str], str]]] = None,
    ) -> str:
        """normalize
        会社名を正規化する。
        Args:
                company_name (str): 正規化対象の会社名。
                normalize_funcs (Optional[list[Callable[[str], str]]], optional): 関数のリスト。Noneの場合は全部実行する。 Defaults to None.
        Returns:
                str: 正規化後の会社名。
        Example:
                >>> CompanyNameNormalizer().normalize("  株式会社ＡＢＣＤＥＦ  ")
                "株式会社ABCDEF"
        """
        normalize_funcs = normalize_funcs or [
            self.strip,
            self.to_halfwidth,
        ]

        for func in normalize_funcs:
            company_name = func(company_name)
        return company_name

    @staticmethod
    def strip(word: str) -> str:
        """strip
        文字列の前後の空白を削除する
        Args:
                        word (str): 対象文字列
        Returns:
                        str: 前後の空白が削除された文字列

        Example:
                        >>> CompanyNameNormalizer().strip("  株式会社テスト  ")
                        "株式会社テスト"
        """
        return word.strip()

    @staticmethod
    def to_halfwidth(word: str) -> str:
        """to_halfwidth
        全角英数記号を半角にする
        Args:
                        word (str): 対象文字列
        Returns:
                        str: 半角になった文字列

        Example:
                        >>> CompanyNameNormalizer().to_halfwidth("株式会社ＡＢＣＤＥＦＧ")
                        "ABCDEFG"
        """
        return unicodedata.normalize("NFKC", word)
