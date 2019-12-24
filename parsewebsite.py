import re
import requests
from influxdb import InfluxDBClient
from bs4 import BeautifulSoup, SoupStrainer

dataPoints = []
dataPoints2 = []

time = ""
date = ""
day = 0
month = 0
year = 0
hour = 0
minute = 0
second = 0
am_pm = ""
temperature = ""
weather = ""

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def main():

    URL = "https://wintermaps.com/grooming-new.php"
    URL2 = "https://wintermaps.com/wax_of_the_day.php"

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

    host = '192.168.0.22'
    port = 8086
    user = 'root'
    password = 'root'
    dbname = 'methow_trails'

    json_body = [
            {
                "measurement": "environment",
                "tags": {
                    "host": "methowtrails",
                    "region": "us-west"
                },
                "time": gatherTimeAndDate(dataPoints[0]),
                "fields": {
                    "temperature": gatherTemp(dataPoints[1]),
                    "weather": gatherWeather(dataPoints[1]),
                    "totalSnow": gatherTotalAccumulation(dataPoints[6]),
                    "newSnow": gatherNewSnowReport(dataPoints[3]),
                    "totalGroomed": gatherTotalMilesGroomed(dataPoints[9]),
                    "newGroomed": gatherLast24HoursGroomed(dataPoints[12]),
                    "recommendedTrail": gatherRecommendedTrail(dataPoints[15]),
                    "glideWax": gatherGlideWaxOfTheDay(dataPoints2[1]),
                    "gripWax": gatherGripWaxOfTheDay(dataPoints2[2]),
                    "trailConditions": gatherTrailConditions( dataPoints[26])
                }
            }
        ]

    client = InfluxDBClient(host, port, user, password, dbname)
    client.write_points(json_body)

def stripWhitespaceRegex(text):
    return re.sub(r'[\s+]', '', text)

def stripNewlinesRegex(text):
    return re.sub('/\r', '', text)

def prettyPrinter(data, text):
    print(text + ": " + data)

def convertTime(time):
    global hour, minute, second, am_pm
    hour = time.split(":")[0]
    #print(hour)
    minute = time.split(":")[1][:-2]
    #print(minute)
    am_pm = time.split(":")[1][2:]
    second = "00"
    #print(am_pm)
    if am_pm == "pm": #24hour conversion
        hour += 12
    else:
        hour = str(hour).zfill(2)

def separateDate(date):
    global day, year, month
    day = date.split("/")[1]
    year = date.split("/")[2]
    month = date.split("/")[0]

def createISO8601date(day, month, year, hour, minute, second):
    return str(year) + "-" + str(month) + "-" + str(day) + "T" + str(hour) + ":" + str(minute) + ":" + str(second) + "-08:00"

#found on stack overflow
#https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def gatherTimeAndDate(data):
    date = stripWhitespaceRegex(data)
    date_reformat = re.sub(u"\u2013", "-", date) # replace unicode EN DASH with HYPHEN MINUS
    date = date_reformat.split('-')
    time = date[1]
    date = date[0]

    convertTime(time)
    separateDate(date)
    prettyPrinter(createISO8601date(day, month, year, hour, minute, second), "ISO8601")
    return createISO8601date(day, month, year, hour, minute, second)

def gatherWeather(data):
    weather = stripWhitespaceRegex(data).split(":")[0]
    prettyPrinter(weather, "Weather")
    return(weather)

def gatherTemp(data):
    temperature = stripWhitespaceRegex(data).split(":")[1][:-1]
    prettyPrinter(temperature, "Temperature")
    return(temperature)

def gatherNewSnowReport(data):
    data = cleanhtml(str(data))
    newSnow24H = data
    prettyPrinter(newSnow24H, "New Snow 24h (inches)")
    return(newSnow24H)
    #print(stripWhitespaceRegex(data + data))

def gatherTotalAccumulation(data):
    data = cleanhtml(str(data))
    totalSnow = data
    prettyPrinter(totalSnow, "Total Snow (inches)")
    return(totalSnow)
    #print(stripWhitespaceRegex(data + data))

def gatherTotalMilesGroomed(data):
    data = cleanhtml(str(data))
    totalMilesGroomed = data
    prettyPrinter(totalMilesGroomed, "Total Miles Groomed")
    return(totalMilesGroomed)
    #print(stripWhitespaceRegex(data + data))

def gatherLast24HoursGroomed(data):
    data = cleanhtml(str(data))
    newMilesGroomed24H = data
    prettyPrinter(newMilesGroomed24H, "New Miles Groomed 24h")
    return(newMilesGroomed24H)
    #print(stripWhitespaceRegex(data + data))

def gatherRecommendedTrail(data):
    data = cleanhtml(str(data))
    recommendedTrail = data
    prettyPrinter(recommendedTrail, "Recommended Trail")
    return(recommendedTrail)
    #print(stripWhitespaceRegex(data + data))

def gatherGlideWaxOfTheDay(data):
    glideWax = data.split(":")[1].strip()
    prettyPrinter(glideWax, "Glide Wax")
    return(glideWax)

def gatherGripWaxOfTheDay(data):
    gripWax = data.split(":")[1].strip()
    prettyPrinter(gripWax, "Grip Wax")
    return(gripWax)

def gatherTrailConditions(data):
    #ugliest line award
    trailConditions = str(str(data).split("<p>")[0])[3:-1].rstrip()
    prettyPrinter(trailConditions, "Trail Conditions")
    return(trailConditions)

if __name__ == '__main__':
    main()



