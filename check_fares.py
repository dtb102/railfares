import requests
from datetime import datetime, timedelta
import time

def run_fare_check():
    # --- CONFIGURATION ---
    # Bergen Stasjon (NSR:StopPlace:59885) to Moss Stasjon (NSR:StopPlace:58957)
    FROM_ID = "NSR:StopPlace:59885"
    TO_ID = "NSR:StopPlace:58957"
    DAYS_TO_SCAN = 14  # As you requested
    MAX_PRICE = 950 

    print(f"--- Fare Report: {datetime.now().strftime('%Y-%m-%d')} ---")
    
    # Identify yourself to Entur
    headers = {
        "ET-Client-Name": "private-fare-tracker-2026",
        "Content-Type": "application/json"
    }

    for i in range(DAYS_TO_SCAN):
        date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
        
        # Using the v3 Production GraphQL API
        url = "https://api.entur.io/journey-planner/v3/graphql"
        
        # This query specifically asks for the "cheapest" price for the day
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
                trips = data.get('data', {}).get('trip', {}).get('tripPatterns', [])
                
                # Filter to find the lowest valid price
                prices = [t['price']['amount'] for t in trips if t.get('price')]
                
                if prices:
                    cheapest = min(prices)
                    status = "✅ DEAL!" if cheapest <= MAX_PRICE else "ℹ️"
                    print(f"{status} {date}: {cheapest} NOK")
                else:
                    # If no prices, it might be too far in the future
                    print(f"ℹ️ {date}: No prices found (Booking may not be open yet)")
            else:
                print(f"❌ {date}: API Error {response.status_code}")
                
        except Exception as e:
            print(f"❌ {date}: Script Error ({str(e)})")

        # Entur allows about 30 requests per minute on this free tier
        time.sleep(1)

    print("--- Check Complete ---")

if __name__ == "__main__":
    run_fare_check()
