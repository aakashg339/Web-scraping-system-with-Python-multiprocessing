
# Web scraping system with Python (with multiprocessing)

Python program to scrape the last 50 years of data from the Wikipedia page below. 

https://en.wikipedia.org/wiki/Summer_Olympic_Games

This project is part of a Computing Lab (CS69201) assignment of IIT Kharagpur. (PDF of the assignment can be found in the repository)

#### Programming Languages Used
* Python

#### Libraries Used
* requests
* sqlite3
* json
* bs4
* re
* random
* datetime
* os
* time
In case of any missing library kindly install it using command - pip3 install <library name>
(Some libraries mentioned above comes as part of python3)

### Role of handler.py 

1. Extract the individual Summer Olympics wiki page URLs of the last 50 years by parsing the HTML from the URL mentioned above.
2. Randomly select any 10 URLs.
3. Save the 10 URLs in DB.
4. Create a process of scraper.py. 
5. Create a process of checker.py.
6. Prints time taken to extract the required content.

### Role of scraper.py
scraper.py continuously extracts required content from one of the 10 URLs stored in DB. 

scraper.py selects a unique URL each time, thus avoiding extracting the content of the same URL multiple times.

Once all the 10 URL data data has been extracted, it terminates.

### Role of checker.py
It continuously checks whether the scraper.py has finished extracting content from all 10 URLs.

Once done, use SQL query to answer the questions below using the data in Database.
1. What were the years chosen?
2. Which country was within the top 3 for the maximum time?
3. What is the average number of athletes?
## Running it locally on your machine

1. Clone this repository, and cd to the project root.
2. Run python3 handler.py
## Purpose

The project was used to study the speedup achieved when three processes of scraper.py are used instead of one.

## Details of Experimental Setup and Results

Experimental setup
For Parallel processing
* Made the program as per the directions given in the question of Problem 3 of the attached assignment.
* Recorded the difference between the end and start time, that is, the time taken between the starting of the three processes and when all the three processes end.

For Sequential processing
* Used the program for Problem 3 of the attached assignment, with the changes below.
    - Instead of calling 3 process, called just one process, which parses all the 10 URLs.
* Recorded the difference between the  end and start time, that is the time taken between starting of the a single process and when it ends.

Experimented five times

With parallel processing
* 3.8247456550598145
* 3.7879176139831543
* 3.6014187335968018
* 3.599642038345337
* 3.6519627571105957
Average = 3.69313736

With sequential process
* 7.893278360366821
* 8.008944272994995
* 8.084598064422607
* 8.070600032806396
* 7.965373516082764
Average = 8.004558849

Speedup = 8.004558849 / 3.69313736 = 2.167414333