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
        
        # --- FIXED QUERY STRUCTURE ---
        query = """
        query($from: String!, $to: String!, $date: DateTime!) {
          journeyPlanner {
            trip(
              from: {place: $from},
              to: {place: $to},
              dateTime: $date
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
        }
        """
        
        # We set the search time to 06:00 AM for the target day
        variables = {
            "from": FROM_STATION_ID,
            "to": TO_STATION_ID,
            "date": f"{search_date}T06:00:00"
        }
        
        try:
            time.sleep(1) 
            response = requests.post(url, json={"query": query, "variables": variables}, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # --- DEBUG: Print raw response to confirm fix ---
                # print(f"DEBUG RAW DATA for {search_date}: {json.dumps(data, indent=2)}")
                # ---------------------------------------------------------------

                # Updated path to trip patterns
                trips = data.get('data', {}).get('journeyPlanner', {}).get('trip', {}).get('tripPatterns', [])
                
                prices = []
                for trip in trips:
                    for leg in trip.get('legs', []):
                        price_data = leg.get('expectedPricing')
                        if price_data and price_data.get('amount'):
                            prices.append(price_data.get('amount'))
                
                if prices:
                    cheapest = min(prices)
                    status = "✅ DEAL!" if cheapest <= MAX_PRICE else "ℹ️"
                    print(f"{status} {search_date}: {cheapest} NOK")
                else:
                    print(f"ℹ️ {search_date}: No prices found")
                    
            else:
                print(f"❌ {search_date}: Entur error {response.status_code}")
                
        except Exception as e:
            print(f"❌ {search_date}: Error ({str(e)})")

    print("--- Check Complete ---")

if __name__ == "__main__":
    run_fare_check_entur()
