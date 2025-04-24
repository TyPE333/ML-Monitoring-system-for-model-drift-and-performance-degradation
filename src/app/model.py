import joblib
import pandas as pd
from app.schema import InputData  # Import your Pydantic schema


def load_model(model_path: str) -> object:
    """Load the pre-trained model from the specified path."""
    try:
        model = joblib.load(model_path)
        return model
    except FileNotFoundError:
        raise RuntimeError(f"Model file not found at path: {model_path}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while loading the model: {e}")

def get_prediction(model: object, data: InputData) -> dict:
    """Make predictions using the loaded model."""
    # Define the expected feature names (same as used during training)
    feature_names = [
        "Time", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9",
        "V10", "V11", "V12", "V13", "V14", "V15", "V16", "V17", "V18", "V19",
        "V20", "V21", "V22", "V23", "V24", "V25", "V26", "V27", "V28", "Amount"
    ]

    # If `data` is an instance of `InputData`, convert it to a dictionary
    if isinstance(data, InputData):
        validated_data = data.dict()
    else:
        # Validate input data using the InputData schema
        try:
            validated_data = InputData(**data).dict()  # Validate and convert to dictionary
        except Exception as e:
            raise ValueError(f"Invalid input data: {e}")

    # Convert validated data to DataFrame with correct feature names
    try:
        data = pd.DataFrame([validated_data], columns=feature_names)
    except Exception as e:
        raise ValueError(f"Failed to convert input data to DataFrame with correct feature names: {e}")

    # Ensure the model is loaded
    if model is None:
        raise ValueError("Model is not loaded for prediction")
    
    # Ensure the model has the required methods
    if not hasattr(model, "predict") or not hasattr(model, "predict_proba"):
        raise ValueError("The provided model does not support 'predict' or 'predict_proba' methods")
    
    try:
        # Make predictions
        prediction_label = model.predict(data)
        prediction_probability = model.predict_proba(data)

        # Create a dictionary to hold the predictions and probabilities
        predictions = {
            'prediction': int(prediction_label[0]),  
            'probability': float(prediction_probability.max())  
        }

        return predictions
    except Exception as e:
        raise RuntimeError(f"An error occurred during prediction: {e}")
