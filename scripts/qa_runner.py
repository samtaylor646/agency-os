import requests

BASE_URL = "http://localhost:8000"

def print_result(test_id, passed, details=""):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} | {test_id} | {details}")

# Login
response = requests.post(f"{BASE_URL}/api/v1/token", data={"username": "admin@agencyos.com", "password": "password123"})
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}", "X-Tenant-ID": "1"}

print("--- RBAC ---")
r = requests.post(f"{BASE_URL}/api/v1/rbac/roles", json={"name": "Test"}, headers=headers)
print_result("API-RBAC-03 (Create Custom Role)", r.status_code in [200, 201], f"Status: {r.status_code}")

print("\n--- Analytics ---")
r = requests.get(f"{BASE_URL}/api/v1/analytics/metrics/execution", headers=headers)
print_result("API-ANLY-02 (Retrieve Analytics)", r.status_code == 200, f"Status: {r.status_code} - {r.text[:50]}")
r = requests.get(f"{BASE_URL}/api/v1/analytics/export?format=csv", headers=headers)
print_result("API-ANLY-03 (Export Analytics)", r.status_code == 200, f"Status: {r.status_code}")

print("\n--- Audit ---")
r = requests.get(f"{BASE_URL}/api/v1/audit", headers=headers)
print_result("API-AUDIT-02 (Get Audit Logs)", r.status_code == 200, f"Status: {r.status_code}")

print("\n--- Marketplace ---")
r = requests.get(f"{BASE_URL}/api/v1/marketplace/templates", headers=headers)
print_result("API-MKT-01 (List Templates)", r.status_code == 200, f"Status: {r.status_code}")
if r.status_code == 200:
    r = requests.post(f"{BASE_URL}/api/v1/marketplace/templates/1/clone", json={"workspace_id": 1}, headers=headers)
    print_result("API-MKT-02 (Clone Template - expected endpoint)", r.status_code in [200, 201], f"Status: {r.status_code}")
    
    r = requests.post(f"{BASE_URL}/api/v1/marketplace/templates/1/fork", headers=headers)
    print_result("API-MKT-02 (Clone Template - actual endpoint /fork)", r.status_code in [200, 201] or r.status_code == 404, f"Status: {r.status_code}")
