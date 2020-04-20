#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import json
from cfscrape import create_scraper
from requests import session
from tqdm import tqdm


class Downloader(object):
    def __init__(self):
        self.f_path = os.path.dirname(os.path.realpath(__file__)) + os.sep
        self.failed_db = {}
        return

    def wco_dl(self, args):
        download_url = args[0]
        output = args[1]
        header = args[2]
        show_info = args[3]
        settings = args[4]
        sess = session()
        sess = create_scraper(sess)

        show_name = show_info[0]
        season = re.search(r'(\d+)', show_info[1]).group(1).zfill(settings.get_setting('seasonPadding'))
        if show_info[2] == "":
            episode = '{0}'.format(re.search(r'(\d+)', show_info[3]).group(1).zfill(
                settings.get_setting('episodePadding')))
        else:
            episode = '{0}'.format(re.search(r'(\d+)', show_info[2]).group(1).zfill(
                settings.get_setting('episodePadding')))
        desc = show_info[3]

        if settings.get_setting('includeShowDesc'):
            file_name = settings.get_setting('saveFormat').format(show=show_name, season=season,
                                                                  episode=episode, desc=desc)
        else:
            file_name = settings.get_setting('saveFormat').format(show=show_name, season=season,
                                                                  episode=episode)
        file_path = output + os.sep + "{0}.mp4".format(file_name)

        print('[wco-dl] - Downloading {0}'.format(file_name))
        while True:
            dlr = sess.get(download_url, stream=True, headers=header)  # Downloading the content using python.
            with open(file_path, "wb") as handle:
                for data in tqdm(dlr.iter_content(chunk_size=64)):  # Added chunk size to speed up the downloads
                    handle.write(data)

            if os.path.getsize(file_path) == 0:
                print("[wco-dl] - Download for {0} did not complete, please try again.\n".format(file_name))
                # Upon failure of download append the episode name, file_name, to a text file in the same directory
                # After finishing download all the shows the program will see if that text file exists and attempt
                # to re-download the missing files
                if os.path.exists(self.f_path + "failed.json"):
                    # Load up the settings
                    with open(self.f_path + "failed.json") as file:
                        self.failed_db = json.load(file)

                f = open(self.f_path + "failed.json", "w")
                self.failed_db[show_info[4]] = {'show_name': show_name, 'output': output}
                f.write(json.dumps(self.failed_db, indent=4, sort_keys=True))
                f.close()
                break
            else:
                print("[wco-dl] - Download for {0} completed.\n".format(file_name))
                break
        return

    def crunchyroll_dl(self):
        print('CrunchyRoll Download - Not yet implemented')
        return
