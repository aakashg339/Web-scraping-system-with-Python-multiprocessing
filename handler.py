import requests
import sqlite3
import json
from bs4 import BeautifulSoup
import re
import random
import datetime
import os
import time

# Helper method
def getData(url, header):
    response = requests.get(url, headers=header)
    #convert to text string and return 
    return response.text

def convertJson(data):
    return json.loads(data)

def createDatabaseConnect(dbName):
	con = sqlite3.connect(dbName)
	cur = con.cursor()
	return con, cur

# Function to make a call to https://en.wikipedia.org/wiki/Summer_Olympic_Games and store relevant data in a table
def makeCallToMainURLAndStoreData():
    # Making the call to get data
    url = 'https://en.wikipedia.org/wiki/Summer_Olympic_Games'
    headers = {'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'}
    html_doc = getData(url, headers)

    # In BeautifulSoup, to parse and get relevant data
    soup = BeautifulSoup(html_doc, 'html.parser')

    # with open('htmldata.txt', 'w') as f:
    #     f.write(soup.prettify())

    # Creating db connection
    dbName = "OlympicsData.db"
    con, cursor = createDatabaseConnect(dbName)

    # Deleting old table
    query = "DROP TABLE IF EXISTS SummerOlympics"
    cursor.execute(query)
    con.commit()

    # Creating table
    query = "CREATE TABLE IF NOT EXISTS SummerOlympics(Name, WikipediaURL, Year, HostCity, ParticipatingNations, Athletes, Sports, Rank_1_nation, Rank_2_nation, Rank_3_nation, DONE_OR_NOT_DONE)"
    cursor.execute(query)
    con.commit()

    # Getting data
    # Getting all the required aref tags of that are within last 50 years
    currentYear = datetime.date.today().year
    year = currentYear - 50
    aRefDatas = []
    tablesWithRequiredClass = soup.find_all('table', class_='sortable wikitable')
    tableWithEveryYearData = tablesWithRequiredClass[1]
    for eachTrData in tableWithEveryYearData.tbody.find_all('tr'):
        tdTag = eachTrData.find('td')
        if(tdTag is not None):
            tdTagText = eachTrData.find('td').text
            tdTagText = tdTagText[0:4]
            if(int(tdTagText) >= year and int(tdTagText) <= currentYear):
                for aRefData in eachTrData.find_all('a'):
                    text = aRefData.text
                    if(re.match('^[XIV]+$', text)):
                        aRefDatas.append(aRefData)
    
    # Using random sample to select any ten aRef tags from aRefDatas
    selectedOlympicaRefs = random.sample(aRefDatas, 10)

    # Getting the URL from the parsed HTML data
    wikipediaURLs = []
    for selectedOlympicaRef in selectedOlympicaRefs:
        wikipediaURL = 'https://en.wikipedia.org' + selectedOlympicaRef['href']
        wikipediaURLs.append(wikipediaURL)
        # Inserting values in table
        query = "INSERT INTO SummerOlympics VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d')"%(None, wikipediaURL, None, None, None, None, None, None, None, None, 0)
        cursor.execute(query)
        con.commit()

    # Closing db connection
    cursor.close()

# Function to check whether scraper.py is still running or not
def isProcessesOfScraperStillRunning():
    count = 0
    for proc in os.popen("ps aux").read().splitlines():
        if 'scraper.py' in proc and 'python3' in proc:
            count += 1
    return count

# Function to check whether all the rows of database was updated or not
def isDatabaseUpdatedComplete():
    # Creating db connection
    dbName = "OlympicsData.db"
    con, cursor = createDatabaseConnect(dbName)

    # Displaying data
    # Displaying year
    query = "SELECT * from SummerOlympics WHERE DONE_OR_NOT_DONE = '0'"
    result = list(cursor.execute(query))

    if len(result) == 0:
        return True
    else:
        return False

# Function to fetch data from the URLs stored in the table
def handlerToFetchDataFromURL():
    # Calling the three process to fetch data from the URLs stored in the table
    os.system('python3 scraper.py&')
    os.system('python3 scraper.py&')
    os.system('python3 scraper.py&')

    # Waiting for some time to let the scraper.py to fetch data from the URLs stored in the table
    time.sleep(1)

    # Calling check.py to check whether all the rows of database is updated or not
    os.system('python3 checker.py&')

def displayData():
    # Creating db connection
    dbName = "OlympicsData.db"
    con, cursor = createDatabaseConnect(dbName)

    # Displaying data
    query = "SELECT * from SummerOlympics"
    result = cursor.execute(query)
    for row in result:
        print(row)
    
    cursor.close()

startTime = time.time()
makeCallToMainURLAndStoreData()
handlerToFetchDataFromURL()
while((isProcessesOfScraperStillRunning() != 0)):
        pass
print('Time taken : ',time.time() - startTime)
#displayData()