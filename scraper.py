import requests
import sqlite3
import json
from bs4 import BeautifulSoup
import re
import random
import bs4

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

def fetchDataFromURL():
    headers = {'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'}
    dbName = "OlympicsData.db"

    # Displaying data
    while(True):
        # Creating db connection
        con, cursor = createDatabaseConnect(dbName)
        query = "SELECT * from SummerOlympics WHERE DONE_OR_NOT_DONE = '0'"
        result = list(cursor.execute(query))

        # If we do not have rows to update, then stop the process
        if len(result) == 0:
            return

        # Using random sample to select any two aRef tags from aRefDatas
        selectedRow = random.sample(result, 1)

        # updating its DONE_OR_NOT_DONE to 1
        query = f"UPDATE SummerOlympics SET DONE_OR_NOT_DONE='%d' WHERE wikipediaURL='{selectedRow[0][1]}'" % (1)
        cursor.execute(query)
        con.commit()
        cursor.close()
        
        # Getting data
        # wikipediaURL
        wikipediaURL = selectedRow[0][1]
        
        html_doc = getData(wikipediaURL, headers)
        soup = BeautifulSoup(html_doc, 'html.parser')
        print('URL called ', wikipediaURL)
        # with open(f'htmldataofPage{i}.txt', 'w') as f:
        #     f.write(soup.prettify())
        # i+=1
        
        # name
        name = soup.find("h1", class_='firstHeading').text.strip()

        # year
        year = name[0:4]

        # hostCity
        hostCity = soup.find_all("th", string="Host city")[0].next_sibling.text
        
        # participatingNations
        participatingNations = set()
        participatingNationsDataHtml = soup.find_all("table", class_='wikitable collapsible')
        for tag in participatingNationsDataHtml:
            if tag.find('li') is not None:
                participatingNationsDataHtml = tag
                break
        # Some pages have different html structure. To take that into consideration, added below.
        if len(participatingNationsDataHtml) == 0:
            participatingNationsDataHtml = soup.find_all("table", class_='wikitable mw-collapsible')
        if type(participatingNationsDataHtml) is list:
            participatingNationsDataHtmlWithLiTags = participatingNationsDataHtml[0].find_all('li')
        else:
            if isinstance(participatingNationsDataHtml, bs4.element.ResultSet):
                participatingNationsDataHtml = list(participatingNationsDataHtml)
                participatingNationsDataHtmlWithLiTags = participatingNationsDataHtml[0].find_all('li')
            else:
                participatingNationsDataHtmlWithLiTags = participatingNationsDataHtml.find_all('li')
        for participatingNationsDataHtmlWithLiTag in participatingNationsDataHtmlWithLiTags:
            participatingNations.add(participatingNationsDataHtmlWithLiTag.find('a').text.strip())
        participatingNations = list(participatingNations)

        # athletes
        athletes = soup.find_all("th", string="Athletes")[0].next_sibling.text
        if '(' in athletes:
            athletes = athletes.split('(')[0]
        if '[' in athletes:
            athletes = athletes.split('[')[0]
        if ',' in athletes:
            athletes = athletes.replace(",", "").strip()

        # sports
        sports = []
        sportsHtml = soup.find("table", class_='multicol')
        if sportsHtml is None:
            sportsHtml = soup.find("div", id='mw-content-text').find('div', class_='div-col').find_all('li')
        else:
            sportsHtml = soup.find("table", class_='multicol').find_all('li')
        for sport in sportsHtml:
            if '(' in sport.text:
                sportsName = sport.text.split('(')[0].strip()
                if '\n' in sportsName:
                    sportsName = sportsName.split('\n')[1].strip()
                sports.append(sportsName)
        
        # Rank_1_nation, Rank_2_nation, Rank_3_nation
        pattern = re.compile(r'^/wiki/')
        rankDatas = soup.find("table", class_= 'wikitable sortable plainrowheaders jquery-tablesorter').find_all('a', href = pattern)
        ranks = []
        for rankData in enumerate(rankDatas):
            ranks.append(rankData[1].text)
        Rank_1_nation = ranks[0]
        Rank_2_nation = ranks[1]
        Rank_3_nation = ranks[2]

        # Creating db connection and inserting values in table
        con, cursor = createDatabaseConnect(dbName)
        query = f"UPDATE SummerOlympics SET name='%s', year=%d, hostCity='%s', participatingNations='%s', athletes='%s', sports='%s', Rank_1_nation='%s', Rank_2_nation='%s', Rank_3_nation='%s' WHERE wikipediaURL='{selectedRow[0][1]}'" % (name, int(year), hostCity, ",".join(participatingNations), athletes, ",".join(sports), Rank_1_nation, Rank_2_nation, Rank_3_nation)
        cursor.execute(query)
        con.commit()
        cursor.close()

def displayData():
    # Creating db connection
    dbName = "OlympicsData.db"
    con, cursor = createDatabaseConnect(dbName)

    # Displaying data
    query = "SELECT * from SummerOlympics"
    result = cursor.execute(query)
    for row in result:
        print(row[1] + ', ' + row[10])
    
    cursor.close()

fetchDataFromURL()
#displayData()