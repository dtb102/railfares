import requests
import json

def check_fares():
    url = "https://api.entur.io/journey-planner/v3/graphql"
    headers = {
        "ET-Client-Name": "private-fare-tracker-2026",
        "Content-Type": "application/json"
    }

    # Query structured to look for fares at the Trip level
    query = """
    {
      trip(
        from: {coordinates: {latitude: 59.9139, longitude: 10.7522}},
        to: {coordinates: {latitude: 59.9495, longitude: 10.7495}},
        dateTime: "2026-03-05T08:00:00"
      ) {
        tripPatterns {
          startTime
          duration
          legs {
            mode
          }
        }
        fares {
          coins
          currency
        }
      }
    }
    """

    print("--- Fetching Fares from Trip Level ---")
    response = requests.post(url, json={'query': query}, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.status_code}")

if __name__ == "__main__":
    check_fares()
