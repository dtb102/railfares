import socket
import ssl
import sys

# Force immediate output to stderr to bypass buffering issues
sys.stdout = sys.stderr

print("--- DIAGNOSTIC SCRIPT STARTING ---", flush=True)

try:
    print("Testing connection to api.entur.io...", flush=True)
    host = "api.entur.io"
    port = 443
    
    # 1. Socket Connection
    print("Attempting to connect to socket...", flush=True)
    s = socket.create_connection((host, port), timeout=10)
    print("✅ Socket connected", flush=True)
    
    # 2. SSL Connection
    print("Attempting SSL handshake...", flush=True)
    context = ssl.create_default_context()
    ss = context.wrap_socket(s, server_hostname=host)
    print(f"✅ SSL Handshake successful: {ss.version()}", flush=True)
    
    ss.close()
    print("--- DIAGNOSTIC SCRIPT COMPLETE ---", flush=True)

except Exception as e:
    print(f"❌ ERROR: {e}", flush=True)
