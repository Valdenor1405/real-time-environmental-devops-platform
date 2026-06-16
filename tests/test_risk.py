from app.core.risk import classify_air_risk

def test_low_risk():
    assert classify_air_risk(5, 10, 20) == "LOW"

def test_moderate_risk():
    assert classify_air_risk(36, 20, 20) == "MODERATE"

def test_high_risk():
    assert classify_air_risk(20, 61, 20) == "HIGH"

def test_critical_risk():
    assert classify_air_risk(20, 30, 100) == "CRITICAL"
