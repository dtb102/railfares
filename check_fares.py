import requests
from datetime import datetime, timedelta
import time

def run_entur_check():
    # --- CONFIGURATION ---
    # These are Entur IDs for Bergen and Moss
    FROM_ID = "NSR:StopPlace:59885"  # Bergen Stasjon
    TO_ID = "NSR:StopPlace:58957"    # Moss Stasjon
    DAYS_TO_SCAN = 28
    MAX_PRICE = 950 

    print(f"--- Fare Report: {datetime.now().strftime('%Y-%m-%d')} ---")
    
    # Entur requires you to identify your script with a header
    headers = {
        "ET-Client-Name": "my-personal-fare-tracker",
        "Accept": "application/json"
    }

    for i in range(DAYS_TO_SCAN):
        date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
        
        # Entur's official price search API
        url = f"https://api.entur.io/offers/v1/search/trip-options"
        
        payload = {
            "from": {"id": FROM_ID},
            "to": {"id": TO_ID},
            "searchTime": f"{date}T08:00:00.000Z", # Checking morning trains
            "adultCount": 1
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                # Finding the cheapest price in the Entur response
                offers = data.get('offers', [])
                prices = [o.get('totalPrice', {}).get('amount') for o in offers if o.get('totalPrice')]
                
                if prices:
                    cheapest = min(prices)
                    status = "✅ DEAL!" if cheapest <= MAX_PRICE else "ℹ️"
                    print(f"{status} {date}: {cheapest} NOK")
                else:
                    print(f"ℹ️ {date}: No prices found (Check if booking is open)")
            else:
                print(f"❌ {date}: Error {response.status_code}")
                
        except Exception as e:
            print(f"❌ {date}: Technical error ({str(e)})")

        time.sleep(1) # Be polite to the API

    print("--- Check Complete ---")

if __name__ == "__main__":
    run_entur_check()
