import requests
import uuid

def run_test():
    job_id = str(uuid.uuid4())[:8]
    url = "http://127.0.0.1:8000/log-compute"
    
    # Add the job_id to the payload so the API accepts it
    payload = {
        "job_id": job_id, 
        "hardware_id": 1, 
        "power_draw_watts": 300.0  # Try changing this to see the graph jump!
    }

    try:
        response = requests.post(url, json=payload)
        # If you still get 422, this print will show you exactly WHAT is wrong
        if response.status_code == 422:
            print(f"Validation Error: {response.json()}")
        else:
            print(f"Status: {response.status_code} | Data Sent: {job_id}")
    except Exception as e:
        print(f"Connection Failed: {e}")

if __name__ == "__main__":
    run_test()