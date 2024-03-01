from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import requests

options = Options()
options.headless = True
driver = webdriver.Firefox()
actions = ActionChains(driver)
url = 'https://cyberscore.live/en/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}
response = requests.get(url, headers=headers)
driver.get(url)


element_present = EC.presence_of_element_located((By.CLASS_NAME, 'live-informer'))
WebDriverWait(driver, 15).until(element_present)

src = driver.page_source
soup = BeautifulSoup(src, 'html.parser')


def matches_schedule():

    live_matches = []
    upcoming_matches = []
    game_info = {}
    all_matches = soup.find_all('a', class_='matches-item')
    for i in all_matches:
        if i.find('i', class_='live-informer'):
            match_title = i.find_all('span', class_='show-on-mb')
            new_list = [span.text for span in match_title]
            formatted_title = f"{' - '.join(new_list)}"
            game_info[f"{' - '.join(new_list)}"] = []
            live_matches.append(formatted_title)
            link_on_match = f"https://cyberscore.live{i.get('href')}"

            response2 = requests.get(link_on_match, headers=headers)
            src2 = response2.text
            soup2 = BeautifulSoup(src2, "html.parser")
            walter = soup2.find_all('div', {'data-tooltip-html': True})
            for element in walter:
                try:
                    tooltip_html = element['data-tooltip-html']
                    tooltip_soup = BeautifulSoup(tooltip_html, 'html.parser')

                    if tooltip_soup.find('b').find_next('i').previous_sibling:
                        hero_name = tooltip_soup.find('b').find_next('i').previous_sibling.text
                        game_info[formatted_title].append(hero_name.strip())
                    else:
                        continue
                except AttributeError:
                    pass

        else:

            if i.find('b'):

                schedule = i.find_all('b')
                schedule_data = [r.text for r in schedule]
                match_title2 = i.find_all('span', class_='show-on-mb')
                new_list2 = [span.text for span in match_title2]
                upcoming_title = f"{' - '.join(new_list2)} starts in {''.join(schedule_data)}"
                upcoming_matches.append(upcoming_title)

            else:
                if i.find('time').text == 'Today':
                    schedule = i.find_all('time')
                    schedule_data = [r.text for r in schedule]
                    schedule_time = schedule_data[2]
                    match_title = i.find_all('span', class_='show-on-mb')
                    new_list = [span.text for span in match_title]
                    upcoming_title = f"{' - '.join(new_list)} starts at {''.join(schedule_time)}"
                    upcoming_matches.append(upcoming_title)

    cleaned_dict = {key: [item.strip() for item in value if item.strip()] for key, value in game_info.items()}
    clean_list = []
    for k, v in cleaned_dict.items():
        if v:
            for data in v:
                cleaned_data = data.replace('(', '').replace(')', '')
                clean_list.append(cleaned_data)
            cleaned_dict[k] = clean_list

    final_live_match_list = []
    final_live_match_dict = {}
    for i in live_matches:
        if cleaned_dict[i]:
            final_live_match_list.append(i)
    counter = 0
    counter2 = 10
    for w in final_live_match_list:
        final_live_match_dict[w] = cleaned_dict[final_live_match_list[0]][counter:counter2]
        counter2 += 10
        counter += 10

    driver.quit()

    return upcoming_matches, live_matches, final_live_match_dict, final_live_match_list
