# This script spawns subprocesses to periodically refresh the drift reports.

import subprocess
import time
import argparse

def refresh_drift_reports(reference_data_path, current_data_path, reference_prediction_path, current_prediction_path, drift_report_path, prediction_drift_report_path):
    # Refresh data drift report
    subprocess.run([
        "python", "monitoring/generate_data_drift_report.py",
        "--reference_path", reference_data_path,
        "--current_path", current_data_path,
        "--output_path", drift_report_path
    ])

    # Refresh prediction drift report
    subprocess.run([
        "python", "monitoring/generate_prediction_drift_report.py",
        "--reference_path", reference_prediction_path,
        "--current_path", current_prediction_path,
        "--output_path", prediction_drift_report_path
    ])

    print("Drift reports refreshed.")

def automate_drift_report_generation(args):
    while True:
        refresh_drift_reports(
            args.reference_data_path,
            args.current_data_path,
            args.reference_prediction_path,
            args.current_prediction_path,
            args.drift_report_path,
            args.prediction_drift_report_path
        )
        print(f"Sleeping for {args.interval} seconds before next refresh...")
        time.sleep(args.interval)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference_data_path", type=str, required=True, help="Path to the reference data")
    parser.add_argument("--current_data_path", type=str, required=True, help="Path to the current data")
    parser.add_argument("--reference_prediction_path", type=str, required=True, help="Path to the reference prediction data")
    parser.add_argument("--current_prediction_path", type=str, required=True, help="Path to the current prediction data")
    parser.add_argument("--drift_report_path", type=str, required=True, help="Path to the drift report output")
    parser.add_argument("--prediction_drift_report_path", type=str, required=True, help="Path to the prediction drift report output")
    parser.add_argument("--interval", type=int, default=3600, help="Interval in seconds to refresh the reports")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    automate_drift_report_generation(args)
