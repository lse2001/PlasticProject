import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

LIST_ACCEPTED_LANGUAGES = ["english", "chinese", "mandarin", "japanese", "korean", "spanish", "vietnamese", "greek"]
ACCEPTED_GEAR_TYPES = ["buoy", "float", "line", "hard plastic", "metal"]
ALLOWED_COLORS = ["multi", "black", "orange", "blue", "white", "green", "red",
                  "yellow", "grey", "clear", "silver", "rust", "pink"]

def clean_data(df):
    df = df[['ID Name', 'Gear Type', 'Color', 'Language']].copy()
    for col in ['Gear Type', 'Color', 'Language']:
        df[col] = df[col].str.lower()

    df = df[df['Gear Type'].isin(ACCEPTED_GEAR_TYPES)]
    df = df[df['Color'].isin(ALLOWED_COLORS)]

    substrings_to_remove = ["arabic numbers", "latin letters", "?", "/", " ", "(", ")"]
    def clean_language_column(lang):
        if pd.isna(lang):
            return lang
        for sub in substrings_to_remove:
            lang = lang.replace(sub, "")
        return lang
    df['Language'] = df['Language'].apply(clean_language_column)

    df = df[df['Language'].apply(lambda x: any(lang in x for lang in LIST_ACCEPTED_LANGUAGES) if isinstance(x, str) else False)]

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


def add_single_bar_to_chart(ax, labels, frequencies, title, color_map=None):
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
    add_single_bar_to_chart(axes[0], country_freq.index.tolist(), country_freq.tolist(), "Garbage by Country")
    add_single_bar_to_chart(axes[1], gear_freq.index.tolist(), gear_freq.tolist(), "Garbage by Gear Type")
    add_single_bar_to_chart(axes[2], color_freq.index.tolist(), color_freq.tolist(), "Garbage by Color", color_map=color_mapping)

    plt.tight_layout()


def plot_horizontal_language_stacked_bars(df):
    grouped = df.groupby(['Gear Type', 'Color', 'Language']).size().reset_index(name='Count')
    pivot = grouped.pivot_table(index=['Gear Type', 'Color'], columns='Language', values='Count', fill_value=0)
    proportions = pivot.div(pivot.sum(axis=1), axis=0)
    proportions = proportions.sort_index()

    fig, ax = plt.subplots(figsize=(10, len(proportions) * 0.4))
    bottom = pd.Series([0] * len(proportions), index=proportions.index)

    for language in proportions.columns:
        ax.barh(
            proportions.index.map(lambda x: f"{x[0]} / {x[1]}"),
            proportions[language] * 100,
            left=bottom,
            label=language
        )
        bottom += proportions[language] * 100

    ax.set_xlabel("Proportion (%)")
    ax.set_title("Language Proportions by Gear Type and Color")
    ax.legend(title="Language", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()


# ----------------------- MAIN ----------------------- #

input_file = 'HPU Subset Data.csv'
output_file = 'HPU Subset Data Filtered.csv'

df_raw = pd.read_csv(input_file)
print(f"Original entry count: {len(df_raw)}")

df_cleaned = clean_data(df_raw)
print(f"Filtered entry count: {len(df_cleaned)}")

df_cleaned.to_csv(output_file, index=False)
print(f"Saved cleaned CSV to '{output_file}'.")

# Generate figures without immediate show
plot_all_stacked_bars(df_cleaned)
plot_horizontal_language_stacked_bars(df_cleaned)

# Display all figures at once
plt.show()
