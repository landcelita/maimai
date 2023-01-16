from bs4 import BeautifulSoup
import re
from datetime import datetime

class Record:
    def __init__(self, play_dt: datetime, title: str, url_idx: int):
        self.play_dt = play_dt
        self.title = title
        self.url_idx = url_idx
        
    def __repr__(self):
        return f'play_dt: {self.play_dt.strftime("%Y/%m/%d %H:%M")}, title: {self.title}, url_idx: {self.url_idx}'

class Result:
    def __init__(
        self, achievement: float, is_new_record: bool, dx_score: int, max_dx_score: int, fast: int, late: int, notes: dict, max_combo: int, full_combo: int
    ):
        self.achievement = achievement
        self.is_new_record = is_new_record
        self.dx_score = dx_score
        self.max_dx_score = max_dx_score
        self.fast = fast
        self.late = late
        self.notes = notes
        self.max_combo = max_combo
        self.full_combo = full_combo
    
    def __repr__(self):
        return f'achievement: {self.achievement}, is_new_record: {self.is_new_record}, dx_score: {self.dx_score}, max_dx_score: {self.dx_score}, '\
            f'fast: {self.fast}, late: {self.late}, notes: {self.notes}, max_combo: {self.max_combo}, full_combo: {self.full_combo}'

def record(soup: BeautifulSoup) -> list[Record]:
    records = []
    dt_pattern = r'[0-9]{4}/(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01]) ([01][0-9]|2[0-3]):[0-5][0-9]'
    main_wrapper = soup.find('div', class_='main_wrapper')
    playlog_tops = main_wrapper.find_all('div', class_='playlog_top_container')
    
    for top in playlog_tops:
        play_dt_span = top.find('span', text=re.compile(dt_pattern))
        play_dt = datetime.strptime(play_dt_span.text, '%Y/%m/%d %H:%M')
        
        playlog_main = top.next_sibling.next_sibling
        title = playlog_main.find('div', class_='basic_block').text
        idx_value = playlog_main.find('input', {'name': 'idx'})['value']
        url_idx = int(idx_value)
        
        records.append(Record(play_dt, title, url_idx))
        
    return records

def playlog_detail(soup: BeautifulSoup) -> Result:
    achievement_txt = re.findall(r'[1-9]?[0-9].[0-9]{4}', soup.find('div', class_='playlog_achievement_txt').text)
    achievement = float(achievement_txt[0])
    if soup.find('img', class_='playlog_achievement_newrecord') is None:
        is_achievement_newrecord = False
    else:
        is_achievement_newrecord = True
    
    dxscore_text = soup.find('div', class_='playlog_score_block').text.strip()
    dx_score = int(dxscore_text[:dxscore_text.find('/')].strip().replace(',', ''))
    max_dx_score = int(dxscore_text[dxscore_text.find('/')+1:].strip().replace(',', ''))
    
    playlog_fl_divs = soup.find('div', class_='playlog_fl_block').findAll('div', recursive=False)
    fast = int(playlog_fl_divs[0].text)
    late = int(playlog_fl_divs[1].text)
    
    table = soup.find('table', class_='playlog_notes_detail')
    trs = soup.findAll('tr')
    note_types = ['tap', 'hold', 'slide', 'touch', 'break']
    note_judges = ['cp', 'p', 'gr', 'gd', 'ms']
    notes = {note_type: {} for note_type in note_types}
    
    for tr in trs:
        th = tr.find('th')
        if th is None:
            continue
        img_tag = th.find('img')
        if img_tag is None:
            continue
        
        for note_type in note_types:
            if img_tag['src'].find(note_type) != -1:
                break
            
        tds = tr.findAll('td')
        # for td in tdsでとっていく 内容がない場合はNoneを入れる
        for (td, note_judge) in zip(tds, note_judges, strict=True):
            if not str.isdecimal(td.text):
                notes[note_type][note_judge] = None
            else:
                notes[note_type][note_judge] = int(td.text)
        
    maxcombo_str = soup.find('img', attrs={'src': re.compile(r'maxcombo\.png')}).parent.text.strip()
    max_combo = int(maxcombo_str[:maxcombo_str.find('/')])
    full_combo = int(maxcombo_str[maxcombo_str.find('/')+1:])
    
    return Result(achievement, is_achievement_newrecord, dx_score, max_dx_score, fast, late, notes, max_combo, full_combo)
    
if __name__ == '__main__':
    # soup = BeautifulSoup(open('record.html'), 'html.parser')
    # print(record(soup))
    soup = BeautifulSoup(open('amazing_migtyyyy_playlog_detail.html'), 'html.parser')
    print(playlog_detail(soup))