import requests
import datetime
import sys
import json

BASE_URL = "http://127.0.0.1:8000/api/v1/account/analyze"

def post_event(payload):
    resp = requests.post(BASE_URL, json=payload)
    if resp.status_code != 200:
        print(f"Error: HTTP {resp.status_code} - {resp.text}")
        return None
    return resp.json()

def run_tests():
    print("ACCOUNT TAKEOVER ENGINE VALIDATION\\n")
    
    timestamp = datetime.datetime.now(datetime.UTC).isoformat()
    
    # CASE 1: NORMAL
    res = post_event({
        "user_id": "user_001",
        "timestamp": timestamp,
        "ip_address": "203.0.113.10",
        "country": "India",
        "device_id": "device_windows_01",
        "device_type": "Windows",
        "login_success": True,
        "failed_login_count": 0,
        "mfa_used": True,
        "mfa_configuration_changed": False,
        "session_id": "sess_123",
        "active_session_count": 1,
        "vpn_detected": False
    })
    
    case1_pass = res and res["risk_level"] in ["SAFE", "LOW"]
    print(f"Normal Case ........ {'PASS' if case1_pass else 'FAIL'} (Score: {res.get('risk_score')})")

    # CASE 2: SINGLE ANOMALY
    res = post_event({
        "user_id": "user_001",
        "timestamp": timestamp,
        "ip_address": "203.0.113.10",
        "country": "India",
        "device_id": "device_mac_99", # New Device
        "device_type": "macOS",
        "login_success": True,
        "failed_login_count": 0,
        "mfa_used": True,
        "mfa_configuration_changed": False,
        "session_id": "sess_124",
        "active_session_count": 1,
        "vpn_detected": False
    })
    case2_pass = res and res["risk_level"] != "CRITICAL"
    print(f"Single Anomaly ..... {'PASS' if case2_pass else 'FAIL'} (Score: {res.get('risk_score')})")

    # CASE 3: MULTIPLE ANOMALY
    res = post_event({
        "user_id": "user_001",
        "timestamp": "2023-10-24T03:00:00Z", # Unusual time
        "ip_address": "198.51.100.10", # New IP
        "country": "Singapore", # New Country
        "device_id": "device_mac_99", # New Device
        "device_type": "macOS",
        "login_success": True,
        "failed_login_count": 0,
        "mfa_used": True,
        "mfa_configuration_changed": False,
        "session_id": "sess_125",
        "active_session_count": 1,
        "vpn_detected": False
    })
    # Should hit ACCOUNT_TAKEOVER_PATTERN (+40), Country (+20), Device (+10), IP (+10), Time (+5)
    # Score should be high.
    case3_pass = res and res["risk_score"] > 50
    print(f"Multiple Anomaly ... {'PASS' if case3_pass else 'FAIL'} (Score: {res.get('risk_score')})")

    # CASE 4: TAKEOVER PATTERN
    res = post_event({
        "user_id": "user_001",
        "timestamp": timestamp,
        "ip_address": "198.51.100.10", # New IP
        "country": "Singapore", # New Country
        "device_id": "device_mac_99", # New Device
        "device_type": "macOS",
        "login_success": True,
        "failed_login_count": 7, # Burst
        "mfa_used": True,
        "mfa_configuration_changed": True, # MFA Hijack
        "session_id": "sess_126",
        "active_session_count": 2,
        "vpn_detected": False
    })
    case4_pass = res and res["risk_level"] in ["HIGH", "CRITICAL"]
    print(f"Takeover Pattern ... {'PASS' if case4_pass else 'FAIL'} (Score: {res.get('risk_score')})")

    # CASE 5: MFA CASE
    res = post_event({
        "user_id": "user_001",
        "timestamp": timestamp,
        "ip_address": "203.0.113.10",
        "country": "India",
        "device_id": "device_windows_01",
        "device_type": "Windows",
        "login_success": True,
        "failed_login_count": 0,
        "mfa_used": True,
        "mfa_configuration_changed": True, # Only MFA change
        "session_id": "sess_127",
        "active_session_count": 1,
        "vpn_detected": False
    })
    case5_pass = res and res["risk_score"] >= 35 # Base 35 for MFA change
    print(f"MFA Case ........... {'PASS' if case5_pass else 'FAIL'} (Score: {res.get('risk_score')})")

    # CASE 6: VPN CASE
    res = post_event({
        "user_id": "user_001",
        "timestamp": timestamp,
        "ip_address": "203.0.113.10",
        "country": "India",
        "device_id": "device_windows_01",
        "device_type": "Windows",
        "login_success": True,
        "failed_login_count": 0,
        "mfa_used": True,
        "mfa_configuration_changed": False,
        "session_id": "sess_128",
        "active_session_count": 1,
        "vpn_detected": True # VPN
    })
    case6_pass = res and res["risk_level"] in ["SAFE", "LOW"]
    print(f"VPN Case ........... {'PASS' if case6_pass else 'FAIL'} (Score: {res.get('risk_score')})")

    print(f"\\nAPI Contract ....... {'PASS' if all([case1_pass, case2_pass, case3_pass, case4_pass, case5_pass, case6_pass]) else 'FAIL'}")
    print("Frontend Contract .. PENDING")
    
    if not all([case1_pass, case2_pass, case3_pass, case4_pass, case5_pass, case6_pass]):
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
