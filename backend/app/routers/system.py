from fastapi import APIRouter
from datetime import datetime
from typing import Dict, Any

router = APIRouter(prefix="/api/v1/system", tags=["system"])

@router.get("/health")
async def get_health() -> Dict[str, Any]:
    return {
        "status": "operational",
        "backend": {
            "status": "operational"
        },
        "engines": {
            "url": "operational",
            "message": "operational",
            "account": "operational",
            "media": "operational"
        },
        "database": {
            "status": "operational"
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/engines")
async def get_system_engines() -> Dict[str, Any]:
    return {
        "engines": [
            {
                "id": "url",
                "name": "URL ENGINE",
                "status": "operational",
                "model": "CyberGuard Structural/Lexical Ensemble",
                "version": "1.0.0",
                "last_loaded": datetime.utcnow().isoformat()
            },
            {
                "id": "message",
                "name": "MESSAGE ENGINE",
                "status": "operational",
                "model": "CyberGuard Social Engineering NLP",
                "version": "1.0.0",
                "last_loaded": datetime.utcnow().isoformat()
            },
            {
                "id": "account",
                "name": "ACCOUNT SECURITY ENGINE",
                "status": "operational",
                "model": "IsolationForest Anomaly + Rule Engine",
                "version": "1.0.0",
                "last_loaded": datetime.utcnow().isoformat()
            },
            {
                "id": "media",
                "name": "MEDIA ENGINE",
                "status": "operational",
                "model": "prithivMLmods/Deep-Fake-Detector-Model",
                "version": "1.0.0",
                "last_loaded": datetime.utcnow().isoformat()
            }
        ]
    }
