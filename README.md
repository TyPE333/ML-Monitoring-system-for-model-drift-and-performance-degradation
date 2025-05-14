# ML Monitoring System for Model Drift and Performance Degradation

A **production-style ML inference service** with built-in monitoring for **data drift** and **prediction drift** using Evidently AI.
Simulates real-time prediction workloads and supports automated drift report generation and extensibility to observability tools like **Prometheus** and **Grafana**.

> Designed to reflect best practices in model serving, schema validation, drift detection, and modular MLOps architecture.

---

## Key Features

* ⚙️ **FastAPI-powered inference server** with Pydantic schema validation and test coverage
* 🔁 **Real-time simulation loop** that mimics incoming prediction traffic
* 📈 **Evidently AI-based drift detection** for both input features and model predictions
* 🧪 **100% unit and integration test coverage** using `pytest`
* 🔄 **Automated report refresh** every N seconds with CLI control
* 🧰 Modular design extensible to **Prometheus metrics** and **Grafana dashboards**

---

## Architecture Overview

```text
                +-------------------------+
                |  Real-time Data Stream  |
                +-----------+-------------+
                            |
          +----------------v------------------+
          |      FastAPI Inference Server      |
          |  /predict       /health            |
          +--------+---------------------------+
                   |
         +---------v---------+
         | RandomForestModel |
         +---------+---------+
                   |
            +------v------+
            | predictions |
            +-------------+
                   |
       +-----------v------------+
       | auto_monitoring_loop.py|
       | (Evidently drift check)|
       +-----------+------------+
                   |
          +--------v--------+
          |  HTML Reports   |
          |   (every 5 min) |
          +-----------------+
```

---

## Technologies Used

* **FastAPI** – backend service and endpoints
* **Scikit-learn** – RandomForest model and prediction logic
* **Evidently AI** – Drift detection and report generation
* **Pydantic** – Input/output schema validation
* **Pytest** – Full unit and integration test suite
* **Uvicorn** – ASGI server
* *(Optional)* **Prometheus + Grafana** for observability (future extension)

---

## Setup Instructions

```bash
# Clone the repo
git clone https://github.com/TyPE333/ML-Monitoring-system-for-model-drift-and-performance-degradation.git
cd ML-Monitoring-system-for-model-drift-and-performance-degradation

# Set up environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run the FastAPI server
uvicorn app.main:app --reload
```

---

## Example API Request

**POST /predict**

```json
{
  "Time": 100000.0,
  "V1": -1.359807,
  "V2": -0.072781,
  "V3": 2.536346,
  ...
  "V28": 0.021,
  "Amount": 149.62
}
```

**Response:**

```json
{
  "prediction": 0,
  "timestamp": "2025-05-10T10:22:45Z"
}
```

---

## Testing

```bash
pytest tests/
```

Covers:

* `/predict` and `/health` endpoints
* schema validation
* model prediction logic
* simulator integration

---

## Drift Monitoring (Auto-Loop)

Generate updated data + prediction drift reports every 5 minutes:

```bash
python monitoring/auto_monitoring_loop.py \
  --reference_data_path data/incoming_data.csv \
  --current_data_path data/incoming_data.csv \
  --reference_prediction_path data/predictions.csv \
  --current_prediction_path data/predictions.csv \
  --drift_report_path monitoring/drift_reports/data_drift_report.html \
  --prediction_drift_report_path monitoring/drift_reports/prediction_drift_report.html \
  --interval 300
```

Drift reports will be saved/updated in the `monitoring/drift_reports/` folder.

---

## Repo Highlights

| File / Folder               | Purpose                                     |
| --------------------------- | ------------------------------------------- |
| `app/`                      | FastAPI server with routes and core logic   |
| `models/`                   | Pretrained RandomForest model (`model.pkl`) |
| `data/`                     | Incoming data and prediction log CSVs       |
| `monitoring/`               | Drift report generators and loop script     |
| `tests/`                    | Unit and integration tests                  |
| `simulate_incoming_data.py` | Fake prediction traffic generator           |

---

## Project Status

| Phase                  | Status          |
| ---------------------- | --------------- |
| API + Inference        | ✅ Complete      |
| Drift detection        | ✅ Complete      |
| Automated report loop  | ✅ Complete      |
| Unit tests             | ✅ 100% coverage |
| Prometheus integration | ⏳ Planned       |
| Grafana dashboard      | ⏳ Planned       |

---
