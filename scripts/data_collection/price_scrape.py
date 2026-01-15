## THIS SCRIPT SCRAPES PRICE DATA FROM FASTFOODMENUPRICES.COM (https://fastfoodmenuprices.com/)
## AND SAVES THE RESULTING CSV FILE IN THE RAW_DATA DIRECTORY
##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# import required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import warnings
warnings.filterwarnings("ignore")


# get html content from homepage
site_url = "https://fastfoodmenuprices.com/all-restaurants/"
site_response = requests.get(site_url)
site_html_content = site_response.text

# parse homepage and get restaurant list
site_soup = BeautifulSoup(site_html_content, "html.parser")
restaurant_list = site_soup.find("ul", class_="restaurants-list")
list_length = len(restaurant_list)/2


# loop over restaurants on homepage
first_run = True
check = .1
count = 1
for line in restaurant_list.find_all("li"):

    # get restaurant name
    restaurant = str(line.find("a").contents[0]).strip()

    # get url
    url = line.find("a")["href"]

    # get all tables from restaurant page
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    all_tables = soup.find_all("table")

    # loop over all tables to build dataframe
    first = True
    for table in all_tables:

        # initialize data
        data = []

        # iterate over rows in table
        for row in table.find_all("tr")[1:]:
            data.append([td.text for td in row.find_all("td")])

        # build dataframe
        if first:
            df = pd.DataFrame(data)
            first = False
        else:
            df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    
    # create formatted dataframe
    format_df = pd.DataFrame(df[0]).rename(columns={0: "item"})
    format_df["restaurant"] = restaurant

    # find, clean, and add price column
    success = False
    for col in df:
        try:
            if re.fullmatch(r"[$]*\d+.\d+", df[col][1]):
                success = True
                price_list = []
                for price in df[col]:
                    try:
                        price_list.append(price.strip().replace("$",""))
                    except:
                        price_list.append(pd.NA)
        except:
            pass
    if success:
        format_df["price_usd"] = price_list
    else:
        format_df["price_usd"] = pd.NA

    # build final dataframe
    if first_run:
        price_data = format_df
        first_run = False
    else:
        price_data = pd.concat([price_data, format_df], ignore_index=True)

    # print progress
    if count/list_length >= check:
        check += .1
        print(f"{round((count/list_length)*100, 0)}% complete...")
    count += 1
print("Complete.")

# drop rows with NA values
price_data = price_data.dropna()


# save price data to csv
price_data.to_csv("../raw_data/price_data.csv", index=False)