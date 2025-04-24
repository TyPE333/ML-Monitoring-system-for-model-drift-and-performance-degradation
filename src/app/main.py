from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from datetime import datetime

from app.schema import InputData, PredictionResponse
from app.model import load_model, get_prediction
from app.logging_utils import log_prediction
from app.constants import MODEL_PATH, LOG_FILE_PATH


############################################################ FAST API LIFESPAN FUNCTION ###########################################################################################

classifier = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager to load and unload the model.
    """
    # Load the model only once at startup
    model = load_model(MODEL_PATH)
    if model is None:
        raise RuntimeError("Failed to load the model at startup")
    
    # Store the loaded model in the classifier dictionary
    classifier["random_forest"] = model
    print("Started up Random Forest model API version")
    yield  # Pause here and allow the application to run

    # Cleanup code to unload the model
    if "random_forest" in classifier:
        print("Shutting down Random Forest model API version")
        del classifier["random_forest"]
    else:
        print("No model to unload")

########################################################### DATA PREPROCESSING ###########################################################################################
# Perform any necessary preprocessing on the input data    
def preprocess_data(input_data: InputData):
    # USE THE SAME PREPROCESSING AS IN THE TRAINING PHASE
    #
    #
    #
    #
    # Return the preprocessed data
    pass

########################################################### API APPLICATION ###########################################################################################
# FastAPI application instance with lifespan context manager
app = FastAPI(lifespan=lifespan)

# Endpoints
@app.get("/health")
async def health():
    """
    Health check endpoint to verify if the API is running.
    """
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(input_data: InputData):
    """
    Endpoint to make predictions using the loaded model.
    input_data: InputData - The input data for prediction.
    Returns the prediction result.
    """
    # Ensure the model is loaded
    model = classifier.get("random_forest")
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded")
    
    # Preprocess input data (if needed)
    # preprocessed_data = preprocess_data(input_data)

    # Make prediction using the loaded model
    prediction = get_prediction(model, input_data)

    timestamp=datetime.utcnow().isoformat()

    #Log the prediction along with the timestamp
    prediction["prediction_timestamp"] = timestamp

    log_prediction(input_data=input_data, prediction=prediction, log_file=LOG_FILE_PATH)

    response = PredictionResponse(
        prediction=prediction["prediction"],
        probability=prediction["probability"],
        prediction_timestamp=timestamp
    )

    # Return the prediction response
    return response

############################################################# MAIN FUNCTION #########################################################################################

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)