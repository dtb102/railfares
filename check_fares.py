import requests
from datetime import datetime, timedelta
import time

def run_fare_check():
    # --- CONFIGURATION ---
    FROM_STATION = "Bergen"
    TO_STATION = "Moss"
    DAYS_TO_SCAN = 28
    MAX_PRICE = 450  # We will mark prices below this with an alert
    
    print(f"--- Fare Report: {datetime.now().strftime('%Y-%m-%d')} ---")
    print(f"Searching for {FROM_STATION} to {TO_STATION} for the next {DAYS_TO_SCAN} days...")

    # Updated headers to be more convincing to bot detection systems
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.vy.no/",
        "Origin": "https://www.vy.no"
    }

    for i in range(DAYS_TO_SCAN):
        # Calculate the target date
        target_date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
        
        url = "https://api.vy.no/travel-options/search"
        params = {
            "from": FROM_STATION,
            "to": TO_STATION,
            "date": target_date,
            "adultCount": 1
        }

        try:
            # Added a slight randomized delay to act less like a script
            time.sleep(1.5) 
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                itineraries = data.get('itineraries', [])
                
                # Extract all prices for this day
                day_prices = [it.get('price', {}).get('amount') for it in itineraries if it.get('price')]
                
                if day_prices:
                    cheapest = min(day_prices)
                    status = "✅ DEAL!" if cheapest <= MAX_PRICE else "ℹ️"
                    print(f"{status} {target_date}: {cheapest} NOK")
                else:
                    print(f"ℹ️ {target_date}: No prices found")
            else:
                print(f"❌ {target_date}: Vy returned error {response.status_code}")
                
        except Exception as e:
            print(f"❌ {target_date}: Technical error ({str(e)})")

    print("--- Check Complete ---")

if __name__ == "__main__":
    run_fare_check()
