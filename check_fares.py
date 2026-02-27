import requests
from datetime import datetime, timedelta
import time
import json

def run_fare_check_entur():
    # --- CONFIGURATION ---
    FROM_STATION_ID = "NSR:StopPlace:59871" # Bergen
    TO_STATION_ID = "NSR:StopPlace:58385"   # Moss
    DAYS_TO_SCAN = 28
    MAX_PRICE = 450
    
    print(f"--- Entur Detailed Report: {datetime.now().strftime('%Y-%m-%d')} ---")
    print(f"Searching from {FROM_STATION_ID} to {TO_STATION_ID}...")

    headers = {
        "Content-Type": "application/json",
        "ET-Client-Name": "railfares-bot-dtb102" 
    }

    url = "https://api.entur.io/journey-planner/v3/graphql"

    for i in range(DAYS_TO_SCAN):
        target_date = (datetime.now() + timedelta(days=i))
        # API expects ISO format
        search_date = target_date.strftime('%Y-%m-%d')
        
        # --- FIXED QUERY ---
        # Removed 'startTime' from trip() and moved it inside the specific call structure
        query = """
        query($from: String!, $to: String!, $date: String!) {
          trip(
            from: {place: $from},
            to: {place: $to},
            date: $date
          ) {
            tripPatterns {
              startTime
              duration
              legs {
                expectedPricing {
                    amount
                    currency
                }
              }
            }
          }
        }
        """
        
        variables = {
            "from": FROM_STATION_ID,
            "to": TO_STATION_ID,
            "date": search_date
        }
        
        try:
            time.sleep(1) 
            response = requests.post(url, json={"query": query, "variables": variables}, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Debug: Print raw response to ensure structure is correct now
                # print(f"DEBUG RAW RESPONSE: {json.dumps(data, indent=2)}")

                trips = data.get('data', {}).get('trip', {}).get('tripPatterns', [])
                
                prices = []
                for trip in trips:
                    # expectedPricing is often inside the legs now
                    for leg in trip.get('legs', []):
                        price_data = leg.get('expectedPricing')
                        if price_data and price_data.get('amount'):
                            prices.append(price_data.get('amount'))
                
                if prices:
                    cheapest = min(prices)
                    status = "✅ DEAL!" if cheapest <= MAX_PRICE else "ℹ️"
                    print(f"{status} {target_date.strftime('%Y-%m-%d')}: {cheapest} NOK")
                else:
                    print(f"ℹ️ {target_date.strftime('%Y-%m-%d')}: No prices found")
                    
            else:
                print(f"❌ {target_date.strftime('%Y-%m-%d')}: Entur error {response.status_code}")
                
        except Exception as e:
            print(f"❌ {target_date.strftime('%Y-%m-%d')}: Error ({str(e)})")

    print("--- Check Complete ---")

if __name__ == "__main__":
    run_fare_check_entur()
