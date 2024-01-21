import json
import random
import time

import requests

mail1 = "youremailgoeshere@service.com"
mail2 = "yoursecondemailgoeshere@service.com"

google = {
    "serviceUrl": "https://google.com",
    "geoRegions": ["us-east1-b"],
    "primaryAdmin": {"email": mail1},
    "secondaryAdmin": {"email": mail2},
    "pollFrequencySecs": 10,
    "alertingWindowNumberOfCalls": 10,
    "alertingWindowCallsFailCount": 4,
    "ackTimeout": 60,
}

amazon = {
    "serviceUrl": "https://amazon.com",
    "geoRegions": ["us-east1-b"],
    "primaryAdmin": {"email": mail1},
    "secondaryAdmin": {"email": mail2},
    "pollFrequencySecs": 10,
    "alertingWindowNumberOfCalls": 10,
    "alertingWindowCallsFailCount": 4,
    "ackTimeout": 60,
}

facebook = {
    "serviceUrl": "https://facebook.com",
    "geoRegions": ["us-east1-b"],
    "primaryAdmin": {"email": mail1},
    "secondaryAdmin": {"email": mail2},
    "pollFrequencySecs": 8,
    "alertingWindowNumberOfCalls": 10,
    "alertingWindowCallsFailCount": 4,
    "ackTimeout": 60,
}

youtube = {
    "serviceUrl": "https://youtube.com",
    "geoRegions": ["us-east1-b"],
    "primaryAdmin": {"email": mail1},
    "secondaryAdmin": {"email": mail2},
    "pollFrequencySecs": 15,
    "alertingWindowNumberOfCalls": 10,
    "alertingWindowCallsFailCount": 4,
    "ackTimeout": 60,
}


services_data = list(map(lambda x: json.dumps(x), [google, amazon, facebook, youtube]))
services_count = len(services_data)

api_url = "https://us-east1-wewu-410223.cloudfunctions.net/wewu_api_register_service"

BATCH_COUNT = 100
BATCH_SIZE = 15
BATCH_TIME_SEC = 6
INITIAL_SIZE = 200

headers = {"Content-type": "application/json"}

for i in range(INITIAL_SIZE):
    service = random.randint(0, services_count - 1)
    response = requests.post(api_url, data=services_data[service], headers=headers)
    if response.status_code != 200:
        print(response.text)

time.sleep(120)
for i in range(BATCH_COUNT):
    for j in range(BATCH_SIZE):
        service = random.randint(0, services_count - 1)
        response = requests.post(api_url, data=services_data[service], headers=headers)
        if response.status_code != 200:
            print(response.text)
    print(f"Batch {i+1} done")
    time.sleep(BATCH_TIME_SEC)
