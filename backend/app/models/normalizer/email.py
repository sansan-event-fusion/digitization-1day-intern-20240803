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
        print(email)
        email = email.replace("c0m", "com")
        return email
