# About this project

This is a portfolio project developed by the author to illustrate the author's web scrapping capabilities in python. The inspiration for this project came from a job description uploaded on Upwork
___

# Objective of this project

There are two objectives this python script aims to achieve:
- Collect the details of all used cars listed for sale on https://www.autoscout24.com
- Present the data in the form of a comma seprated file(.csv)
___

# How the python script works ?

The python script follows the following control flow:

1. Read the required url and the total number of pages from <mark><i>input_website.txt</i></mark>
2. Extract Search ID for the url provided in <mark><i>input_website.txt</i></mark>
3. Extract the urls of cars from all the pages and save it in <mark><i>urls.txt</i></mark>
4. Read <mark><i>urls.txt</i></mark> and save extracted the car deatils along with urls in <mark><i>car_details.txt</i></mark>
5. Clean the data in <mark><i>car_details.txt</i></mark> and save the results in <mark><i>car_details_clean.txt</i></mark>
6. Read the results of <mark><i>car_details_clean.txt</i></mark> and store the results in a pandas dataframe
7. Arrange the columns of the dataframe as per the order provided in <mark><i>input_desired_order.txt</i></mark>
___

# Function of various files in this project

- <mark><i>scrapping_script.py</i></mark> : Python file containing the coscript required to do the web scrapping
- <mark><i>input_website.txt</i></mark> : Text file containing the following information:
  - the first line contains the url of the page containing the search results
  - the second line contains the page number of the last page
- <mark><i>input_desired_order.txt</i></mark> : This file contains the name of the column in desired order
- <mark><i>urls.txt</i></mark> : Text file generated when the script is executed. This stores the urls of all the vehicle listed on https://www.autoscout24.com
- <mark><i>car_details.txt</i></mark> : Text file generated during the exection of the script. This contains all the attributes and their values for al the cars whose urls are listed in <mark><i><mark><i>urls.txt</i></mark></i></mark>.
-  <mark><i>car_details_clean.txt</i></mark> : Text file generated during the execution of the script. Certain data cleaning operations are performed on <mark><i>car_details.txt</i></mark> and results are stored in <mark><mark><i>car_details_clean.txt</i></mark></mark>

___

# How to use this script

In order to use this script please follow the following steps:
- Edit <mark><i>input_website.txt</i></mark> :
  - The first line should containt the url of the page (note*: This script can only scrape https://www.autoscout24.com)
  - The second line should contain the page number of the last page of the search results
- OPTIONAL - Edit <mark><i>input_desired_order.txt</i></mark> :
  - This file contains the order of the column names which will be sued to create the <mark><i>car_details.csv</i></mark>

___

###### Developer Notes

```python
link_url = parent_obj.find("a", href=True)["href"] # Partial address of the car
final_url = "https://www.autoscout24.com" + link_url + "?cldtidx=1&cldtsrc=listPage&searchId=" + str(sid) # Complete Address of the car
```

Acessing the value of the "href" tag does not gives the entire address hence it needs to be constructed as shown above

```python
sid_html = parsed_code.find("script", id="cl-search-id") # HTML code containig search id
sid_str = str(sid_html) # Converting html code of search id to string
sid = sid_str.split(":")[1].split("}")[0] # Search id
sid = sid.lstrip() # Stripping white space from the beginnig of the strip
print("Search id Successuffly extracted on", now.strftime("%d-%B-%Y"), "at", now.strftime("%H:%M:%S"),  "\n")
```

The address of the car listing is incomplete without the search id which is extracted as shown above


```python
footer_text = "You can obtain more information on the official fuel consumption and official specific CO2 emissions of new passenger vehicles from the guideline on fuel consumption and CO2 emissions of new passenger vehicles. This guideline is available free of charge at all dealerships and from Deutsche Automobil Treuhand GmbH at www.dat.de."
```


The above string is added as a footer in some of the attributes hence it is extracted while extracting the attributes from a listing.
A workaround that involves the filtering of this unwanted string at the time of extraction would be a more complex approach hence it is filtered out from the text file which contains scrapped data i.e. <mark><i>car_details.txt</mark><i>
