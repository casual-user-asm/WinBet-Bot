from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
import requests
import emoji
import os

# Settings to use Firefox with Selenium.
options = Options()
options.binary_location = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
browser = webdriver.Firefox(executable_path='C:\\Users\\Влад\\Desktop\\some\\python_projects\\WinBet_Bot\\firefoxdriver\\geckodriver.exe', options=options)
# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
# browser = webdriver.Chrome()


# A function for collecting the heroes whose teams have chosen, then we call the function to issue a prediction for which team has a better set of heroes.
def hero_set():
    browser.get('https://hawk.live/ru/matches/86539')
    team_name = browser.find_elements(By.CLASS_NAME, "series-teams-item__name")
    team_names = [i.text for i in team_name]
    
    info_about_heroes = browser.find_elements(By.CLASS_NAME, 'match-view-draft-team')
    hero_set = []
    for hero in info_about_heroes:
        if hero.find_element(By.TAG_NAME, 'img').get_attribute('alt') == "Логотип Dota 2 на темном фоне":
            break
        elif hero.find_element(By.TAG_NAME, 'img').get_attribute('alt') in hero_set:
            break
        else:
            hero_set.append(hero.find_element(By.TAG_NAME, 'img').get_attribute('alt'))
    
    first_team_hero_set = hero_set[:5]
    second_team_hero_set = hero_set[5:]
    
    return prediction(first_team_hero_set, second_team_hero_set, team_names)

# This function calculates which team has the best set of heroes based on statistics about each hero.
def prediction(first_team_heroes, second_team_heroes, team_names):
    
    first_team_hero_winrate = {}
    second_team_hero_winrate = {}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}
    for hero in first_team_heroes:
        new_format = hero.split(' ')
        url_heroes = 'https://ru.dotabuff.com/heroes/' + '-'.join(new_format).lower() + '/counters'
        response = requests.get(url_heroes, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        first_team_hero_winrate[hero] = []
        table = soup.find('table', class_='sortable')
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            hero_name = cols[1].get_text()
            winrate_procent = cols[2].get_text()
            hero_stats = hero_name + ' ' + winrate_procent
            first_team_hero_winrate[hero].append(hero_stats)
    
    for hero in second_team_heroes:
        new_format = hero.split(' ')
        url_heroes = 'https://ru.dotabuff.com/heroes/' + '-'.join(new_format).lower() + '/counters'
        response = requests.get(url_heroes, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        second_team_hero_winrate[hero] = []
        table = soup.find('table', class_='sortable')
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            hero_name = cols[1].get_text()
            winrate_procent = cols[2].get_text()
            hero_stats = hero_name + ' ' + winrate_procent
            second_team_hero_winrate[hero].append(hero_stats)
    
    first_team_heroes_winrate_stats = []
    for hero in first_team_heroes:
        for hero_2 in second_team_heroes:
            for winrate_stats in first_team_hero_winrate[hero]:
                if hero_2 in winrate_stats:
                    hero_stats = winrate_stats.split(' ')
                    if len(hero_stats) > 2:
                        first_team_heroes_winrate_stats.append(hero_stats[2])
                    else:
                        first_team_heroes_winrate_stats.append(hero_stats[1])
    
    second_team_heroes_winrate_stats = []
    for hero in second_team_heroes:
        for hero_2 in first_team_heroes:
            for winrate_stats in second_team_hero_winrate[hero]:
                if hero_2 in winrate_stats:
                    hero_stats = winrate_stats.split(' ')
                    if len(hero_stats) > 2:
                        second_team_heroes_winrate_stats.append(hero_stats[2])
                    else:
                        second_team_heroes_winrate_stats.append(hero_stats[1])
    
    first_team_advantage_counter = 0
    second_team_advantage_counter = 0
    for advantage in first_team_heroes_winrate_stats:
        if '-' in advantage:
            first_team_advantage_counter += 1
    for advantage in second_team_heroes_winrate_stats:
        if '-' in advantage:
            second_team_advantage_counter += 1
    
    if first_team_advantage_counter == 0:
        print(f"The game {team_names[0]} vs {team_names[1]} hasn't started yet")
    elif first_team_advantage_counter == second_team_advantage_counter:
        print('Both team have equal good draft')
    elif first_team_advantage_counter > second_team_advantage_counter:
        print(emoji.emojize(":green_circle:") + f'In game {team_names[0]} vs {team_names[1]}\n\n' + emoji.emojize(":crystal_ball:") + f'{team_names[0]} has better pick')
    else:
        print(emoji.emojize(":green_circle:") + f'In game {team_names[0]} vs {team_names[1]}\n\n' + emoji.emojize(":crystal_ball:") + f'{team_names[1]} has better pick')

browser.get('https://hawk.live/ru/matches/86539')
team_name = browser.find_elements(By.CLASS_NAME, "match-view-team__name")
team_names = [i.text for i in team_name]
print(team_names)
