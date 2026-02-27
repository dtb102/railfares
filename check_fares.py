import requests
from datetime import datetime, timedelta
import time
import json

def run_fare_check_entur():
    # --- CONFIGURATION ---
    # Entur uses IDs for stations, but for search, names usually work 
    # if they are precise.
    FROM_STATION = "Bergen"
    TO_STATION = "Moss"
    DAYS_TO_SCAN = 28
    MAX_PRICE = 450
    
    print(f"--- Entur Fare Report: {datetime.now().strftime('%Y-%m-%d')} ---")
    print(f"Searching for {FROM_STATION} to {TO_STATION}...")

    headers = {
        "Content-Type": "application/json",
        # Entur requests a specific User-Agent identifying your application
        "ET-Client-Name": "railfares-bot-dtb102" 
    }

    url = "https://api.entur.io/journey-planner/v3/graphql"

    for i in range(DAYS_TO_SCAN):
        target_date = (datetime.now() + timedelta(days=i))
        # Entur requires ISO 8601 format with timezone
        start_time = target_date.strftime('%Y-%m-%dT00:00:00Z')
        
        # GraphQL Query
        query = """
        query($from: String!, $to: String!, $date: DateTime!) {
          trip(
            from: {place: $from},
            to: {place: $to},
            startTime: $date,
            transportModes: [{transportMode: rail}]
          ) {
            tripPatterns {
              expectedPricing {
                amount
                currency
              }
            }
          }
        }
        """
        
        variables = {
            "from": FROM_STATION,
            "to": TO_STATION,
            "date": start_time
        }
        
        try:
            time.sleep(1) # Be polite
            response = requests.post(url, json={"query": query, "variables": variables}, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                trips = data.get('data', {}).get('trip', {}).get('tripPatterns', [])
                
                prices = []
                for trip in trips:
                    price_data = trip.get('expectedPricing')
                    if price_data and price_data.get('amount'):
                        prices.append(price_data.get('amount'))
                
                if prices:
                    cheapest = min(prices)
                    status = "✅ DEAL!" if cheapest <= MAX_PRICE else "ℹ️"
                    print(f"{status} {target_date.strftime('%Y-%m-%d')}: {cheapest} NOK")
                else:
                    print(f"ℹ️ {target_date.strftime('%Y-%m-%d')}: No prices found")
                    
            else:
                print(f"❌ {target_date.strftime('%Y-%m-%d')}: Entur returned error {response.status_code}")
                
        except Exception as e:
            print(f"❌ {target_date.strftime('%Y-%m-%d')}: Technical error ({str(e)})")

    print("--- Check Complete ---")

if __name__ == "__main__":
    run_fare_check_entur()
