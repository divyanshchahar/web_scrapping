# Importing Libraries and Functionality
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd

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

all_urls = open("urls.txt", "w")

for p in page_num:

    page_url = basic_url + str(p) + url_extension  # Creating URL of the page

    code_url = requests.get(page_url).text  # HTML code of the page
    parsed_code = BeautifulSoup(code_url, "lxml")  # parsed HTML code of the page

    # Loop to extract URLs
    for parent_obj in parsed_code.find_all("div", class_="cl-list-element cl-list-element-gap"):

        link_url = parent_obj.find("a", href=True)["href"] # Partial address of the car

        final_url = "https://www.autoscout24.com" + link_url + "?cldtidx=1&cldtsrc=listPage&searchId=" + str(sid) # Complete Address of the car

        all_urls.write(final_url + "\n") # Writing results to a file

    print("Page ", p)

all_urls.close()

now = datetime.now()
print("URL EXTRACTION COMPLETE  ON", now.strftime("%d-%B-%Y"), "at", now.strftime("%H:%M:%S"), "\n")

# #####################################
# # EXTRACTING ALL FEATURES FROM URLS #
# #####################################

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

###################################
# CREATING SET OF UNIQUE FEATURES #
###################################

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

# print(len(unique_atrrbts)) = 38

##################
# SCRAPPING DATA #
##################

all_urls = open("urls.txt", "r") # File Object for the urls file
content_all_urls = all_urls.read() # Reading content form the file
url_items = content_all_urls.split("\n") # Splitting into different urls by line ending
url_items.pop(-1) # Removing last line(because it is blank)

attributes1 = ["price", "car name", "variant", "mileage", "first registration", "horse power"] # List of attributes

temp1 = [] # First list to hold values of attributes

# Loop to initialize first list
for i in range(0, len(attributes1)):
    temp1.append([])

counter = 1

# Loop to iterate through urls
for page_url in url_items:

    print(counter, "out of ", len(url_items))

    code_url = requests.get(page_url).text # HTML code of the page
    parsed_code = BeautifulSoup(code_url, "lxml") # parsed HTML code of the page

    # Extracting price
    try:
        parent_obj = parsed_code.find("div", class_="cldt-stage-headline")
    except:
        print("Unable to extract parent object for price")

    try:
        price = parent_obj.find("h2")
        temp1[0].append(price.text.strip())
    except:
        print("Unable to extract price")
        temp1[0].append("")

    # Extracting Vehicle Name and Variant
    try:
        parent_obj = parsed_code.find("div", class_="cldt-headline")
    except:
        print("unable to locate parent object containig vehicle name and variant")

    # vehicle name
    try:
        vehicle_name = parent_obj.find("span", class_="cldt-detail-makemodel sc-ellipsis")
        temp1[1].append(vehicle_name.text)
    except:
        print("Unable to extract vehicle name")
        temp1[1].append("")

    # vehicle variant
    try:
        vehicle_variant = parent_obj.find("span", class_="cldt-detail-version sc-ellipsis")
        temp1[2].append(vehicle_variant.text)
    except:
        print("Unable to extract vehicle variant")
        temp1[2].append("")

    # Extracting mileage, first registration, horse power
    try:
        parent_obj = parsed_code.find("div", class_="cldt-stage-basic-data")
    except:
        print("Unable to find parent object")

    try:
        mileage = parent_obj.find("span", class_="sc-font-l cldt-stage-primary-keyfact").text.replace(",", "").split()[0]
        temp1[3].append(mileage)
    except:
        print("Unable to extract mileage")
        temp1[3].append("")

    try:
        first_registration = parent_obj.find("span", class_="sc-font-l cldt-stage-primary-keyfact", attrs={"id":"basicDataFirstRegistrationValue"}).text
        temp1[4].append(first_registration)
    except:
        print("Unable to extract first registration date")
        temp1[4].append("")

    try:
        horse_power = parent_obj.find("span", class_="sc-font-m cldt-stage-primary-keyfact").text.split()[0]
        temp1[5].append(horse_power)
    except:
        print("Unable to extract horse power")
        temp1[5].append("")

    counter = counter + 1

dict1_db = {}

for i in range(0, len(attributes1)):
    dict1_db[attributes1[i]] = temp1[i]

df_cardetails = pd.DataFrame(dict1_db)

df_cardetails.to_csv("cars.csv", index=False)

now = datetime.now()
print("EXECUTION COMPLTETD AT", now.strftime("%d-%B-%Y"), "at", now.strftime("%H:%M:%S"), "\n")
