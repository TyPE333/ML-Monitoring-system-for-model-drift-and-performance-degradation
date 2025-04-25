import pytest
from pydantic import ValidationError
from app.schema import InputData

valid_data = {
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

def test_valid_inputdata():
    data = InputData(**valid_data)
    assert isinstance(data, InputData)

def test_missing_field():
    bad_data = valid_data.copy()
    del bad_data["V12"]
    with pytest.raises(ValidationError):
        InputData(**bad_data)

def test_wrong_type():
    bad_data = valid_data.copy()
    bad_data["Amount"] = "fifty"
    with pytest.raises(ValidationError):
        InputData(**bad_data)
