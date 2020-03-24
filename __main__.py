#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__author__ = "iEpic"
__email__ = "epicunknown@gmail.com"

All inspired by Anime-dl by Xonshiz
"""
import os
import sys
import inspect
import argparse
import logging
import platform
from sys import exit
# from Anime-dl import AnimeDL
from version import __version__
from verify import Verify
# from Settings import Settings

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


class Main:
    if __name__ == '__main__':
        # Run the settings script
        # settings = Settings()

        parser = argparse.ArgumentParser(description='MAD downloads anime from CrunchyRoll, WCOStream and other websites.')

        parser.add_argument('--version', action='store_true', help='Shows version and exits.')

        required_args = parser.add_argument_group('Required Arguments :')
        required_args.add_argument('-i', '--input', nargs=1, help='Inputs the URL to anime.')

        parser.add_argument('-p', '--password', nargs=1, help='Indicates password for a website.')
        parser.add_argument('-u', '--username', nargs=1, help='Indicates username for a website.')
        parser.add_argument('-r', '--resolution', nargs=1, help='Inputs the resolution to look for.', default='720')
        parser.add_argument('-l', '--language', nargs=1, help='Selects the language for the show.', default='Japanese')
        parser.add_argument('-rn', '--range', nargs=1, help='Specifies the range of episodes to download.',
                            default='All')
        parser.add_argument('-se', '--season', nargs=1, help='Specifies what season to download.')
        parser.add_argument('-o', '--output', nargs=1, help='Specifies the directory of which to save the files.')
        parser.add_argument('--skip', action='store_true', help='skips the video download and downloads only subs.')
        parser.add_argument('-nl', '--nologin', action='store_true', help='Skips login for websites.')
        parser.add_argument("-v", "--verbose", help="Prints important debugging messages on screen.",
                            action="store_true")
        logger = "False"
        args = parser.parse_args()
        skipper = "no"

        if args.verbose:
            logging.basicConfig(format='%(levelname)s: %(message)s', filename="Error Log.log", level=logging.DEBUG)
            logging.debug('You have successfully set the Debugging On.')
            logging.debug("Arguments Provided : {0}".format(args))
            logging.debug(
                "Operating System : {0} - {1} - {2}".format(platform.system(), platform.release(), platform.version()))
            logging.debug("Python Version : {0} ({1})".format(platform.python_version(), platform.architecture()[0]))
            logger = "True"

        if args.version:
            print("Current Version: {0}".format(__version__))
            exit()

        if args.skip:
            print("Will be skipping video downloads")
            skipper = "yes"

        if args.nologin:
            args.username = ['username']
            args.password = ['password']

        if args.input is None:
            print("Please enter the required arguments. Run __main__.py --help")
            exit(1)
        else:
            # If the argument has been provided for resolution and language,
            # they're going to be lists, otherwise, they're
            # going to be simple value == 720p.
            # So, if return type comes out to be list, send the first element, otherwise, send 720p as it is.
            # Same approach for the audio as well.
            if type(args.username) == list:
                args.username = args.username[0]
            else:
                args.username = False
            if type(args.password) == list:
                args.password = args.password[0]
            else:
                args.password = False

            if type(args.resolution) == list:
                if "," in args.resolution[0]:
                    args.resolution = args.resolution[0].split(',')
                else:
                    args.resolution = args.resolution[0]
            if type(args.language) == list:
                args.language = args.language[0]
            if type(args.range) == list:
                args.range = args.range[0]
            if type(args.season) == list:
                args.season = args.range[0]
            if type(args.output) == list:
                args.output = args.output[0]

            # Lets check if the url is a website we support and if it requires a username and password
            verify = Verify(url=args.input, username=args.username, password=args.password)
            if verify.isVerified():
                # It is a website we support. Lets use it
                # Test if we require a login to download from that website
                if verify.requireLogin():
                    # Lets pass the input, username and password along with other args
                    pass
                else:
                    # This website doesn't require logging in. Don't pass username and password
                    pass

            #AnimeDL(url=args.input, username=args.username, password=args.password,
            #        resolution=args.resolution, language=args.language, skipper=skipper,
            #        logger=logger, episode_range=args.range, output=args.output, settings=settings)
