#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import sites
from urllib.parse import urlparse
from sys import exit


class Verify(object):

    def __init__(self, args):
        self.url = args['input'][0]
        self.username = args['username']
        self.password = args['password']
        self.verified = False
        website = self.check()

        if website == "Crunchyroll":
            if (not self.url[0] or not self.username or not self.password) and args['resolution'] in ['720', '1080']:
                print("CrunchyRoll requires username and password if downloading 720p or higher.")
                exit()
            else:
                self.login = True
                self.verified = True
                self.website = 'Crunchyroll'
        elif website == 'WCO':
            self.login = False
            self.verified = True
            self.website = 'WCO'
        elif website is None:
            print('{0} is not a supported website.'.format(self.url[0]))
            exit(1)

    def check(self):
        # Check which website we are directing to
        
        if "https://" in self.url:
            self.url = str(self.url)
        elif "http://" not in self.url:
            self.url = "http://" + str(self.url)

        domain = urlparse(self.url).netloc

        if domain in ['www.wcostream.com', 'wcostream.com']:
            return 'WCO'
        elif domain in ["www.crunchyroll.com", "crunchyroll.com"]:
            return "Crunchyroll"
        return None

    def isVerified(self):
        return self.verified
    def requireLogin(self):
        return self.login
    def getWebsite(self):
        return self.website