from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from ..services.event_store import EventStore

router = APIRouter(prefix="/api/v1/cases", tags=["cases"])
store = EventStore()

@router.get("")
async def get_cases() -> Dict[str, Any]:
    return {"items": store.get_cases()}

@router.get("/{case_id}")
async def get_case(case_id: str) -> Dict[str, Any]:
    case = store.get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case
