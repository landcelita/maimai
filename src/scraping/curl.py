import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests
from requests import Session, Response
from bs4 import BeautifulSoup
import time

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

LOGIN_URL = 'https://maimaidx.jp/maimai-mobile/'
LOGIN_POST_URL = 'https://maimaidx.jp/maimai-mobile/submit/'
AIME_URL = 'https://maimaidx.jp/maimai-mobile/aimeList/submit/?idx=0'
RECORD_URL = 'https://maimaidx.jp/maimai-mobile/record/'
PLAYLOG_DETAIL_URL = 'https://maimaidx.jp/maimai-mobile/record/playlogDetail/?idx={}'
AIME_INDEX = 0

class Curl:
    def __init__(self):
        self.session = requests.session()
        
    def __del__(self):
        self.session.close()

    def login(self) -> Response:
        SEGAID = os.environ.get("SEGAID")
        PASSWORD = os.environ.get("PASSWORD")
        
        response = self.session.get(LOGIN_URL, verify='./GlobalSign.crt')
        time.sleep(1.)
        soup = BeautifulSoup(response.text, 'html.parser')
        authenticity = soup.find(attrs={'name':'token'}).get('value')

        info = {
            "token": authenticity,
            "segaId": SEGAID,
            "password": PASSWORD,
        }
        res = self.session.post(LOGIN_POST_URL, data=info)
        time.sleep(1.)
        return res

    def select_aime(self) -> Response:
        res = self.session.get(AIME_URL)
        time.sleep(1.)
        return res

    def record(self) -> Response:
        res = self.session.get(RECORD_URL)
        time.sleep(1.)
        return res
    
    def playlog_detail(self, idx: int) -> Response:
        res = self.session.get(PLAYLOG_DETAIL_URL.format(idx))
        time.sleep(1.)
        return res
    
# if __name__ == '__main__':
#     curl = Curl()
#     curl.login()
#     curl.select_aime()
#     curl.record()
