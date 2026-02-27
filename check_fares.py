import requests
from datetime import datetime, timedelta

# IDs for Bergen and Moss (Entur StopPlace IDs)
ORIGIN = "NSR:StopPlace:37369"  # Bergen
DESTINATION = "NSR:StopPlace:59885"  # Moss
DAYS_TO_CHECK = 28
PRICE_THRESHOLD = 300  # Notify if cheaper than this (in NOK)

def get_cheapest_fare(date):
    url = "https://api.entur.io/journey-planner/v3/graphql"
    
    # GraphQL query to find trips and approximate prices
    query = """
    {
      trip(
        from: { place: "%s" }
        to: { place: "%s" }
        dateTime: "%sT06:00:00.000Z"
        numVariants: 20
      ) {
        tripPatterns {
          startTime
          expectedArrivalTime
          legs {
            line { name }
          }
          # Note: Real-time commercial prices often require a specific 
          # ticket offer query, but we can look for the 'Lowfare' category.
        }
      }
    }
    """ % (ORIGIN, DESTINATION, date)

    # Note: For production scripts, Vy's internal web API is often more 
    # reliable for price-specific scraping than the open JourneyPlanner.
    # Below is a simplified request logic for the Vy Web API:
    vy_url = f"https://api.vy.no/travel-options/search"
    params = {
        "from": "Bergen",
        "to": "Moss",
        "date": date,
        "adultCount": 1,
        "studentCount": 0
    }
    
    try:
        # We simulate a search against the Vy search endpoint
        # This endpoint structure is what the Vy website uses
        response = requests.get(vy_url, params=params)
        data = response.json()
        
        # Logic to find the minimum price in the returned options
        prices = [opt['price']['amount'] for opt in data.get('itineraries', []) if 'price' in opt]
        return min(prices) if prices else None
    except:
        return None

print(f"--- Fare Report: {datetime.now().strftime('%Y-%m-%d')} ---")
for i in range(DAYS_TO_CHECK):
    check_date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
    cheapest = get_cheapest_fare(check_date)
    
    if cheapest and cheapest <= PRICE_THRESHOLD:
        print(f"✅ ALERT: {check_date} is only {cheapest} NOK!")
    elif cheapest:
        print(f"ℹ️ {check_date}: {cheapest} NOK")
