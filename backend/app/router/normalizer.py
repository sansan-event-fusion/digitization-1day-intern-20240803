from app.models.entry import EntryModel
from app.models.normalizer.entries import EntryNormalizer
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("", operation_id="normalize")
def normalizer(entry: EntryModel) -> EntryModel:
    """
    ユーザーの入力をノーマライズする
    """
    try:
        normalized_entry = EntryNormalizer().normalize(entry)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    else:
        return normalized_entry
