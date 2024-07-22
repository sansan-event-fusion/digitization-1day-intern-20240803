"""app.models.normalizer.test_address
住所ノーマライザーのテスト用モジュール
"""

import pytest

from app.models.normalizer.address import AddressNormalizer

normalizer = AddressNormalizer()


# 都道府県を正しくノーマライズできることを確認する
@pytest.mark.parametrize(
    ["address", "expected"],
    [
        pytest.param(
            "東京都渋谷区神宮前5-52-2青山オーバルビル13F",
            "東京都渋谷区神宮前5-52-2青山オーバルビル13F",
        ),
    ],
)
def test_normalize(address, expected) -> None:
    assert normalizer.normalize(address) == expected
