"""
Continuous Traffic Generator
Keeps the dashboard populated with real-time data.
"""
import requests
import time
import random

BASE_URL = "http://localhost:8000"
ENDPOINTS = [
    "/api/data", "/api/users", "/api/products", 
    "/api/orders", "/api/search", "/api/login",
    "/api/dashboard", "/api/settings"
]

def generate_traffic():
    print("Starting continuous traffic generation... (Press Ctrl+C to stop)")
    session = requests.Session()
    
    while True:
        try:
            # Generate 1-5 requests per second
            for _ in range(random.randint(1, 5)):
                endpoint = random.choice(ENDPOINTS)
                
                # Simulate calls
                # Mostly normal, occasional 403/429
                if random.random() < 0.05:
                    # Simulate suspicious
                    pass 
                
                try:
                    # We can just hit a generic endpoint or the public router if it exists
                    # For now, hit health or root to minimal load, or non-existent to generate 404s (which are still traffic)
                    # Or better, hit the simulate endpoint to do it properly if available
                    response = requests.get(f"{BASE_URL}/simulate/high-traffic?count=1&ip=random")
                except:
                    pass
            
            time.sleep(1)
            print(".", end="", flush=True)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    generate_traffic()
