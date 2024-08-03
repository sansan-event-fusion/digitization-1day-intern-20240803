import re
from app.models.normalizer.common import CommonNormalizer
from app.models.entry import EntryModel

"""app.modules.normalizer.company_name
会社名のノーマライズを行うクラスを提供するモジュール。
"""

ABBREVIATION_COMPANY_MAP = {
    "（株）": "株式会社",
    "（有）": "有限会社",
}

POSITION_NAME_SUFFIX = ["部", "店", "営業所", "支店", "事業所"]
COMPANIES_WITH_POSITION_NAME = {"世界総研": "データサイエンス研究所"}


class CompanyNameNormalizer(CommonNormalizer):
    """CompanyNameNormalizer
    会社名のノーマライズを行う。
    """

    def normalize(self, entry: EntryModel) -> str:
        """会社名をノーマライズする。

        Args:
            entry (EntryModel): エントリーモデル。

        Returns:
            str: ノーマライズ後の会社名。

        Example:
            >>> CompanyNameNormalizer().normalize(EntryModel(company_name="  株式会社テスト  "))
            "株式会社テスト"
        """

        # 会社名の略称を全称に変換する
        company_name = self._expand_abbreviation_company(entry.company_name)

        # 括弧書きをトリムする
        company_name = self._trim_bracket(company_name)

        # 会社名に含まれる部署名を取り出し、移動する
        company_name = self._move_position_name(company_name, entry)

        return company_name.strip()

    def _expand_abbreviation_company(self, text: str) -> str:
        """略称の会社名を全称に変換する。

        Args:
            text (str): 変換対象のテキスト。

        Returns:
            str: 変換後のテキスト。

        Example:
            >>> CompanyNameNormalizer().expand_abbreviation_company("（株）テスト")
            "株式会社テスト"
        """
        expanded_text = text

        for abbreviation, company in ABBREVIATION_COMPANY_MAP.items():
            expanded_text = expanded_text.replace(abbreviation, company)
        return expanded_text

    def _move_position_name(self, company_name: str, entry: EntryModel) -> str:
        """会社名から部署名を取り出し、部署名を移動する。

        Args:
            company_name (str): ノーマライズ対象の会社名。
            entry (EntryModel): エントリーモデル。

        Returns:
            str: 部署名を移動した後の会社名。
        """
        company_name_words = company_name.split()
        position_name_suffix_pattern = rf".*({'|'.join(POSITION_NAME_SUFFIX)})"

        for index, word in enumerate(company_name_words):
            if re.match(position_name_suffix_pattern, word):
                # マッチした単語以降を部署名として取り出す
                position_name = " ".join(company_name_words[index:])
                entry.position_name = f"{position_name} {entry.position_name}".strip()
                company_name_words = company_name_words[:index]
                break

        # 特定の会社名に対して部署名を移動させる
        for company, position_name in COMPANIES_WITH_POSITION_NAME.items():
            if company in company_name:
                entry.position_name = f"{position_name} {entry.position_name}".strip()
                company_name_words.remove(position_name)
                break

        return " ".join(company_name_words)
