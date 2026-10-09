import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, Any, List

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'cyberguard.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # scan_events table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scan_events (
        id TEXT PRIMARY KEY,
        timestamp TEXT,
        engine TEXT,
        input_type TEXT,
        classification TEXT,
        risk_score INTEGER,
        risk_level TEXT,
        status TEXT,
        summary TEXT,
        raw_result_json TEXT
    )
    ''')
    
    # threat_cases table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS threat_cases (
        id TEXT PRIMARY KEY,
        event_id TEXT,
        timestamp TEXT,
        engine TEXT,
        classification TEXT,
        risk_score INTEGER,
        risk_level TEXT,
        status TEXT,
        summary TEXT,
        raw_result_json TEXT,
        FOREIGN KEY(event_id) REFERENCES scan_events(id)
    )
    ''')
    
    conn.commit()
    conn.close()

# Initialize DB on import
init_db()

class EventStore:
    def __init__(self):
        self.db_path = DB_PATH
        
    def _get_conn(self):
        return sqlite3.connect(self.db_path)
        
    def record_event(self, event_data: Dict[str, Any]):
        conn = self._get_conn()
        cursor = conn.cursor()
        
        event_id = event_data.get("request_id")
        timestamp = event_data.get("timestamp", datetime.utcnow().isoformat())
        engine = event_data.get("engine")
        input_type = event_data.get("input_type", "unknown")
        classification = event_data.get("classification")
        risk_score = event_data.get("risk_score", 0)
        risk_level = event_data.get("risk_level", "SAFE")
        status = event_data.get("status", "COMPLETED")
        summary = event_data.get("summary", "")
        raw_json = json.dumps(event_data)
        
        cursor.execute('''
        INSERT INTO scan_events (id, timestamp, engine, input_type, classification, risk_score, risk_level, status, summary, raw_result_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (event_id, timestamp, engine, input_type, classification, risk_score, risk_level, status, summary, raw_json))
        
        # Create case policy
        if risk_level in ["HIGH", "CRITICAL"]:
            case_id = f"CASE-{event_id[:8]}"
            cursor.execute('''
            INSERT INTO threat_cases (id, event_id, timestamp, engine, classification, risk_score, risk_level, status, summary, raw_result_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (case_id, event_id, timestamp, engine, classification, risk_score, risk_level, "OPEN", summary, raw_json))
            
        conn.commit()
        conn.close()

    def get_dashboard_summary(self) -> Dict[str, Any]:
        conn = self._get_conn()
        cursor = conn.cursor()
        
        # threats_detected (High/Critical)
        cursor.execute("SELECT COUNT(*) FROM scan_events WHERE risk_level IN ('HIGH', 'CRITICAL')")
        threats_detected = cursor.fetchone()[0]
        
        # critical_threats
        cursor.execute("SELECT COUNT(*) FROM scan_events WHERE risk_level = 'CRITICAL'")
        critical_threats = cursor.fetchone()[0]
        
        # scans_analyzed
        cursor.execute("SELECT COUNT(*) FROM scan_events")
        scans_analyzed = cursor.fetchone()[0]
        
        # active_cases
        cursor.execute("SELECT COUNT(*) FROM threat_cases WHERE status = 'OPEN'")
        active_cases = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "threats_detected": threats_detected,
            "critical_threats": critical_threats,
            "scans_analyzed": scans_analyzed,
            "active_cases": active_cases,
            "last_updated": datetime.utcnow().isoformat()
        }

    def get_risk_distribution(self) -> Dict[str, int]:
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute("SELECT risk_level, COUNT(*) FROM scan_events GROUP BY risk_level")
        rows = cursor.fetchall()
        conn.close()
        
        dist = {"SAFE": 0, "LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
        for level, count in rows:
            if level in dist:
                dist[level] = count
                
        return {
            "safe": dist["SAFE"],
            "low": dist["LOW"],
            "medium": dist["MEDIUM"],
            "high": dist["HIGH"],
            "critical": dist["CRITICAL"]
        }

    def get_engine_statistics(self) -> List[Dict[str, Any]]:
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute("SELECT engine, COUNT(*), SUM(CASE WHEN risk_level IN ('HIGH', 'CRITICAL') THEN 1 ELSE 0 END), MAX(timestamp) FROM scan_events GROUP BY engine")
        rows = cursor.fetchall()
        conn.close()
        
        engine_stats = {}
        for engine, scans, threats, last_act in rows:
            engine_stats[engine] = {
                "total_scans": scans,
                "threats_detected": threats or 0,
                "last_activity": last_act
            }
            
        return engine_stats
        
    def get_recent_activity(self, limit: int = 10) -> List[Dict[str, Any]]:
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, timestamp, engine, input_type, classification, risk_score, risk_level, summary FROM scan_events ORDER BY timestamp DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        items = []
        for row in rows:
            items.append({
                "id": row[0],
                "timestamp": row[1],
                "engine": row[2],
                "event_type": row[4],  # using classification as event type
                "title": row[7] or f"{row[4]} detected",
                "risk_score": row[5],
                "risk_level": row[6],
                "classification": row[4]
            })
            
        return items

    def get_high_risk_case(self) -> Dict[str, Any]:
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute("SELECT raw_result_json FROM scan_events WHERE risk_level IN ('HIGH', 'CRITICAL') ORDER BY timestamp DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return json.loads(row[0])
        return {}
        
    def get_cases(self) -> List[Dict[str, Any]]:
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, timestamp, engine, classification, risk_score, risk_level, status FROM threat_cases ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        conn.close()
        
        items = []
        for row in rows:
            items.append({
                "id": row[0],
                "timestamp": row[1],
                "engine": row[2],
                "classification": row[3],
                "risk_score": row[4],
                "risk_level": row[5],
                "status": row[6]
            })
        return items

    def get_case(self, case_id: str) -> Dict[str, Any]:
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, event_id, timestamp, engine, classification, risk_score, risk_level, status, summary, raw_result_json FROM threat_cases WHERE id = ?", (case_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "event_id": row[1],
                "timestamp": row[2],
                "engine": row[3],
                "classification": row[4],
                "risk_score": row[5],
                "risk_level": row[6],
                "status": row[7],
                "summary": row[8],
                "raw_result": json.loads(row[9])
            }
        return None
