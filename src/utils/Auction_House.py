import requests
import time
from table2ascii import table2ascii as t2a, PresetStyle

auction_url = 'https://api.hypixel.net/skyblock/auctions'

# Returns GET request response from url
def request_info(url: str):
    r = requests.get(url)
    return r.json()

# Returns a list of all active auctions
def get_auction_data(page):

    page = request_info(f"{auction_url}?page={page}")

    auction_data = page.get("auctions")

    return auction_data

# Gets all items matching given item_name
def retrieve_item_auction_data(item_name: str):
    total_pages = request_info(auction_url).get('totalPages')
    print(f'Total Pages: {total_pages}')
    start = time.time()
    hits = []
    for page in range(0,total_pages):
        data = get_auction_data(page)
        for d in data:
            if d.get('item_name') == item_name or item_name in d.get('item_name'):
                hits.append(d)

        time.sleep(.7)

    end = time.time()
    print(f'Retrieval and Processing Time Elapsed: {end-start}')
    return hits

# Format the data into list of lists and sort by Price
def format_and_sort(hits: list, limit: int = 10):
    # Pull only desired field values
    refined_data_list = [get_filtered_data_as_list(hit) for hit in hits ]

    sorted_refined_data_list = sorted(refined_data_list, key=lambda x: x[3])  # Sort by Price, 2nd item in list

    print(f'Number of hits: {len(sorted_refined_data_list)}')

    # Insert row number for table
    for i in range(len(sorted_refined_data_list)):
        sorted_refined_data_list[i].insert(0,i+1)

    return sorted_refined_data_list[:limit]

# Grabs only relevant data we want from the api
def get_filtered_data_as_list(hit: dict):
    item_name = hit.get('item_name')
    auction_uuid = hit.get('uuid')
    seller = request_info(f'https://sessionserver.mojang.com/session/minecraft/profile/{hit.get("auctioneer")}')['name']
    starting_bid = hit.get('starting_bid')
    bin = hit.get('bin')
    return [item_name, auction_uuid, seller, starting_bid, bin]

# Currently not used
def get_filtered_data_as_map(hit: dict):
    entry = {}
    entry['Auction ID'] = hit.get('uuid')
    entry['Seller ID'] = hit.get('auctioneer')
    entry['Price'] = hit.get('starting_bid')
    entry['BIN'] = hit.get('bin')
    return entry

# Format data into table output
def format_to_table(sorted_data: list):
    output = t2a(
        header=["#", "Item", "Auction ID", "Seller ID", "Price", "BIN"],
        body=sorted_data,
        style=PresetStyle.thin_compact
    )

    print(output)
    return f"```\n{output}\n```"

# Where it all begins
def handle_auction_data_retrieval(item_name: str, limit: int):
    # item_name = 'Greater Backpack'
    hits = retrieve_item_auction_data(item_name)
    filtered_and_sorted_data = format_and_sort(hits, limit)
    return format_to_table(filtered_and_sorted_data)
