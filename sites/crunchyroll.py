# -*- coding: utf-8 -*-

import os
import sys
import requests
from bs4 import BeautifulSoup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from downloader import *


class Crunchyroll(object):
    def __init__(self, args):
        print('Called CR')
        # Define our variables
        self.dl = Downloader()
        self.url = args['input'][0]
        self.resolution = args['resolution']
        self.logger = args['logger']
        self.season = args['season']
        self.ep_range = args['range']
        self.exclude = args['exclude']
        self.newest = args['newest']
        self.output = args['output']
        self.settings = args['settings']
        self.output_saver = args['outputsaver']
        self.show_info = self.get_info()

    def get_info(self):
        video_id = self.url.split('-')[-1].replace('/', '')
        info_url = "http://www.crunchyroll.com/xml/?req=RpcApiVideoPlayer_GetStandardConfig&media_id=%s&video_format=108&video_quality=80&current_page=%s" % (
            video_id, self.url)
        page = requests.get(info_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        show_name = self.url.split('/')[1]
        download_url = soup.file
        desc = soup.episode_title
        episode_number = soup.episode_number
        return show_name.title().strip(), season, episode_number, desc.title().strip(), self.url, download_url

