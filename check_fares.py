import requests
from datetime import datetime, timedelta
import time
import sys

# Forces immediate output regardless of buffering
sys.stdout.reconfigure(line_buffering=True) 

def run_total_debug():
    print("--- Starting Total Control Debugger ---")
    
    # Bergen to Moss IDs
    FROM_ID = "NSR:StopPlace:59885"
    TO_ID = "NSR:StopPlace:58957"
    
    # Test only 1 day to keep it fast
    date = datetime.now().strftime('%Y-%m-%d')
    print(f"Testing date: {date}")
    
    headers = {
        "ET-Client-Name": "total-debug-tracker-2026",
        "Content-Type": "application/json"
    }
    
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
        print(f"Attempting POST request to {url}...")
        # Add a short timeout to see if it hangs
        response = requests.post(url, json={'query': query}, headers=headers, timeout=10)
        
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        
    except requests.exceptions.RequestException as e:
        # This catches DNS failures, timeouts, and network blocks
        print(f"❌ NETWORK ERROR: {str(e)}")
    except Exception as e:
        print(f"❌ UNKNOWN ERROR: {str(e)}")
        
    print("--- Debugger Complete ---")

if __name__ == "__main__":
    run_total_debug()
