#! /usr/bin/python3 

import urllib.request
from bs4 import BeautifulSoup
import re
import pprint

base_url = 'http://www.nu.nl'
url = 'http://www.nu.nl'

ufp = urllib.request.urlopen(url)

html = ufp.read()

soup = BeautifulSoup(html,'lxml')
content = soup.find('div', class_="column first")
links = content.findAll("a", attrs={"href":re.compile("/[^/]+/\d+/[^/]+\.html")})

for link in links:
    pprint.pprint(base_url + link['href'])
