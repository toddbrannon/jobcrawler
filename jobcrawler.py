import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

def extract(page):
    headers = {'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    
    search_term = 'nodejs developer'
    search_term = search_term.replace(' ', '+')
    
    url = f'https://www.indeed.com/jobs?q={search_term}&l=southlake,+tx&start={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    divs = soup.find_all('div', class_ = 'job_seen_beacon')
    
    for item in divs:
        title = item.find('h2', class_ = 'jobTitle').text.strip().replace('new', '')
        company = item.find('span', class_ = 'companyName').text.strip()
        location = item.find('div', class_ = 'companyLocation').text.strip()
        try:
            salary = item.find('span', class_ = 'salary-snippet').text.strip()
        except:
            salary = ''
        summary = item.find('div', class_ = 'job-snippet').text.strip().replace('\n', '')
        
        
        job = {
            'title': title,
            'company': company,
            'location': location,
            'salary': salary,
            'summary': summary
        }
        joblist.append(job)
    return

joblist = []

for i in range(0, 40, 10):
    print(f'Getting page {i}')
    c = extract(0)
    transform(c)

df = pd.DataFrame(joblist)
print(df.head())
now = datetime.now()
dt_string = now.strftime("%d%m%y %H%M%S")
path = 'C:\\Users\\toddq\\Development\\Python\\jobcrawler\\exports\\'
df.to_csv(os.path.join(path,'jobs' + dt_string + '.csv'))
