from fastapi import APIRouter, HTTPException, Response, status
from datetime import datetime

from app.models.inspector.base import InspectionResult, InspectedVirtualCardModel
from app.models.inspector.inspector import Inspector
from app.models.virtual_card import VirtualCardModel
from app.repositories.delivered import DeliveredRepository
from app.repositories.inspector import InspectorRepository

router = APIRouter()


@router.post("", operation_id="inspect")
def inspect(model: VirtualCardModel) -> InspectionResult:
    """
    定義されたルールに従ってVirtualCardを検証する
    """
    return Inspector().inspect(model)


@router.get("/new", operation_id="new_inspector_entry")
def new_inspector_entry() -> InspectedVirtualCardModel:
    """
    インスペクター入力対象のVirtualCardをランダムに1件返す
    """
    model = InspectorRepository().get_random()
    if model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return model


@router.post(
    "/create", operation_id="create_inspector_entry", response_model_exclude_none=True
)
def create_inspector_entry(model: VirtualCardModel) -> Response:
    """
    ユーザーの入力を受け取りインスペクター入力の1入力を作成する
    """
    target = InspectorRepository().get(model.id)
    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="入力対象が見つかりません"
        )

    delivered_at = datetime.now().isoformat()
    model.delivered_at = delivered_at

    DeliveredRepository().save(model.id, model)
    InspectorRepository().delete(model.id)
    return Response(status_code=status.HTTP_201_CREATED)
