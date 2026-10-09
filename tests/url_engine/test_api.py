import os
import sys
import pytest
from fastapi.testclient import TestClient

# Make sure we can import backend.app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.app.main import app
from backend.app.services.normalizer import normalize_url
from backend.app.services.extractor import StaticFeatureExtractor

client = TestClient(app)

def test_normalization_basic():
    res = normalize_url("example.com")
    assert res["normalized_url"] == "http://example.com/"
    assert "Added default scheme 'http://'" in res["normalization_changes"]
    
def test_normalization_complex():
    res = normalize_url("HTTPS://WWW.EXAMPLE.COM:443/LOGIN?REF=1#TOP")
    assert res["normalized_url"] == "https://www.example.com/LOGIN?REF=1#TOP"

def test_extractor_impersonation():
    ext = StaticFeatureExtractor()
    norm = normalize_url("http://paypal-security-check.example.com")
    features = ext.extract(norm)
    assert features["brand_in_subdomain"] == 1
    assert features["legit_brand"] == 0

def test_extractor_typosquatting():
    ext = StaticFeatureExtractor()
    norm = normalize_url("http://p4yp4l.com")
    features = ext.extract(norm)
    assert features["typosquatting"] == 1

def test_extractor_safe():
    ext = StaticFeatureExtractor()
    norm = normalize_url("https://www.netflix.com/login")
    features = ext.extract(norm)
    assert features["legit_brand"] == 1
    assert features["kw_auth"] == 1

def test_api_safe_url():
    # Because models might be loading, we'll just check the structure.
    response = client.post("/api/predict", json={"url": "https://google.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["classification"]["label"] == "LEGITIMATE"
    assert data["risk"]["severity"] == "SAFE"

def test_api_malicious_url():
    response = client.post("/api/predict", json={"url": "http://192.168.1.10/login?redirect=https%3A%2F%2Fevil.example.com.zip"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    # Should flag IP address, auth keyword, suspicious extension, etc.
    assert data["risk"]["score"] > 20
    
def test_api_obfuscation():
    response = client.post("/api/predict", json={"url": "http://example.com/path?redirect_url=https%3A%2F%2Fbad.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["features"]["nested_url"] == 1

def test_invalid_url():
    response = client.post("/api/predict", json={"url": "http://[invalid_url]/@@"})
    # May return 400 if normalizer fails heavily, but for now we fallback gracefully
    assert response.status_code in [200, 400]
