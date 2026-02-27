import requests
from datetime import datetime, timedelta
import time
import sys

# Forces immediate output to the log file
sys.stdout.reconfigure(line_buffering=True)

def run_debug_check():
    print("--- Starting Detailed Debugger ---")
    
    # Official NSR IDs
    FROM_ID = "NSR:StopPlace:59885" # Bergen
    TO_ID = "NSR:StopPlace:58957"   # Moss
    
    # Check just 1 day to keep it fast
    date = datetime.now().strftime('%Y-%m-%d')
    print(f"Testing date: {date}")
    
    # Mandatory Header for 2026
    headers = {
        "ET-Client-Name": "detailed-debug-tracker-2026",
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
        
        # A 10-second timeout allows us to see if the network is hanging
        response = requests.post(url, json={'query': query}, headers=headers, timeout=10)
        
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✅ Success! Raw Response Text: {response.text}")
        else:
            print(f"❌ API Error! Raw Response Text: {response.text}")
        
    except requests.exceptions.RequestException as e:
        # This catches DNS failures, timeouts, and network blocks
        print(f"❌ NETWORK ERROR: {str(e)}")
    except Exception as e:
        print(f"❌ UNKNOWN ERROR: {str(e)}")
        
    print("--- Debugger Complete ---")

if __name__ == "__main__":
    run_debug_check()
