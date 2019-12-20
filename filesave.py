#testing

# Michael Peters
# filesave.py
# 12.20.19

#import http request library
import requests
import json

URL = "https://skitrails.info/api/report/methowtrails"

request = requests.get(URL)
print('requesting...')

data = request.json()
print('parsing...')

with open('data.json', 'w') as file:
    file.write(json.dumps(data, indent=4))

print('saving...')