#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import sites
from urllib.parse import urlparse
from sys import exit


class Verify(object):

    def __init__(self, url, username, password):
        self.verified = False
        website = self.check(url[0])

        if website == "Crunchyroll":
            if not url[0] or not username or not password:
                print("CrunchyRoll requires username and password if downloading 720p or higher.")
                exit()
            else:
                self.login = True
                self.verified = True
        elif website == 'WCO':
            self.login = False
            self.verified = True
        elif website is None:
            print('{0} is not a supported website.'.format(url[0]))
            exit(1)

    def check(self, url):
        # Check which website we are directing to
        
        if "https://" in url:
            url = str(url)
        elif "http://" not in url:
            url = "http://" + str(url)

        domain = urlparse(url).netloc

        if domain in ['www.wcostream.com', 'wcostream.com']:
            return 'WCO'
        elif domain in ["www.crunchyroll.com", "crunchyroll.com"]:
            return "Crunchyroll"
        return None

    def isVerified(self):
        return self.verified
    def requireLogin(self):
        return self.login