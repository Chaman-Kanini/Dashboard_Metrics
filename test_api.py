import requests
import json

def test_endpoint(url, name):
    try:
        r = requests.get(url, timeout=10)
        print(f"\n{name}")
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print(f"✅ Success")
            data = r.json()
            print(f"Response preview: {json.dumps(data, indent=2)[:300]}...")
        else:
            print(f"❌ Error")
            print(f"Response: {r.text[:500]}")
    except Exception as e:
        print(f"\n{name}")
        print(f"❌ Exception: {e}")

print("Testing API Endpoints...")
print("="*60)

test_endpoint("http://localhost:5000/api/dashboard/stats", "Stats Endpoint")
test_endpoint("http://localhost:5000/api/dashboard/summary", "Summary Endpoint")
test_endpoint("http://localhost:5000/api/dashboard/sessions?limit=5", "Sessions Endpoint")
test_endpoint("http://localhost:5000/api/dashboard/timeseries?days=7", "Timeseries Endpoint")
test_endpoint("http://localhost:5000/api/dashboard/health-distribution", "Health Distribution Endpoint")
