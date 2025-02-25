import pandas as pd
from my_functions import *
import csv


def calculate_language_proportions(file_name):
    """
    Calculates the proportion of languages for each 'Gear Type' and 'Color' combination.
    The result is saved to 'Language Proportions.csv'.

    :param file_name: The CSV file containing the dataset
    """
    # Load the data from the CSV
    df = pd.read_csv(file_name)

    # Group by 'Gear Type' and 'Color', then calculate the frequency of each 'Language'
    language_counts = df.groupby(['Gear Type', 'Color', 'Language']).size().reset_index(name='Count')

    # Group by 'Gear Type' and 'Color' to get the total count for each combination
    total_counts = df.groupby(['Gear Type', 'Color']).size().reset_index(name='Total')

    # Merge the counts with the total counts to calculate the proportions
    language_counts = language_counts.merge(total_counts, on=['Gear Type', 'Color'])

    # Calculate the proportion
    language_counts['Proportion'] = language_counts['Count'] / language_counts['Total']

    # Optionally, save the result to a CSV
    language_counts.to_csv('Language Proportions.csv', index=False)

    # Display the result in the console
    print(language_counts.head())  # Display the first few rows in the console


def process_master_data():
    # Define allowed gear types
    allowed_gear_types = {"buoy", "float", "hard plastic", "metal", "line"}

    # Define allowed colors (from the keys of the color mapping dict)
    allowed_colors = ["multi", "black", "orange", "blue", "white", "green", "red",
                      "yellow", "grey", "clear", "silver", "rust", "pink"]

    # Load the master dataset
    file = "HPU Master Data.csv"
    df = pd.read_csv(file)

    # Step 1: Remove duplicates based on 'ID Name', keeping the first instance
    df_cleaned = df.drop_duplicates(subset='ID Name', keep='first')

    # Step 2: Remove rows where 'Gear Type' or 'Color' are missing (NaN)
    df_cleaned = df_cleaned.dropna(subset=['Gear Type', 'Color'])

    # Step 3: Select only the columns we want
    columns_to_keep = ['ID Name', 'Gear Type', 'Color', 'Language']
    df_cleaned = df_cleaned[columns_to_keep]

    # Step 4: Convert DataFrame to list of dictionaries
    df_dict = df_cleaned.to_dict(orient='records')

    # Step 5: Apply the data cleaning functions to Gear Type and Color
    df_dict = convert_to_lower(df_dict, 'Gear Type')  # Apply to Gear Type
    df_dict = convert_to_lower(df_dict, 'Color')  # Apply to Color
    df_dict = convert_to_lower(df_dict, 'Language')  # Apply to Language - will safely skip missing values

    # Step 6: Filter for allowed gear types and colors
    df_dict = [item for item in df_dict if item['Gear Type'] in allowed_gear_types
               and item['Color'] in allowed_colors]

    # Step 7: Remove substrings from Language field
    df_dict = remove_substrings_from_languages(df_dict)

    # Save filtered data to new CSV
    output_file = "HPU Master Data Filtered.csv"
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns_to_keep)
        writer.writeheader()
        writer.writerows(df_dict)

    print(f"\nTotal entries in filtered dataset: {len(df_dict)}")
    print(f"Filtered data has been saved to {output_file}")
    print("\nFirst few entries in filtered dataset:")
    for item in df_dict[:5]:  # Print first 5 entries to verify
        print(item)

    return df_dict


# Using the cleaned up subset data that main.py creates a CSV for, we will calculate the proportional breakdown of language given a gear-color combination.
# Based on these proportions we will run a simulation to assign a language to a specific gear-color instance when the language is unknown. This is gathered from the HPU Master Data Filtered.csv
# The assigned proportions based on the probabilities gathered from the sample of the original subset it then assigned and stored in Simulation Outcomes.csv

calculate_language_proportions('HPU Subset Data Final.csv')
df_dict = process_master_data()
