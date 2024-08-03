from app.models.entry import EntryModel
import re
from typing import List


class CommonNormalizer:
    def normalize(self, entry: EntryModel) -> str:
        raise NotImplementedError("normalize メソッドが実装されていません")

    def _trim_bracket(self, text: str):
        """
        括弧書きをトリムする。
        Args:
                text (str): 括弧書きをトリムする文字列。
        Returns:
                str: 括弧書きをトリムした文字列。
        Example:
                >>> CommonNormalizer().bracket_trim("（田中　太郎）")
                ""
        """

        return re.sub(r"[（(].+[）)]", "", text)

    def _trim_label(self, text: str, label_expressions: List[str]):
        """
        ラベルをトリムする。
        Args:
                text (str): ラベルをトリムするテキスト。
        Returns:
                str: ラベルをトリムしたテキスト。
        Example:
                >>> CommonNormalizer().label_trim("  メールアドレス： info@sample.com ")
                "info@sample.com"
        """
        for expression in label_expressions:
            text = text.replace(f"{expression}:", "")
            text = text.replace(expression, "")

        return text
