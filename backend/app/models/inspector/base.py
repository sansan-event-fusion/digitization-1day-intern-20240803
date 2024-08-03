from abc import ABC, abstractmethod

from pydantic import BaseModel, Field

from app.models.entry import EntryItems
from app.models.virtual_card import VirtualCardModel


class InspectionResetRule(BaseModel):
    """
    `item`で指定された項目の値が`value`で指定された値の場合リセット対象になる
    このモデルでは検証対象の項目名と値を指定する。
    実際にどの項目に修正が必要かは`InspectionRule`モデルの`inspected_items`で指定する。

    fields:
        item: EntryItems: 検証対象の項目名
        value: str: 検証する値
    """

    item: EntryItems = Field(description="検証対象の項目名")
    value: str = Field(description="検証する値")


class InspectionRule(BaseModel):
    """
    検証ルールを定義するモデル
    `rules`で検証ルールのリストを指定する。
    `inspected_items`でリセットすべき項目名のリストを指定する。
    `rule`で指定された検証ルール全てに合致した場合、`inspected_items`で指定された項目名の値をリセットする。

    fields:
        rules: List[InspectionResetRule]: 検証ルールのリスト
        inspected_items: List[EntryItems]: リセットすべき項目名のリスト
    """

    rules: list[InspectionResetRule] = Field(
        default=[], description="検証ルールのリスト"
    )
    inspected_items: list[EntryItems] = Field(
        default=[], description="修正が必要な項目名のリスト"
    )

# データ化結果が怪しいものを検知し，項目名を保持
class InspectionResult(BaseModel):
    """
    検証の結果を格納するモデル
    `inspected_items` で修正が必要な項目名のリストを指定する。

    fields:
        inspected_items: List[EntryItems]: 修正が必要な項目名のリスト
    """

    inspected_items: list[EntryItems] = Field(
        default=[], description="修正が必要な項目名のリスト"
    )

    @property
    def has_inspected_items(self) -> bool:
        return len(self.inspected_items) > 0

# ()継承してるやつ
class InspectedVirtualCardModel(VirtualCardModel, InspectionResult):
    def __init__(self, **data):
        super().__init__(**data)

    def inspect(self, *args: EntryItems) -> None:
        """
        検証結果を更新する。
        `reset_item`で指定された項目名を`reset_items`に追加する。

        Args:
            reset_item (EntryItems): リセットすべき項目名
        """
        for reset_item in args:
            if reset_item not in self.inspected_items:
                self.inspected_items.append(reset_item)


class BaseInspector(ABC):
    @abstractmethod
    def inspect(self, model: VirtualCardModel) -> InspectedVirtualCardModel:
        raise NotImplementedError
