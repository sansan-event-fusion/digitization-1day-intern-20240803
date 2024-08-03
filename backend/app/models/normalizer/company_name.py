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
        import unicodedata
        for char in range(len(company_name)):
            if unicodedata.east_asian_width(company_name[char] )== 'F':
                normarized = unicodedata.normalize('NFKC', company_name)
                return normarized
                break

            
        return company_name.strip()
