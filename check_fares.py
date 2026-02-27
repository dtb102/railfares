import requests
from datetime import datetime, timedelta
import time

# Settings
ORIGIN = "Bergen"
DESTINATION = "Moss"
DAYS_TO_CHECK = 28
PRICE_THRESHOLD = 399 # Notify if cheaper than this

# We use a header to identify the script as a search routine
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) FareChecker/1.0",
    "Accept": "application/json"
}

def get_fare(date):
    # Public Vy Search API
    url = "https://api.vy.no/travel-options/search"
    params = {
        "from": ORIGIN,
        "to": DESTINATION,
        "date": date,
        "adultCount": 1
    }
    
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=15)
        
        # If we get blocked (Error 403), this will tell us
        if response.status_code != 200:
            return f"Status {response.status_code}"

        data = response.json()
        itineraries = data.get('itineraries', [])
        
        prices = []
        for trip in itineraries:
            price_val = trip.get('price', {}).get('amount')
            if price_val:
                prices.append(price_val)
        
        return min(prices) if prices else "No prices found"
    except Exception as e:
        return f"Error: {str(e)}"

# --- Execution Start ---
print(f"--- Fare Report: {datetime.now().strftime('%Y-%m-%d')} ---")
print(f"Checking {DAYS_TO_CHECK} days from {ORIGIN} to {DESTINATION}...")

for i in range(DAYS_TO_CHECK):
    # Calculate each date
    check_date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
    
    # Get the price
    result = get_fare(check_date)
    
    # Print results immediately so we see progress in the logs
    if isinstance(result, (int, float)):
        icon = "✅" if result <= PRICE_THRESHOLD else "ℹ️"
        print(f"{icon} {check_date}: {result} NOK")
    else:
        print(f"❌ {check_date}: {result}")
    
    # Wait 1 second between requests to avoid being blocked
    time.sleep(1)

print("--- Check Finished ---")
