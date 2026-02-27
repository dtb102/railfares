import requests
import sys

def run_network_diagnostic():
    print("--- Starting Network Diagnostic ---")
    sys.stdout.flush()

    # Testing a simpler API endpoint: Geocoder
    url = "https://api.entur.io/geocoder/v1/autocomplete"
    params = {"text": "Oslo", "size": 1}
    
    headers = {
        "ET-Client-Name": "network-diagnostic-2026",
    }

    try:
        print(f"Connecting to {url}...")
        sys.stdout.flush()
        
        # Test GET request
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        
    except Exception as e:
        print(f"❌ Connection FAILED: {str(e)}")
        
    sys.stdout.flush()
    print("--- Diagnostic Complete ---")

if __name__ == "__main__":
    run_network_diagnostic()
