
git clone https://github.com/Ziga12341/clone_page_on_disk.git

pip install -r requirements.txt

run python script 
cmd cd to working directory

import classes
from class_pywebcopy import Get_urls, Download_page,  Final, Mapping

to get all urls from web page run 
get_urls = Get_urls()
get_urls.get_all_urls()

wait about a minute that program scrape page and get all 253 links store it in all_urls.txt

scrape = Final()
scrape.write_bat_and_vbs()
in few seconds you will get .bat and .vbs file for each url

This step is needed because pywebcopy.save_webpage() do not work properly. After downloading page program stucks. I solve this problem creating with .bat and .vbs files

Than you run...
scrape.run_vbs()
This function will take you about na hour.
For each URL program will collect everything from page including pictures, css, js, html and stored on your computer.

After that you need to close python script and run it again
again import
from class_pywebcopy import Get_urls, Download_page,  Final, Mapping
map = Mapping()
map.reorder()

This function will put all .htmls in map !all and rename file to title of article (last name in url)



