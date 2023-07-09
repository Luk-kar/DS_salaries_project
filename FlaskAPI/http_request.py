import requests
from data_input import data_in

url = "http://127.0.0.1:5000/predict"
headers = {"Content-Type": "application/json"}
data = {"input": data_in["invalid"]}

response = requests.get(url, headers=headers, json=data)
print(response.status_code)
print(response.text)
