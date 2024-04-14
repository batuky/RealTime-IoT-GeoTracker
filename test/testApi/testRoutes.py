import requests
from datetime import datetime

BASE_URL = "http://localhost:8000"

def create_test_location_data():
    url = f"{BASE_URL}/locations-data/"
    current_time = datetime.now()
    payload = {
        "device": 99,
        "time": current_time.isoformat(),
        "latitude": 22.400004938897936,
        "longitude": 146.10261653135495
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['id']
    else:
        raise Exception(f"Doesn't create a data, status code: {response.status_code}")

def get_test_location_data(location_data_id):
    url = f"{BASE_URL}/locations-data/{location_data_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"There is no data!, status code: {response.status_code}")

if __name__ == "__main__":
    try:
        location_id = create_test_location_data()
        print(f"Created data ID: {location_id}")
        location_data = get_test_location_data(location_id)
        print("Pulled data details:")
        print(location_data)
    except Exception as e:
        print(str(e))