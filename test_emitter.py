import requests
import time
import uuid

def run_test():
    job_id = str(uuid.uuid4())[:8]
    url = "http://127.0.0.1:8000/log-compute"
    
    payload = {
        "job_id": job_id,
        "hardware_id": 1,
        "power_draw_watts": 150.5
    }

    try:
        response = requests.post(url, json=payload)
        print(f"Status: {response.status_code} | Data Sent: {job_id}")
    except Exception as e:
        print(f"Connection Failed: {e}")

if __name__ == "__main__":
    run_test()