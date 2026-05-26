#  AI Carbon & Cost Tracker

A full-stack data pipeline designed to monitor GPU power consumption in real-time, calculating both the financial cost and environmental impact (CO2 emissions) of machine learning workloads.

##  Key Features
* **Real-time Ingestion:** FastAPI endpoint capable of receiving high-frequency hardware logs.
* **Relational Mapping:** Implements a Star Schema in PostgreSQL to link compute logs with hardware specifications.
* **Automated Analytics:** Provides instant reporting on energy (kWh), total cost ($), and carbon footprint (kg).
* **Environment Security:** Uses `.env` configuration to protect sensitive database credentials.

##  Tech Stack
* **Language:** Python 3.x
* **Backend:** FastAPI (Asynchronous API)
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy (Async)
* **Environment:** python-dotenv

##  How to Run
1. **Setup Database:** Ensure PostgreSQL is running and the `dim_hardware` table is populated.
2. **Configure Environment:** Create a `.env` file with your `DATABASE_URL`.
3. **Start the API:** ```bash
   python -m app.main