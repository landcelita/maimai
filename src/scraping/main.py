import parse
import curl
import ds
from datetime import datetime
from bs4 import BeautifulSoup
import requests

def main():
    cu = curl.Curl()
    cu.login()
    cu.select_aime()
    
    response = cu.record()
    soup = BeautifulSoup(response.text, 'html.parser')
    records = parse.record(soup)
    
    datasource = ds.DS()
    latest_record = datasource.read_latest_record()
    # プレイ履歴がなかった場合は古いダミーの時刻を入れる
    if latest_record is None:
        latest_record = {'played_at': datetime(1980, 1, 1, 0, 0, 0)}
    
    # 逆順(古い順)にレコードをみていく
    for record in reversed(records):
        if record.play_dt <= latest_record['played_at']:
            continue
        response = cu.playlog_detail(record.url_idx)
        soup = BeautifulSoup(response.text, 'html.parser')
        detail = parse.playlog_detail(soup)

if __name__ == '__main__':
    main()