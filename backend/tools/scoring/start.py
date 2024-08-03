import requests
from app.models.virtual_card import VirtualCardModel
from app.repositories.delivered import DeliveredRepository
from app.repositories.inspector import InspectorRepository
from app.repositories.virtual_card import VirtualCardRepository

STATIC_DIR = "static"
BACKEND_ENDPOINT = "http://localhost:8000"


class StartCommand:
    def __init__(self):
        self.virtual_card_repository = VirtualCardRepository()
        self.delivered_repository = DeliveredRepository()
        self.inspector_repository = InspectorRepository()

    def execute(self, id=None):
        try:
            self._clear_previous_data()

            if id is not None:
                self._post_single_virtual_card(id)
                return

            self._post_multiple_virtual_cards()
        except Exception as e:
            raise e

    def _clear_previous_data(self):
        """
        前回までの出力データを削除する
        """
        self.delivered_repository.delete_all()
        self.inspector_repository.delete_all()

    def _get_virtual_card(self, id) -> VirtualCardModel | None:
        return self.virtual_card_repository.get(id)

    def _get_virtual_cards(self) -> list[VirtualCardModel]:
        return self.virtual_card_repository.get_all()

    def _post_single_virtual_card(self, id):
        requests.post(f"{BACKEND_ENDPOINT}/virtual_card/task/{id}")

    def _post_multiple_virtual_cards(self):
        requests.post(f"{BACKEND_ENDPOINT}/virtual_card/tasks")
