import requests
from datetime import datetime, timedelta
import time

# Settings
DAYS_TO_CHECK = 10
PRICE_THRESHOLD = 450 

def get_cheapest_fare(date):
    # Vy's web API endpoint
    url = "https://api.vy.no/travel-options/search"
    
    # We add "Headers" to look like a real web browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
    }
    
    params = {
        "from": "Bergen",
        "to": "Moss",
        "date": date,
        "adultCount": 1,
        "studentCount": 0
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return f"Error: {response.status_code}"

        data = response.json()
        
        # Pulling prices from the Vy response structure
        prices = []
        for trip in data.get('itineraries', []):
            if 'price' in trip and 'amount' in trip['price']:
                prices.append(trip['price']['amount'])
        
        return min(prices) if prices else "No trains found"
    except Exception as e:
        return f"Script Error: {str(e)}"

print(f"--- Fare Report: {datetime.now().strftime('%Y-%m-%d')} ---")

for i in range(DAYS_TO_CHECK):
    check_date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
    cheapest = get_cheapest_fare(check_date)
    
    if isinstance(cheapest, (int, float)):
        if cheapest <= PRICE_THRESHOLD:
            print(f"✅ ALERT: {check_date} is {cheapest} NOK!")
        else:
            print(f"ℹ️ {check_date}: {cheapest} NOK")
    else:
        # This will tell us exactly why it didn't find a price (e.g., "Error: 403")
        print(f"❌ {check_date}: {cheapest}")
    
    # Small pause so we don't overwhelm the Vy server
    time.sleep(1)
