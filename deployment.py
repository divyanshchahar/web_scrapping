# Importing Libraries and Functionality
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd

now = datetime.now()
print("EXECUTION STARTED ON ", now.strftime("%d-%B-%Y"), "at", now.strftime("%H:%M:%S"), "\n")

# Reading Essential data from website.txt
f_website = open("website.txt", "r")
f_website_content = f_website.readlines()

basic_url = f_website_content[0].split("page=")[0] + "page=" # First half of URL
url_extension = f_website_content[0].split("page=1")[1] # Second half of URL

page_num = list(range(1, int(f_website_content[1])+1)) # List containing page numbers


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

f_all_urls = open("urls.txt", "w")

for p in page_num:

    page_url = basic_url + str(p) + url_extension  # Creating URL of the page

    code_url = requests.get(page_url).text  # HTML code of the page
    parsed_code = BeautifulSoup(code_url, "lxml")  # parsed HTML code of the page

    # Loop to extract URLs
    for parent_obj in parsed_code.find_all("div", class_="cl-list-element cl-list-element-gap"):

        link_url = parent_obj.find("a", href=True)["href"] # Partial address of the car

        final_url = "https://www.autoscout24.com" + link_url + "?cldtidx=1&cldtsrc=listPage&searchId=" + str(sid) # Complete Address of the car

        f_all_urls.write(final_url + "\n") # Writing results to a file

    print("Completed pages ", p, "out of ", page_num[-1])

f_all_urls.close()

now = datetime.now()
print("URL EXTRACTION COMPLETE  ON", now.strftime("%d-%B-%Y"), "at", now.strftime("%H:%M:%S"), "\n")

###################
# EXTRACTING DATA #
###################

now = datetime.now()
print("DATA SCRAPPING STARTED ON", now.strftime("%d-%B-%Y"), "at", now.strftime("%H:%M:%S"), "\n")

f_all_urls = open("urls.txt", "r") # File Object for the urls file
content_all_urls = f_all_urls.read() # Reading content form the file
url_items = content_all_urls.split("\n") # Splitting into different urls by line ending
url_items.pop(-1) # Removing last line(because it is blank)

f_attributes_data = open("car_details.txt", "w")

attributes1 = ["price", "car name", "variant", "mileage", "first registration", "horse power"] # List of attributes

temp1 = [] # First list to hold values of attributes, same for all page (attributes1)
temp2 = [] # Second list to hold value of attibutes, different for different pages(attributes2)

# Loop to initialize first list
for i in range(0, len(attributes1)):
    temp1.append([])

counter = 1

# LOOP TO ITERATE THROUGH URLs
for page_url in url_items:

    print(counter, "out of ", len(url_items))

    f_attributes_data.write(page_url + "\n") # Writing page url to file

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
        f_attributes_data.write("name : " + vehicle_name + "\n")
    except:
        print("Unable to extract vehicle name")
        f_attributes_data.write("name : " + "\n")

    # vehicle variant
    try:
        vehicle_variant = parent_obj.find("span", class_="cldt-detail-version sc-ellipsis").text
        f_attributes_data.write("variant : " + vehicle_variant + "\n")
    except:
        print("Unable to extract vehicle variant")
        f_attributes_data.write("variant : " + "\n")

    f_attributes_data.write("price : " + price + "\n")  # writing price to the file

    # EXTRACTING MILEAGE, FIRST REGISTRATION, HORSE POWER

    # parent object for mileage, first registration and horse power
    try:
        parent_obj = parsed_code.find("div", class_="cldt-stage-basic-data")
    except:
        print("Unable to find parent object")

    # mileage
    try:
        mileage = parent_obj.find("span", class_="sc-font-l cldt-stage-primary-keyfact").text.replace(",", "").split()[0]
        f_attributes_data.write("mileage : " + mileage + "\n")
    except:
        print("Unable to extract mileage")
        f_attributes_data.write("mileage : " + "\n")

    # first registration
    try:
        first_registration = parent_obj.find("span", class_="sc-font-l cldt-stage-primary-keyfact", attrs={"id":"basicDataFirstRegistrationValue"}).text
        f_attributes_data.write("first registration : " + first_registration + "\n")
    except:
        print("Unable to extract first registration date")
        f_attributes_data.write("first registration : " + "\n")

    # horse power
    try:
        horse_power = parent_obj.find("span", class_="sc-font-m cldt-stage-primary-keyfact").text.split()[0]
        f_attributes_data.write("horse power : " + horse_power + "\n")
    except:
        print("Unable to extract horse power")
        f_attributes_data.write("horse power : " + "\n")

    # EXTRACTING ATTRIBUTES AND ATTRIBUTE VALUES ON THE PAGE

    try:
        parent_obj = parsed_code.find("div", class_="cldt-item", attrs={"data-item-name":"car-details"}) # parent object containing all other attributes
    except:
        print("Unable to extract parent object for other attributes")

    page_attributes = []
    page_attribute_features = []

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
            f_attributes_data.write(str(page_attributes[i]) + " : " + str(page_attribute_features[i] + "\n"))
    else:
        f_attributes_data.write("FALSE" + "\n")
        print("Attribues and values have different lenghts" + "\n")

    counter = counter + 1

f_attributes_data.close()

now = datetime.now()
print("DATA SCRAPPING COMPLETED ON", now.strftime("%d-%B-%Y"), "at", now.strftime("%H:%M:%S"), "\n")

#####################
# CREATING CSV FILE #
#####################

f_car_details = open("car_details.txt", "r")
f_content = f_car_details.read()
car_details = f_content.split("\n")
car_details.pop(-1)

footer_text = "You can obtain more information on the official fuel consumption and official specific CO2 emissions of new passenger vehicles from the guideline on fuel consumption and CO2 emissions of new passenger vehicles. This guideline is available free of charge at all dealerships and from Deutsche Automobil Treuhand GmbH at www.dat.de."

unique_attributes = [] # List to hold attributes


# Loop to extract attributes from text file
for detail in car_details:

    if "https" in detail:
        pass

    if ((("https" in detail) == False) & (" : " in detail)):
        unique_attributes.append((detail.split(" : ")[0]))

unique_attributes = set(unique_attributes) # set of unique attributes

final_dict = {} # Dictionary to hold attributes and their values for all cars

# Loop to initialize dictionary
for x in unique_attributes:
    final_dict[x] = []

# Loop to extract data from text file and populate final_dict
for i in range(0, len(car_details)):

    # Checking if the current line is a link
    if "https" in car_details[i]:
        my_dict = {}

    # Checking if the the current line is not a link
    if ((("https" in car_details[i]) == False) & (" : " in car_details[i])):
        my_dict[car_details[i].split(" : ")[0]] = car_details[i].split(" : ")[1]

    # checking if it is the end of file (and also if the next line is a link)
    if i < (len(car_details) - 2):
        # checking if the next line is a link
        if "https" in car_details[i+1]:
            # Loop to populate fianl_dict with my_dict
            for attribute in unique_attributes:
                if attribute in my_dict.keys():
                    final_dict[attribute].append(my_dict[attribute])
                else:
                    final_dict[attribute].append(None)


df = pd.DataFrame(final_dict)

df.to_csv("car_details.csv", index=False)