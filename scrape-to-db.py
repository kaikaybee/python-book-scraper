import re
import requests
import sqlite3
from bs4 import BeautifulSoup
from pathlib import Path
from sqlite3 import Error

# SQL queries specific to books.db
QUERIES = {
  'all_reviews':
    '''
        select * from reviews
    ''',
  'create_reviews':
    '''
        insert into reviews
        values(?,?,?)
    ''',
  'find_reviews_by_name':
    '''
        select * from reviews
        where name = ?
    '''
}

# Initializes db/table, creates methods from QUERIES
class Books_db:
    def __init__(self, QUERIES):
        self.connection = self.create_connection()
        self.create_table()
        for method in QUERIES:
            self.add_method(method, QUERIES[method])
        
    def add_method(self, method, query):
        query = re.sub('^\n+|\s+$', '', query) + ';'
        def hydrate_and_execute(values = None):
            try:
                self.connection.execute(query, values)
                self.connection.commit()
            except Error as e:
                print('ERROR WHILE ATTEMPTING:')
                print(query, '? =', values)
                print('...' + str(e))
        setattr(self, method, hydrate_and_execute)

    def create_connection(self):
        connection = None
        path = Path(__file__).parent / 'books.db'
        try:
            connection = sqlite3.connect(path)
            print('connection successful')
        except Error as e:
            print('ERROR: ' + str(e))
        return connection
    
    def create_table(self):
        string = '''CREATE TABLE IF NOT EXISTS 'reviews' (
            [name] TEXT PRIMARY KEY,
            [date] TEXT,
            [url] TEXT
        );
        '''
        self.connection.execute(string)


# Required for accessing websites
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36'
}

# Initialize Table
db = Books_db(QUERIES)

# Start loop
title = ''
num = 1
URL = 'https://slatestarcodex.com/tag/book-review/'
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
title = soup.title.text
while title.startswith('Page not found') == False:
    print('getting page ' + str(num) + '...')

    # Get/format data
    entry = soup.find(class_='entry-title')

    entry_title = entry.text.strip()
    if entry_title.startswith('Book'):
        if entry_title.startswith('Book Review: '):
            entry_title = entry_title[13:]
        elif entry_title.startswith('Book Review and Highlights: '):
            entry_title = entry_title[28:]

    entry_url = entry.find('a')['href']

    date = soup.find(class_='entry-date').text.strip()

    # Add data to table
    tup = (entry_title, date, entry_url)
    db.create_reviews(tup)

    # Iterate
    num += 1
    URL = 'https://slatestarcodex.com/tag/book-review/' + 'page/' + str(num) + '/'
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.title.text

print('done!')