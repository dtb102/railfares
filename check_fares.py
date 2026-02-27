import requests
from datetime import datetime, timedelta
import time
import sys # Mandatory for flushing the output

def run_debug_check():
    # Bergen (NSR:StopPlace:59885) to Moss (NSR:StopPlace:58957)
    FROM_ID = "NSR:StopPlace:59885"
    TO_ID = "NSR:StopPlace:58957"
    DAYS_TO_SCAN = 1
    
    print(f"--- VERBOSE Report: {datetime.now().strftime('%Y-%m-%d')} ---")
    sys.stdout.flush() # Force immediate print

    # Entur requires identifying your script
    headers = {
        "ET-Client-Name": "robust-debug-tracker-2026",
        "Content-Type": "application/json"
    }

    date = datetime.now().strftime('%Y-%m-%d')
    print(f"Checking date: {date}")
    sys.stdout.flush()
    
    # Using the mandatory Journey Planner v3 API
    url = "https://api.entur.io/journey-planner/v3/graphql"
    
    query = """
    {
      trip(from: {place: "%s"}, to: {place: "%s"}, dateTime: "%sT08:00:00") {
        tripPatterns {
          price { amount }
        }
      }
    }
    """ % (FROM_ID, TO_ID, date)

    try:
        print("Sending request to Entur...")
        sys.stdout.flush()
        
        # Make the API call
        response = requests.post(url, json={'query': query}, headers=headers, timeout=15)
        
        print(f"Status Code: {response.status_code}")
        sys.stdout.flush()
        
        print(f"Raw Response: {response.text}")
        sys.stdout.flush()
        
    except Exception as e:
        # --- THIS CATCHES THE SILENT ERRORS ---
        print(f"❌ CRITICAL ERROR: {str(e)}")
        sys.stdout.flush()

    print("--- Check Complete ---")
    sys.stdout.flush()

if __name__ == "__main__":
    run_debug_check()
