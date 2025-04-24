from app.schema import InputData
import pandas as pd
import os
import re

def log_prediction(input_data: InputData, prediction: dict, log_file: str = "data/predictions.csv"):
    """Logs the prediction results to a CSV file."""
    if isinstance(input_data, InputData):
        formatted_data = input_data.dict()
    else:
        try:
            formatted_data = InputData(**input_data).dict()
        except Exception as e:
            raise ValueError(f"Invalid input data: {e}")
    
    if "prediction_timestamp" not in prediction:
            raise ValueError("Missing prediction_timestamp in prediction dict")
    
    time_stamp = prediction["prediction_timestamp"] 
    prediction_value = prediction.get("prediction", "N/A")
    prediction_proba = prediction.get("probability", "N/A")

    data_to_log = {
        "prediction_timestamp": time_stamp,
        **formatted_data,
        "prediction": prediction_value,
        "probability": prediction_proba
    }

    columns = list(data_to_log.keys())

    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Check if the file exists to decide whether to write the header
    file_exists = os.path.exists(log_file)


    pd.DataFrame([data_to_log]).to_csv(
        log_file, mode="a", header=not file_exists, index=False, columns=columns
    )

    print(f"Logged prediction to {log_file}: {data_to_log}")
