import requests
from datetime import datetime, timedelta
import time
import sys # Mandatory for the 'flush' fix

def run_fare_check():
    # Official NSR IDs for Bergen (59885) and Moss (58957)
    FROM_ID = "NSR:StopPlace:59885"
    TO_ID = "NSR:StopPlace:58957"
    DAYS_TO_SCAN = 14
    
    print(f"--- Fare Report: {datetime.now().strftime('%Y-%m-%d')} ---")
    sys.stdout.flush() # Forces GitHub to show this line immediately

    # Required header for 2026
    headers = {
        "ET-Client-Name": "my-personal-fare-tracker",
        "Content-Type": "application/json"
    }

    for i in range(DAYS_TO_SCAN):
        date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
        
        # Latest v3 GraphQL Endpoint
        url = "https://api.entur.io/journey-planner/v3/graphql"
        
        # GraphQL query required to get pricing data
        query = """
        {
          trip(from: {place: "%s"}, to: {place: "%s"}, dateTime: "%sT08:00:00") {
            tripPatterns {
              expectedStartTime
              price { amount }
            }
          }
        }
        """ % (FROM_ID, TO_ID, date)

        try:
            response = requests.post(url, json={'query': query}, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                trips = data.get('data', {}).get('trip', {}).get('tripPatterns', [])
                
                # Filter for valid prices
                prices = [t['price']['amount'] for t in trips if t.get('price')]
                
                if prices:
                    print(f"ℹ️ {date}: {min(prices)} NOK")
                else:
                    print(f"ℹ️ {date}: No price data found yet")
            else:
                print(f"❌ {date}: API Error {response.status_code}")
        except Exception as e:
            print(f"❌ {date}: Script Error ({str(e)})")

        sys.stdout.flush() # CRITICAL: Tells GitHub "don't wait, show this line now"
        time.sleep(1) # Be polite to the API rate limit

    print("--- Check Complete ---")
    sys.stdout.flush()

if __name__ == "__main__":
    run_fare_check()
