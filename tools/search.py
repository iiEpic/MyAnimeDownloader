
import re
import os
import sys
import json
import requests
from bs4 import BeautifulSoup


class Search:
    def __init__(self, settings):
        self.base_url = "https://www.wcostream.com"
        self.cache_path = sys.argv[0].replace('__main__.py', '').replace('__main__.exe', '') + 'resources' + os.sep +\
            'cache.json'
        self.main_dict = {}
        self.settings = settings
        if os.path.exists(self.cache_path):
            # Load up the settings
            with open(self.cache_path) as file:
                self.main_dict = json.load(file)

    def start(self, get_url=None, find_me=None, cached=True):
        print('Getting information...')
        if get_url is None:
            get_url = input('Is this [(S)ubbed/(D)ubbed/(C)artoon]: ')

        if find_me is None:
            find_me = input('Input the show you are looking for: ')

        if '--no-cache' in get_url:
            cached = False
            get_url = get_url.replace('--no-cache', '')

        if get_url.lower() in ['', 's', 'sub', 'subbed']:
            url = "https://www.wcostream.com/subbed-anime-list"
            json_search = 'subbed'
        elif get_url.lower() in ['d', 'dub', 'dubbed']:
            url = "https://www.wcostream.com/dubbed-anime-list"
            json_search = 'dubbed'
        else:
            url = "https://www.wcostream.com/cartoon-list"
            json_search = 'cartoon'

        if not cached:
            find_me = find_me.replace(' ', '-').lower()
            return self.pull_from_url(url, find_me)
        else:
            # Lets use the JSON
            p_array = []
            for k, v in self.main_dict.items():
                if json_search == v['type']:
                    if find_me.lower() in k.lower():
                        p_array.append(
                            '{0} - {1} - {2}'.format(
                                k, self.settings.get_season_display(v['seasons']), v['url']))
            return p_array

    def pull_from_url(self, url, find_me):

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        episode_container = soup.findAll('div', {'class': 'ddmcc'})

        anime_list = []
        results = 0
        for container in episode_container:
            shows = container.findAll('a')
            for show in shows:
                if results >= 1000:
                    print('Search results are greater than 10. Please be more specific.')
                    break
                try:
                    if 'anime' in show['href']:
                        # show_name = show['href'].replace('/anime/', '').replace('-', ' ').title().strip()
                        if find_me.startswith("^"):
                            if re.findall('^/anime/{0}'.format(find_me[1]), show['href']):
                                anime_list.append(show['href'])
                                results += 1
                        else:
                            if re.findall(find_me, show['href']):
                                anime_list.append(show['href'])
                                results += 1
                except:
                    pass

        info_array = []
        for anime in anime_list:
            try:
                results = self.get_show_seasons(self.base_url + anime)
            except:
                print('[Fatal Error]: Skipping {0}'.format(anime))
                pass
            info_array.append('{0} - {1} - {2}'.format(anime.replace('/anime/', '').replace('-', ' ').title().strip(),
                                                       self.get_total_episodes_str(results),
                                                       self.base_url + anime))
            if self.settings.get_setting('saveSearchToCache'):
                # print('Saving show to cache...')
                self.update_cache(self.base_url + anime, results)
        return info_array

    @staticmethod
    def get_total_episodes_str(results):
        total = 0
        for key, value in results.items():
            total += int(value)
        return '{0} Seasons, {1} Episodes'.format(len(results), total)

    @staticmethod
    def get_total_episodes( results):
        total = 0
        for key, value in results.items():
            total += int(value)
        return len(results), total

    @staticmethod
    def get_show_seasons(url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        episode_links = soup.findAll('a', {'class': 'sonra'})
        seasons = {}

        highest_season = 100
        highest_episode = 0
        for episode in episode_links:
            try:
                if 'special' in episode['href'] or 'ova' in episode['href'] or 'movie' in episode['href'] \
                        or 'episode' not in episode['href']:
                    continue
                if 'season' in episode['href']:
                    result = re.search('-season-([0-9]+)-episode-([0-9]+)', episode['href'])
                    if int(result.group(1)) < highest_season:
                        highest_season = int(result.group(1))
                        if highest_season not in seasons:
                            seasons[str(highest_season)] = int(result.group(2))
                else:
                    result = re.search('-episode-([0-9]+)', episode['href'])
                    if int(result.group(1)) > highest_episode:
                        highest_episode = int(result.group(1))
            except:
                pass
        if '1' not in seasons:
            seasons['1'] = highest_episode
        return seasons

    def update_cache(self, url, season_info):

        try:
            show_info = {}
            show_name = re.search('/anime/(.*)', url).group(1).replace('-', ' ').title().strip()

            if 'subbed' in url:
                show_info['type'] = 'subbed'
            elif 'dubbed' in url:
                show_info['type'] = 'dubbed'
            else:
                show_info['type'] = 'cartoon'

            show_info['seasons'] = season_info
            show_info['url'] = url
            show_info['download_location'] = ''
            if show_name not in self.main_dict.keys():
                self.main_dict[show_name] = show_info
            else:
                self.main_dict.pop(show_name)
                self.main_dict[show_name] = show_info
        except:
            # Well we missed one.. whoops..
            pass
        file = open(self.cache_path, 'w')
        file.write(json.dumps(self.main_dict, indent=4, sort_keys=True))
        file.close()
