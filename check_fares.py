import requests
from datetime import datetime, timedelta
import time
import json # Required for printing raw JSON for debugging

def run_fare_check():
    # --- CONFIGURATION ---
    # Stops: Bergen to Oslo (Example)
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
        
        # GraphQL query to fetch trip patterns and prices
        query = """
        {
          trip(
            from: { place: "%s" }
            to: { place: "%s" }
            dateTime: "%sT08:00:00"
            searchMode: FORWARD
          ) {
            tripPatterns {
              expectedStartTime
              expectedEndTime
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
                
                # Check for errors in the GraphQL response
                if 'errors' in data:
                    print(f"❌ {date}: GraphQL Error: {data['errors']}")
                    continue

                trips = data.get('data', {}).get('trip', {}).get('tripPatterns', [])
                
                prices = []
                for t in trips:
                    if t.get('price') and t['price'].get('amount'):
                        prices.append(t['price']['amount'])
                
                if prices:
                    cheapest = min(prices)
                    status = "✅ DEAL!" if cheapest <= MAX_PRICE else "ℹ️"
                    print(f"{status} {date}: {cheapest} NOK")
                else:
                    print(f"ℹ️ {date}: No prices found in response.")
                    # --- DEBUG: Print Raw Response ---
                    print(f"--- DEBUG: Raw Response for {date} ---")
                    print(json.dumps(data, indent=2))
                    print("-----------------------------------")
            else:
                print(f"❌ {date}: API Error {response.status_code}")
                
        except Exception as e:
            print(f"❌ {date}: Script Error ({str(e)})")

        # Be nice to the API
        time.sleep(1)

    print("--- Check Complete ---")

if __name__ == "__main__":
    run_fare_check()
