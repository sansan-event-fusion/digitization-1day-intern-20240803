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
        # Email:を削除
        email = email.replace('Email:', '')

        # ,を.に変換
        email = email.replace(',', '.')




        return email.strip()
