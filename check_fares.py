import requests
from datetime import datetime, timedelta
import time
import sys

def run_fare_check():
    # Bergen Stasjon to Moss Stasjon
    FROM_ID = "NSR:StopPlace:59885"
    TO_ID = "NSR:StopPlace:58957"
    DAYS_TO_SCAN = 2
    
    print(f"--- VERBOSE Report: {datetime.now().strftime('%Y-%m-%d')} ---")
    sys.stdout.flush()

    headers = {
        "ET-Client-Name": "personal-fare-checker-2026",
        "Content-Type": "application/json"
    }

    # Test only 2 days to keep the log small
    for i in range(DAYS_TO_SCAN):
        date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
        print(f"Attempting to check: {date}")
        sys.stdout.flush()
        
        url = "https://api.entur.io/journey-planner/v3/graphql"
        
        # Explicit query
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
            print("Sending request...")
            sys.stdout.flush()
            response = requests.post(url, json={'query': query}, headers=headers, timeout=15)
            
            print(f"Status Code: {response.status_code}")
            # --- THIS LINE IS THE KEY ---
            print(f"Raw Response: {response.text}")
            sys.stdout.flush()
            
        except Exception as e:
            print(f"❌ Connection Error: {str(e)}")
            sys.stdout.flush()

        time.sleep(1)

    print("--- Check Complete ---")
    sys.stdout.flush()

if __name__ == "__main__":
    run_fare_check()
