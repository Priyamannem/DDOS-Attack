"""
Traffic Simulator for Testing DDoS Protection
"""
import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed


BASE_URL = "http://localhost:8000"


def single_request(session, endpoint="/protected-resource"):
    """Make a single request"""
    try:
        response = session.get(f"{BASE_URL}{endpoint}")
        return {
            "status_code": response.status_code,
            "blocked": response.status_code in [429, 403],
            "response": response.json() if response.status_code == 200 else response.text
        }
    except Exception as e:
        return {"error": str(e)}


def simulate_normal_traffic(duration_seconds=60, requests_per_second=5):
    """Simulate normal traffic patterns"""
    print(f"\n🟢 Starting NORMAL traffic simulation for {duration_seconds} seconds...")
    print(f"   Rate: {requests_per_second} requests/second")
    
    session = requests.Session()
    endpoints = ["/protected-resource", "/test-endpoint", "/"]
    
    start_time = time.time()
    total_requests = 0
    blocked_requests = 0
    
    while time.time() - start_time < duration_seconds:
        endpoint = random.choice(endpoints)
        result = single_request(session, endpoint)
        
        total_requests += 1
        if result.get("blocked", False):
            blocked_requests += 1
            print(f"   ⚠️  Request blocked: {result}")
        
        time.sleep(1 / requests_per_second)
    
    print(f"\n✅ Normal traffic completed:")
    print(f"   Total: {total_requests} | Blocked: {blocked_requests}")


def simulate_rate_limit_attack(requests_count=200):
    """Simulate rate limit attack from single IP"""
    print(f"\n🔴 Starting RATE LIMIT attack simulation...")
    print(f"   Sending {requests_count} rapid requests from single IP...")
    
    session = requests.Session()
    blocked_count = 0
    allowed_count = 0
    
    for i in range(requests_count):
        result = single_request(session)
        
        if result.get("blocked", False):
            blocked_count += 1
            if blocked_count == 1:
                print(f"   🛡️  First block at request #{i+1}")
        else:
            allowed_count += 1
        
        # Small delay to simulate rapid clicks
        time.sleep(0.01)
    
    print(f"\n✅ Rate limit test completed:")
    print(f"   Allowed: {allowed_count} | Blocked: {blocked_count}")


def simulate_distributed_attack(num_threads=50, requests_per_thread=100):
    """Simulate distributed DDoS attack"""
    print(f"\n🔴 Starting DISTRIBUTED DDoS simulation...")
    print(f"   Threads: {num_threads} | Requests per thread: {requests_per_thread}")
    
    def worker(thread_id):
        session = requests.Session()
        blocked = 0
        for _ in range(requests_per_thread):
            result = single_request(session)
            if result.get("blocked", False):
                blocked += 1
            time.sleep(random.uniform(0.01, 0.05))
        return blocked
    
    total_blocked = 0
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(worker, i) for i in range(num_threads)]
        
        for future in as_completed(futures):
            total_blocked += future.result()
    
    total_requests = num_threads * requests_per_thread
    print(f"\n✅ Distributed attack completed:")
    print(f"   Total: {total_requests} | Blocked: {total_blocked}")


def test_ip_reputation():
    """Test IP reputation system"""
    print(f"\n🔵 Testing IP reputation system...")
    
    # Test adding to blacklist
    print("   Adding IP to blacklist...")
    response = requests.post(
        f"{BASE_URL}/admin/add_to_blacklist",
        json={"ip": "1.2.3.4", "reason": "test_malicious"}
    )
    print(f"   Blacklist response: {response.json()}")
    
    # Test adding to whitelist
    print("   Adding IP to whitelist...")
    response = requests.post(
        f"{BASE_URL}/admin/add_to_whitelist",
        json={"ip": "10.0.0.1"}
    )
    print(f"   Whitelist response: {response.json()}")
    
    print("✅ IP reputation test completed")


def view_stats():
    """View current system statistics"""
    print(f"\n📊 Fetching system statistics...")
    
    # Get rules
    response = requests.get(f"{BASE_URL}/admin/rules")
    print(f"\n   Current Rules: {response.json()}")
    
    # Get recent logs
    response = requests.get(f"{BASE_URL}/admin/logs/recent?limit=10")
    logs = response.json()
    print(f"\n   Recent Logs ({logs['count']} entries):")
    for log in logs['logs'][:5]:
        print(f"      - {log['timestamp']}: {log['ip']} -> {log['endpoint']} [{log['status']}]")
    
    # Get blocked IPs
    response = requests.get(f"{BASE_URL}/admin/blocked_ips")
    blocked = response.json()
    print(f"\n   Blocked IPs: {blocked['count']}")


if __name__ == "__main__":
    print("=" * 60)
    print("DDoS PROTECTION SYSTEM - TRAFFIC SIMULATOR")
    print("=" * 60)
    
    while True:
        print("\n\nSelect simulation mode:")
        print("1. Normal Traffic (60 seconds)")
        print("2. Rate Limit Attack (200 rapid requests)")
        print("3. Distributed DDoS (50 threads)")
        print("4. Test IP Reputation")
        print("5. View Statistics")
        print("6. Run All Tests")
        print("0. Exit")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == "1":
            simulate_normal_traffic()
        elif choice == "2":
            simulate_rate_limit_attack()
        elif choice == "3":
            simulate_distributed_attack()
        elif choice == "4":
            test_ip_reputation()
        elif choice == "5":
            view_stats()
        elif choice == "6":
            simulate_normal_traffic(duration_seconds=30, requests_per_second=3)
            time.sleep(2)
            simulate_rate_limit_attack(requests_count=100)
            time.sleep(2)
            simulate_distributed_attack(num_threads=20, requests_per_thread=50)
            time.sleep(2)
            view_stats()
        elif choice == "0":
            print("\n👋 Exiting...")
            break
        else:
            print("❌ Invalid choice")
