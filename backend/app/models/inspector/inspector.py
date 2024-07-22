from app.models.inspector.base import BaseInspector, InspectedVirtualCardModel
from app.models.virtual_card import VirtualCardModel


class Inspector(BaseInspector):
    def inspect(self, model: VirtualCardModel) -> InspectedVirtualCardModel:
        return InspectedVirtualCardModel(**model.model_dump())
