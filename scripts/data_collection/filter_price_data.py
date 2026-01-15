## THIS SCRIPT USES TOP SELLER DATA AND THE RAW PRICE DATA TO CREATE A CLEANER DATASET TO BE USED FOR
## MERGING, THE RESULTING DATASET WILL BE SAVED IN THE RAW DATA DIRECTORY
##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# import packages
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# load price and top seller data
price_data = pd.read_csv("../raw_data/price_data.csv")
top_data = pd.read_csv("../raw_data/top_items_data.csv")

# format retaurant columns
price_data["restaurant"] = price_data["restaurant"].apply(lambda x: x.lower().replace(" ", "_").replace("'", "").strip())
top_data["restaurant"] = top_data["restaurant"].apply(lambda x: x.lower().replace(" ", "_").replace("'", "").strip())

# rename mcdonalds, panera, and dominos in price data
price_data["restaurant"] = price_data["restaurant"].replace({"mcdonalds_with": "mcdonalds"})
price_data["restaurant"] = price_data["restaurant"].replace({"panera_bread": "panera"})
price_data["restaurant"] = price_data["restaurant"].replace({"dominos": "dominos_pizza"})

# filter down price data
restaurant_list = top_data["restaurant"].unique()
filtered_price_data = price_data[price_data["restaurant"].isin(restaurant_list)]

# clean item names to match
filtered_price_data["item"] = filtered_price_data["item"].apply(lambda x: x.replace("®", "").replace("™", ""))

# save filtered price data
filtered_price_data.to_csv("../raw_data/filtered_price_data.csv", index=False)