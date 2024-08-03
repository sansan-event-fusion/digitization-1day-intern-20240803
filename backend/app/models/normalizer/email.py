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
        email = email.lower()
        email = email.replace("email: ", "").replace(",", ".") # 上で小文字になってるからEはeに
        return email.strip()
