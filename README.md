# Real-Time Green AI Carbon Audit Pipeline

An end-to-end MLOps and data engineering system for streaming, monitoring, logging, and predicting the carbon footprint and computational efficiency of live AI training workloads.

The project uses a distributed, Dockerized microservices architecture to capture real-time GPU and CPU power metrics, generate carbon estimation forecasts, evaluate machine learning models, and track experiment artifacts in a production-style workflow.

***

## System Architecture

The platform is built as five decoupled components that work together in real time:

- **Telemetry Emitter (`test_emitter.py`)**: Simulates live compute workloads and sends JSON telemetry payloads through high-frequency `POST` requests.
- **FastAPI Gateway Engine (`app/main.py`)**: Ingests hardware parameters, runs drift analysis, serves predictions, and stores audit trails.
- **PostgreSQL Relational Database (v17)**: Persists telemetry and prediction audit records using a fact/dimension-style schema.
- **MLflow Tracking Server (v2.11.3)**: Tracks experiment runs, parameters, metrics, and model evaluation artifacts.
- **Streamlit Dashboard (`app/dashboard.py`)**: Visualizes hardware utilization, live power trends, prediction outputs, and drift alerts.

```text
[Telemetry Emitter] ---> (JSON / POST) ---> [FastAPI Gateway] <---> [PostgreSQL DB]
                                                     |
                                                     +------> [MLflow Tracker]
                                                     |
[Streamlit Dashboard] <--- (REST API) <--------------+
```

## Features

### 1. Centralized Experiment Tracking with MLflow

- Dockerized MLflow tracking server with persistent storage.
- Automated logging of training runs, hyperparameters, and validation metrics.
- Captures model tuning values such as alpha smoothing and dynamic rolling window settings.
- Tracks key evaluation metrics including MAE and R².

### 2. Statistical Data Drift Detection

- Sliding-window drift checks embedded in the FastAPI backend.
- Rolling analysis over the latest 10 telemetry events.
- Variance threshold monitoring for abnormal shifts beyond ±150W from the baseline 250W.
- Real-time Streamlit warnings when drift threatens prediction reliability.

### 3. Asynchronous Model Evaluation Layer

- Prediction results are written into a persistent audit ledger.
- Historical forecasts are matched against actual workload outcomes.
- Accuracy and reconciliation metrics are updated continuously for dashboard visibility.

## Tech Stack

| Layer | Tools |
|---|---|
| Backend API | FastAPI, Python |
| Database | PostgreSQL 17 |
| Experiment Tracking | MLflow 2.11.3 |
| Frontend | Streamlit |
| Containerization | Docker, Docker Compose |
| Telemetry Simulation | Python emitter script |

## Getting Started

### 1. Create the environment file

Add a `.env` file in the project root:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=Joleia#1273
POSTGRES_DB=carbon_tracker_db
```

### 2. Build and start the services

Run the full multi-container stack:

```bash
docker compose up --build -d
```

Check service health:

```bash
docker compose ps
```

### 3. Log training runs to MLflow

Execute the training and validation workflow:

```bash
python train_model.py
```

Then open [http://localhost:5000](http://localhost:5000) to inspect runs, parameters, and model metrics.

### 4. Stream live telemetry

Start the workload simulation client:

```bash
python test_emitter.py
```

### 5. Open the monitoring dashboard

Visit [http://localhost:8501](http://localhost:8501) to monitor real-time power charts, utilization trends, prediction outputs, and drift alerts.

## Project Highlights

- Real-time AI workload telemetry ingestion.
- Carbon footprint estimation pipeline.
- Drift-aware prediction monitoring.
- Persistent experiment and audit tracking.
- Production-style container orchestration.
- Portfolio-ready full-stack MLOps architecture.

## Suggested Repository Structure

```text
.
├── .github/
│   └── workflows/          # CI/CD automated integration pipelines
├── app/
│   ├── routes/
│   │   └── tracking.py     # Endpoint route definitions
│   ├── services/
│   │   └── audit.py        # Async model performance evaluation & reconciliation workers
│   ├── dashboard.py        # Streamlit web UI application
│   ├── database.py         # SQLAlchemy async engine configuration & session engine
│   ├── main.py             # FastAPI gateway entry point & statistical drift detection core
│   ├── models.py           # Relational schema mappings (FactComputeLogs / PredictionAudit)
│   ├── predictor.py        # Machine learning inference engine layer
│   └── schemas.py          # Pydantic telemetry input serialization constraints
├── assets/
│   └── dashboard_preview.png
├── .env                    # System baseline secrets file
├── .gitignore
├── docker-compose.yml      # Multi-container multi-service runtime cluster configurations
├── Dockerfile              # Python web microservice blueprint configuration
├── README.md               # Pipeline documentation index
├── requirements.txt        # Deep ecosystem dependency versions checklist
├── test_emitter.py         # Mock active load sensor metric simulation client
└── train_model.py          # Experiment run hyperparameter training script

## Notes

This project is designed to demonstrate practical MLOps, data engineering, observability, and model monitoring skills in a single portfolio-ready system. It is especially suited for showcasing experience with real-time pipelines, experiment tracking, telemetry-driven analytics, and containerized deployment.