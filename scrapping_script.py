# Importing Libraries and Functionality
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd

now = datetime.now()
print("EXECUTION STARTED ON ", now.strftime("%d-%B-%Y"), "at", now.strftime("%H:%M:%S"), "\n")

# Reading Essential data from input_website.txt
f_input_website = open("input_website.txt", "r")
content_input_website = f_input_website.readlines()
f_input_website.close()

basic_url = content_input_website[0].split("page=")[0] + "page=" # First half of URL
url_extension = content_input_website[0].split("page=1")[1] # Second half of URL

page_num = list(range(1, int(content_input_website[1]) + 1)) # List containing page numbers

########################
# EXTRACTING SEARCH ID #
########################

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

f_urls = open("urls.txt", "w")

for p in page_num:

    page_url = basic_url + str(p) + url_extension  # Creating URL of the page

    code_url = requests.get(page_url).text  # HTML code of the page
    parsed_code = BeautifulSoup(code_url, "lxml")  # parsed HTML code of the page

    # Loop to extract URLs
    for parent_obj in parsed_code.find_all("div", class_="cl-list-element cl-list-element-gap"):

        link_url = parent_obj.find("a", href=True)["href"] # Partial address of the car
        final_url = "https://www.autoscout24.com" + link_url + "?cldtidx=1&cldtsrc=listPage&searchId=" + str(sid) # Complete Address of the car

        f_urls.write(final_url + "\n") # Writing results to a file

    print("Completed pages ", p, "out of ", page_num[-1])

f_urls.close()

now = datetime.now()
print("URL EXTRACTION COMPLETE  ON", now.strftime("%d-%B-%Y"), "at", now.strftime("%H:%M:%S"), "\n")

###################
# EXTRACTING DATA #
###################

now = datetime.now()
print("DATA SCRAPPING STARTED ON", now.strftime("%d-%B-%Y"), "at", now.strftime("%H:%M:%S"))

f_urls = open("urls.txt", "r") # File Object for the urls file
content_urls = f_urls.read() # Reading content form the file
urls = content_urls.split("\n") # Splitting into different urls by line ending
urls.pop(-1) # Removing last line(because it is blank)

f_car_details = open("car_details.txt", "w")

global_attributes = ["price", "car name", "variant", "mileage", "first registration", "horse power"] # List of global attributes

counter = 1 # Counter to count the number of urls sucessfully scrapped

# LOOP TO ITERATE THROUGH URLs
for page_url in urls:

    print(counter, "out of ", len(urls))

    f_car_details.write(page_url + "\n") # Writing page url to file

    code_url = requests.get(page_url).text # HTML code of the page
    parsed_code = BeautifulSoup(code_url, "lxml") # parsed HTML code of the page

    #  EXTRACTING PRICE
    # parent object for price
    try:
        parent_obj = parsed_code.find("div", class_="cldt-stage-headline") # Parent Object for price
    except:
        print("Unable to extract parent object for price")

    # price
    try:
        price = parent_obj.find("h2").text.strip()
    except:
        print("Unable to extract price")
        price = ""

    # EXTRACTING VEHICLE NAME AND VARIANT
    # parent object for name and variant
    try:
        parent_obj = parsed_code.find("div", class_="cldt-headline")
    except:
        print("unable to locate parent object containig vehicle name and variant")

    # vehicle name
    try:
        vehicle_name = parent_obj.find("span", class_="cldt-detail-makemodel sc-ellipsis").text
        f_car_details.write("name : " + vehicle_name + "\n")
    except:
        print("Unable to extract vehicle name")
        f_car_details.write("name : " + "\n")

    # vehicle variant
    try:
        vehicle_variant = parent_obj.find("span", class_="cldt-detail-version sc-ellipsis").text
        f_car_details.write("variant : " + vehicle_variant + "\n")
    except:
        print("Unable to extract vehicle variant")
        f_car_details.write("variant : " + "\n")

    f_car_details.write("price : " + price + "\n")  # writing price to the file

    # EXTRACTING MILEAGE, FIRST REGISTRATION, HORSE POWER
    # parent object for mileage, first registration and horse power
    try:
        parent_obj = parsed_code.find("div", class_="cldt-stage-basic-data")
    except:
        print("Unable to find parent object")

    # mileage
    try:
        mileage = parent_obj.find("span", class_="sc-font-l cldt-stage-primary-keyfact").text.replace(",", "").split()[0]
        f_car_details.write("mileage : " + mileage + "\n")
    except:
        print("Unable to extract mileage")
        f_car_details.write("mileage : " + "\n")

    # first registration
    try:
        first_registration = parent_obj.find("span", class_="sc-font-l cldt-stage-primary-keyfact", attrs={"id":"basicDataFirstRegistrationValue"}).text
        f_car_details.write("first registration : " + first_registration + "\n")
    except:
        print("Unable to extract first registration date")
        f_car_details.write("first registration : " + "\n")

    # horse power
    try:
        horse_power = parent_obj.find("span", class_="sc-font-m cldt-stage-primary-keyfact").text.split()[0]
        f_car_details.write("horse power : " + horse_power + "\n")
    except:
        print("Unable to extract horse power")
        f_car_details.write("horse power : " + "\n")

    # EXTRACTING ATTRIBUTES AND ATTRIBUTE VALUES ON THE PAGE
    # parent object for attributes and attribute values
    try:
        parent_obj = parsed_code.find("div", class_="cldt-item", attrs={"data-item-name":"car-details"}) # parent object containing all other attributes
    except:
        print("Unable to extract parent object for other attributes")

    page_attributes = [] # List to hold attributes on the page
    page_attribute_features = [] # List to hold value of attributes on the page

    # Extracting Attributes on page
    try:
        for a in parent_obj.find_all("dt"):
            page_attributes.append(a.text.strip())
    except:
        print("Unable to extract attributes")

    # Extracting attribute values from the page
    try:
        for v in parent_obj.find_all("dd"):
            page_attribute_features.append(v.text.strip())
    except:
        print("Unable to extract attribute values")

    # writing values in the file
    if (len(page_attribute_features) == len(page_attributes)):
        for i in range(0, len(page_attributes)):
            f_car_details.write(str(page_attributes[i]) + " : " + str(page_attribute_features[i] + "\n"))
    else:
        f_car_details.write("FALSE" + "\n")
        print("Attribues and values have different lenghts" + "\n")

    counter = counter + 1

f_car_details.close()

now = datetime.now()
print("DATA SCRAPPING COMPLETED ON", now.strftime("%d-%B-%Y"), "at", now.strftime("%H:%M:%S"), "\n")

#####################
# CREATING CSV FILE #
#####################

now = datetime.now()
print("CSV CREATION STARED ON", now.strftime("%d-%B-%Y"), "at", now.strftime("%H:%M:%S"))

# CLEANING THE FILE

footer_text = "You can obtain more information on the official fuel consumption and official specific CO2 emissions of new passenger vehicles from the guideline on fuel consumption and CO2 emissions of new passenger vehicles. This guideline is available free of charge at all dealerships and from Deutsche Automobil Treuhand GmbH at www.dat.de."

f_car_details = open("car_details.txt", "r")
f_content = f_car_details.read()
car_details = f_content.split("\n")
car_details.pop(-1)

f_car_details_clean = open("car_details_clean.txt", "w")

for detail in car_details:
    if "https" in detail:
        f_car_details_clean.write("url_address : " + detail + "\n")

    elif footer_text in detail:
        a = detail.split("You")[0]
        b = detail.split(" : ")[1]
        f_car_details_clean.write(a + " : " + b + "\n")

    elif "(city)" in detail:
        f_car_details_clean.write("consumption_city" + " : " + detail + "\n")

    elif "(country)" in detail:
        f_car_details_clean.write("consumption_country" + " : " + detail + "\n")

    else:
        f_car_details_clean.write(detail + "\n")

f_car_details.close()
f_car_details_clean.close()

# GENERATING THE DATABASE FROM THE CLEANED FILE

f_car_details_clean = open("car_details_clean.txt", "r")
f_content_clean = f_car_details_clean.read()
car_details_clean = f_content_clean.split("\n")
car_details_clean.pop(-1)

footer_text = "You can obtain more information on the official fuel consumption and official specific CO2 emissions of new passenger vehicles from the guideline on fuel consumption and CO2 emissions of new passenger vehicles. This guideline is available free of charge at all dealerships and from Deutsche Automobil Treuhand GmbH at www.dat.de."

unique_attributes = [] # List to hold attributes

# Loop to extract attributes from text file
for detail in car_details_clean:

    if "url_address" in detail:
        unique_attributes.append("url_address")

    if ((("url_address" in detail) == False) & (" : " in detail)):
        unique_attributes.append((detail.split(" : ")[0]))

unique_attributes = set(unique_attributes) # set of unique attributes

final_dict = {} # Dictionary to hold attributes and their values for all cars

# Loop to initialize dictionary
for x in unique_attributes:
    final_dict[x] = []

# Loop to extract data from text file and populate final_dict
for i in range(0, len(car_details_clean)):

    # Checking if the current line is a link
    if "url_address" in car_details_clean[i]:
        my_dict = {}
        my_dict[car_details_clean[i].split(" : ")[0]] = car_details_clean[i].split(" : ")[1]

    # Checking if the the current line is not a link
    if ((("url_address" in car_details_clean[i]) == False) & (" : " in car_details_clean[i])):
        my_dict[car_details_clean[i].split(" : ")[0]] = car_details_clean[i].split(" : ")[1]

    # checking if it is the end of file (and also if the next line is a link)
    if i < (len(car_details_clean) - 2):
        # checking if the next line is a link
        if "url_address" in car_details_clean[i + 1]:
            # Loop to populate fianl_dict with my_dict
            for attribute in unique_attributes:
                if attribute in my_dict.keys():
                    final_dict[attribute].append(my_dict[attribute])
                else:
                    final_dict[attribute].append(None)


df = pd.DataFrame(final_dict)

# ARRANGING THE COLUMNS IN DESIRED ORDER

# Reading File input_desired_order (file containing desired order of columns)
f_desired_order = open("input_desired_order.txt", "r")
content_desired_order = f_desired_order.read()
desired_order = content_desired_order.split("\n")
desired_order.pop(-1)

df_clean = pd.DataFrame()

for x in desired_order:
    df_clean[x] = df[x]

df_clean.to_csv("car_details.csv", index=False)

now = datetime.now()
print("SUCCESSFULLY CREATED CSV ON", now.strftime("%d-%B-%Y"), "at", now.strftime("%H:%M:%S"), "\n")

now = datetime.now()
print("PROGRAM EXECUTION COMPLETED ON", now.strftime("%d-%B-%Y"), "at", now.strftime("%H:%M:%S"), "\n")