"""app.modules.normalizer.company_name
会社名のノーマライズを行うクラスを提供するモジュール。
"""


class CompanyNameNormalizer:
    """CompanyNameNormalizer
    会社名のノーマライズを行う。
    """

    def normalize(self, company_name: str):
        """normalize
        会社名をノーマライズする。
        Args:
                company_name (str): ノーマライズ対象の会社名。
        Returns:
                str: ノーマライズ後の会社名。
        Example:
                >>> CompanyNameNormalizer().normalize("  株式会社テスト  ")
                "株式会社テスト"
        """
        # return company_name.strip()
        # 左右の空白を除去
        company_name = company_name.strip()

        # 全角英数字を半角英数字に揃える
        # 謎のライブラリに丸投げだけどまあいいでしょう．
        # ref: https://docs.python.org/ja/3/library/unicodedata.html#unicodedata.normalize
        import unicodedata
        company_name = unicodedata.normalize("NFKC", company_name)

        return company_name
