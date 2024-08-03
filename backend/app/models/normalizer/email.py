from app.models.normalizer.common import CommonNormalizer
from app.models.entry import EntryModel

"""app.models.normalizer.email
メールアドレスのノーマライズを行うクラスを提供するモジュール。
"""

LABEL_EXPRESSIONS = [
    "メールアドレス",
    "Email",
    "email",
]


class EmailNormalizer(CommonNormalizer):
    """EmailNormalizer
    メールアドレスのノーマライズを行う。
    """

    def normalize(self, entry: EntryModel) -> str:
        """メールアドレスをノーマライズする。

        Args:
            entry (EntryModel): エントリーモデル。

        Returns:
            str: ノーマライズ後のメールアドレス。

        Example:
            >>> EmailNormalizer().normalize(EntryModel(email=" expmple@example.com "))
            "example@example.com"
        """

        # メールアドレスのラベルをトリムする
        email = self._trim_label(entry.email, LABEL_EXPRESSIONS)

        # カンマをドットに置き換える
        email = self._replace_comma(email)

        return email.strip()

    def _replace_comma(self, text: str) -> str:
        """カンマをドットに置き換える。

        Args:
            text (str): カンマを置換するテキスト。

        Returns:
            str: カンマを置換したテキスト。

        Example:
            >>> EmailNormalizer()._replace_comma("example,example.com")
            "example.example.com"
        """
        return text.replace(",", ".")

    def _trim_label(self, text: str, label_expressions: list[str]) -> str:
        """ラベルをトリムする。

        Args:
            text (str): ラベルをトリムするテキスト。
            label_expressions (list[str]): トリムするラベルのリスト。

        Returns:
            str: ラベルをトリムしたテキスト。

        Example:
            >>> EmailNormalizer()._trim_label("  メールアドレス： info@sample.com ", ["メールアドレス"])
            "info@sample.com"
        """
        for expression in label_expressions:
            text = text.replace(f"{expression}:", "")
            text = text.replace(expression, "")
        return text.strip()
