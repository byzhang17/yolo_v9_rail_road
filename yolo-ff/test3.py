import requests 

url = "http://127.0.0.1:3333/endpoint"  # Replace with your API endpoint
headers = {"Content-Type": "application/json"}
data = {"get_progress" : 1}  # Replace with your payload

response = requests.post(url, data=data)

if response.status_code == 200:
    print("Request successful:", response.json())
else:
    print("Request failed with status code:", response.status_code)