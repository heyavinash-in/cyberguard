from fastapi import APIRouter
from typing import Dict, Any
from ..services.event_store import EventStore

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])
store = EventStore()

@router.get("/summary")
async def get_summary() -> Dict[str, Any]:
    return store.get_dashboard_summary()

@router.get("/engines")
async def get_engines() -> Dict[str, Any]:
    stats = store.get_engine_statistics()
    
    # Merge with static engine info
    engines = []
    for engine_id, name in [("url", "URL Engine"), ("message", "Message Engine"), ("account", "Account Security"), ("media", "Media Intelligence")]:
        st = stats.get(engine_id, {})
        engines.append({
            "id": engine_id,
            "name": name,
            "status": "operational",
            "total_scans": st.get("total_scans", 0),
            "threats_detected": st.get("threats_detected", 0),
            "last_activity": st.get("last_activity", None)
        })
    return {"engines": engines}

@router.get("/activity")
async def get_activity(limit: int = 10) -> Dict[str, Any]:
    return {"items": store.get_recent_activity(limit)}

@router.get("/risk-distribution")
async def get_risk_distribution() -> Dict[str, int]:
    return store.get_risk_distribution()

@router.get("/high-risk-case")
async def get_high_risk_case() -> Dict[str, Any]:
    return store.get_high_risk_case()
