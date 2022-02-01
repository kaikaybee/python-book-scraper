import csv
import requests
import re
from bs4 import BeautifulSoup
from pathlib import Path

# User agent taken from FireFox browser GET request. If I don't use this I'll get a 403 Forbidden error
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0'
}

titles = []
urls = []
dates = []

# Prepare loop
title = ''
num = 1
URL = 'https://slatestarcodex.com/tag/book-review/' # first page
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
title = soup.title.text

while title.startswith('Page not found') == False:
    print('Getting page ' + str(num) + '...')

    # Get data from page
    posts = soup.find(id="pjgm-content").find_all(id=re.compile("^post.*"))
    for post in posts:
        reviewTitle = post.h2.a.text
        reviewLink = post.h2.a.get('href')
        reviewDate = post.find(class_="pjgm-postmeta").a.text

        # Format book title
        split = reviewTitle.split(': ', maxsplit=1)
        if len(split) > 1:
            bookTitle = split[1]
        else:
            bookTitle = split[0]

        # Store data in arrays
        titles.append(bookTitle)
        urls.append(reviewLink)
        dates.append(reviewDate)

    # Iterate
    num += 1
    URL = 'https://slatestarcodex.com/tag/book-review/' + 'page/' + str(num) + '/'
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.title.text
  
# Write to CSV
print('Writing to CSV...')
path = Path(__file__).parent / 'books.csv'
with open(path, mode='w') as book_file:
    book_writer = csv.writer(book_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    book_writer.writerow(['Name', 'Date', 'URL'])
    for i in range(len(titles)):
        book_writer.writerow([titles[i], dates[i], urls[i]])

print('Done!')