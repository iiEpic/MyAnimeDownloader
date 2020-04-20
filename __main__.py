
import os
import re
import sys
import requests
import tkinter
import webbrowser
from bs4 import BeautifulSoup
from tkinter import messagebox


class Main(tkinter.Frame):
    if __name__ == '__main__':
        def __init__(self, master=None):
            super().__init__(master)
            self.version = "v2020.04.20.1-beta"
            self.master = master
            self.base_url = "https://github.com/EpicUnknown/MyAnimeDownloader/"
            self.base_path = sys.argv[0].replace('__main__.py', '')
            print(sys.argv[0])
            self.define_settings()

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
            dl_menu = tkinter.Menu(menubar, tearoff=0)
            dl_menu.add_command(label="Start New Download", command=self.start_new)
            menubar.add_cascade(label="Download", menu=dl_menu)

            # Help Menu
            helpmenu = tkinter.Menu(menubar, tearoff=0)
            helpmenu.add_command(label="About", command=self.about)
            helpmenu.add_command(label="Wiki", command=self.open_wiki)
            helpmenu.add_command(label="Check for Updates", command=self.check_update)
            helpmenu.add_separator()
            helpmenu.add_command(label="Report Issue", command=self.report_issue)
            menubar.add_cascade(label="Help", menu=helpmenu)

            self.master.config(menu=menubar)


m = tkinter.Tk()
frame = Main(master=m)
frame.mainloop()
