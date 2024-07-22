from app.models.virtual_card import VirtualCardModel
from app.repositories.base import BaseRepository


class VirtualCardRepository(BaseRepository):
    def __init__(self):
        super().__init__("static/virtual_cards")

    def get(self, id) -> VirtualCardModel | None:
        content = super().get(id)
        if not content:
            return None
        if "image_path" not in content:
            content["image_path"] = ""
        return VirtualCardModel(**content)

    def get_all(self) -> list[VirtualCardModel]:
        contents = super().get_all()
        models = []
        for content in contents:
            if "image_path" not in content:
                content["image_path"] = ""
            models.append(VirtualCardModel(**content))
        return models

    def save(self, id: str, model: VirtualCardModel) -> None:
        super().save(id, model)

    def delete(self, id: str) -> None:
        super().delete(id)
