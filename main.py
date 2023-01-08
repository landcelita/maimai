import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import time

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
SEGAID = os.environ.get("SEGAID")
PASSWORD = os.environ.get("PASSWORD")

login_url = 'https://maimaidx.jp/maimai-mobile/'
login_post_url = 'https://maimaidx.jp/maimai-mobile/submit/'
aime_url = 'https://maimaidx.jp/maimai-mobile/aimeList/submit/?idx=0'
record_url = 'https://maimaidx.jp/maimai-mobile/record/'
aime_index = 0

session = requests.session()
response = session.get(login_url, verify='./GlobalSign.crt')
soup = BeautifulSoup(response.text, 'html.parser')
authenticity = soup.find(attrs={'name':'token'}).get('value')
cookie = response.cookies


info = {
    "token": authenticity,
    "segaId": SEGAID,
    "password": PASSWORD,
}
res = session.post(login_post_url, data=info, cookies=cookie)
cookie = res.cookies

res = session.get(aime_url, cookies=cookie)
cookie = res.cookies

res = session.get(record_url, cookies=cookie)
cookie = res.cookies
