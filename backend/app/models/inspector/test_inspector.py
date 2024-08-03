"""app.models.normalizer.test_inspector
インスペクターのテスト用モジュール
"""

import pytest
from app.models.entry import EntryItems, EntryModel
from app.models.inspector.hands_on_inspector import InspectorEntryPoint
from app.models.virtual_card import VirtualCardModel

inspector = InspectorEntryPoint()


def make_entry(**kwargs):
    return EntryModel(
        address=kwargs.get("address", "東京都港区"),
        full_name=kwargs.get("full_name", "Sansan太郎"),
        position_name=kwargs.get("position_name", "Digitization部"),
        email=kwargs.get("email", "test@sansan.com"),
        company_name=kwargs.get("company_name", "Sansan株式会社"),
    )


@pytest.mark.parametrize(
    ["model", "expected"],
    [
        pytest.param(
            VirtualCardModel(
                id="",
                image_path=None,
                entry=make_entry(email="test@sansan.c0m"),
                created_at="",
            ),
            [EntryItems.email],
        ),
    ],
)
def test_email_inspector(model, expected):
    result = inspector.inspect(model)
    assert result.inspected_items == expected
