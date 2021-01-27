# -*- coding: utf-8 -*-

import re
import base64
import requests
import sys
from bs4 import BeautifulSoup
from downloader import *
import urllib3
urllib3.disable_warnings()


class WCOStream:
    def __init__(self, args):
        self.args = args
        self.show_name = args['show_name']
        self.show_info = args['show_info']
        self.base_url = "https://wcostream.com"
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
        self.header = {
            'User-Agent': self.user_agent, 'Accept': '*/*', 'X-Requested-With': 'XMLHttpRequest'
        }
        self.dl = Downloader()
        self.build_urls()

    def build_urls(self):
        base_url = self.show_info['url'].replace('anime/', '').replace('-english-dubbed',
                                                                       '').replace('-english-subbed', '')
        # Check if we are getting a specific season
        if self.args['season'] != 'All':
            if int(self.args['season'][0]) > len(self.show_info['seasons']):
                pass

        if self.args['newest']:
            episode_url = f"{base_url}"
            season = len(self.show_info['seasons'])
            if season != 1:
                episode_url += f"-season-{season}"

            episode = self.show_info['seasons'][str(season)]
            if self.show_info['type'] == 'cartoon':
                episode_url += f'-episode-{episode}'
            elif self.show_info['type'] == 'dubbed':
                episode_url += f'-episode-{episode}-english-dubbed'
            else:
                episode_url += f'-episode-{episode}-english-subbed'

            episode_page = self.request_c(url=episode_url)
            if episode_page.ok:
                download_url = self.get_download_url(episode_url)
                if '480' in self.args['resolution']:
                    download_url = download_url[0][1]
                else:
                    download_url = download_url[1][1]

                self.header['Referer'] = episode_url
                args = []
                args.append(download_url)
                args.append(self.args['output'])
                args.append(self.header)
                args.append(self.show_name)
                args.append(episode_page.url)
                args.append(self.args['settings'])
                self.dl.wco_dl(args)
                self.header.pop('Referer')
            else:
                print('Episode did not download, please report this on GitHub.')
                sys.exit(1)

        if isinstance(self.args['range'], list):
            episode_url = f'{base_url}'
            if '-' in self.args['range'][0]:
                ep_range = self.args['range'][0].split('-')
            elif 'All' not in self.args['range']:
                ep_range = []
                ep_range.append(self.args['range'][0])
                ep_range.append(self.args['range'][0])

            if self.args['season'] != 'All':
                episode_url += f"-season-{self.args['season'][0]}"

            for episode in range(int(ep_range[0]), int(ep_range[1])+1):
                new_url = episode_url
                if self.show_info['type'] == 'cartoon':
                    new_url += f'-episode-{episode}'
                elif self.show_info['type'] == 'dubbed':
                    new_url += f'-episode-{episode}-english-dubbed'
                else:
                    new_url += f'-episode-{episode}-english-subbed'

                episode_page = self.request_c(url=new_url)

                if episode_page.ok:
                    download_url = self.get_download_url(new_url)
                    if '480' in self.args['resolution']:
                        download_url = download_url[0][1]
                    else:
                        download_url = download_url[1][1]

                    self.header['Referer'] = new_url
                    args = []
                    args.append(download_url)
                    args.append(self.args['output'])
                    args.append(self.header)
                    args.append(self.show_name)
                    args.append(episode_page.url)
                    args.append(self.args['settings'])
                    self.dl.wco_dl(args)
                    self.header.pop('Referer')
                else:
                    print('Episode {0} did not download, please report this on GitHub.'.format(episode))

    def get_download_url(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        script_url = repr(soup.find("meta", {"itemprop": "embedURL"}).next_element.next_element)
        letters = script_url[script_url.find("[") + 1:script_url.find("]")]
        ending_number = int(re.search(' - ([0-9]+)', script_url).group(1))
        hidden_url = self._decode(letters.split(', '), ending_number)
        return self.get_source_url(hidden_url)[0]

    def _decode(self, array, ending):
        iframe = ''
        for item in array:
            decoded = base64.b64decode(item).decode('utf8')
            numbers = re.sub('[^0-9]+', '', decoded)
            iframe += chr(int(numbers) - ending)
        html = BeautifulSoup(iframe, 'html.parser')
        return self.base_url + html.find("iframe")['src']

    def request_c(self, url, extra_headers=None):
        myheaders = {
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml,application/json;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'DNT': '1'
        }
        if extra_headers:
            myheaders.update(extra_headers)

        response = requests.get(url, headers=myheaders, verify=False, cookies=None, timeout=10)
        return response

    def get_source_url(self, embed_url):
        page = self.request_c(embed_url)
        html = page.text

        # Find the stream URLs.
        if 'getvid?evid' in html:
            # Query-style stream getting.
            source_url = re.search(r'get\("(.*?)"', html, re.DOTALL).group(1)

            page2 = self.request_c(
                self.base_url + source_url,
                extra_headers={
                    'User-Agent': self.user_agent, 'Accept': '*/*', 'Referer': embed_url,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            )
            if not page2.ok:
                raise Exception('Sources XMLHttpRequest request failed')
            json_data = page2.json()

            # Only two qualities are ever available: 480p ("SD") and 720p ("HD").
            source_urls = []
            sd_token = json_data.get('enc', '')
            hd_token = json_data.get('hd', '')
            source_base_url = json_data.get('server', '') + '/getvid?evid='
            if sd_token:
                source_urls.append(('480 (SD)', source_base_url + sd_token))  # Order the items as (LABEL, URL).
            if hd_token:
                source_urls.append(('720 (HD)', source_base_url + hd_token))
            # Use the same backup stream method as the source: cdn domain + SD stream.
            backup_url = json_data.get('cdn', '') + '/getvid?evid=' + (sd_token or hd_token)
        else:
            # Alternative video player page, with plain stream links in the JWPlayer javascript.
            sources_block = re.search(r'sources:\s*?\[(.*?)\]', html, re.DOTALL).group(1)
            stream_pattern = re.compile(r'\{\s*?file:\s*?"(.*?)"(?:,\s*?label:\s*?"(.*?)")?')
            source_urls = [
                # Order the items as (LABEL (or empty string), URL).
                (sourceMatch.group(2), sourceMatch.group(1))
                for sourceMatch in stream_pattern.finditer(sources_block)
            ]
            # Use the backup link in the 'onError' handler of the 'jw' player.
            backup_match = stream_pattern.search(html[html.find(b'jw.onError'):])
            backup_url = backup_match.group(1) if backup_match else ''
        # print("debug:", backup_url)
        # print("debug:", source_urls)

        return source_urls, backup_url
