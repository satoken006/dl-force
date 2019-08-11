# -*- Coding: utf-8 -*-

import urllib.request, urllib.error
from bs4 import BeautifulSoup

from const import MEMBERS, MEMBERS_EN
from RepositoryParser import RepositoryParser
from JSONWriter import JSONWriter

parser = RepositoryParser()
writer = JSONWriter()
RANGE = 194
### For test run ###
# RANGE = 91

for i in range(1, RANGE + 1):
    # Connect to the Web and get HTML
    try:
        html = urllib.request.urlopen("http://dl.nkmr-lab.org/papers/" + str(i))
        print(str(i) + " / " + str(RANGE))
    except urllib.error.HTTPError as e:
        continue
    except NameError as e:
        continue

    soup = BeautifulSoup(html, "lxml")
    parser.add_authors_and_edges(soup)


repositoryJSON = parser.getResult()

print("result: ")
print(repositoryJSON)

JSONWriter.export(repositoryJSON, "output.json")