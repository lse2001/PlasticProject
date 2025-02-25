import csv
from my_functions import *
import numpy as np
import matplotlib.pyplot as plt



def plot_garbage(countries, frequencies, ax):
    total_frequency = sum(frequencies)
    relative_frequencies = [(freq / total_frequency) * 100 for freq in frequencies]
    sorted_data = sorted(zip(countries, relative_frequencies), key=lambda x: x[1], reverse=True)
    countries, relative_frequencies = zip(*sorted_data)

    bottoms = np.zeros(1)
    for i, (country, freq) in enumerate(zip(countries, relative_frequencies)):
        ax.bar(0, freq, bottom=bottoms, color=plt.cm.tab10(i), label=f"{country} ({freq:.1f}%)")
        bottoms += freq

    ax.set_ylim(0, 100)
    ax.set_ylabel('Relative Frequency (%)')
    ax.set_title('Pacific Ocean Garbage by Country')
    ax.set_xticks([])
    ax.set_xlabel('Countries', rotation=45)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(reversed(handles), reversed(labels), title="Countries", bbox_to_anchor=(1.05, 1), loc='upper left')


def plot_color(colors, frequencies2, ax):
    total_frequency = sum(frequencies2)
    relative_frequencies = [(freq / total_frequency) * 100 for freq in frequencies2]
    sorted_data = sorted(zip(colors, relative_frequencies), key=lambda x: x[1], reverse=True)
    colors, relative_frequencies = zip(*sorted_data)

    color_mapping = {
        "multi": "limegreen", "black": "black", "orange": "orange", "blue": "blue",
        "white": "white", "green": "green", "red": "red", "yellow": "yellow",
        "grey": "grey", "clear": "#d3d3d3", "silver": "silver", "rust": "#b7410e", "pink": "pink"
    }
    bottoms = 0.0
    for i, (color_name, freq) in enumerate(zip(colors, relative_frequencies)):
        color = color_mapping.get(color_name, "gray")
        ax.bar(0, freq, bottom=bottoms, color=color, label=f"{color_name} ({freq:.1f}%)")
        bottoms += freq

    ax.set_ylim(0, 100)
    ax.set_ylabel('Relative Frequency (%)')
    ax.set_title('Garbage Composition by Color')
    ax.set_xticks([])
    ax.set_xlabel('Colors', rotation=45)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(reversed(handles), reversed(labels), title="Colors", bbox_to_anchor=(1.05, 1), loc='upper left')


def plot_gear(gear_types, frequencies3, ax):
    total_frequency = sum(frequencies3)
    relative_frequencies = [(freq / total_frequency) * 100 for freq in frequencies3]
    sorted_data = sorted(zip(gear_types, relative_frequencies), key=lambda x: x[1], reverse=True)
    gear_types, relative_frequencies = zip(*sorted_data)

    bottoms = np.zeros(1)
    for i, (gear, freq) in enumerate(zip(gear_types, relative_frequencies)):
        ax.bar(0, freq, bottom=bottoms, color=plt.cm.tab10(i), label=f"{gear} ({freq:.1f}%)")
        bottoms += freq

    ax.set_ylim(0, 100)
    ax.set_ylabel('Relative Frequency (%)')
    ax.set_title('Garbage Composition by Gear Type')
    ax.set_xticks([])
    ax.set_xlabel('Gear Types', rotation=45)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(reversed(handles), reversed(labels), title="Gear Types", bbox_to_anchor=(1.05, 1), loc='upper left')


def plot_all(countries, frequencies, gear_types, frequencies3, colors, frequencies2):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Calculate the total number of items for each category
    total_countries = sum(frequencies)
    total_gear = sum(frequencies3)
    total_colors = sum(frequencies2)

    # Plot countries data with total count in the x-axis label
    plot_garbage(countries, frequencies, axes[0])
    axes[0].set_xlabel(f'Countries ({total_countries} items)', rotation=45)

    # Plot gear data with total count in the x-axis label
    plot_gear(gear_types, frequencies3, axes[1])
    axes[1].set_xlabel(f'Gear Types ({total_gear} items)', rotation=45)

    # Plot color data with total count in the x-axis label
    plot_color(colors, frequencies2, axes[2])
    axes[2].set_xlabel(f'Colors ({total_colors} items)', rotation=45)

    plt.tight_layout()
    plt.show()


# ----------------------- MAIN ----------------------- #
data = []
with open('HPU Subset Data.csv', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)

data = convert_to_lower(data, "Language")
data = remove_non_accepted_languages(data)
data = remove_substrings_from_languages(data)
data = remove_english_substring(data)

for item in data:
    if item["Language"] == "mandarin":
        item["Language"] = "chinese"

language_frequency = find_frequency(data, "Language")
country = map_language_to_country(language_frequency)

# Extract country names and frequencies
countries = [c['country_of_origin'] for c in country]
frequencies = [c['frequency'] for c in country]

"""
[c['country_of_origin'] for c in country]: This list comprehension iterates over each dictionary c in the country list and extracts the value of 'country_of_origin' to form a new list of country names.
[c['frequency'] for c in country]: Similarly, this list comprehension extracts the 'frequency' value from each dictionary in country to form a list of frequencies.
"""


# Process for color data
data = convert_to_lower(data, "Color")
data = [d for d in data if d.get("Color") != ""]
colors = find_frequency(data, "Color")

color = [c['Color'] for c in colors]
frequencies2 = [c['Frequency'] for c in colors]


# Process for gear type data
data = convert_to_lower(data, "Gear Type")
allowed_gear_types = {"buoy", "float", "hard plastic", "metal", "line"}
data = [d for d in data if d.get("Gear Type") in allowed_gear_types]
gear_types = find_frequency(data, "Gear Type")
gear = [g['Gear Type'] for g in gear_types]
frequencies3 = [g['Frequency'] for g in gear_types]



print(sum(frequencies))
print(sum(frequencies3))
print(sum(frequencies2))

plot_all(countries, frequencies, gear, frequencies3, color, frequencies2)

# main.py cleans up subset data for relevant data. Plots bar chart for us to better understand distribution of trash instances.
# The generated, cleaned up, csv is used to in simulation.py

print(data)


