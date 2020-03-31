#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from cfscrape import create_scraper
from requests import session
from tqdm import tqdm


class Downloader(object):
    def __init__(self):
        return

    def wco_dl(self, args):
        self.download_url = args[0]
        self.output = args[1]
        self.header = args[2]
        self.show_info = args[3]
        self.settings = args[4]
        
        sess = session()
        sess = create_scraper(sess)

        self.show_name = self.show_info[0]
        self.season = re.search(r'(\d+)', self.show_info[1]).group(1).zfill(self.settings.get_setting('seasonPadding'))
        if self.show_info[2] == "":
            self.episode = '{0}'.format(re.search(r'(\d+)', self.show_info[3]).group(1).zfill(
                self.settings.get_setting('episodePadding')))
        else:
            self.episode = '{0}'.format(re.search(r'(\d+)', self.show_info[2]).group(1).zfill(
                self.settings.get_setting('episodePadding')))
        self.desc = self.show_info[3]

        if self.settings.get_setting('includeShowDesc'):
            self.file_name = self.settings.get_setting('saveFormat').format(show=self.show_name, season=self.season,
                                                                       episode=self.episode, desc=self.desc)
        else:
            self.file_name = self.settings.get_setting('saveFormat').format(show=self.show_name, season=self.season,
                                                                       episode=self.episode)
        self.file_path = self.output + os.sep + "{0}.mp4".format(self.file_name)

        print('[wco-dl] - Downloading {0}'.format(self.file_name))
        while True:
            dlr = sess.get(self.download_url, stream=True, headers=self.header)  # Downloading the content using python.
            with open(self.file_path, "wb") as handle:
                for data in tqdm(dlr.iter_content(chunk_size=64)):  # Added chunk size to speed up the downloads
                    handle.write(data)

            if os.path.getsize(self.file_path) == 0:
                print("[wco-dl] - Download for {0} did not complete, please try again.\n".format(self.file_name))
                # Upon failure of download append the episode name, file_name, to a text file in the same directory
                # After finishing download all the shows the program will see if that text file exists and attempt
                # to re-download the missing files
                f_path = os.path.dirname(os.path.realpath(__file__)) + os.sep
                f = open(f_path + "failed.json", "a+")
                item = {self.show_name: {'output': self.output, 'url': self.show_info[4]}}
                f.write(item)
                f.close()
                break
            else:
                print("[wco-dl] - Download for {0} completed.\n".format(self.file_name))
                break
        return

    def crunchyroll_dl(self, args):
        print('CrunchyRoll Download - Not yet implemented')
        return
