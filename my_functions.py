LIST_ACCEPTED_LANGUAGES = ["english", "chinese", "mandarin", "japanese", "korean", "spanish", "vietnamese", "greek"]


def convert_language_to_lower(data):
    """
    Converts the "Language" key for a list of dictionaries to lower.
    Need to make lower case to help filter repeated and unaccepted data entries. Will help us later on.
    :param data: List of dictionaries containing "Language" key.
    :return: The same list that is accepted as the parameter, this time the "Language" key is converted to lower.
    """
    for item in data:
        item["Language"] = item["Language"].lower()
    return data


def find_language_frequency(data):
    """
    Counts the frequency of each language in the provided list of dictionaries.
    This information can be used to extrapolate the location of origin for trash items.
    The function is case insensitive.

    :param data: A list of dictionaries, each containing a "Language" key.
    :return: A list of dictionaries, each containing "Language" and its "Frequency".
    """

    language_count = []

    # Iterate through the list of dictionaries
    for item in data:
        for entry in language_count:
            if entry["Language"] == item["Language"]:
                entry["Frequency"] += 1  # Increment frequency
                break
        else:
            # This else block executes only if the loop iterates over all items
            # in language_count without encountering a break. If the loop is
            # exited with a break statement, this else block will not run.
            language_count.append({"Language": item["Language"], "Frequency": 1})  # Directly use item['Language']

    return language_count


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
