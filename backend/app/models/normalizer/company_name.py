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
        # [hands-on] 全角英数字を半角英数字に揃える
        # 謎のライブラリに丸投げだけどまあいいでしょう．
        # ref: https://docs.python.org/ja/3/library/unicodedata.html#unicodedata.normalize
        import unicodedata
        company_name = unicodedata.normalize("NFKC", company_name)

        # [work] 省略表記を展開
        company_name = company_name.replace("（株）", "株式会社")
        company_name = company_name.replace("（有）", "有限会社")

        # [work] 正しい名前
        company_name = company_name.replace("キャノン", "キヤノン")
        company_name = company_name.replace("ブリジストン", "ブリヂストン")

        # 左右の空白を除去
        company_name = company_name.strip()
        return company_name
