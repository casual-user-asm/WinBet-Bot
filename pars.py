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
# options = Options()
# options.binary_location = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
# browser = webdriver.Firefox(executable_path='C:\\Users\\Влад\\Desktop\\some\\python_projects\\WinBet_Bot\\firefoxdriver\\geckodriver.exe', options=options)

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

# Function to determine the matches that are already going, and then we call the function to find the page with the live broadcast of the match.
def current_match():
    
    url = 'https://dota2.ru/esport/matches/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}
    response = requests.get(url, headers=headers)
    src = response.text
    soup = BeautifulSoup(src, "html.parser")
    all_matches = soup.find('div', class_='cybersport-matches__block esport-match').find_all('div', class_='cybersport-matches__matches-match list-match-item')

    current_matches = []
    for num in range(len(all_matches)):
        for match in all_matches:
            if match.find('span', class_='esport-match-duration-dynamic') or match.find('span', class_='cybersport-matches__matches-games-count'):
                match_name = match.find('div', class_='cybersport-matches__matches-block cybersport-matches__matches-block-left').find('p', class_='cybersport-matches__matches-name').text
                match_name2 = match.find('div', class_='cybersport-matches__matches-block cybersport-matches__matches-block-right').find('p', class_='cybersport-matches__matches-name').text
                current_match_name = f'{match_name} {match_name2}'
                if current_match_name in current_matches:
                    break
                else:
                    current_matches.append(current_match_name)


    formatted_match_name = []
    for match in current_matches:
        formatted_match_name.append(' '.join(current_matches).replace(' ', '').lower())
    
    return live_broadcast_page(formatted_match_name)

# In this function, we find the page with the live broadcast of the match and go to it, and then we call the function to collect data about the set of heroes in each team.
def live_broadcast_page(match_name):
    
    while True:
        try:
            if len(match_name) < 1:
                return 'There are no matches now'
                break
                
            browser.get('https://hawk.live/ru')
            browser.implicitly_wait(10)
                    
            all_current_matches = []
            formatted_current_matches = []
            current_matches = browser.find_element(By.CLASS_NAME, 'series-list')
            for match in current_matches.find_elements(By.CLASS_NAME, 'series-teams-item__name'):
                all_current_matches.append(match.text)

            
            while len(all_current_matches) > 0:
                match = f'{all_current_matches[0]} {all_current_matches[1]}'
                formatted_current_matches.append(match.lower())
                del all_current_matches[0:2]
            
            for match1 in match_name:
                for num,match in enumerate(formatted_current_matches):
                    if match1 == match.replace(' ', ''):
                        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[1]/div/div/div/main/div/div/div[3]/div/div[{num+1}]/a'))).click()
                        
                        match_score = browser.find_element(By.CLASS_NAME, 'series-teams__primary-label').text
                        type_of_series = browser.find_element(By.CLASS_NAME, 'series-teams__secondary-label').text
                        
                        if type_of_series == 'BO3':
                            if match_score == '0 - 0':
                                return hero_set()
                            elif match_score == '1 - 0' or match_score == '0 - 1':
                                WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[2]/button/span[3]'))).click()
                                WebDriverWait(browser, 50).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/a[2]/div/div'))).click()
                                return hero_set()
                            elif match_score == '1 - 1':
                                WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[2]/button/span[3]'))).click()
                                WebDriverWait(browser, 50).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/a[3]/div/div'))).click()
                                return hero_set()
                        if type_of_series == 'BO5':
                            if match_score == '0 - 0':
                                return hero_set()
                            elif match_score == '1 - 0' or match_score == '0 - 1':
                                WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[2]/button/span[3]'))).click()
                                WebDriverWait(browser, 50).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/a[2]/div/div'))).click()
                                return hero_set()
                            elif match_score == '1 - 1' or match_score == '2 - 0' or match_score == '0 - 2':
                                WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[2]/button/span[3]'))).click()
                                WebDriverWait(browser, 50).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/a[3]/div/div'))).click()
                                return hero_set()
                            elif match_score == '2 - 1' or '1 - 2':
                                WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[2]/button/span[3]'))).click()
                                WebDriverWait(browser, 50).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/a[4]/div/div'))).click()
                                return hero_set()
                            elif match_score == '2 - 2':
                                WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[2]/button/span[3]'))).click()
                                WebDriverWait(browser, 50).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/a[5]/div/div'))).click()
                                return hero_set()
                    else:
                        continue
            break
        except Exception as e:
            print(e)
            continue

# A function for collecting the heroes whose teams have chosen, then we call the function to issue a prediction for which team has a better set of heroes.
def hero_set():
    
    team_name = browser.find_elements(By.CLASS_NAME, "match-view-team__name")
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
    browser.quit()
    
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
        return "The game hasn't started yet"
    elif first_team_advantage_counter == second_team_advantage_counter:
        return emoji.emojize(":scream_cat:") + 'Both team have equal good picks of heroes'
    elif first_team_advantage_counter > second_team_advantage_counter:
        return emoji.emojize(":green_circle:") + f'In game {team_names[0]} vs {team_names[1]}\n\n' + emoji.emojize(":crystal_ball:") + f'{team_names[0]} has better pick'
    else:
        return emoji.emojize(":green_circle:") + f'In game {team_names[0]} vs {team_names[1]}\n\n' + emoji.emojize(":crystal_ball:") + f'{team_names[1]} has better pick'


if __name__ == '__main__':
    current_match()
