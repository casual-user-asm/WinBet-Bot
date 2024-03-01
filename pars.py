from bs4 import BeautifulSoup
import requests
from schedule_matches import matches_schedule

info_for_def = matches_schedule()
current_matches = info_for_def[1]
heroes_info = info_for_def[2]
live_match = info_for_def[3]


def prediction(hero_set, live_match):

    first_team_hero_winrate = {}
    second_team_hero_winrate = {}
    first_team_heroes_winrate_stats = []
    second_team_heroes_winrate_stats = []

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}
    for v in hero_set.values():
        first_set = v[:5]
        second_set = v[5:]

        for heroes in first_set:
            new_format = heroes.split(' ')
            url_heroes = 'https://dotabuff.com/heroes/' + '-'.join(new_format).lower() + '/counters'
            response = requests.get(url_heroes, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            first_team_hero_winrate[heroes] = []
            table = soup.find('table', class_='sortable')
            for row in table.find_all('tr')[1:]:
                cols = row.find_all('td')
                hero_name = cols[1].get_text()
                winrate_procent = cols[2].get_text()
                hero_stats = hero_name + ' ' + winrate_procent
                first_team_hero_winrate[heroes].append(hero_stats)

        for heroes in second_set:
            try:
                new_format = heroes.split(' ')
                url_heroes = 'https://dotabuff.com/heroes/' + '-'.join(new_format).lower() + '/counters'
                response = requests.get(url_heroes, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                second_team_hero_winrate[heroes] = []
                table = soup.find('table', class_='sortable')
                for row in table.find_all('tr')[1:]:
                    cols = row.find_all('td')
                    hero_name = cols[1].get_text()
                    winrate_procent = cols[2].get_text()
                    hero_stats = hero_name + ' ' + winrate_procent
                    second_team_hero_winrate[heroes].append(hero_stats)
            except AttributeError:
                pass

        for hero in first_set:
            for hero_2 in second_set:
                for winrate_stats in first_team_hero_winrate[hero]:
                    if hero_2 in winrate_stats:
                        hero_stats = winrate_stats.split(' ')
                        if len(hero_stats) > 2:
                            first_team_heroes_winrate_stats.append(hero_stats[2])
                        else:
                            first_team_heroes_winrate_stats.append(hero_stats[1])

        for hero in second_set:
            for hero_2 in first_set:
                for winrate_stats in second_team_hero_winrate[hero]:
                    if hero_2 in winrate_stats:
                        hero_stats = winrate_stats.split(' ')
                        if len(hero_stats) > 2:
                            second_team_heroes_winrate_stats.append(hero_stats[2])
                        else:
                            second_team_heroes_winrate_stats.append(hero_stats[1])

    formatted_matches_name = []
    for format in live_match:
        formatted_matches_name.append(format.split('-'))

    result_list = []
    for teams in formatted_matches_name:
        first_team_advantage_counter = 0
        second_team_advantage_counter = 0
        for advantage in first_team_heroes_winrate_stats:
            if '-' in advantage:
                first_team_advantage_counter += 1
        for advantage in second_team_heroes_winrate_stats:
            if '-' in advantage:
                second_team_advantage_counter += 1

        if first_team_advantage_counter > second_team_advantage_counter:
            result_list.append(f'{teams[0]} team has more chances')
        elif first_team_advantage_counter == second_team_advantage_counter:
            result_list.append('Both teams have equal chances')
        else:
            result_list.append(f'{teams[1]} team has more chances')

    return result_list


if __name__ == '__main__':
    prediction(heroes_info, live_match)
