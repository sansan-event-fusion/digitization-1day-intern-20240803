"""app.modules.normalizer.company_name
会社名のノーマライズを行うクラスを提供するモジュール。
"""
import unicodedata

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
        result = unicodedata.normalize('NFKC', company_name).strip()
        if "(有)" in result:
            result = self.replace_string(result,"(有)","有限会社")
        return result
    
    def replace_string(self, original_string, target, replacement):
        return original_string.replace(target, replacement)
