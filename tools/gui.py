
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

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


class Gui(tkinter.Frame):

    def __init__(self):
        self.master = tkinter.Tk()
        super().__init__(self.master)
        self.version = "v2020.04.22.2-beta"
        self.base_url = "https://github.com/EpicUnknown/MyAnimeDownloader/"
        self.base_path = sys.argv[0].replace('__main__.py', '')
        self.new_frame = tkinter.Frame(self.master, width=800, height=400)
        self.define_settings()
        self.new_frame.mainloop()

    def hello(self):
        print('Hello')

    def about(self):
        tkinter.messagebox.showinfo("About", "My Anime Downloader\nCreated by: iEpic\nVersion: {0}".format(
            self.version))

    def edit_settings(self):
        file_path = self.base_path + 'tools' + os.sep + 'settings.json'
        try:
            os.system(r"start notepad++ " + file_path)
        except:
            os.system(r"notepad.exe " + file_path)

    def edit_locations(self):
        file_path = self.base_path + 'tools' + os.sep + 'savedLocations.json'
        try:
            os.system(r"start notepad++ " + file_path)
        except:
            os.system(r"notepad.exe " + file_path)

    def edit_url(self):
        file_path = self.base_path + 'tools' + os.sep + 'savedURL.json'
        try:
            os.system(r"start notepad++ " + file_path)
        except:
            os.system(r"notepad.exe " + file_path)

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
        url = self.base_url + "releases/latest"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        version = soup.findAll('span', {'class': 'css-truncate-target'})[0].text
        version = re.sub('[a-zA-Z.-]', '', version)
        print(version)
        if version != self.version:
            msgbox = tkinter.messagebox.askyesno("Update", "There is a newer version out.\nNew Version: {0}\n"
                                                           "Current Version: {1}\n"
                                                           "Do you wish to proceed to the update page?".format(
                                                            version, self.version
            ))
            if msgbox:
                webbrowser.open_new(url)
        else:
            tkinter.messagebox.showinfo("Check Updates", "You are up-to-date!")

    @staticmethod
    def start_new():
        pass

    def search(self):
        new_search = tools.search.Search()
        output = new_search.start()
        base_url = "https://www.wcostream.com"

        list_box = tkinter.Listbox(self.new_frame)
        for item in output:
            list_box.insert(output.index(item), item)
        list_box.pack(fill='both', expand=True)
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
