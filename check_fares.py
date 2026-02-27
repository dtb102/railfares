import requests
from datetime import datetime, timedelta
import time

def run_fare_check():
    # --- CONFIGURATION ---
    # These are the official IDs for Bergen and Moss from the National Stop Register
    FROM_ID = "NSR:StopPlace:59885"  # Bergen Stasjon
    TO_ID = "NSR:StopPlace:58957"    # Moss Stasjon
    DAYS_TO_SCAN = 14
    MAX_PRICE = 950 

    print(f"--- Fare Report: {datetime.now().strftime('%Y-%m-%d')} ---")
    print(f"Scanning for {DAYS_TO_SCAN} days using Entur Open Data...")

    # Entur requires identifying your script with this header
    headers = {
        "ET-Client-Name": "my-personal-fare-tracker",
        "Accept": "application/json"
    }

    for i in range(DAYS_TO_SCAN):
        # Calculate the date and format for Entur
        date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
        
        # Entur Offers API URL
        url = "https://api.entur.io/offers/v1/search/trip-options"
        
        payload = {
            "from": {"id": FROM_ID},
            "to": {"id": TO_ID},
            "searchTime": f"{date}T08:00:00.000Z", # Morning search
            "adultCount": 1
        }

        try:
            # We use POST for the Entur search
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                offers = data.get('offers', [])
                
                # Extract prices
                prices = [o.get('totalPrice', {}).get('amount') for o in offers if o.get('totalPrice')]
                
                if prices:
                    cheapest = min(prices)
                    status = "✅ DEAL!" if cheapest <= MAX_PRICE else "ℹ️"
                    print(f"{status} {date}: {cheapest} NOK")
                else:
                    print(f"ℹ️ {date}: No prices found in current booking window")
            else:
                print(f"❌ {date}: API Error {response.status_code}")
                
        except Exception as e:
            print(f"❌ {date}: Connection issue ({str(e)})")

        time.sleep(0.5) # Be polite to the national API

    print("--- Check Complete ---")

if __name__ == "__main__":
    run_fare_check()
