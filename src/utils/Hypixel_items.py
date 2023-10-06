import requests
import json

# This path is modifying the Run configs
FILE_PATH = 'files/mappings.json'

def request_info(url: str):
    r = requests.get(url)
    return r.json()

def get_items_data() -> dict:
    items_data = request_info(f"https://api.hypixel.net/resources/skyblock/items")
    items = items_data.get("items")
    return items

def format_items_to_list_of_dicts(items_data : list) -> list:
    items_mapping_list = []
    items_set = set()
    for items in items_data:
        item_name = items.get('name')
        if item_name in items_set:
            continue
        items_map = {}
        items_map['name'] = item_name
        items_map['value'] = item_name
        items_mapping_list.append(items_map)
        items_set.add(item_name)
    return items_mapping_list

def write_mappings_to_json(items_mapping_list: list):
    mappings_file = open(FILE_PATH, 'w')
    json.dump(items_mapping_list, mappings_file, indent=4)

# Use this function to get the dictionary
def read_mappings_from_json() -> list:
    mappings_file = open(FILE_PATH, 'r')
    mappings = json.load(mappings_file)
    return mappings

# Main Function to update items name
def refresh_mappings():
    # Retrieve all items from
    items_data = get_items_data()

    # Map out each item name to list of dicts for auto-suggest
    items_mapping_list = format_items_to_list_of_dicts(items_data)

    # Write mapping to json file
    write_mappings_to_json(items_mapping_list)

refresh_mappings()
