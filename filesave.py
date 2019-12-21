#testing

# Michael Peters
# filesave.py
# 12.20.19

#import http request library
import requests
import json

trailNames = []
URL = "https://skitrails.info/api/report/methowtrails"

request = requests.get(URL)
print('requesting...')

data = request.json()
print('parsing...')

for trail in data['trails']:
    trailNames.append(trail['name'])
    print(trail['name'])

with open('trailnames.txt', 'a') as file1:
    for trail2 in trailNames:
        file1.write('%s\n' % trail2) #fancy soln to fix newline issues

with open('data.json', 'w') as file2:
    file2.write(json.dumps(data, indent=4))

print('saving...')