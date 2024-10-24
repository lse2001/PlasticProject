LIST_ACCEPTED_LANGUAGES = ["english", "chinese", "mandarin", "japanese", "korean", "spanish", "vietnamese", "greek"]


def convert_to_lower(data, key):
    """
    Converts the provided key for a list of dictionaries to lower.
    Need to make lower case to help filter repeated and unaccepted data entries. Will help us later on.
    :param data: List of dictionaries containing the key param to lower.
    :param key: The key name as a string for which you are converting its values in the data list of dictionaries to lower.
    :return: The same list that is accepted as the parameter, this time the specified key is converted to lower.
    """
    for item in data:
        item[key] = item[key].lower()
    return data


def find_frequency(data, key):
    """
    Counts the frequency of each value for the specified key that is passed as a parameter in the provided list of dictionaries.
    This information can be used to extrapolate the location of origin for trash items.

    :param data: A list of dictionaries, each containing the specified key.
    :param key: The key as a string for which you are finding the frequencies of its values.
    :return: A list of dictionaries, each containing the key and its "Frequency".
    """

    key_count = []

    # Iterate through the list of dictionaries
    for item in data:
        # Iterate through the list and check if the key exists
        for entry in key_count:
            if entry[key] == item[key]:
                entry["Frequency"] += 1  # Increment frequency
                break
        else:
            # The else block of the for-loop runs only if no break was encountered
            key_count.append({key: item[key], "Frequency": 1})  # Simply use "Frequency"

    return key_count


def remove_non_accepted_languages(data):
    """
    Filters the list of dictionaries to include only those items where the "Language" contains any of the accepted languages.
    :param data: A list of dictionaries, each containing a "Language" key.
    :return: A filtered list of dictionaries containing only the items with accepted languages.
    """

    filtered_data = []

    for item in data:
        for language in LIST_ACCEPTED_LANGUAGES:
            if language in item["Language"]:
                filtered_data.append(item)

    return filtered_data


def remove_substrings_from_languages(data):
    """
    Removes specified substrings from the 'Language' key in each dictionary
    within the provided list of dictionaries.

    :param data: A list of dictionaries, each containing a 'Language' key.
    :return: The modified list of dictionaries with cleaned 'Language' values.
    """
    # List of substrings to remove
    substrings_to_remove = ["arabic numbers", "latin letters", "?", "/", " ", "(", ")"]

    # Iterate through the list of dictionaries
    for item in data:
        for substring in substrings_to_remove:
            # Check if the substring is in the 'Language' string before replacing
            if substring in item["Language"]:
                item["Language"] = item["Language"].replace(substring, "")

    return data


def remove_english_substring(data):
    """
    Removes the substring 'english' from the 'Language' key in each dictionary
    within the provided list of dictionaries if certain conditions are met.

    :param data: A list of dictionaries, each containing a 'Language' key.
    :return: The modified list of dictionaries with 'english' removed from 'Language' values when applicable.
    """
    for item in data:
        if "english" in item["Language"] and len(item["Language"]) > len("english"):
            item["Language"] = item["Language"].replace("english",
                                                        "").strip()  # Remove 'english' and strip extra spaces

    return data


def map_language_to_country(data):
    """
    Maps specified languages to their respective countries of origin.

    :param data: A list of dictionaries, each containing 'Language' and 'Frequency' keys.
    :return: A list of dictionaries with 'country_of_origin' and 'frequency' keys.
    """
    # Define the mapping of specified languages to countries
    language_to_country = {
        "english": "USA",
        "chinese": "China",
        "japanese": "Japan",
        "vietnamese": "Vietnam",
        "greek": "Greece",
        "korean": "South Korea",
        "spanish": "LATAM",  # Changed 'spanish' to 'LATAM'
    }

    # Initialize the result list
    result = []

    # Iterate through the list of dictionaries
    for item in data:
        # Append the new dictionary to the result list without a separate variable
        result.append({
            "country_of_origin": language_to_country.get(item["Language"], "Unknown"),
            # Default to 'Unknown' if not found
            "frequency": item["Frequency"]
        })

    return result
