import requests
from datetime import datetime
import sys
import os

# --- FORCE LINE BUFFERING ---
sys.stdout.reconfigure(line_buffering=True) 

def run_with_proxy():
    print("--- Starting Fare Check with Proxy ---")
    
    # Entur requires a specific user-agent or client name
    headers = {
        "ET-Client-Name": "github-action-proxy-2026",
        "Content-Type": "application/json"
    }
    
    FROM_ID = "NSR:StopPlace:59885" # Bergen
    TO_ID = "NSR:StopPlace:58957"   # Moss
    date = datetime.now().strftime('%Y-%m-%d')
    
    url = "https://api.entur.io/journey-planner/v3/graphql"
    
    query = """
    {
      trip(from: {place: "%s"}, to: {place: "%s"}, dateTime: "%sT08:00:00") {
        tripPatterns {
          price { amount }
        }
      }
    }
    """ % (FROM_ID, TO_ID, date)

    # --- PROXY CONFIGURATION ---
    # We use a free proxy service to bypass the Azure IP block
    proxies = {
        'http': 'http://proxy.webshare.io:80',
        'https': 'http://proxy.webshare.io:80'
    }
    
    # IF THE ABOVE PROXY FAILS, ALTERNATIVE FREE PROXY:
    # proxies = { 'http': 'http://165.22.47.165:80', 'https': 'http://165.22.47.165:80' }

    try:
        print(f"Attempting POST request via proxy...")
        
        # Make request with proxy
        response = requests.post(
            url, 
            json={'query': query}, 
            headers=headers, 
            proxies=proxies, # <-- Added proxy
            timeout=15       # Increased timeout
        )
        
        print(f"Response Status Code: {response.status_code}")
        print(f"Raw Response Text: {response.text}")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        
    print("--- Check Complete ---")

if __name__ == "__main__":
    run_with_proxy()
