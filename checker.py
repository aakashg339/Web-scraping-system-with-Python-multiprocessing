import requests
import sqlite3
import json
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

# Function to check whether scraper.py is still running or not
def isProcessesOfScraperStillRunning():
    count = 0
    for proc in os.popen("ps aux").read().splitlines():
        if 'scraper.py' in proc and 'python3' in proc:
            count += 1
    return count

# Function to execute scraper.py until all the rows of database is updated. At max three scraper.py will be running at a time
def executeProcessToCompleteDatabaseUpdate():
    # Checking whether all the scraper.py process is completed or not
    while((not isDatabaseUpdatedComplete()) or (isProcessesOfScraperStillRunning() != 0)):
        time.sleep(1)
    
    print('All the rows of database is updated and all the scraper.py process is completed')

# Function to print the results of questions from database
def printResultsOfQuestionsFromDB():
    dbName = "OlympicsData.db"
    con, cursor = createDatabaseConnect(dbName)

    # Displaying data
    # Displaying year
    query = "SELECT * from SummerOlympics"
    result = cursor.execute(query)
    for row in result:
        print(row[2])
    
    # Countries which are in top 3 maximum number of times
    query = "SELECT Rank_1_nation, Rank_2_nation, Rank_3_nation from SummerOlympics"
    result = cursor.execute(query)
    countriesInTopThree = {}
    for row in result:
        for i in range(3):
            if row[i] in countriesInTopThree:
                countriesInTopThree[row[i]] += 1
            else:
                countriesInTopThree[row[i]] = 1
    
    maxKey = list(countriesInTopThree.keys())[0]
    for key in countriesInTopThree:
        if countriesInTopThree[key] > countriesInTopThree[maxKey]:
            maxKey = key

    print('Countries which are in top 3 maximum number of times : ', maxKey)

    # Average number of athletes participated
    query = "SELECT Athletes from SummerOlympics"
    result = cursor.execute(query)
    athletes = 0
    countOfRows = 0
    for row in result:
        athletes += int(row[0])
        countOfRows += 1
    print('Average number of athletes participated : ', athletes/countOfRows)

    cursor.close()
    print('All the results of questions from database is printed')

executeProcessToCompleteDatabaseUpdate()
printResultsOfQuestionsFromDB()