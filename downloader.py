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
        show_name = args[3]
        episode_url = args[4]
        settings = args[5]
        sess = session()
        sess = create_scraper(sess)
        print(header['Referer'])

        try:
            season = re.search(r'season-([0-9]+)-episode', episode_url).group(1).zfill(settings.get_setting('seasonPadding'))
        except:
            season = '1'.zfill(settings.get_setting('seasonPadding'))
        episode = '{0}'.format(re.search(r'episode-([0-9]+)-', episode_url).group(1).zfill(
            settings.get_setting('episodePadding')))
        desc = re.search(r'episode-[0-9]+-(.*)', episode_url).group(1).replace("-", " ").title().replace(" ", "-")

        if settings.get_setting('includeShowDesc'):
            file_name = settings.get_setting('saveFormat').format(show=show_name, season=season,
                                                                  episode=episode, desc=desc)
        else:
            file_name = settings.get_setting('saveFormat').format(show=show_name, season=season,
                                                                  episode=episode)
        if output is None:
            if not os.path.exists(os.getcwd() + os.sep + "Output"):
                os.mkdir(os.getcwd() + os.sep + "Output")
            if not os.path.exists(os.getcwd() + os.sep + "Output" + os.sep + show_name):
                os.mkdir(os.getcwd() + os.sep + "Output" + os.sep + show_name)
            output = os.getcwd() + os.sep + "Output" + os.sep + show_name + os.sep
        if not os.path.exists(output):
            print('Path does not exists.')
            exit(0)
        file_path = output + "{0}.mp4".format(file_name)

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
                self.failed_db[episode_url] = {'show_name': show_name, 'output': output}
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
