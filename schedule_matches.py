import datetime
from datetime import datetime
import calendar
from bs4 import BeautifulSoup
import requests
import emoji

def schedule_today_matches():
    
    url = 'https://dota2.ru/esport/matches/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}
    response = requests.get(url, headers=headers)
    src = response.text
    soup = BeautifulSoup(src, "html.parser")
    all_matches = soup.find('div', class_='esport-match-future-list').find_all('div', class_='cybersport-matches__matches-match list-match-item')
    
    current_match = []
    date_now = datetime.now()
    formatted_date = datetime.strftime(date_now, "%m.%d.%Y")
    form_date_list = formatted_date.split('.')

    for match in all_matches:
        name = [x.text for x in match.find_all('p', class_='cybersport-matches__matches-name')]
        try:
            time_match = match.find('div', class_='time').text.split('\n')[1].strip()
            data = match.span.text.strip()
            data_list = data.split('.')
            if data_list[0] == form_date_list[1]:
                today_match = f"{time_match} " + emoji.emojize(":man_tipping_hand:") + f" {name[0]} vs {name[1]}"
                current_match.append(today_match)
            else:
                break
        except:
            continue
    
    all_matches_in_string = ''
    for match in current_match:
        all_matches_in_string += emoji.emojize(":alarm_clock:") + f' {match}\n\n'
    
    if len(all_matches_in_string) < 1:
        return 'No matches today'
    else:
        return all_matches_in_string
