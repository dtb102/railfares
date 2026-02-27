import requests
from datetime import datetime, timedelta
import time
import sys # Added to force the screen to update

def run_fare_check():
    # Bergen Stasjon to Moss Stasjon IDs
    FROM_ID = "NSR:StopPlace:59885"
    TO_ID = "NSR:StopPlace:58957"
    DAYS_TO_SCAN = 14
    
    print(f"--- Fare Report: {datetime.now().strftime('%Y-%m-%d')} ---")
    # This 'flush' command forces GitHub to show the text IMMEDIATELY
    sys.stdout.flush() 

    headers = {
        "ET-Client-Name": "personal-fare-checker-2026",
        "Content-Type": "application/json"
    }

    for i in range(DAYS_TO_SCAN):
        date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
        
        # Current 2026 Production GraphQL Endpoint
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
            response = requests.post(url, json={'query': query}, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                trips = data.get('data', {}).get('trip', {}).get('tripPatterns', [])
                prices = [t['price']['amount'] for t in trips if t.get('price')]
                
                if prices:
                    print(f"ℹ️ {date}: {min(prices)} NOK")
                else:
                    print(f"ℹ️ {date}: No price data found yet")
            else:
                print(f"❌ {date}: API Error {response.status_code}")
        except Exception as e:
            print(f"❌ {date}: Error: {str(e)}")

        # FORCE REFRESH: This ensures you see the progress live!
        sys.stdout.flush()
        time.sleep(1)

    print("--- Check Complete ---")
    sys.stdout.flush()

if __name__ == "__main__":
    run_fare_check()
