from googlesearch import search
import pandas as pd
import requests
from urllib.request import urlopen
import numpy as np
import re
import time
from bs4 import BeautifulSoup
# stored queries in a list
mails=[]
query_list = [" buy"]
i=1
a = []
email=[]
b=[]
c=[]
URLlist = pd.DataFrame({'ID': ()})
URLcrawled=pd.DataFrame({'ID':()})
EMAIL_REGEX = ('\S+@\S+')
# save the company name in a variable
def searher():
    company_name = input("What are we looking for?:")
    for j in query_list:
        for i in search(company_name + j, lang='en'):
            a.append(i)

searher()
URLlist.insert(1, 'Name', pd.Series(a))
del URLlist['ID']
URLlist = URLlist[~URLlist['Name'].str.contains('amazon')]
URLlist = URLlist[~URLlist['Name'].str.contains('ebay')]
URLlist.drop_duplicates('Name')
print('Google search done. Starting to crawl')
for x in URLlist['Name'].tolist():
    try:
    #urlopen.add_header('Referer', 'http://www.python.org/')
    #data = urlopen(x)
        soup = BeautifulSoup(urlopen(x,),features="lxml",)
        for link in soup.find_all('a'):
            try:
                if link.get('href').startswith('/'):
                    b.append(link+link.get('href'))
                elif link.get('href').startswith('java'):
                    pass
                elif link.get('href').startswith('#'):
                    pass
                else:
                    b.append(link.get('href'))

            except:
                pass
    except:
        pass
URLcrawled.insert(1,"URL", pd.Series(b))
del URLcrawled['ID']
print('Tidying up the data')
URLcrawled = URLcrawled[~URLcrawled['URL'].str.contains('youtube')]
URLcrawled = URLcrawled[~URLcrawled['URL'].str.contains('google')]
URLcrawled = URLcrawled[~URLcrawled['URL'].str.contains('instagram')]
URLcrawled = URLcrawled[~URLcrawled['URL'].str.contains('facebook')]
URLcrawled = URLcrawled[~URLcrawled['URL'].str.contains('linkedin')]
URLcrawled = URLcrawled[~URLcrawled['URL'].str.contains('twitter')]
URLcrawled = URLcrawled[~URLcrawled['URL'].str.contains('skimresources')]
URLcrawled['URL'].replace('', np.nan, inplace=True)
URLcrawled.dropna(subset=['URL'], inplace=True)
print('Extracting emails. Will be slow :(')
print(URLcrawled.shape)
for URL in URLcrawled['URL'].tolist():
    try:
        r=requests.get(URL)
        data=r.text
        soup=BeautifulSoup(data,'html.parser')
        for name in soup.find_all('a'):
            if (name is not None):
                emailText = name.text
                match = bool(re.match('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', emailText))
                if ('@' in emailText and match == True):
                    emailText = emailText.replace(" ", '').replace('\r', '')
                    emailText = emailText.replace('\n', '').replace('\t', '')
                    if (len(mails) == 0) or (emailText not in mails):
                        print(emailText)
                    mails.append(emailText)
            #email = soup.find_all(EMAIL_REGEX)[3].text.strip()
    except:
        print("fail")
        mails.append('None')

URLcrawled.insert(1,"Email", pd.Series(mails))
URLcrawled.drop_duplicates(subset='Email')
URLcrawled.to_csv(r'C:\Users\Eduard\Desktop\export.csv')

