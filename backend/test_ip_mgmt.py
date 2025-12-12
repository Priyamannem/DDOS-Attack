import requests
import json

BASE_URL = "http://localhost:8000"
TEST_IP = "192.168.1.150"

def test_ip_manager():
    print("Testing IP Management APIs...")
    
    # 1. Add to Blacklist
    print(f"\n[1] Adding {TEST_IP} to blacklist...")
    r = requests.post(f"{BASE_URL}/admin/add_to_blacklist", json={"ip": TEST_IP, "reason": "Test Block"})
    print(f"Status: {r.status_code}, Response: {r.json()}")
    
    # 2. Verify in Blocked LIst
    print(f"\n[2] Checking blocked IPs...")
    r = requests.get(f"{BASE_URL}/admin/blocked_ips")
    data = r.json()
    blocked = [ip for ip in data['blocked_ips'] if ip['ip_address'] == TEST_IP]
    if blocked:
        print("✅ IP found in blocked list.")
    else:
        print("❌ IP NOT found in blocked list!")
        
    # 3. Remove from Blacklist
    print(f"\n[3] Removing {TEST_IP} from blacklist...")
    r = requests.post(f"{BASE_URL}/admin/remove_ip", json={"ip": TEST_IP})
    print(f"Status: {r.status_code}, Response: {r.json()}")

    # 4. Add to Whitelist
    print(f"\n[4] Adding {TEST_IP} to whitelist...")
    r = requests.post(f"{BASE_URL}/admin/add_to_whitelist", json={"ip": TEST_IP})
    print(f"Status: {r.status_code}, Response: {r.json()}")
    
    # 5. Verify Whitelist
    print(f"\n[5] Checking whitelist...")
    r = requests.get(f"{BASE_URL}/admin/whitelist")
    data = r.json()
    whitelisted = [ip for ip in data['whitelist'] if ip['ip_address'] == TEST_IP]
    if whitelisted:
        print("✅ IP found in whitelist.")
    else:
        print("❌ IP NOT found in whitelist!")

if __name__ == "__main__":
    try:
        test_ip_manager()
    except Exception as e:
        print(f"Error: {e}")
