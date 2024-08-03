"""app.models.normalizer.test_company_name
会社名ノーマライザーのテスト用モジュール
"""

import pytest
from app.models.normalizer.company_name import CompanyNameNormalizer

normalizer = CompanyNameNormalizer()


# "ダミー株式会社"を正しくノーマライズできることを確認する
@pytest.mark.parametrize(
    ["company_name", "expected"],
    [
        pytest.param(
            "ダミー株式会社",
            "ダミー株式会社",
        ),
        pytest.param(
            "Ｓａｎｓａｎ株式会社",
            "Sansan株式会社",
        ),
    ],
)
def test_normalize(company_name, expected):
    assert normalizer.normalize(company_name) == expected
