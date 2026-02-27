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
        
        # --- ATTEMPT #4: RESTRUCTURING QUERY ---
        query = """
        {
          trip(
            from: { place: "%s" }
            to: { place: "%s" }
            dateTime: "%sT08:00:00"
          ) {
            tripPatterns {
              expectedStartTime
              expectedEndTime
              legs {
                mode
              }
            }
            # Attempting to fetch prices outside of tripPatterns
            estimatedPrices {
              amount
              currency
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
                
                # Check for prices at the top level of the trip object
                prices = trip_data.get('estimatedPrices', [])
                
                if prices:
                    # Assuming we want the cheapest price if multiple are returned
                    amount = min([p['amount'] for p in prices if 'amount' in p])
                    status = "✅ DEAL!" if amount <= MAX_PRICE else "ℹ️"
                    print(f"{status} {date}: {amount} NOK")
                else:
                    print(f"ℹ️ {date}: No prices found (estimatedPrices empty or missing).")
                    
            else:
                print(f"❌ {date}: API Error {response.status_code}")
                
        except Exception as e:
            print(f"❌ {date}: Script Error ({str(e)})")

        time.sleep(1)

    print("--- Check Complete ---")

if __name__ == "__main__":
    run_fare_check()
