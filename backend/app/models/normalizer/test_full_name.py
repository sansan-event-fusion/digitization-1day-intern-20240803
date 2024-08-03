"""app.models.normalizer.test_full_name
氏名のノーマライザーのテスト用モジュール
"""

import pytest
from app.models.normalizer.full_name import FullNameNormalizer

normalizer = FullNameNormalizer()


# "ダミー太郎"を正しくノーマライズできることを確認する
@pytest.mark.parametrize(
    ["full_name", "expected"],
    [
        pytest.param(
            "Sansan太郎",
            "Sansan太郎",
        ),
    ],
)
def test_normalize(full_name, expected):
    assert normalizer.normalize(full_name) == expected
