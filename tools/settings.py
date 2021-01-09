#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__author__ = "iEpic"
__email__ = "epicunknown@gmail.com"
"""

import os
import re
import sys
import json
import base64
import string
import random
from version import __version__


class Settings:

    def __init__(self):
        self.loaded_settings = {}
        self.path = sys.argv[0].replace('__main__.py', '').replace('__main__.exe', '') + 'tools' +\
            os.sep + 'settings.json'
        self.cache_path = sys.argv[0].replace('__main__.py', '').replace('__main__.exe', '') + 'resources' +\
            os.sep + 'cache.json'
        if os.path.exists(self.cache_path):
            # Load up the settings
            with open(self.cache_path) as file:
                self.cache = json.load(file)

        # Does settings.json file exist?
        if os.path.exists(self.path):
            # Load up the settings
            with open(self.path) as file:
                self.loaded_settings = json.load(file)
                print('Settings Loaded.')
        else:
            # Lets create a new settings file
            self.loaded_settings['defaultOutputLocation'] = False
            self.loaded_settings['episodePadding'] = 2
            self.loaded_settings['includeShowDesc'] = True
            self.loaded_settings['saveDownloadLocation'] = True
            self.loaded_settings['saveFormat'] = '{show}-S{season}E{episode}-{desc}'
            self.loaded_settings['saveSearchToCache'] = True
            self.loaded_settings['saveShowURL'] = True
            self.loaded_settings['seasonPadding'] = 2
            self.loaded_settings['useKnownDownloadLocation'] = True

            file = open(self.path, 'w')
            file.write(json.dumps(self.loaded_settings, indent=4, sort_keys=True))
            file.close()
            print('Settings have been created!')

    def get_setting(self, setting_name):
        if setting_name in self.loaded_settings:
            return self.loaded_settings[setting_name]

    def set_setting(self, setting_name, setting_value):
        if setting_name in self.loaded_settings:
            self.loaded_settings[setting_name] = setting_value
            file = open(self.path, 'w')
            file.write(json.dumps(self.loaded_settings, indent=4, sort_keys=True))
            file.close()

    def get_show_info(self, show_name=None, url=None, show_type=None):
        for key, value in self.cache.items():
            try:
                if show_name.lower() in key.lower():
                    if show_type == value['type']:
                        return key, value
                if value['url'] == url and show_type == value['type']:
                    return key, value
            except TypeError:
                pass
        return None, None

    def get_shows_by_type(self, show_type):
        shows = []
        for key, value in self.cache.items():
            if isinstance(value, dict):
                if value['type'] == show_type:
                    shows.append(value)
        return shows

    @staticmethod
    def get_season_display(results):
        total = 0
        for key, value in results.items():
            total += int(value)
        return '{0} Seasons, {1} Episodes'.format(len(results), total)

    def create_link(self, url, season, ep_range):
        show_info = self.get_show_info(url=url)
        if int(season) > int(show_info['seasons']):
            print('There are only {0} seasons of this show, not {1} seasons.'.format(show_info['seasons'], season))
            return []
        episode_links = []
        url = url.replace('english-subbed', '').replace('english-dubbed', '').replace('anime/', '')
        if '-' in ep_range:
            ep_range = ep_range.split('-')

        for n in range(int(ep_range[0]), int(ep_range[1]) + 1):
            # print('{0}episode-{1}-english-subbed'.format(url, n))
            if season is not None and season is not '1':
                episode_links.append('{0}season-{1}-episode-{2}-english-subbed'.format(url, season, n))
            else:
                episode_links.append('{0}episode-{1}-english-subbed'.format(url, n))

        return episode_links
