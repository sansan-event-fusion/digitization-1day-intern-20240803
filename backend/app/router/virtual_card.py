import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException, Response, status

from app.models.inspector.inspector import Inspector
from app.models.normalizer.entries import EntryNormalizer
from app.models.virtual_card import VirtualCardModel
from app.repositories.delivered import DeliveredRepository
from app.repositories.inspector import InspectorRepository
from app.repositories.virtual_card import VirtualCardRepository
from app.schemas.virtual_card import (
    VirtualCard,
    VirtualCardCreate,
    VirtualCardCreateBulk,
)

router = APIRouter()


def create_virtual_card_model(param: VirtualCardCreate) -> VirtualCardModel:
    id = uuid.uuid4().hex
    created_at = datetime.now().isoformat()
    model = VirtualCardModel(
        id=id, image_path=param.image_path, entry=param.entry, created_at=created_at
    )
    VirtualCardRepository().save(id, model)
    return model


def format_and_inspect_virtual_card(model: VirtualCardModel) -> None:
    normalized_entry = EntryNormalizer().normalize(model.entry)
    if normalized_entry is None:
        raise ValueError("ノーマライズに失敗しました")
    model.entry = normalized_entry

    inspected_card_model = Inspector().inspect(model)

    if inspected_card_model.has_inspected_items:
        InspectorRepository().save(model.id, inspected_card_model)
    else:
        delivered_at = datetime.now().isoformat()
        model.delivered_at = delivered_at
        DeliveredRepository().save(model.id, model)


@router.post(
    "/task/{card_id}",
    operation_id="create_virtual_card_task",
    response_model_exclude_none=True,
)
def create_virtual_card_task(card_id: str) -> Response:
    """
    指定されたIDのデータを対象にノーマライズおよびインスペクターを実行する
    """
    model = VirtualCardRepository().get(card_id)
    if model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    format_and_inspect_virtual_card(model)
    return Response(status_code=status.HTTP_201_CREATED)


@router.post(
    "/tasks", operation_id="create_virtual_card_tasks", response_model_exclude_none=True
)
def create_virtual_card_tasks() -> Response:
    """
    `/virtual_card`に格納されているデータを対象にノーマライズおよびインスペクターを実行する
    """
    for model in VirtualCardRepository().get_all():
        format_and_inspect_virtual_card(model)
    return Response(status_code=status.HTTP_201_CREATED)


@router.post("", operation_id="create_virtual_card", response_model_exclude_none=True)
def create_virtual_card(param: VirtualCardCreate) -> Response:
    """
    入力を受け取りVirtualCardを作成し、ノーマライズおよびインスペクターを実行する
    """
    model = create_virtual_card_model(param)
    format_and_inspect_virtual_card(model)
    return Response(status_code=status.HTTP_201_CREATED)


@router.post(
    "/bulk", operation_id="create_virtual_cards", response_model_exclude_none=True
)
def create_virtual_cards(params: VirtualCardCreateBulk) -> Response:
    """
    複数の入力を受け取りVirtualCardを作成し、ノーマライズおよびインスペクターを実行する
    """
    for entry in params.entries:
        model = create_virtual_card_model(entry)
        format_and_inspect_virtual_card(model)
    return Response(status_code=status.HTTP_201_CREATED)


@router.get("", operation_id="list_virtual_cards")
def list_virtual_cards() -> list[VirtualCard]:
    """
    VirtualCardの一覧を返す
    """
    cards = VirtualCardRepository().get_all()
    return [VirtualCard.from_model(card) for card in cards]


@router.get("/{card_id}", operation_id="get_virtual_card")
def get_virtual_card(card_id: str) -> VirtualCard:
    """
    指定されたIDのVirtualCardを返す
    """
    card = VirtualCardRepository().get(card_id)
    if card is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return VirtualCard.from_model(card)
