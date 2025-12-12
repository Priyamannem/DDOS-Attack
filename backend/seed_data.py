"""
Data Seeding Script
Automatically runs traffic simulation to populate the database with initial data.
"""
import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://localhost:8000"

def single_request(session, endpoint="/protected-resource"):
    try:
        response = session.get(f"{BASE_URL}{endpoint}")
        return {
            "status_code": response.status_code,
            "blocked": response.status_code in [429, 403],
            "response": response.json() if response.status_code == 200 else response.text
        }
    except Exception as e:
        return {"error": str(e)}

def simulate_normal_traffic(duration_seconds=30, requests_per_second=5):
    print(f"\n🟢 Starting NORMAL traffic simulation for {duration_seconds} seconds...")
    session = requests.Session()
    endpoints = ["/protected-resource", "/test-endpoint", "/"]
    start_time = time.time()
    total = 0
    while time.time() - start_time < duration_seconds:
        endpoint = random.choice(endpoints)
        single_request(session, endpoint)
        total += 1
        time.sleep(1 / requests_per_second)
    print(f"✅ Normal traffic completed: {total} requests")

def simulate_attacks():
    print(f"\n🔴 Starting ATTACK simulation...")
    # Rate limit attack
    session = requests.Session()
    print("   Running rate limit attack...")
    for _ in range(50):
        single_request(session)
        time.sleep(0.01)
    
    # Distributed attack (small scale)
    print("   Running distributed attack...")
    def worker(_):
        s = requests.Session()
        for _ in range(10):
            single_request(s)
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        list(executor.map(worker, range(5)))
        
    print("✅ Attack simulation completed")

def wait_for_backend():
    print("Waiting for backend to be ready...")
    for _ in range(30):
        try:
            requests.get(f"{BASE_URL}/health")
            print("Backend is ready!")
            return True
        except:
            time.sleep(1)
            print(".", end="", flush=True)
    print("\nBackend not reachable!")
    return False

if __name__ == "__main__":
    if wait_for_backend():
        print("Starting data seeding...")
        simulate_normal_traffic(duration_seconds=10, requests_per_second=5)
        simulate_attacks()
        simulate_normal_traffic(duration_seconds=5, requests_per_second=2)
        print("\n✨ Data seeding finished!")
    else:
        exit(1)
