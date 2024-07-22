from fastapi import APIRouter, HTTPException, status
from typing import List

from app.repositories.delivered import DeliveredRepository
from app.schemas.virtual_card import VirtualCard


router = APIRouter()


@router.get("", operation_id="list_delivered_virtual_cards")
def list_virtual_cards() -> List[VirtualCard]:
    """
    納品されたVirtualCardの一覧を返す
    """
    cards = DeliveredRepository().get_all()
    return [VirtualCard.from_model(card) for card in cards]


@router.get("/{card_id}", operation_id="get_delivered_virtual_card")
def get_virtual_card(card_id: str) -> VirtualCard:
    """
    指定されたIDの納品済みVirtualCardを返す
    """
    card = DeliveredRepository().get(card_id)
    if card is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return VirtualCard.from_model(card)
