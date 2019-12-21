import re
import requests
from bs4 import BeautifulSoup, SoupStrainer

dataPoints = []
dataPoints2 = []

def stripWhitespaceRegex(text):
    return re.sub(r'[\s+]', '', text)

#found on stack overflow
#https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def gatherTimeAndDate(data):
    print(stripWhitespaceRegex(data))

def gatherWeatherAndTemp(data):
    print(stripWhitespaceRegex(data))

def gatherNewSnowReport(data, data2):
    data2 = cleanhtml(str(data2))
    print(stripWhitespaceRegex(data + data2))

def gatherTotalAccumulation(data, data2):
    data2 = cleanhtml(str(data2))
    print(stripWhitespaceRegex(data + data2))

def gatherTotalMilesGroomed(data, data2):
    data2 = cleanhtml(str(data2))
    print(stripWhitespaceRegex(data + data2))

def gatherLast24HoursGroomed(data, data2):
    data2 = cleanhtml(str(data2))
    print(stripWhitespaceRegex(data + data2))

def gatherRecommendedTrail(data, data2):
    data2 = cleanhtml(str(data2))
    print(stripWhitespaceRegex(data + data2))

def gatherWaxOfTheDay(data, data2):
    print(data)
    print(data2)

def gatherTrailConditions(data, data2):
    #ugliest line award
    print(stripWhitespaceRegex(data) + str(str(data2).split("<p>")[0])[3:-1])

URL = "https://wintermaps.com/grooming-new.php"
URL2 = "https://wintermaps.com/wax_of_the_day.php"

#strainer = SoupStrainer(id='p-xs-5')

request = requests.get(URL)
request2 = requests.get(URL2)

soup = BeautifulSoup(request.content, 'html.parser')
soup2 = BeautifulSoup(request2.content,'html.parser')

for text in soup.find_all("div", class_="p-xs-5"):
    vals = list(text.children)

    for val in vals:
        dataPoints.append(val)

for text2 in soup2.find_all("h3"):
    vals2 = list(text2.children)

    for val2 in vals2:
        dataPoints2.append(val2)
    
gatherTimeAndDate(dataPoints[0])
gatherWeatherAndTemp(dataPoints[1])
gatherNewSnowReport(dataPoints[2], dataPoints[3])
gatherTotalAccumulation(dataPoints[5], dataPoints[6])    
gatherTotalMilesGroomed(dataPoints[8], dataPoints[9])
gatherLast24HoursGroomed(dataPoints[11], dataPoints[12])
gatherRecommendedTrail(dataPoints[14], dataPoints[15])
gatherTrailConditions(dataPoints[23], dataPoints[26])
gatherWaxOfTheDay(dataPoints2[1], dataPoints2[2])


#print(str(str(dataPoints[26]).split("<p>")[0])[3:])

