import csv
from my_functions import *
import matplotlib.pyplot as plt

# ----------------------- MAIN ----------------------- #
data = []
with open('HPU Filtered Data.csv', newline='') as file:
    reader = csv.DictReader(file)
    # treats each row of data as a dictionary
    for row in reader:
        data.append(row)

data = convert_language_to_lower(data)
print("Number of entries is: " + str(len(data)) + ".")
for item in find_language_frequency(data):
    print(item)


print("\n\n")


data = remove_non_accepted_languages(data)
print("Number of entries is: " + str(len(data)))
for item in find_language_frequency(data):
    print(item)


print("\n\n")


data = remove_substrings_from_languages(data)
print("Number of entries is: " + str(len(data)))
for item in find_language_frequency(data):
    print(item)


print("\n\n")


data = remove_english_substring(data)
print("Number of entries is: " + str(len(data)))
for item in find_language_frequency(data):
    print(item)


print("\n\n")


for item in data:
    # Check if the Language is 'mandarin' and change it to 'chinese'
    if item["Language"] == "mandarin":
        item["Language"] = "chinese"
print("Number of entries is: " + str(len(data)))
for item in find_language_frequency(data):
    print(item)


print("\n\n")


language_frequency = find_language_frequency(data)
country = map_language_to_country(language_frequency)
for item in country:
    print(item)


# Using list comprehensions to extract country names and frequencies
countries = [c['country_of_origin'] for c in country]  # Country names
frequencies = [c['frequency'] for c in country]        # Frequencies

# Plotting
plt.figure(figsize=(6, 6))
plt.bar('Countries', frequencies, color=plt.cm.tab10.colors[:len(countries)], label=countries)

# Adding labels and title
plt.xlabel('Country of Origin')
plt.ylabel('Frequency of Trash Items')  # Updated y-axis label
plt.title('Frequency of Countries of Origin')
plt.xticks([0], ['All Countries'])  # Single label for the x-axis
plt.legend(countries)

# Show the plot
plt.tight_layout()
plt.show()
