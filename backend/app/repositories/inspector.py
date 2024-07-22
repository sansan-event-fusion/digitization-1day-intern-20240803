import os
import random

from app.models.inspector.base import InspectedVirtualCardModel
from app.repositories.base import BaseRepository


class InspectorRepository(BaseRepository):
    def __init__(self):
        super().__init__("static/inspectors")

    def get(self, id) -> InspectedVirtualCardModel | None:
        content = super().get(id)
        if not content:
            return None
        return InspectedVirtualCardModel(**content)

    def get_random(self) -> InspectedVirtualCardModel | None:
        files = list(filter(lambda f: f.endswith(".json"), os.listdir(self.path)))
        if not files:
            return None
        file_path = random.choice(files)
        filename, _ = os.path.splitext(file_path)
        content = super().get(filename)
        if not content:
            return None
        return InspectedVirtualCardModel(**content)

    def get_all(self) -> list[InspectedVirtualCardModel]:
        contents = super().get_all()
        return [InspectedVirtualCardModel(**content) for content in contents]

    def save(self, id: str, model: InspectedVirtualCardModel) -> None:
        super().save(id, model)

    def delete(self, id: str) -> None:
        super().delete(id)
