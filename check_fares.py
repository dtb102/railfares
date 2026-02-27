import subprocess
import sys

# --- FORCE LINE BUFFERING ---
sys.stdout.reconfigure(line_buffering=True) 

def run_network_diagnostics():
    print("--- Starting Network Diagnostics ---")
    
    url = "https://api.entur.io/journey-planner/v3/graphql"
    
    # We use curl to see exactly what happens at a low level
    command = [
        "curl", 
        "-v",                # Verbose mode to see DNS and Handshake
        "-H", "ET-Client-Name: debug-tracker-2026",
        "-H", "Content-Type: application/json",
        "-X", "POST",
        "-d", '{"query": "{__schema{types{name}}}"}', # Simple query
        url
    ]
    
    print(f"Running command: {' '.join(command)}")
    
    try:
        # Run curl and capture output
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            timeout=20 # 20 seconds
        )
        
        print("\n--- Curl Output (STDOUT) ---")
        print(result.stdout)
        
        print("\n--- Curl Errors/Verbose (STDERR) ---")
        print(result.stderr)
        
    except subprocess.TimeoutExpired:
        print("❌ ERROR: Curl command timed out.")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        
    print("--- Diagnostics Complete ---")

if __name__ == "__main__":
    run_network_diagnostics()
