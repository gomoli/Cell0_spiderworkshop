#! /usr/bin/python3 -tt

import urllib.request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from collections import deque
import re
import time
from datetime import datetime
import locale

locale.setlocale(locale.LC_ALL,'nl_NL.utf-8')
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
starttime = time.time()

for start_url in start_urls:
    time.sleep(2)
    ufp = urllib.request.urlopen(start_url)
    html = ufp.read()

    soup = BeautifulSoup(html,'lxml')
    content = soup.find('div', class_="column first")
    links = content.findAll("a", attrs={"href":re.compile("/[^/]+/\d+/[^/]+\.html")})

    for link in links:
        queue_urls(base_url + link['href'])

while len(urls_todo) > 0:
    url = urls_todo.popleft()
    time.sleep(2)
    print('GET :  %s' % url)
    ufp = urllib.request.urlopen(url)
    html = ufp.read()
    if not html:
        print('FAILED : %s' % url)
        continue
    soup = BeautifulSoup(html, "lxml")
    
    title = soup.find("div", class_="title").get_text(strip=True)
    date = soup.find("span", class_="published").find_next("span", class_="large").get_text()
    result = soup.find("div", attrs={"data-type":"article.body"}).find_next("div", class_="block-content").get_text(strip=True)

    print("\n%s" % title)
    print("%s\n" % date)
    print("\t%s\n" % result)
    
    file = title+"\n"+date+"\n"+result
    filename = datetime.strptime(date,'%d %B %Y %H:%M').isoformat()+".txt"

    with open(filename, 'w') as f:
        f.write(file)

    urls_done.add(url)

runtime = time.time() - starttime
print("Done with run in %d seconds!"%runtime)
