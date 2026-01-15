## THIS SCRIPT SCRAPES "POPULAR ITEMS" DATA FROM FASTFOODNUTRITION.ORG (https://fastfoodnutrition.org/fast-food-restaurants)
## AND SAVES THE RESULTING CSV FILE IN THE RAW_DATA DIRECTORY
##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from bs4 import BeautifulSoup
import csv
import time
import random
import re
import pandas as pd

# setup selenium 
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in background
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

base_url = 'https://fastfoodnutrition.org'
main_url = f'{base_url}/fast-food-restaurants'

driver.get(main_url)
time.sleep(2)

soup = BeautifulSoup(driver.page_source, 'html.parser')

# get restaurant links
restaurant_links = []
for a in soup.select('div.logo_box a[href]'):
    href = a['href']
    full_url = f'{base_url}{href}/popular'
    restaurant_links.append(full_url)

print(f"Found {len(restaurant_links)} restaurants")

# scrape popular items
with open('raw_data/top_items_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['restaurant', 'popular_item'])

    for link in restaurant_links:
        try:
            print(f"Scraping {link}...")
            driver.get(link)
            time.sleep(2)

            # close popup ad
            try:
                close_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.popup a.close, .modal-close, .popup-close"))
                )
                close_button.click()
                print("Closed a pop-up ad")
                time.sleep(1)
            except (TimeoutException, NoSuchElementException):
                pass
            except ElementClickInterceptedException:
                print("Ad close button blocked, trying again after scroll")
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(1)
                try:
                    close_button.click()
                except:
                    pass

            # scroll to bottom of webpage
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # wait for the actual menu list to appear
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ul.list.mobilenoround.allround"))
                )
            except TimeoutException:
                print("Timed out waiting for menu list.")
                # skip to next restuarant
                continue 

            # parse top items
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # clean the restaurant name
            restaurant_name = soup.find('h1').text.replace("Most Popular Items at ", "").strip()

            # extract and clean popular item names
            items = []
            for li in soup.select("ul.list.mobilenoround.allround li"):
                text_div = li.select_one("div.col-9")
                if text_div:
                    item_name = text_div.get_text(separator=" ", strip=True)
                    item_name = item_name.split("#")[0].strip()
                    item_name = re.sub(r"[™®©]", "", item_name)
                    item_name = item_name.strip()
                    items.append(item_name)


            print(f"{restaurant_name}: {len(items)} items found")

            # write top 15 to CSV
            for item in items[:15]:
                writer.writerow([restaurant_name, item])



            time.sleep(random.uniform(1, 2))

        except TimeoutException:
            print(f"Timeout waiting for popular items on {link}")
        except Exception as e:
            print(f"Error scraping {link}: {type(e).__name__} - {e}")

driver.quit()

# Load the CSV file
csv_file_path = 'raw_data/top_items_data.csv'
df = pd.read_csv(csv_file_path)

# Add the "bestseller" column with the label 1
df['bestseller'] = 1

# Remove duplicate rows
df = df.drop_duplicates()

# Save the updated CSV file
df.to_csv(csv_file_path, index=False)

print(f"Updated CSV file saved with 'bestseller' column added.")





