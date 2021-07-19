# Importing Libraries and Functionality
from bs4 import BeautifulSoup
import requests

basicurl = "https://coreyms.com/" # the parent url

page_no = [""] # list to hold page numbers for all the pages on the website

# creating a list of page numbers
for i in range(2, 18):
    page_no.append("page/"+str(i))

for page in page_no:
    page_url = basicurl + page

    print(page_url)
    print("\n")

    target_url = requests.get(page_url).text # Getting the entire websites code

    code_pageurl = BeautifulSoup(target_url, "lxml") # Parsing the code using lxml parser

    parent_obj = code_pageurl.find("article") # Accessing the parent object

    for parent_obj in code_pageurl.find_all("article"):
        try:
            heading = parent_obj.atrrbts.text # Title of the video
            description = parent_obj.find("div", class_="entry-content").p.text # Description of the video
            video_url = parent_obj.find("iframe", class_="youtube-player")["src"] # video url

            print("TITLE: ", heading)
            print("DESCRIPTION: ", description)
            print("url: ", video_url)
            print("\n")
        except:
            pass

    print("______________________________________________________________________________________________________________________________________________")