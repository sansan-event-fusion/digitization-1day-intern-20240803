"""app.modules.normalizer.company_name
会社名のノーマライズを行うクラスを提供するモジュール。
"""
import unicodedata
import re
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
        
        company_name = unicodedata.normalize('NFKC',company_name)

        
        # (株)を株式会社に変換
        company_name = company_name.replace('(株)', '株式会社')
        # (有)を有限会社に変換
        company_name = company_name.replace('(有)', '有限会社')
        return company_name.strip()
