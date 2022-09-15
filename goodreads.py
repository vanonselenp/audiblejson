from re import S
from lxml import html
import requests

import json
import sys

base_url = "https://www.goodreads.com/"

def get_page(url):
    page = requests.get(url)
    text = page.text
    return html.fromstring(text)

def get_books(tree):
    result = []
    books = tree.xpath('//tr[@itemtype="http://schema.org/Book"]')
    for book in books:
        tds = book.getchildren()
        title = tds[0].getchildren()[1].values()
        rating = tds[1].getchildren()[5].getchildren()[0].getchildren()[0].getchildren()[0].tail.split('—')[1].split(' ')
        result.append({
            "title": title[0],
            "url": "%s%s" % (base_url, title[1]),
            "rating": rating[0],
            "#ratings": int("".join(rating[1].split(',')))
        })
    return result

def get_next_page(page):
    next = page.xpath('//a[@class="next_page"]')[0]
    return "%s%s" % (base_url, next.values()[2])
    
def download_all_books(url, filename):
    page = get_page(url)
    books = []
    counter = 0;

    while(True):
        books.extend(get_books(page))
        try:
            x = get_next_page(page)
        except Exception as e:
            print(e)
            break
        page = get_page(x)
        counter += 1
        print(counter)

    print(len(books))
    with open('books.json', 'w') as f:
        f.write(json.dumps(books))

def load_and_sort(filename):
    with open(filename, 'r') as f:
        data = json.loads(f.read())

    def sorter(element):
        return element["#ratings"]
    
    data.sort(reverse=True, key=sorter)
    print(json.dumps(data))

if __name__ == "__main__":
    print(sys.argv)

    try:
        command = sys.argv[1]
    except:
        command = 'help'

    if command == 'load':
        try:
            url = sys.argv[2]
        except:
            url = 'https://www.goodreads.com/search?q=watercolor&qid='

        try:
            filename = sys.argv[3]
        except:
            filename = 'books.json'

        download_all_books(url, filename)
        exit(0)

    if command == 'sort':
        try:
            filename = sys.argv[2]
        except:
            filename = 'books.json'
            
        load_and_sort(filename)
        exit(0)

    print("Usage: \n    load url filename\n    sort filename")
