import requests
import json

def check_fares():
    url = "https://api.entur.io/journey-planner/v3/graphql"
    headers = {
        "ET-Client-Name": "private-fare-tracker-2026",
        "Content-Type": "application/json"
    }

    # Updated query following the schema structure
    query = """
    {
      trip(from: {place: "NSR:StopPlace:58223"}, to: {place: "NSR:StopPlace:58222"}, dateTime: "2026-03-01T08:00:00") {
        tripPatterns {
          duration
          legs {
            mode
            serviceJourney {
              estimatedCalls {
                # Look for fare info in the journey details
                forfeit {
                  id
                  currency
                  price
                }
              }
            }
          }
        }
      }
    }
    """

    print("--- Fetching Fares ---")
    response = requests.post(url, json={'query': query}, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.status_code}")

if __name__ == "__main__":
    check_fares()
