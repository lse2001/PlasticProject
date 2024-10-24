import csv
from my_functions import *
import numpy as np
import matplotlib.pyplot as plt

# ----------------------- MAIN ----------------------- #
data = []
with open('HPU Filtered Data.csv', newline='') as file:
    reader = csv.DictReader(file)
    # treats each row of data as a dictionary
    for row in reader:
        data.append(row)

data = convert_to_lower(data, "Language")
data = remove_non_accepted_languages(data)
data = remove_substrings_from_languages(data)
data = remove_english_substring(data)



for item in data:
    # Check if the Language is 'mandarin' and change it to 'chinese'
    if item["Language"] == "mandarin":
        item["Language"] = "chinese"

print(len(data))
language_frequency = find_frequency(data, "Language")
print(language_frequency)



country = map_language_to_country(language_frequency)
print(country)

# Using list comprehensions to extract country names and frequencies
countries = [c['country_of_origin'] for c in country]  # Country names
frequencies = [c['frequency'] for c in country]        # Frequencies

"""
[c['country_of_origin'] for c in country]: This list comprehension iterates over each dictionary c in the country list and extracts the value of 'country_of_origin' to form a new list of country names.
[c['frequency'] for c in country]: Similarly, this list comprehension extracts the 'frequency' value from each dictionary in country to form a list of frequencies.
"""

# Calculate total frequency
total_frequency = sum(frequencies)

# Calculate relative frequencies as percentages
relative_frequencies = [(freq / total_frequency) * 100 for freq in frequencies]

# Create a list of tuples and sort it in descending order to have more polluting countries at the bottom
sorted_data = sorted(zip(countries, relative_frequencies), key=lambda x: x[1], reverse=True)
countries, relative_frequencies = zip(*sorted_data)

# Create a stacked bar chart with a smaller figure size
plt.figure(figsize=(6, 6))  # Adjusted height to make it smaller

# Create an array to hold the bottom position for each bar
bottoms = np.zeros(1)  # Only one bar, so we use 1

# Plot each country's percentage as a segment of the stacked bar
for i, (country, freq) in enumerate(zip(countries, relative_frequencies)):
    plt.bar(0, freq, bottom=bottoms, color=plt.cm.tab10(i), label=f"{country} ({freq:.1f}%)")
    bottoms += freq

# Setting the y-axis limit to a smaller range
plt.ylim(0, 100)  # You can adjust this if needed

# Adding labels and title
plt.ylabel('Relative Frequency (%)')
plt.title('Pacific Ocean Garbage and its Countries of Origin')
plt.xticks([])  # Remove x-axis ticks as we only have one bar

# Add a tilted x-axis label
plt.xlabel('Countries', rotation=45)

# Customize the legend, reversing the order
plt.legend(reversed(plt.gca().get_legend_handles_labels()[0]),
           reversed(plt.gca().get_legend_handles_labels()[1]),
           title="Countries", bbox_to_anchor=(1.05, 1), loc='upper left')

# Show the plot
plt.tight_layout()
plt.show()
