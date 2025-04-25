# ML Monitoring System for Model Drift and Performance Degradation

A **FastAPI-based ML inference service** with integrated logging, monitoring of model performance and data drift using **Evidently AI**, and (optional future extension) metrics exposure to **Prometheus/Grafana**.  
Designed to simulate a real-time, production-ready ML pipeline with full testing and automation.

📄 **[Planning Doc →](https://docs.google.com/document/d/15xdKI6FNmNespsRWUIYhiF2diZbcUP3nN_nlZnq9X74/edit?usp=sharing)**

---

## Project Checklist (Development Phase)

### 📁 Repo Structure
- [x] `/app/` module (FastAPI core)
- [x] `/models/` trained RandomForest model (`model.pkl`)
- [x] `/data/` for incoming data and prediction logs
- [x] `/monitoring/` for drift reports and auto-monitoring scripts
- [x] `/tests/` for unit and integration tests
- [x] `simulate_incoming_data.py` (real-time data simulator)
- [x] `requirements.txt`

---

### 🧱 Core Modules
- [x] `main.py` – FastAPI service & endpoints
- [x] `model.py` – Model loading & prediction logic
- [x] `schema.py` – Input/output schema validation (Pydantic)
- [x] `logging_utils.py` – Prediction logging utility
- [x] `generate_drift_report.py` – Data drift detection
- [x] `generate_prediction_drift_report.py` – Prediction drift detection
- [x] `auto_monitoring_loop.py` – Automated drift report generation loop

---

### 🚀 API Functionality
- [x] `/predict` POST endpoint (model inference)
- [x] `/health` GET endpoint (API health check)
- [x] Manual Swagger UI tests
- [x] Timestamped prediction responses
- [x] Request and response logging to `predictions.csv`

---

### 🧪 Testing & Evaluation
- [x] API endpoint tests (`test_api.py`)
- [x] Schema validation tests (`test_schema.py`)
- [x] Model loading and prediction tests (`test_model.py`)
- [x] Simulator integration test (`test_simulator.py`)
- [x] Full test automation via `pytest`

---

### 🔥 Monitoring Functionality
- [x] Data Drift report generation (Evidently AI)
- [x] Prediction Drift report generation (Evidently AI)
- [x] Automated periodic refresh of drift reports
- [ ] (Optional Future) Prometheus integration for real-time drift metrics
- [ ] (Optional Future) Grafana dashboards

---

## 🧰 Development Setup

```bash
# Clone the repo
git clone https://github.com/your-username/ML-Monitoring-system-for-model-drift-and-performance-degradation.git
cd ML-Monitoring-system-for-model-drift-and-performance-degradation

# Set up environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run the FastAPI server
uvicorn app.main:app --reload
```

---

## 📦 Example Prediction Request (JSON)
```json
{
  "Time": 100000.0,
  "V1": -1.359807,
  "V2": -0.072781,
  ...
  "V28": 0.021,
  "Amount": 149.62
}
```

---

## 📈 Drift Monitoring Automation

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

✅ Generates updated drift reports every 5 minutes automatically.

---

## 📁 Project Status: ✅ Phase 4 Complete
> Core system is complete.  
> Future upgrades include live Prometheus metrics, Grafana dashboards, and dynamic online learning support.
