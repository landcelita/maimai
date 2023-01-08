import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

# 日付を得るところ
soup = BeautifulSoup(open('record.html'), 'html.parser')
top_containers = soup.find_all('div', class_='playlog_top_container')
print(len(top_containers))
print(top_containers[0])
print(top_containers[0].find_all('span')[1].text)
d = datetime.strptime(top_containers[0].find_all('span')[1].text, "%Y/%m/%d %H:%M")
print(d)