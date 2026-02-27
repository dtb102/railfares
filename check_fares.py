import requests
import json
import sys
import datetime

# Configure logging to stdout
def log(message):
    print(f"[{datetime.datetime.now().isoformat()}] {message}", flush=True)

def check_fares():
    log("--- Starting Fare Check ---")
    
    # Replace this with your actual API endpoint
    url = "https://api.entur.io/..."
    
    # Ensure you include appropriate headers, especially User-Agent
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "railfares-bot/1.0 (GitHub Action)"
    }
    
    # Replace with your actual payload
    payload = {
        "query": "..."
    }

    try:
        log(f"Sending request to {url}...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        # Raise an exception for HTTP errors (4xx or 5xx)
        response.raise_for_status()
        
        log("Request successful.")
        data = response.json()
        
        # Process data here
        # Example: print(json.dumps(data, indent=2))
        
        log("--- Fare Report: SUCCESS ---")

    except requests.exceptions.HTTPError as http_err:
        log(f"❌ HTTP error occurred: {http_err}")
        log(f"Response Body: {response.text}")
    except requests.exceptions.ConnectionError as conn_err:
        log(f"❌ Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        log(f"❌ Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        log(f"❌ An error occurred: {req_err}")
    except Exception as e:
        log(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    check_fares()
