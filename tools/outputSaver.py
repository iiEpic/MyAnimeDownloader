#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__author__ = "iEpic"
__email__ = "epicunknown@gmail.com"
"""

import os
import json


class OutputSaver:

    def __init__(self):
        self.savedLocation = {}
        self.path = 'tools' + os.sep + 'savedLocations.json'
        # Does settings.json file exist?
        if os.path.exists(self.path):
            # Load up the settings
            with open(self.path) as file:
                self.savedLocation = json.load(file)
                print('Saved Locations Loaded.')
        else:
            file = open(self.path, 'w')
            file.write(json.dumps(self.savedLocation, indent=4, sort_keys=True))
            file.close()
            print('Saved Locations have been created!')

    def get_location(self, show_name):
        if show_name in self.savedLocation:
            return self.savedLocation[show_name]

    def set_location(self, show_name, location):
        if show_name in self.savedLocation:
            self.savedLocation[show_name] = location
            file = open(self.path, 'w')
            file.write(json.dumps(self.savedLocation, indent=4, sort_keys=True))
            file.close()
