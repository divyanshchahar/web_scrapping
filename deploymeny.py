# Importing Libraries and Functionality
from bs4 import BeautifulSoup
import requests
from datetime import datetime

now = datetime.now()

print("EXECUTION STARTED ON ", now.strftime("%d-%B-%Y"), "at", now.strftime("%H:%M:%S"), "\n")

# URLs
basic_url = "https://www.autoscout24.com/lst/?sort=standard&desc=0&ustate=N%2CU&size=20&page="
page_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
url_extension = "&atype=C&recommended_sorting_based_id=675ba481-a475-4485-8ce6-9d0181dc17b9&"

page_url = basic_url + str(page_num[0]) + url_extension # Creating URL of the page

code_url = requests.get(page_url).text # HTML code of the page
parsed_code = BeautifulSoup(code_url, "lxml") # parsed HTML code of the page

# Extracting Search ID
sid_html = parsed_code.find("script", id="cl-search-id") # HTML code containig search id
sid_str = str(sid_html) # Converting html code of search id to string
sid = sid_str.split(":")[1].split("}")[0] # Search id
sid = sid.lstrip() # Stripping white space from the beginnig of the strip
print("Search id Successuffly extracted on", now.strftime("%d-%B-%Y"), "at", now.strftime("%H:%M:%S"),  "\n")

##################
# SCRAPPING URLs #
##################

now = datetime.now()
print("URL EXTRACTION STARTED ON ", now.strftime("%d-%B-%Y"), "at", now.strftime("%H:%M:%S"))

f = open("urls.txt", "w")

for p in page_num:

    page_url = basic_url + str(p) + url_extension  # Creating URL of the page

    code_url = requests.get(page_url).text  # HTML code of the page
    parsed_code = BeautifulSoup(code_url, "lxml")  # parsed HTML code of the page

    # Loop to extract URLs
    for parent_obj in parsed_code.find_all("div", class_="cl-list-element cl-list-element-gap"):

        car_name = parent_obj.find("h2", class_="cldt-summary-makemodel sc-font-bold sc-ellipsis").text # Name of the car

        link_url = parent_obj.find("a", href=True)["href"] # Partial address of the car

        final_url = "https://www.autoscout24.com" + link_url + "?cldtidx=1&cldtsrc=listPage&searchId=" + str(sid) # Complete Address of the car

        f.write(final_url + "\n") # Writing results to a file

    print("Page ", p)

f.close()

now = datetime.now()
print("URL EXTRACTION COMPLETE  ON", now.strftime("%d-%B-%Y"), "at", now.strftime("%H:%M:%S"), "\n")

#####################################
# EXTRACTING ALL FEATURES FROM URLS #
#####################################

now = datetime.now()
print("STARTING FEATURE EXTRACTION",  now.strftime("%d-%B-%Y"), "at", now.strftime("%H:%M:%S"))

all_urls = open("urls.txt", "r")
content_all_urls = all_urls.read() # Reading content form the file
url_items = content_all_urls.split("\n") # Splitting into different urls by line ending
url_items.pop(-1) # Removing last line(because it is blank)

f_attributes = open("attributes.txt", "w") # File to write attributes

counter = 1

# Loop to iterate through all urls
for page_url in url_items:

    f_attributes.write(page_url + "\n") # File to hold attribute information

    code_url = requests.get(page_url.rstrip()).text  # HTML code of the page
    parsed_code = BeautifulSoup(code_url, "lxml")  # parsed HTML code of the page

    parent_obj = parsed_code.find("div", class_="cldt-item", attrs={"data-item-name":"car-details"})

    # Loop to iterate through all required attributes of a url
    for j in parent_obj.find_all("dt"):
        f_attributes.write(j.text + "\n")

    print("Completed ", counter, "out of ", len(url_items), " urls")
    counter = counter + 1

f_attributes.close()

now = datetime.now()
print("FEATURE EXTRACTION COMPLETE", now.strftime("%d-%B-%Y"), "at", now.strftime("%H:%M:%S"), "\n")

##########################
# CREATING SET OF UNIQUE #
##########################

now = datetime.now()
print("STARTING CREATION OF SET OF UNIQUE FEATURES AT ", now.strftime("%d-%B-%Y"), "at", now.strftime("%H:%M:%S"), "\n")

f_attributes = open("attributes.txt", "r")

atrrbts = f_attributes.readlines()
unique_atrrbts = []

for s in atrrbts:
    if (s.find("https") == 0):
        pass

    else:
        unique_atrrbts.append(s.rstrip())

unique_atrrbts = filter(None, unique_atrrbts)

unique_atrrbts = set(unique_atrrbts)

now = datetime.now()
print("SUCCESSFULLY CREATED SET OF UNIQUE FEATURES AT ",now.strftime("%d-%B-%Y"), "at", now.strftime("%H:%M:%S"), "\n")


now = datetime.now()
print("EXECUTION COMPLTETD AT", now.strftime("%d-%B-%Y"), "at", now.strftime("%H:%M:%S"), "\n")
