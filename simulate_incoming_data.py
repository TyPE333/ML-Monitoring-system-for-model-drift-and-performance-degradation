# This script simulates a real-time data stream to an inference API by reading data from a CSV file and sending it to the API endpoint.

import pandas as pd
import os
import requests
import time
import argparse
from datetime import datetime
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from tenacity import retry, stop_after_attempt, wait_fixed
import logging
import json
from src.app.schema import InputData # Assuming InputData is a Pydantic model for input validation


########################################################### Validation Functions ###########################################################
# Validating the input file
def validate_file(file_path: str) -> bool:
    """
    Validates the input file path.
    Returns True if valid, False otherwise.
    """
    try:
        # Check if file path follows proper format
        if not isinstance(file_path, str):
            raise ValueError("File path must be a string")
        
        # Check if file exists
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Check if file is a CSV
        if not file_path.endswith('.csv'):
            raise ValueError("File must be a CSV")
        
        return True
    except (ValueError, FileNotFoundError) as e:
        logger.error(f"File validation error: {e}")
        return False
        
# Input data validation
def validate_input_data(data_dict: dict) -> bool:
    """
    Validates the input data against the InputData schema.
    Returns True if valid, False otherwise.
    """
    # Assuming InputData is a Pydantic model for input validation
    try:
        # Example of how to validate data using Pydantic
        data = InputData(**data_dict)  
        return True
    except Exception as e:
        logger.error(f"Input data validation error: {e}")
        return False

# Validating the endpoint URL
def validate_endpoint_url(endpoint: str) -> bool:
    """
    Validates the API endpoint URL.
    Returns True if valid, False otherwise.
    """
    try:
        # Check if the endpoint URL is valid
        parsed_url = urlparse(endpoint)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError("Invalid endpoint URL")
        return True
    except ValueError as e:
        logger.error(f"Endpoint validation error: {e}")
        return False    

# Endpoint health check
def check_api_health(endpoint: str = "http://localhost:8000/health") -> bool:
    """
    Checks the health of the inference API.
    Returns True if the API is healthy, False otherwise.
    """
    try:
        response = requests.get(endpoint, timeout=5)
        if response.status_code == 200:
            print("API is healthy.")
            return True
        else:
            print(f"API health check failed with status code {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Could not connect to API: {e}")
        return False

############################################################ API request and response ############################################################
# API request function with retry and rate limiting
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def api_request(endpoint: str, data: dict) -> dict:

    """
    Sends a POST request to the API endpoint with the input data.
    Returns the API response.
    """
    try:
        # format the data for the API request
        formatted_data = json.dumps(data)
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.post(endpoint, data=formatted_data, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

        return response.json()
    except requests.RequestException as e:
        logger.error(f"API request error: {e}")
        return None
    
    
        
############################################################## Simulate data stream ###############################################################################

def simulate_data_stream(input_file: str, endpoint: str, delay: float, execution_mode: str) -> None:
    """
    Simulates a real-time data stream by reading data from a CSV file and sending it to the API endpoint.
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    # Validate the input file
    if not validate_file(input_file):
        logger.error("Invalid input file. Exiting.")
        return

    # Validate the endpoint
    if not validate_endpoint_url(endpoint):
        logger.error("Invalid endpoint URL. Exiting.")
        return

    # Ping API endpoint to check if it's alive
    if not check_api_health():
        logger.error("API is not healthy. Exiting.")
        return

    # Read and validate data from CSV file 
    # use validate_input_data function to validate each row of data before sending it to the API
    try:
        data = pd.read_csv(input_file)
    except Exception as e:
        logger.error(f"Error reading CSV file: {e}")
        return
    
    if "Class" in data.columns:
        logger.warning("'Class' column found in input — dropping it for inference.")
        data = data.drop(columns=["Class"])

    
    if execution_mode == "sequential":
        # Sequential execution: Read the CSV file and validate each row of data using the validate_input_data function
        for index, row in data.iterrows():
            # Validate each row of data using the validate_input_data function
            if not validate_input_data(row.to_dict()):
                logger.error(f"Invalid input data at row {index}. Skipping this row.")
                continue
            # Send data to API endpoint with rate limiting and retry mechanism
            try:
                response = api_request(endpoint, row.to_dict())
                logger.info(f"API response: {response}")
                time.sleep(delay)
            except Exception as e:
                logger.error(f"Error sending data to API: {e}")
                continue

    elif execution_mode == "parallel":
        # Parallel execution: Use ThreadPoolExecutor to send multiple requests in parallel
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_row = {executor.submit(api_request, endpoint, row.to_dict()): row for _, row in data.iterrows()}
            for future in as_completed(future_to_row):
                row = future_to_row[future]
                try:
                    response = future.result()
                    logger.info(f"API response for row {row}: {response}")
                except Exception as e:
                    logger.error(f"Error sending data to API for row {row}: {e}")

    else:
        logger.error(f"Invalid execution mode: {execution_mode}. Please choose 'sequential' or 'parallel'.")

    return 

def argument_parser():
    parser = argparse.ArgumentParser(description="Simulate real-time data stream to the inference API.")
    parser.add_argument("--input_file", type=str, help="Path to the input CSV file.", required=True)
    parser.add_argument("--endpoint", type=str, help="API endpoint URL.", required=True)
    parser.add_argument("--delay", type=float, default=1, help="Delay between requests in seconds.", required=False)
    parser.add_argument("--log_file", type=str, default="./sim_log_file.txt", help="Path to the log file.", required=False)
    parser.add_argument("--execution_mode", type=str, choices=["sequential", "parallel"], default="sequential", help="Execution mode: sequential or parallel.", required=False)

    return parser.parse_args()

if __name__ == "__main__":
    args = argument_parser()
    # Configure logging
    logging.basicConfig(filename=args.log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    simulate_data_stream(args.input_file, args.endpoint, args.delay, args.execution_mode)
    logger.info("Simulation completed.")

                    



