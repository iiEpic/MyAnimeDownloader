
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

    def start(self):
        get_url = input('Is this [(S)ubbed/(D)ubbed/(C)artoon]: ')
        find_me = input('Input the show you are looking for: ')
        find_me = find_me.replace(' ', '-').lower()

        if get_url.lower() in ['', 's', 'sub', 'subbed']:
            url = "https://www.wcostream.com/subbed-anime-list"
        elif get_url.lower() in ['d', 'dub', 'dubbed']:
            url = "https://www.wcostream.com/dubbed-anime-list"
        else:
            url = "https://www.wcostream.com/cartoon-list"

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        shows = soup.findAll('a')

        s_array = []

        for show in shows:
            try:
                if 'anime' in show['href']:
                    if find_me.startswith("^"):
                        if re.findall('^/anime/{0}'.format(find_me[1]), show['href']):
                            if show['href'] not in s_array:
                                s_array.append(show['href'])
                    else:
                        if re.findall(find_me, show['href']):
                            if show['href'] not in s_array:
                                s_array.append(show['href'])
            except:
                pass

        new_array = []
        for item in s_array:
            new_array.append('{0} - {1} - {2}'.format(item.replace('/anime/', '').replace('-', ' ').title().strip(),
                                                      self.get_episode_count(self.base_url + item),
                                                      self.base_url + item))
        if self.settings.get_setting('saveSearchToCache'):
            self.save_to_cache(new_array)
        return new_array

    @staticmethod
    def get_episode_count(url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        episodes = soup.findAll('a', {'class': 'sonra'})
        message = ''
        for episode in episodes:
            try:
                if 'season' in episode['href']:
                    groups = re.search('season-([0-9]+)', episode['href'])
                    message = "{0} Seasons, {1} Episodes".format(groups.group(1), len(episodes))
                else:
                    message = "{0} Episodes".format(len(episodes))
                return message
            except:
                return 'Unknown'

    def save_to_cache(self, array):
        for item in array:
            show_info = {}
            item_split = item.split(' - ')
            show_name = item_split[0]
            if 'Seasons' in item_split[1]:
                seasons = re.search('^([0-9]+)', item_split[1]).group(1)
                episodes = re.search('Seasons, ([0-9]+) Episodes', item_split[1]).group(1)
                url = item_split[2]
            else:
                seasons = '1'
                episodes = re.search('^([0-9]+)', item_split[1]).group(1)
                url = item_split[2]
            show_info['seasons'] = seasons
            show_info['episodes'] = episodes
            show_info['url'] = url
            if show_name not in self.main_dict.keys():
                self.main_dict[show_name] = show_info

        file = open(self.cache_path, 'w')
        file.write(json.dumps(self.main_dict, indent=4, sort_keys=True))
        file.close()
