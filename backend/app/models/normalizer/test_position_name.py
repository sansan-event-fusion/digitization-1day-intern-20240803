"""app.models.normalizer.test_position_name
部署名ノーマライザーのテスト用モジュール
"""

import pytest
from app.models.normalizer.position_name import PositionNameNormalizer

normalizer = PositionNameNormalizer()


# 部署名を正しくノーマライズできることを確認する
@pytest.mark.parametrize(
    ["position_name", "expected"],
    [
        pytest.param(
            "Digitization部",
            "Digitization部",
        ),
    ],
)
def test_normalize(position_name, expected):
    assert normalizer.normalize(position_name) == expected
