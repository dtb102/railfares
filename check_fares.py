import requests
from datetime import datetime, timedelta
import time
import json

def run_fare_check():
    # --- CONFIGURATION ---
    FROM_ID = "NSR:StopPlace:59885"
    TO_ID = "NSR:StopPlace:58957"
    DAYS_TO_SCAN = 14
    MAX_PRICE = 950

    print(f"--- Fare Report: {datetime.now().strftime('%Y-%m-%d')} ---")
    
    headers = {
        "ET-Client-Name": "private-fare-tracker-2026",
        "Content-Type": "application/json"
    }

    for i in range(DAYS_TO_SCAN):
        date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
        
        url = "https://api.entur.io/journey-planner/v3/graphql"
        
        # --- ATTEMPT #6: USING FARES NODE ---
        query = """
        {
          trip(
            from: { place: "%s" }
            to: { place: "%s" }
            dateTime: "%sT08:00:00"
          ) {
            tripPatterns {
              expectedStartTime
            }
            # Attempting to fetch prices via top-level fares node
            fares {
              price {
                amount
                currency
              }
            }
          }
        }
        """ % (FROM_ID, TO_ID, date)

        try:
            response = requests.post(url, json={'query': query}, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'errors' in data:
                    print(f"❌ {date}: GraphQL Error: {data['errors']}")
                    continue

                trip_data = data.get('data', {}).get('trip', {})
                fares = trip_data.get('fares', [])
                
                cheapest_trip = float('inf')
                found_price = False

                for fare in fares:
                    if fare.get('price') and 'amount' in fare['price']:
                        cheapest_trip = min(cheapest_trip, fare['price']['amount'])
                        found_price = True

                if found_price:
                    status = "✅ DEAL!" if cheapest_trip <= MAX_PRICE else "ℹ️"
                    print(f"{status} {date}: {cheapest_trip} NOK")
                else:
                    print(f"ℹ️ {date}: No prices found (fares empty or missing).")
                    
            else:
                print(f"❌ {date}: API Error {response.status_code}")
                
        except Exception as e:
            print(f"❌ {date}: Script Error ({str(e)})")

        time.sleep(1)

    print("--- Check Complete ---")

if __name__ == "__main__":
    run_fare_check()
