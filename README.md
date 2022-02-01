# Python Book Scraper and SQLite wrapper

Scrapes the website https://slatestarcodex.com for book reviews, and complies them into a database where each record 
holds:

1. Book name
2. Date of review
3. URL to review

Includes two versions, one that writes to a CSV file and one that writes to an SQLite database, implementing a wrapper 
that converts Python strings into SQLite queries

Important packages include:

1. [requests](https://docs.python-requests.org/en/master/)
2. [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
3. [sqlite3](https://docs.python.org/3/library/sqlite3.html)

## Usage
1. Clone repo
2. To scrape to csv:
  - Run `python3 scrape-to-csv.py`
  - View output in preferred editor
  - Verify output against `books-answer.csv`
3. To scrape to db:
  - Run `python3 scrape-to-db.py`
  - View output in a db viewer that is compatible with SQLite or to view in cli:
    - Open with `sqlite3 books.db`
    - `.mode column .headers on`
    - `.select * from reviews;`
  - Verify output against with `books-answer.db`
