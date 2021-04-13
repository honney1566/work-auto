# importing the module
from googlesearch import search
import pandas as pd
from urllib.request import urlopen
import re
import requests
from requests import get
from bs4 import BeautifulSoup

# stored queries in a list
query_list = [" buy"]
a = []
b=[]
URLlist = pd.DataFrame({'ID': ()})
URLcrawled=pd.DataFrame({'ID':()})
EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""



# save the company name in a variable
def searher():
    company_name = input("Please provide the stock name:")
    # iterate through different keywords, search and print
    for j in query_list:
        for i in search(company_name + j, lang='en'):
            a.append(i)


searher()
URLlist.insert(1, 'Name', pd.Series(a))
del URLlist['ID']
print(URLlist)
for x in URLlist['Name'].tolist():
    try:
    #urlopen.add_header('Referer', 'http://www.python.org/')
    #data = urlopen(x)
        soup = BeautifulSoup(urlopen(x,),features="lxml",)
        print('tik')
        for link in soup.find_all('a'):
            try:
                b.append(link.get('href'))
            except:
                pass
    except:
        pass

URLcrawled.insert(1,"URL", pd.Series(b))
del URLcrawled['ID']
URLcrawled = URLcrawled[~URLcrawled['URL'].isin(['youtube', 'google','instagram','facebook','linkedin','twitter'])]
print(URLcrawled)

URLcrawled.to_csv(r'C:\Users\Eduard\Desktop\export.csv')