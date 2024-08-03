import re
import unicodedata
from typing import Callable, Optional


class BaseNormalizer:
    def normalize(
        self,
        text: str,
        normalize_funcs: Optional[list[Callable[[str], str]]] = None,
    ) -> str:
        """normalize_text
        共通の正規化処理
        Args:
                text (str): ノーマライズ対象のテキスト。
                normalize_funcs (Optional[list[Callable[[str], str]]]): ノーマライズ関数のリスト。
        Returns:
                str: ノーマライズ後のテキスト。
        """
        funcs = [
            self.split_slash,
            self.split_backet,
            self.strip,
            self.to_halfwidth,
        ]
        for func in funcs:
            text = func(text)
        return text

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
    def split_slash(word: str) -> list[str]:
        """split
        文字列を分割する
        Args:
                        word (str): 対象文字列
        Returns:
                        list[str]: 分割された文字列

        Example:
                        >>> CompanyNameNormalizer().split("株式会社テスト")
                        ["株式会社", "テスト"]
        """
        return word.split("/")[0]

    @staticmethod
    def split_backet(word: str) -> list[str]:
        """split
        文字列を分割する
        Args:
                        word (str): 対象文字列
        Returns:
                        list[str]: 分割された文字列

        Example:
                        >>> CompanyNameNormalizer().split("株式会社テスト")
                        ["株式会社", "テスト"]
        """
        return word.split("(")[0]

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

    def __call__(self, text: str) -> str:
        return self.normalize(text)
