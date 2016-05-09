#! /usr/bin/python3 

import urllib.request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from collections import deque
import re

urls_todo = deque()
urls_done = set()

def queue_urls(add_urls, last_url=None):
    if type(add_urls) == str:
        add_urls = [add_urls]
        if add_urls:
            for add_url in set(add_urls):
                if last_url:
                    # If the url is not a complete and valid url this will
                    # create a valid url for that website.
                    add_url = urljoin(last_url, add_url)
                if (add_url not in urls_done) and (add_url not in urls_todo):
                    print('\tQueued: %s' % add_url)
                    urls_todo.append(add_url)

base_url = 'http://www.nu.nl'
start_urls = ['http://www.nu.nl']

for start_url in start_urls:
    ufp = urllib.request.urlopen(start_url)
    html = ufp.read()

    soup = BeautifulSoup(html,'lxml')
    content = soup.find('div', class_="column first")
    links = content.findAll("a", attrs={"href":re.compile("/[^/]+/\d+/[^/]+\.html")})

    for link in links:
        queue_urls(base_url + link['href'])

