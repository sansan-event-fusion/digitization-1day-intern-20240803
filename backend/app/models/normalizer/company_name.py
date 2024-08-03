"""app.modules.normalizer.company_name
会社名のノーマライズを行うクラスを提供するモジュール。
"""

import re

from app.models.normalizer.base import BaseNormalizer


class CompanyNameNormalizer(BaseNormalizer):
    """CompanyNameNormalizer
    会社名の正規化を行う。
    """

    def normalize(
        self,
        company_name: str,
    ) -> str:
        """normalize
        会社名を正規化する。
        Args:
                company_name (str): 正規化対象の会社名。
        Returns:
                str: 正規化後の会社名。
        Example:
                >>> CompanyNameNormalizer().normalize("  株式会社ＡＢＣＤＥＦ  ")
                "株式会社ABCDEF"
        """

        company_name = super(CompanyNameNormalizer, self).normalize(company_name)
        company_name = self.to_company_name_use_regex(company_name)
        company_name = self.irregular_company_name(company_name)
        return company_name

    @staticmethod
    def to_company_name_use_regex(company_name: str) -> str:
        """to_company_name_use_regex
        会社名を正規表現で正規化する。
        Args:
                company_name (str): 正規化対象の会社名。
        Returns:
                str: 正規化後の会社名。
        Example:
                >>> CompanyNameNormalizer().to_company_name_use_regex("  株式会社ＡＢＣＤＥＦ  ")
                "株式会社ABCDEF"
        """
        company_name = company_name.replace("（", "(").replace("）", ")")
        company_name = company_name.replace("(株)", "株式会社")
        company_name = company_name.replace("(有)", "有限会社")
        company_name = company_name.replace("(合)", "合同会社")
        company_name = company_name.replace("㈱", "株式会社")
        company_name = company_name.replace("㈲", "有限会社")
        return company_name

    @staticmethod
    def irregular_company_name(company_name: str) -> str:
        """irregular_company_name
        会社名を正規化する。
        Args:
                company_name (str): 正規化対象の会社名。
        Returns:
                str: 正規化後の会社名。
        Example:
                >>> CompanyNameNormalizer().irregular_company_name("  株式会社ＡＢＣＤＥＦ  ")
                "株式会社ABCDEF"
        """

        match company_name:
            case "ブリジストン株式会社":
                return "ブリヂストン株式会社"
            case "キャノン株式会社":
                return "キヤノン株式会社"
            
            case _:
                return company_name
