import pandas as pd
from evidently.report import Report
from evidently.metric_preset import TargetDriftPreset
import os
import argparse

def generate_prediction_drift_report(reference_path: str, current_path: str, output_path: str):
    # Load datasets
    reference = pd.read_csv(reference_path)
    current = pd.read_csv(current_path)

    # Create Evidently report
    report = Report(metrics=[TargetDriftPreset()])

    # Run the comparison
    report.run(reference_data=reference, current_data=current)

    # Save the report
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    report.save_html(output_path)

    print(f"✅ Prediction drift report generated at: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Prediction Drift Report")
    parser.add_argument("--reference_path", type=str, required=True)
    parser.add_argument("--current_path", type=str, required=True)
    parser.add_argument("--output_path", type=str, required=True)

    args = parser.parse_args()

    generate_prediction_drift_report(
        reference_path=args.reference_path,
        current_path=args.current_path,
        output_path=args.output_path
    )
