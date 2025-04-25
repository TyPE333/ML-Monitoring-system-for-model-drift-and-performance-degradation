import pytest
import pandas as pd
import os
from unittest.mock import patch
from simulate_incoming_data import simulate_data_stream

@pytest.fixture
def dummy_csv(tmp_path):
    # Create a temporary CSV file
    data = {
        "Time": [100000.0],
        "V1": [-1.5],
        "V2": [0.2],
        "V3": [-0.1],
        "V4": [0.3],
        "V5": [-0.2],
        "V6": [0.1],
        "V7": [0.0],
        "V8": [-0.1],
        "V9": [0.5],
        "V10": [0.4],
        "V11": [0.3],
        "V12": [0.2],
        "V13": [-0.3],
        "V14": [0.0],
        "V15": [-0.2],
        "V16": [0.1],
        "V17": [0.2],
        "V18": [0.3],
        "V19": [-0.1],
        "V20": [0.4],
        "V21": [-0.2],
        "V22": [0.1],
        "V23": [0.3],
        "V24": [0.0],
        "V25": [-0.1],
        "V26": [0.2],
        "V27": [-0.3],
        "V28": [0.1],
        "Amount": [50.0]
    }
    df = pd.DataFrame(data)
    csv_path = tmp_path / "dummy.csv"
    df.to_csv(csv_path, index=False)
    return csv_path

@patch("simulate_incoming_data.api_request")
@patch("simulate_incoming_data.check_api_health", return_value=True)
def test_simulator_success(mock_health, mock_api, dummy_csv):
    mock_api.return_value = {"prediction": 0, "probability": 0.01}

    simulate_data_stream(
        input_file=str(dummy_csv),
        endpoint="http://testserver/predict",
        delay=0,
        execution_mode="sequential"
    )

    assert mock_api.called
    assert mock_health.called
