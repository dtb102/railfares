import requests
import sys

def run_diagnostic():
    print("--- Starting Diagnostic ---")
    sys.stdout.flush()

    # The exact endpoint we are trying to use
    url = "https://api.entur.io/journey-planner/v3/graphql"
    
    # Simple test query to Entur
    query = "{ __schema { types { name } } }"
    
    headers = {
        "ET-Client-Name": "diagnostic-tracker",
        "Content-Type": "application/json"
    }

    try:
        print(f"Connecting to {url}...")
        sys.stdout.flush()
        
        # Try a quick connection
        response = requests.post(url, json={'query': query}, headers=headers, timeout=10)
        
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Success: Successfully connected to Entur API.")
        else:
            print(f"❌ Failed: API returned code {response.status_code}")
            
    except Exception as e:
        print(f"❌ Failed: Could not connect to API. Error: {str(e)}")
        
    sys.stdout.flush()
    print("--- Diagnostic Complete ---")

if __name__ == "__main__":
    run_diagnostic()
