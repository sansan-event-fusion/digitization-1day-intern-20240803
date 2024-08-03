"""app.models.normalizer.test_email
メールアドレスノーマライザーのテスト用モジュール
"""

import pytest
from app.models.normalizer.email import EmailNormalizer

normalizer = EmailNormalizer()


# メールアドレスを正しくノーマライズできることを確認する
@pytest.mark.parametrize(
    ["email", "expected"],
    [
        pytest.param(
            "test@sansan.com",
            "test@sansan.com",
        ),
    ],
)
def test_normalize(email, expected):
    assert normalizer.normalize(email) == expected
