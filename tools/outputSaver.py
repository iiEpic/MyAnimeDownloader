#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__author__ = "iEpic"
__email__ = "epicunknown@gmail.com"
"""

import os
import sys
import json


class OutputSaver:

    def __init__(self):
        def create_file(file_location, data):
            f = open(file_location, 'w')
            f.write(json.dumps(data, indent=4, sort_keys=True))
            f.close()

        self.saved_location = {}
        self.saved_url = {}
        self.path_location = sys.argv[0].replace('__main__.py', '').replace('__main__.exe', '') + 'tools' +\
            os.sep + 'savedLocations.json'
        self.path_url = sys.argv[0].replace('__main__.py', '').replace('__main__.exe', '') + 'tools' + \
            os.sep + 'savedURL.json'
        # Does settings.json file exist?
        if os.path.exists(self.path_location):
            # Load up the savedLocation file
            with open(self.path_location) as file:
                self.saved_location = json.load(file)
                print('Saved Locations Loaded.')
        else:
            create_file(self.path_location, self.saved_location)
            print('Saved URLs have been created!')

        if os.path.exists(self.path_url):
            # Load up the savedURL file
            with open(self.path_url) as file:
                self.saved_url = json.load(file)
                print('Saved URLs Loaded.')
        else:
            create_file(self.path_url, self.saved_url)
            print('Saved URLs have been created!')

    def get_location(self, show_name):
        if show_name in self.saved_location:
            return self.saved_location[show_name]

    def set_location(self, show_name, location):
        self.saved_location[show_name] = location
        file = open(self.path_location, 'w')
        file.write(json.dumps(self.saved_location, indent=4, sort_keys=True))
        file.close()

    def set_show_url(self, show_name, url):
        self.saved_url[show_name] = url
        file = open(self.path_url, 'w')
        file.write(json.dumps(self.saved_url, indent=4, sort_keys=True))
        file.close()

    def get_show_url(self, show_name):
        return self.saved_url[show_name] or None
