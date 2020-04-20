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
        def create_file(fileLocation, data):
            file = open(fileLocation, 'w')
            file.write(json.dumps(data, indent=4, sort_keys=True))
            file.close()

        self.savedLocation = {}
        self.savedURL = {}
        self.pathLocation = sys.argv[0].replace('__main__.py', '') + 'tools' + os.sep + 'savedLocations.json'
        self.pathURL = sys.argv[0].replace('__main__.py', '') + 'tools' + os.sep + 'savedURL.json'
        # Does settings.json file exist?
        if os.path.exists(self.pathLocation):
            # Load up the savedLocation file
            with open(self.pathLocation) as file:
                self.savedLocation = json.load(file)
                print('Saved Locations Loaded.')
        else:
            create_file(self.pathLocation, self.savedLocation)
            print('Saved URLs have been created!')

        if os.path.exists(self.pathURL):
            # Load up the savedURL file
            with open(self.pathURL) as file:
                self.savedURL = json.load(file)
                print('Saved URLs Loaded.')
        else:
            create_file(self.pathURL, self.savedURL)
            print('Saved URLs have been created!')

    def get_location(self, show_name):
        if show_name in self.savedLocation:
            return self.savedLocation[show_name]

    def set_location(self, show_name, location):
        self.savedLocation[show_name] = location
        file = open(self.pathLocation, 'w')
        file.write(json.dumps(self.savedLocation, indent=4, sort_keys=True))
        file.close()

    def set_show_url(self, show_name, url):
        self.savedURL[show_name] = url
        file = open(self.pathURL, 'w')
        file.write(json.dumps(self.savedURL, indent=4, sort_keys=True))
        file.close()

    def get_show_url(self, show_name):
        return self.savedURL[show_name] or None
