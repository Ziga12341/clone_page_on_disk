from pywebcopy import save_webpage
from urllib import request
import subprocess
import time
import os
import shutil


class Get_urls:
    def __init__(self):
        self.initial_url = 'http://www.psiblog.si/2012/10/' # first blog post
        self.all_urls_list = []

    def all_article_urls_on_page(self, url):
        # if you open one month from archive; there could be multiple sides for one month... this function grabs all urls from one side
        page_article_url = []
        try:
            socket = request.urlopen(url)
            for line in socket:
                line = line.decode("utf-8")
                if line.startswith('			<h3 class="title"><a href='):
                    article_url = line.split('>')[1]
                    article_url = article_url.split('=')[1]
                    article_url = article_url.replace('"', '')
                    page_article_url.append(article_url)
        except:
            print("HTTP Error 404: Not Found")
        return page_article_url #return all article urls from one page

    def older_entries(self, url):
        #for every month get all urls of "older entries" aka preview atcicles - not all articles urls
        socket = request.urlopen(url)
        all_mounthly_articles = [url]

        for line in socket:
            line = line.decode("utf-8")
            if line.startswith('	<div class="alignleft"><a href='):
                line = line.split('"')[3]
                all_mounthly_articles.append(line)
        if len(all_mounthly_articles) > 1:
            first = all_mounthly_articles[1]
            for i in range(3, 20):
                next_url = first.replace('/2/', f'/{i}/')  # replacing last number
                try:
                    request.urlopen(next_url)  # chacking if urlopen return something
                    all_mounthly_articles.append(next_url)
                except:
                    break  ##if there is error ("No Results Found") .. no more older pages .. than brake
        return all_mounthly_articles


    def get_all_arhive(self):
        #get all links from archive aka. for every month one link
        all_arhive_pages = []
        socket = request.urlopen(self.initial_url)
        for line in socket:
            line = line.decode("utf-8")
            if line.startswith("	<option value='h"):
                line = line.split("'")[1]
                all_arhive_pages.append(line)
        return all_arhive_pages

    def get_all_urls(self):
        try: # if file with all urls exists just skip this function
            open("all_urls.txt", "r")
        except: #if there is not file named "all_urls.txt" than create it
            file = open("all_urls.txt", "w", encoding="utf-8")
            for url_from_arhive in self.get_all_arhive():
                for old_url in self.older_entries(url_from_arhive):
                    self.all_urls_list.extend(self.all_article_urls_on_page(old_url))
            file.write("\n".join(self.all_urls_list))



class Download_page(Get_urls):
    def __init__(self, i):
        super().__init__()
        self.get_all_urls()
        self.url = [line for line in open("all_urls.txt", "r")][i] # read urls from .txt. this .txt is created from Get_urls
        self.project_folder = os.getcwd()


    def downloader(self):
        print(self.url)
        kwargs = {'bypass_robots': True, 'project_name': 'test_psiblog_git'}
        save_webpage(url=self.url, project_folder=self.project_folder, **kwargs)

class Final(Get_urls):
    def __init__(self):
        super().__init__()
        self.get_all_urls()
        self.urls_from_file = [line for line in open("all_urls.txt", "r")]

    def write_bat_and_vbs(self):
        for i in range(len(self.urls_from_file) - 1):
            file_name_bat = f"{i}_class_scrape.bat"
            file_bat = open(file_name_bat, "w", encoding="UTF-8")
            file_bat.write(f'python -c "import class_pywebcopy;class_pywebcopy.Download_page({i}).downloader()"\npause')

            file_name_vbs = f"{i}_class_scrape.vbs"
            file_vbs = open(file_name_vbs, "w", encoding="UTF-8")
            file_vbs.write(f'Set WshShell = CreateObject("WScript.Shell") \nWshShell.Run chr(34) & "{os.getcwd()}\\{file_name_bat}" & Chr(34), 0\nSet WshShell = Nothing')

    def run_vbs(self):
        for i in range(len(self.urls_from_file) - 1):
            subprocess.call(f"cmd /c {i}_class_scrape.vbs")
            time.sleep(15)

class Mapping:

    #created directory !all rename all .html's on article title and put all pages (allhtmls) in that dir

    def reorder(self):
        dir_name = os.getcwd()
        os.makedirs("test_psiblog_git\www.psiblog.si\!all") #create directory !all
        dst_path = dir_name + "\\" + 'test_psiblog_git\www.psiblog.si\!all'
        for root, dirs, files in os.walk("test_psiblog_git\www.psiblog.si"):
            for file in files:
                if file.endswith(".html"):
                    print(os.path.join(root, file))
                    old_name = dir_name + "\\" + root + "\\" + 'index.html'
                    new_name = dir_name + "\\" + root + "\\" + (root.split('\\')[-1]) + '.html'
                    os.rename(old_name, new_name) ## renaming
                    shutil.move(new_name, dst_path) #move all .html in one dir named !all


def main():
    Get_urls().get_all_urls() #create directory all_urls... with list of all urls from that page
    time.sleep(120)
    Final().write_bat_and_vbs() #crate .bat and .vbs files (because Pywebcopy().save_webpage() not working properly)
    time.sleep(10)
    Final().run_vbs() #this use each link and download whole page for each link... when this is done all pages are on disk
    time.sleep(60)
    Mapping().reorder() #this metod put all .html files in one dorectory and rename it as original title of article

if __name__ == '__main__':
    main()
