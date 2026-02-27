import requests
import sys

# Force immediate output
sys.stdout.reconfigure(line_buffering=True)

def check_connectivity():
    print("--- Starting Basic Network Test ---")
    
    # Try connecting to a reliable public site
    target = "https://www.google.com"
    
    try:
        print(f"Connecting to {target}...")
        response = requests.get(target, timeout=10)
        
        print(f"✅ Success! Response Status Code: {response.status_code}")
        print("Your runner HAS internet access.")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed! Could not connect to {target}")
        print(f"Error Details: {str(e)}")
        print("Your runner does NOT have internet access (or is being blocked).")
        
    print("--- Test Complete ---")

if __name__ == "__main__":
    check_connectivity()
