import requests
import json

def check_fares():
    url = "https://api.entur.io/journey-planner/v3/graphql"
    headers = {
        "ET-Client-Name": "private-fare-tracker-2026",
        "Content-Type": "application/json"
    }

    # Query to introspect the schema and find the correct field
    query = """
    {
      __type(name: "TripPattern") {
        name
        fields {
          name
          type {
            name
            kind
          }
        }
      }
    }
    """

    print("--- Fetching Schema Details ---")
    response = requests.post(url, json={'query': query}, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.status_code}")

if __name__ == "__main__":
    check_fares()
