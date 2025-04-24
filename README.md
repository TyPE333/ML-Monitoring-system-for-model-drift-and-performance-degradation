# ML Monitoring System for Model Drift and Performance Degradation

A **FastAPI-based ML inference service** with integrated logging and monitoring of model performance and data drift using **Evidently AI** (and Prometheus/Grafana in later stages). Designed to simulate a real-time, production-ready ML pipeline.

📄 **[Planning Doc →](https://docs.google.com/document/d/15xdKI6FNmNespsRWUIYhiF2diZbcUP3nN_nlZnq9X74/edit?usp=sharing)**

---

## ✅ Project Checklist (Development Phase)

### 📁 Repo Structure
- [x] `/app/` module (FastAPI core)
- [x] `/models/` with trained model `.pkl`
- [x] `/data/` for incoming data and predictions log
- [x] `/monitoring/` folder (to hold drift reports later)
- [x] `requirements.txt`
- [x] `simulate_incoming_data.py` (up next)

### 🧱 Core Modules
- [x] `main.py` – FastAPI service & endpoints
- [x] `model.py` – Model loading & prediction logic
- [x] `schema.py` – Input/output data validation via Pydantic
- [x] `logging_utils.py` – Logs prediction results to CSV

### 🚀 API Functionality
- [x] `/predict` POST endpoint
- [x] `/health` check endpoint
- [x] Swagger UI tested
- [x] Timestamped response
- [x] Request/response logging

### 🧪 Testing & Evaluation
- [x] Manual tests via Swagger UI
- [ ] `requests.post()` or curl test scripts (to be added)
- [ ] Basic test coverage (optional dev phase goal)

### 🔜 Next Steps
- [ ] Phase 3: Simulate incoming data (`simulate_incoming_data.py`)
- [ ] Phase 4: Add monitoring pipeline with **Evidently AI**
- [ ] (Optional) Phase 5: Add Prometheus metrics + Grafana dashboards

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

## 📁 Project Status: 🚧 In Development
> This project is under active development. Expect additional monitoring, alerting, and streaming components soon.
