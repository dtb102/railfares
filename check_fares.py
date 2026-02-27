import requests
import json

def introspect_schema():
    url = "https://api.entur.io/journey-planner/v3/graphql"
    headers = {
        "ET-Client-Name": "private-fare-tracker-2026",
        "Content-Type": "application/json"
    }

    # Query to list all fields available on the 'Trip' type
    query = """
    {
      __type(name: "Trip") {
        fields {
          name
          type {
            name
            kind
            ofType {
              name
              kind
            }
          }
        }
      }
    }
    """

    print("--- Introspecting Schema for 'Trip' type ---")
    response = requests.post(url, json={'query': query}, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.status_code}")

if __name__ == "__main__":
    introspect_schema()
