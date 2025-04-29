"""
simulate_missing.py

This script loads the full HPU Master Data file, filters it down to only
relevant and valid rows, and fills in missing Language values using
weighted probabilities learned from the subset sample (language_proportions.csv).

Output files:
- HPU Master Data Filtered.csv → Cleaned version ready for simulation
- HPU Simulated Data.csv → Final dataset with simulated Language values
"""

import pandas as pd
import numpy as np

# Accepted values from your main logic
LIST_ACCEPTED_LANGUAGES = ["english", "chinese", "mandarin", "japanese", "korean", "spanish", "vietnamese", "greek"]
ACCEPTED_GEAR_TYPES = ["buoy", "float", "line", "hard plastic", "metal"]
ALLOWED_COLORS = ["multi", "black", "orange", "blue", "white", "green", "red",
                  "yellow", "grey", "clear", "silver", "rust", "pink"]


def clean_master_data(df):
    """
    Filters and standardizes the master data:
    - Keeps only required columns
    - Converts to lowercase
    - Filters out invalid Gear Type or Color
    - Cleans Language field but still allows missing values
    """
    df = df[['ID Name', 'Gear Type', 'Color', 'Language']].copy()

    for col in ['Gear Type', 'Color', 'Language']:
        df[col] = df[col].str.lower()

    df = df[df['Gear Type'].isin(ACCEPTED_GEAR_TYPES)]
    df = df[df['Color'].isin(ALLOWED_COLORS)]

    # Step 1: Remove substrings from Language (if not NaN)
    substrings_to_remove = ["arabic numbers", "latin letters", "?", "/", " ", "(", ")"]
    def clean_lang(value):
        if pd.isna(value):
            return value
        for sub in substrings_to_remove:
            value = value.replace(sub, "")
        return value

    df['Language'] = df['Language'].apply(clean_lang)

    # Step 2: Filter out bad language entries — unless it's still NaN
    def is_valid_lang_or_blank(value):
        if pd.isna(value) or value == "":
            return True  # keep blank (we’ll simulate it)
        return any(lang in value for lang in LIST_ACCEPTED_LANGUAGES)

    df = df[df['Language'].apply(is_valid_lang_or_blank)]

    # Step 3: Keep only first valid language if combined
    def extract_first_lang(value):
        if pd.isna(value):
            return value
        for lang in LIST_ACCEPTED_LANGUAGES:
            if value.startswith(lang):
                return lang
        return value

    df['Language'] = df['Language'].apply(extract_first_lang)

    # Step 4: Normalize mandarin to chinese
    df['Language'] = df['Language'].replace("mandarin", "chinese")

    return df


def load_language_proportions(file_path):
    """
    Loads language proportions from CSV and builds a lookup dictionary
    keyed by (Gear Type, Color).
    """
    proportions_df = pd.read_csv(file_path)
    lookup = {}

    for _, row in proportions_df.iterrows():
        key = (row['Gear Type'], row['Color'])
        if key not in lookup:
            lookup[key] = []
        lookup[key].append((row['Language'], row['Proportion']))

    return lookup


def simulate_language(row, lookup):
    """
    Uses probabilities from the lookup table to fill in missing Language.
    If no match found for (Gear Type, Color), leaves Language as is.
    """
    if pd.isna(row['Language']):
        key = (row['Gear Type'], row['Color'])
        options = lookup.get(key)
        if options:
            langs, probs = zip(*options)
            probs = np.array(probs)
            probs = probs / probs.sum()  # Normalize to ensure sum = 1
            return np.random.choice(langs, p=probs)
    return row['Language']


def simulate_missing_languages(master_file, proportions_file, filtered_output_file, simulated_output_file):
    """
    Main runner:
    - Loads and filters master data
    - Saves filtered master data
    - Simulates missing Language values
    - Flags which rows were filled
    - Saves final simulated dataset
    """
    df = pd.read_csv(master_file)
    df = clean_master_data(df)

    # Print available entries
    print(f"There are {len(df)} available rows to simulate.")

    # Save filtered master dataset
    df.to_csv(filtered_output_file, index=False)
    print(f"Saved filtered master dataset to '{filtered_output_file}'.")

    lookup = load_language_proportions(proportions_file)

    # Track which were simulated
    df['Simulated'] = df['Language'].isna()
    df['Language'] = df.apply(simulate_language, axis=1, lookup=lookup)

    # Save final simulated dataset
    final_output_file = simulated_output_file
    df.to_csv(final_output_file, index=False)
    print(f"Saved simulated dataset to '{final_output_file}'.")

    # Final check: how many were retained (not simulated)
    num_retained = (~df['Simulated']).sum()
    print(f"{num_retained} rows already had a known Language (not simulated).")

# ----------------------- MAIN ----------------------- #


if __name__ == "__main__":
    simulate_missing_languages(
        master_file='HPU Master Data.csv',
        proportions_file='language_proportions.csv',
        filtered_output_file='HPU Master Data Filtered.csv',
        simulated_output_file='HPU Simulated Data.csv'
    )
