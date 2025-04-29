import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

LIST_ACCEPTED_LANGUAGES = ["english", "chinese", "mandarin", "japanese", "korean", "spanish", "vietnamese", "greek"]
ACCEPTED_GEAR_TYPES = ["buoy", "float", "line", "hard plastic", "metal"]
ALLOWED_COLORS = ["multi", "black", "orange", "blue", "white", "green", "red",
                  "yellow", "grey", "clear", "silver", "rust", "pink"]

def clean_data(df):
    """
    Cleans and filters the input DataFrame.
    Returns only relevant, standardized, and validated entries.
    """
    df = df[['ID Name', 'Gear Type', 'Color', 'Language']].copy()

    for col in ['Gear Type', 'Color', 'Language']:
        df[col] = df[col].str.lower()

    # Filter for accepted gear types and allowed colors
    df = df[df['Gear Type'].isin(ACCEPTED_GEAR_TYPES)]
    df = df[df['Color'].isin(ALLOWED_COLORS)]

    # Remove unwanted substrings from Language
    substrings_to_remove = ["arabic numbers", "latin letters", "?", "/", " ", "(", ")"]
    def clean_language_column(lang):
        if pd.isna(lang):
            return lang
        for sub in substrings_to_remove:
            lang = lang.replace(sub, "")
        return lang
    df['Language'] = df['Language'].apply(clean_language_column)

    # Filter accepted language substrings
    df = df[df['Language'].apply(lambda x: any(lang in x for lang in LIST_ACCEPTED_LANGUAGES) if isinstance(x, str) else False)]

    # Keep only first valid language
    def split_first_valid_language(value):
        if not isinstance(value, str):
            return value
        for lang in LIST_ACCEPTED_LANGUAGES:
            if value.startswith(lang):
                return lang
        return value
    df['Language'] = df['Language'].apply(split_first_valid_language)

    df['Language'] = df['Language'].replace('mandarin', 'chinese')

    return df

def plot_stacked_bar(ax, labels, frequencies, title, color_map=None):
    """
    Draws a single stacked bar chart on the provided axis.
    Each segment represents a category with proportional frequency.
    """
    total = sum(frequencies)
    rel_freq = [(f / total) * 100 for f in frequencies]
    sorted_data = sorted(zip(labels, rel_freq), key=lambda x: x[1], reverse=True)
    labels, rel_freq = zip(*sorted_data)

    bottoms = 0
    for i, (label, freq) in enumerate(zip(labels, rel_freq)):
        color = color_map.get(label, f"C{i}") if color_map else f"C{i}"
        ax.bar(0, freq, bottom=bottoms, color=color, label=f"{label} ({freq:.1f}%)")
        bottoms += freq

    ax.set_ylim(0, 100)
    ax.set_ylabel("Relative Frequency (%)")
    ax.set_title(title)
    ax.set_xticks([])
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

def plot_all_stacked_bars(df):
    """
    Groups cleaned data and generates three stacked bar plots:
    1. Garbage by Country (from Language)
    2. Garbage by Gear Type
    3. Garbage by Color
    """
    lang_to_country = {
        "english": "USA", "chinese": "China", "japanese": "Japan",
        "vietnamese": "Vietnam", "greek": "Greece", "korean": "South Korea",
        "spanish": "LATAM"
    }

    country_freq = df['Language'].map(lang_to_country).fillna("Unknown").value_counts()
    gear_freq = df['Gear Type'].value_counts()
    color_freq = df['Color'].value_counts()

    color_mapping = {
        "multi": "limegreen", "black": "black", "orange": "orange", "blue": "blue",
        "white": "white", "green": "green", "red": "red", "yellow": "yellow",
        "grey": "grey", "clear": "#d3d3d3", "silver": "silver", "rust": "#b7410e", "pink": "pink"
    }

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    plot_stacked_bar(axes[0], country_freq.index.tolist(), country_freq.tolist(), "Garbage by Country")
    plot_stacked_bar(axes[1], gear_freq.index.tolist(), gear_freq.tolist(), "Garbage by Gear Type")
    plot_stacked_bar(axes[2], color_freq.index.tolist(), color_freq.tolist(), "Garbage by Color", color_map=color_mapping)

    plt.tight_layout()
    plt.show()

# ----------------------- MAIN ----------------------- #

input_file = 'HPU Subset Data.csv'
output_file = 'HPU Subset Data Filtered.csv'

df_raw = pd.read_csv(input_file)
print(f"Original entry count: {len(df_raw)}")

df_cleaned = clean_data(df_raw)
print(f"Filtered entry count: {len(df_cleaned)}")

df_cleaned.to_csv(output_file, index=False)
print(f"Saved cleaned CSV to '{output_file}'.")

plot_all_stacked_bars(df_cleaned)
