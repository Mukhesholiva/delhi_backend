import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    try:
        # Test health endpoint
        print("Testing health endpoint...")
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
        
        # Test summary stats
        print("\nTesting summary stats...")
        response = requests.get(f"{base_url}/credit-balances/stats/summary")
        print(f"Summary stats: {response.status_code}")
        if response.status_code == 200:
            stats = response.json()
            print(f"Total records: {stats['total_records']}")
            print(f"Total balance: ₹{stats['total_balance_amount']:,.2f}")
            print(f"Centers: {stats['centers']}")
        
        # Test getting credit balances
        print("\nTesting credit balances endpoint...")
        response = requests.get(f"{base_url}/credit-balances/?limit=5")
        print(f"Credit balances: {response.status_code}")
        if response.status_code == 200:
            balances = response.json()
            print(f"Retrieved {len(balances)} records")
            if balances:
                print(f"First record: {balances[0]['client_code']} - {balances[0]['client_name']}")
        
        print("\n✅ All API tests passed!")
        
    except Exception as e:
        print(f"❌ API test failed: {e}")

if __name__ == "__main__":
    test_api()

