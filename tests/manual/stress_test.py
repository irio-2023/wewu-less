import json
import time

import requests

mail1 = "fuchs.przemyslaw@gmail.com"
mail2 = "hubertmirek@gmail.com"
test_service_url = "https://us-east1-wewu-410223.cloudfunctions.net/wewu_tester"

test_service = {
    "serviceUrl": test_service_url,
    "geoRegions": ["us-east1-b"],
    "primaryAdmin": {"email": mail1},
    "secondaryAdmin": {"email": mail2},
    "pollFrequencySecs": 1,
    "alertingWindowNumberOfCalls": 10,
    "alertingWindowCallsFailCount": 4,
    "ackTimeout": 60,
}

api_url = "https://us-east1-wewu-410223.cloudfunctions.net/wewu_api_register_service"

BATCH_COUNT = 40
BATCH_SIZE = 5
BATCH_TIME_SEC = 1
INITIAL_SIZE = 200

headers = {"Content-type": "application/json"}

test_service = json.dumps(test_service)


for i in range(INITIAL_SIZE):
    response = requests.post(api_url, data=test_service, headers=headers)
    if response.status_code != 200:
        print(response.text)

# vvvv code used only in first iteration vvvv

print("sleeping...")
time.sleep(120)
response = requests.post(
    test_service_url, data=json.dumps({"status_code": 500}), headers=headers
)
print("Response from tester: ")
print(response.text)

for i in range(BATCH_COUNT):
    for j in range(BATCH_SIZE):
        response = requests.post(api_url, data=test_service, headers=headers)
        if response.status_code != 200:
            print(response.text)
    time.sleep(BATCH_TIME_SEC)
