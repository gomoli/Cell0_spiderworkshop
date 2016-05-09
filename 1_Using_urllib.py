#! /usr/bin/python3 

import urllib.request
url = 'http://www.nu.nl'

ufp = urllib.request.urlopen(url)

print(ufp.read())
print(ufp.getcode())
