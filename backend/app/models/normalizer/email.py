"""app.models.normalizer.email
メールアドレスのノーマライズを行うクラスを提供するモジュール。
"""


class EmailNormalizer:
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
        # [work] ラベルの削除
        email = email.replace("メールアドレス：", "")
        email = email.replace("Email:", "")
        email = email.replace("email:", "")

        email = email.strip()
        return email
