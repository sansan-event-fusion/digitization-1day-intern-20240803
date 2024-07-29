import difflib
from app.repositories.delivered import DeliveredRepository
from app.repositories.correct import CorrectRepository
from app.repositories.inspector import InspectorRepository
from app.models.virtual_card import VirtualCardModel
from app.models.entry import EntryModel
from app.models.inspector.base import InspectedVirtualCardModel
from typing import List, TypeGuard
from pydantic import BaseModel
import os
import contextlib
import csv


STATIC_DIR = "static"

COLOR = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "reset": "\033[0m",
}


class CollationDiff(BaseModel):
    item_type: str
    diff: List[str]


class CollationResult(BaseModel):
    card_id: str
    diffs: List[CollationDiff]
    inspected_items: List[str]

    @property
    def correct_count(self) -> int:
        return len(EntryModel.__annotations__.keys()) - len(self.failed_item_types)

    @property
    def automated_count(self) -> int:
        return len(EntryModel.__annotations__.keys()) - len(self.inspected_items)

    def log_result(self):
        print("------------------------------------------------------")
        print(f"ID: {self.card_id} {self.summary_text()}")
        print("------------------------------------------------------")

        for item_type in EntryModel.__annotations__.keys():
            if item_type in self.inspected_items:
                continue

            if item_type not in self.failed_item_types:
                continue

            collation_diff = self.get_diff(item_type)
            diff = collation_diff.diff
            print(f"{item_type}:")
            for line in diff:
                match line[:2]:
                    case "- ":
                        print(COLOR["red"] + line + COLOR["reset"])
                    case "+ ":
                        print(COLOR["green"] + line + COLOR["reset"])
                    case "  ", "? ":
                        pass

        print()

    @property
    def failed_item_types(self) -> List[str]:
        return [diff.item_type for diff in self.diffs]

    def item_type_result(self, item_type: str) -> str:
        if item_type in self.inspected_items:
            return "inspected"

        if item_type not in self.failed_item_types:
            return "correct"

        return "failed"

    def summary_text(self):
        text = ""
        for item_type in EntryModel.__annotations__.keys():
            c = ""
            match self.item_type_result(item_type):
                case "inspected":
                    c = COLOR["yellow"] + " \U0001F50D" + COLOR["reset"]
                case "correct":
                    c = COLOR["green"] + " \u2713" + COLOR["reset"]
                case "failed":
                    c = COLOR["red"] + " \u2717" + COLOR["reset"]
            text += c

        return text

    def get_diff(self, item_type: str) -> CollationDiff:
        for diff in self.diffs:
            if diff.item_type == item_type:
                return diff


class CollationResultList(BaseModel):
    results: List[CollationResult]

    @property
    def correct_count(self) -> int:
        return sum([result.correct_count for result in self.results])

    @property
    def total_count(self) -> int:
        return len(self.results) * len(EntryModel.__annotations__.keys())

    @property
    def automated_count(self) -> int:
        return sum([result.automated_count for result in self.results])

    @property
    def accuracy(self) -> float:
        return self.correct_count / self.total_count * 100

    @property
    def automated_rate(self) -> float:
        return self.automated_count / self.total_count * 100

    def log_metrics(self):
        print("------------------------------------------------------")
        print("Metrics")
        print("------------------------------------------------------")

        print(f"精度: {self.accuracy}% ({self.correct_count}/{self.total_count})")
        print(
            f"自動化率: {self.automated_rate}% ({self.automated_count}/{self.total_count})"
        )

        print()

    def append(self, result: CollationResult):
        self.results.append(result)


class TestCommand:
    def __init__(self):
        self.delivered_repository = DeliveredRepository()
        self.correct_repository = CorrectRepository()
        self.inspector_repository = InspectorRepository()

    def execute(self, id=None):
        if id is not None:
            self.run_single_test(id)
        else:
            self.run_all_tests()

    def run_single_test(self, id):
        target_card = self._get_target_card(id)
        correct_card = self._get_correct_card(id)

        if target_card is None:
            raise ValueError(f"ID: {id} のデータが見つかりませんでした")

        collation_result = self._collate(correct_card, target_card)
        collation_result.log_result()
        return

    def run_all_tests(self):
        # 全ての出力データを取得する
        correct_cards = self._get_correct_cards()
        correct_cards = sorted(correct_cards, key=lambda x: int(x.id))

        results_for_csv = []

        collation_result_list = CollationResultList(results=[])
        for correct_card in correct_cards:
            target_card = self._get_target_card(correct_card.id)

            if target_card is None:
                raise ValueError(
                    f"ID: {correct_card.id} のデータが見つかりませんでした"
                )

            collation_result = self._collate(correct_card, target_card)
            collation_result.log_result()
            collation_result_list.append(collation_result)

            # CSV出力用のデータを作成
            results_for_csv.extend(
                [
                    {
                        "id": correct_card.id,
                        "item_type": item_type,
                        "correct": correct_card.entry.model_dump()[item_type],
                        "target": target_card.entry.model_dump()[item_type],
                        "match": self._match(
                            correct_card.entry.model_dump(),
                            target_card.entry.model_dump(),
                        ),
                    }
                    for item_type in EntryModel.__annotations__.keys()
                ]
            )

        collation_result_list.log_metrics()

        self._output_csv(results_for_csv)

    def _get_target_card(
        self, id
    ) -> VirtualCardModel | InspectedVirtualCardModel | None:
        # inspector と delivered 片方にしかデータが存在せず、存在しない場合は標準出力にエラーが出てしまうので、力技で対応
        with contextlib.redirect_stdout(open(os.devnull, "w")):
            delivered_card = self._get_delivered_card(id)
            if delivered_card:
                return delivered_card

            inspector_card = self._get_inspector_card(id)
            if inspector_card:
                return inspector_card

            return None

    def _get_inspector_card(self, id) -> InspectedVirtualCardModel | None:
        return self.inspector_repository.get(id)

    def _get_delivered_card(self, id) -> VirtualCardModel | None:
        return self.delivered_repository.get(id)

    def _get_correct_card(self, id) -> VirtualCardModel | None:
        return self.correct_repository.get(id)

    def _get_correct_cards(self) -> List[VirtualCardModel]:
        return self.correct_repository.get_all()

    def _is_inspected(
        self, card: VirtualCardModel | InspectedVirtualCardModel
    ) -> TypeGuard[InspectedVirtualCardModel]:
        # インスペクション済みかどうかを返す
        return card.__class__.__name__ == "InspectedVirtualCardModel"

    def _match(self, correct, target):
        # 一致しているかどうかを返す
        # 現時点では純粋に文字列の一致を見ているが、条件を緩くする場合にはここの実装を変更する
        return correct == target

    def _collate(
        self,
        correct_card: VirtualCardModel,
        target_card: VirtualCardModel | InspectedVirtualCardModel,
    ) -> CollationResult:
        correct_count, inspected_count = 0, 0
        inspected_items = []
        diffs = []
        for key in EntryModel.__annotations__.keys():
            # インスペクタを通過している場合、正解として扱う
            if self._is_inspected(target_card) and key in [
                item.value for item in target_card.inspected_items
            ]:
                inspected_items.append(key)
                inspected_count += 1
                correct_count += 1
                continue

            # 精度
            if self._match(
                correct_card.entry.model_dump()[key],
                target_card.entry.model_dump()[key],
            ):
                correct_count += 1
            else:
                d = difflib.Differ()
                diff = d.compare(
                    target_card.entry.model_dump()[key].splitlines(),
                    correct_card.entry.model_dump()[key].splitlines(),
                )
                diffs.append(CollationDiff(item_type=key, diff=[line for line in diff]))

        return CollationResult(
            card_id=correct_card.id, diffs=diffs, inspected_items=inspected_items
        )

    def _output_csv(self, results_for_csv):
        os.makedirs("tools/scoring/output", exist_ok=True)
        with open("tools/scoring/output/results.csv", "w") as f:
            writer = csv.DictWriter(f, fieldnames=results_for_csv[0].keys())
            writer.writeheader()
            writer.writerows(results_for_csv)
