#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__author__ = "iEpic"
__email__ = "epicunknown@gmail.com"
"""

import os
import sys
import json


class Settings:

    def __init__(self):
        self.loaded_settings = {}
        self.path = sys.argv[0].replace('__main__.py', '').replace('__main__.exe', '') + 'tools' +\
            os.sep + 'settings.json'
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
