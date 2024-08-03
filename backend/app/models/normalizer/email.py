"""app.models.normalizer.email
メールアドレスのノーマライズを行うクラスを提供するモジュール。
"""

import re

from app.models.normalizer.base import BaseNormalizer


class EmailNormalizer(BaseNormalizer):
    """EmailNormalizer
    メールアドレスのノーマライズを行う。
    """

    def normalize(self, email: str):
        """normalize
        メールアドレスをノーマライズする。
        Args:
                email (str): ノーマライズ対象のメールアドレス。
        Returns:
                str: ノーマライズ後のメールアドレス。
        Example:
                >>> EmailNormalizer().normalize(" expmple@example.com ")
                "example@example.com"
        """
        email = super(EmailNormalizer, self).normalize(email)
        table = str.maketrans(
            {
                "＠": "@",
                "．": ".",
                " ": "",
                ",": ".",
                "、": ".",
                "。": ".",
            }
        )
        email = email.translate(table)
        if email.startswith("Email:"):
            email = email.replace("Email:", "")
        valid = re.findall(r"^[A-Z0-9+_.-]+@[A-Z0-9.-]+$", email)
        if valid:
            email = valid[0]
        return email
