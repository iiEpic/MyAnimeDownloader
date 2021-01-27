
import os
import re
import sys
import requests
import tkinter
import webbrowser
import inspect
import tools
from bs4 import BeautifulSoup
from tkinter import messagebox
from version import __version__

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


class Gui(tkinter.Frame):

    def __init__(self, settings):
        self.master = tkinter.Tk()
        self.settings = settings
        super().__init__(self.master)
        self.version = __version__
        self.base_url = "https://github.com/EpicUnknown/MyAnimeDownloader/"
        self.base_path = sys.argv[0].replace('__main__.py', '').replace('__main__.exe', '')
        self.new_frame = tkinter.Frame(self.master, width=800, height=400)
        self.list_box = tkinter.Listbox(self.new_frame)
        self.platform = sys.platform
        self.define_settings()
        self.new_frame.mainloop()

    def about(self):
        tkinter.messagebox.showinfo("About", "My Anime Downloader\nCreated by: iEpic\nVersion: {0}".format(
            self.version))

    def edit_settings(self):
        file_path = self.base_path + 'tools' + os.sep + 'settings.json'
        self.open_file(file_path)

    def edit_locations(self):
        file_path = self.base_path + 'resources' + os.sep + 'cache.json'
        self.open_file(file_path)

    def edit_url(self):
        file_path = self.base_path + 'resources' + os.sep + 'cache.json'
        self.open_file(file_path)

    def open_file(self, file):
        if self.platform == 'win32':
            os.system(file)
            return
        if self.platform == 'linux':
            if os.getenv('EDITOR') is None:
                print('[WARNING] You do not have an EDITOR defined in .bashrc, please put the following into .bashrc\n'
                      '"export EDITOR=\'program name\'" for example "export EDITOR=\'nano\'"')
                os.system('%s %s' % ('xdg-open', file))
                return
            else:
                os.system('%s %s' % (os.getenv('EDITOR'), file))
                return

    def open_wiki(self):
        url = self.base_url + "wiki"
        msgbox = tkinter.messagebox.askyesno("Open Wiki", "Do you wish to proceed to GitHub to read the Wiki?")
        if msgbox:
            webbrowser.open_new(url)

    def report_issue(self):
        url = self.base_url + "issues"
        msgbox = tkinter.messagebox.askyesno("Report an Issue",
                                             "Do you wish to proceed to GitHub to report the issue?")
        if msgbox:
            webbrowser.open_new(url)

    def check_update(self):
        url = "https://raw.githubusercontent.com/EpicUnknown/MyAnimeDownloader/master/version.py"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        content = soup.contents[0].splitlines()
        version = int(re.sub(r'[a-zA-Z.\-_\s\"=]', '', content[0]))
        current_version = int(re.sub(r'[a-zA-Z.\-]', '', self.version))

        if version > current_version:
            msgbox = tkinter.messagebox.askyesno("Update", "There is a newer version out.\nNew Version: {0}\n"
                                                           "Current Version: {1}\n"
                                                           "Do you wish to proceed to the update page?".format(
                                                            version, self.version
            ))
            if msgbox:
                webbrowser.open_new(self.base_url + "releases/latest")
        else:
            tkinter.messagebox.showinfo("Check Updates", "You are up-to-date!")

    @staticmethod
    def start_new():
        pass

    def search(self):
        new_search = tools.search.Search(self.settings)
        output = new_search.start()

        for item in output:
            self.list_box.insert(output.index(item), item)
        self.list_box.pack(fill='both', expand=True)
        self.new_frame.pack(fill='both', expand=True)

    def define_settings(self):
        print('Setting up GUI...')
        self.master.title('My Anime Downloader - GUI')
        self.master.wm_minsize(1000, 500)
        self.master.resizable(0, 0)

        menubar = tkinter.Menu(self.master)

        # File Menu
        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Edit Settings", command=self.edit_settings)
        filemenu.add_command(label="Edit savedLocations", command=self.edit_locations)
        filemenu.add_command(label="Edit savedURL", command=self.edit_url)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        # Download Menu
        action_menu = tkinter.Menu(menubar, tearoff=0)
        action_menu.add_command(label="Search for show", command=self.search)
        action_menu.add_command(label="Start New Download", command=self.start_new)
        menubar.add_cascade(label="Action", menu=action_menu)

        # Help Menu
        helpmenu = tkinter.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.about)
        helpmenu.add_command(label="Wiki", command=self.open_wiki)
        helpmenu.add_command(label="Check for Updates", command=self.check_update)
        helpmenu.add_separator()
        helpmenu.add_command(label="Report Issue", command=self.report_issue)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.master.config(menu=menubar)
