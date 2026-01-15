### merge top_items_data.csv and labelled_data.csv


import pandas as pd

# Load the two datasets
top_items_df = pd.read_csv("raw_data/top_items_data.csv")
labelled_df = pd.read_csv("raw_data/labelled_data.csv")

labelled_df = labelled_df.drop(columns=['Unnamed: 0', 'menu_item_id', 'serving_size_text', 'serving_size_household', 'potassium', 'notes', 'calories_text', 'total_fat_text', 'saturated_fat_text', 'trans_fat_text',
       'cholesterol_text', 'sodium_text', 'carbohydrates_text', 'serving_size', 'serving_size_unit', 
       'dietary_fiber_text', 'sugar_text', 'protein_text'])

labelled_df = labelled_df.rename(columns={'bestseller': 'bestseller_5'})
print(labelled_df.columns)

labelled_df['item'] = labelled_df['item'].str.replace(r'\bMeal\b', '', case=False, regex=True).str.strip()

top_items_df['restaurant'] = (
    top_items_df['restaurant']
    .str.lower()                      # convert to lowercase
    .str.replace("'", "", regex=False)  # remove apostrophes
    .str.replace(" ", "_", regex=False) # replace spaces with underscores
)

# merge not working well
# merged_df = labelled_df.merge(
#     top_items_df,
#     left_on=['restaurant', 'item'],
#     right_on=['restaurant', 'popular_item'],
#     how='left',
# )

# Normalize both columns for better matching
labelled_df['item'] = labelled_df['item'].str.lower().str.strip()
labelled_df['ms_item'] = labelled_df['ms_item'].str.lower().str.strip()
top_items_df['popular_item'] = top_items_df['popular_item'].str.lower().str.strip()

# Function to check if any popular item from the same restaurant is in the item string
def is_bestseller(row):
    restaurant = row['restaurant']
    item_text = row['item']
    ms_item_text = row['ms_item']
    
    popular_items = top_items_df[top_items_df['restaurant'] == restaurant]['popular_item']
    return any((pop_item in item_text) or (pop_item in ms_item_text) for pop_item in popular_items)

# Apply the function to label bestsellers
labelled_df['bestseller'] = labelled_df.apply(is_bestseller, axis=1)

merged_df = labelled_df



# Show the column names to help decide how to merge
# top_items_df_columns = top_items_df.columns.tolist()
# labelled_df_columns = labelled_df.columns.tolist()

# top_items_df_columns, labelled_df_columns

# # Step 1: Normalize item names by lowercasing and stripping whitespace
# top_items_df['popular_item_clean'] = top_items_df['popular_item'].str.lower().str.strip()
# labelled_df['ms_item_clean'] = labelled_df['ms_item'].astype(str).str.lower().str.strip()

# Step 2: Try merging on 'restaurant' and 'item_clean' first
# merged_on_item = labelled_df.merge(
#     top_items_df,
#     left_on=['restaurant', 'ms_item_clean'],
#     right_on=['restaurant', 'popular_item_clean'],
#     how='left',
#     indicator=True
# )

print(merged_df.columns)


if 'bestseller' in merged_df.columns:
    bestseller_counts = merged_df['bestseller'].value_counts()
    print("\nBestseller Distribution:")
    print(bestseller_counts)

# Fill missing values in the 'bestseller' column with 0
merged_df['bestseller'] = merged_df['bestseller'].fillna(0).astype(int)

# Remove duplicate rows
merged_df = merged_df.drop_duplicates()

# Remove dollar signs or other non-numeric characters if present
merged_df['price'] = merged_df['price'].replace('[\$,]', '', regex=True)

# Convert to float
merged_df['price'] = pd.to_numeric(merged_df['price'], errors='coerce')

# Group by all columns except 'price' and average the price
group_cols = ['restaurant', 'item', 'bestseller']

# Group and average
averaged_df = (
    merged_df
    .groupby(group_cols, as_index=False)
    .agg({'price': 'mean'})
)

# Drop old price column before merging
merged_df_no_price = merged_df.drop(columns=['price'])

# Merge the averaged price back in
final_df = merged_df_no_price.merge(
    averaged_df,
    on=['restaurant', 'item', 'bestseller'],
    how='left'
)

#merged_df = merged_df.drop(index=[153, 155])
print("Final_df length\n")
print(len(final_df))

# Remove duplicate rows
final_df = final_df.drop_duplicates()

# Count the number of 1s and 0s in the 'bestseller' column
bestseller_counts = final_df['bestseller'].value_counts()

# Print the counts
print("\nBestseller Counts:")
print(f"1 (Bestseller): {bestseller_counts.get(1, 0)}")
print(f"0 (Not Bestseller): {bestseller_counts.get(0, 0)}")

# Drop the 'bestseller_5' column
final_df = final_df.drop(columns=['bestseller_5'], errors='ignore')

# Save the merged dataframe to a CSV file
final_df.to_csv("clean_data/final_merged_data.csv", index=False)

# Step 3: Mark bestseller based on match
#merged_on_item['bestseller_flag'] = (merged_on_item['_merge'] == 'both').astype(int)

# # Step 4: For rows not matched, try again using 'ms_item_clean'
# not_matched = merged_on_item[merged_on_item['bestseller_flag'] == 0].copy()
# matched_ids = merged_on_item[merged_on_item['bestseller_flag'] == 1].index

# # Try merging remaining on 'ms_item_clean'
# second_merge = not_matched.merge(
#     top_items_df,
#     left_on=['restaurant', 'ms_item_clean'],
#     right_on=['restaurant', 'popular_item_clean'],
#     how='left',
#     indicator=True
# )

# Mark matches
# second_merge['bestseller_flag'] = (second_merge['_merge'] == 'both').astype(int)

# # Combine matches from both rounds
# final_combined = pd.concat([
#     merged_on_item.loc[matched_ids],
#     second_merge
# ], ignore_index=True)

# # Count how many items are matched as bestsellers
# bestseller_count = final_combined['bestseller_flag'].sum()
# non_bestseller_count = len(final_combined) - bestseller_count

# bestseller_count, non_bestseller_count
