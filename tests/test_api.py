import pytest
from httpx import AsyncClient, ASGITransport
from src.app.main import app

valid_payload = {
    "Time": 100000.0,
    "V1": -1.5,
    "V2": 0.2,
    "V3": -0.1,
    "V4": 0.3,
    "V5": -0.2,
    "V6": 0.1,
    "V7": 0.0,
    "V8": -0.1,
    "V9": 0.5,
    "V10": 0.4,
    "V11": 0.3,
    "V12": 0.2,
    "V13": -0.3,
    "V14": 0.0,
    "V15": -0.2,
    "V16": 0.1,
    "V17": 0.2,
    "V18": 0.3,
    "V19": -0.1,
    "V20": 0.4,
    "V21": -0.2,
    "V22": 0.1,
    "V23": 0.3,
    "V24": 0.0,
    "V25": -0.1,
    "V26": 0.2,
    "V27": -0.3,
    "V28": 0.1,
    "Amount": 50.0
}

@pytest.mark.asyncio
async def test_predict_valid():
    """
    Test the /predict endpoint with valid payload.
    This test checks if the /predict endpoint returns a 200 status code and the expected response format.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/predict", json=valid_payload)

    assert response.status_code == 200
    json_data = response.json()
    assert "prediction" in json_data
    assert "probability" in json_data
    assert isinstance(json_data["prediction"], int)
    assert isinstance(json_data["probability"], float)

@pytest.mark.asyncio
async def test_predict_invalid_missing_field():
    """
    Test the /predict endpoint with a missing field in the payload.
    This test checks if the /predict endpoint returns a 422 status code.
    """
    bad_payload = valid_payload.copy()
    del bad_payload['V10']
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/predict", json=bad_payload)

    print(response.json())
    assert response.status_code == 422
