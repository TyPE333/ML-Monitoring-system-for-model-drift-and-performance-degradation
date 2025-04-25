import pytest
import pandas as pd
from src.app.model import load_model, get_prediction

# Define a fixture for loading the model
@pytest.fixture
def model():
    """Fixture to load the model."""
    return load_model("models/rfc_model.pkl")

# Define a fixture for dummy input data
@pytest.fixture
def input_data():
    """Fixture to create dummy input data."""
    return pd.DataFrame([{
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
    }])

def test_load_model_success(model):
    """Test if the model loads successfully."""
    assert model is not None
    assert hasattr(model, "predict_proba")

def test_get_prediction_success(model, input_data):
    """Test if predictions are returned successfully."""
    predictions = get_prediction(model, input_data)
    
    # Extract values from the dictionary
    pred_label = predictions['prediction']
    pred_proba = predictions['probability']
    
    # Assert the types of the returned values
    assert isinstance(pred_label, int)
    assert isinstance(pred_proba, float)
