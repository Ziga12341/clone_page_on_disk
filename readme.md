
git clone https://github.com/Ziga12341/clone_page_on_disk.git


Open CMD
cd ... to directory you cloned this project.

type: 

pip install -r requirements.txt

or:

You can download pywebcopy 6.3.0 here [Pywebcopy Link](https://github.com/rajatomar788/pywebcopy/)
Copy downloaded files in directory in which you cloned this project.

than:

python class_pywebcopy.py

Explanation what each class will do.

to get all urls from web page run 
get_urls = Get_urls()
get_urls.get_all_urls()

wait about a minute that program scrape page and get all 253 links store it in all_urls.txt

scrape = Final()
scrape.write_bat_and_vbs()
in few seconds you will get .bat and .vbs file for each url

This step is needed because pywebcopy.save_webpage() do not work properly. After downloading page program stucks. I solve this problem creating with .bat and .vbs files
scrape.run_vbs()
This function will take you about na hour.
For each URL program will collect everything from page including pictures, css, js, html and stored on your computer.

map = Mapping()
map.reorder()

This function will put all .htmls in map !all and rename file to title of article (last name in url)


You will find all pages copied from blog to your hard drive in C:\\...\\test_psiblog_git\\www.psiblog.si\\!all



TODO:
implement treading... chack if it is possible to avoid .bat and .vbs files
