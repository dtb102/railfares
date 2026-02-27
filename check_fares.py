import socket
import ssl
import sys
import traceback

# --- FORCE LINE BUFFERING ---
sys.stdout.reconfigure(line_buffering=True) 

def diagnose_connection():
    print("--- Starting Socket Diagnostics ---")
    host = "api.entur.io"
    port = 443

    try:
        print(f"1. Attempting to connect to {host}:{port}...")
        s = socket.create_connection((host, port), timeout=10)
        print("✅ Socket connected successfully.")

        # Wrap with SSL
        print("2. Attempting SSL handshake...")
        context = ssl.create_default_context()
        ss = context.wrap_socket(s, server_hostname=host)
        print(f"✅ SSL Handshake successful. Protocol: {ss.version()}")

        # Send a basic HTTP HEAD request
        print("3. Sending HTTP HEAD request...")
        request = f"HEAD /journey-planner/v3/graphql HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        ss.send(request.encode())
        
        # Read the response headers
        response = ss.recv(1024).decode()
        print("\n--- Response Headers ---")
        print(response)
        
        ss.close()
        print("--- Diagnostics Complete ---")

    except Exception:
        print("❌ CRITICAL ERROR:")
        traceback.print_exc() # This prints the full error stack trace
        print("--- Diagnostics Complete (with errors) ---")

if __name__ == "__main__":
    diagnose_connection()
