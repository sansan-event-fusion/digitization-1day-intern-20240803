from app.models.virtual_card import VirtualCardModel
from app.repositories.base import BaseRepository


class DeliveredRepository(BaseRepository):
    def __init__(self):
        super().__init__("static/delivered")

    def get(self, id) -> VirtualCardModel | None:
        content = super().get(id)
        if not content:
            return None
        return VirtualCardModel(**content)

    def get_all(self) -> list[VirtualCardModel]:
        contents = super().get_all()
        return [VirtualCardModel(**content) for content in contents]

    def save(self, id: str, model: VirtualCardModel) -> None:
        super().save(id, model)

    def delete(self, id: str) -> None:
        super().delete(id)
