from bs4 import BeautifulSoup
import scrython
import urllib
import sys
import requests
import re
import os
import datetime
from pathlib import Path

def receive_update():
    """
    Method that requests the cardmarket page and extract all cards from the html content returned.
    """

    # Define the time strin for the data file
    current_time_string: str = datetime.datetime.now().strftime('%Y-%m-%dT%H%M')

    # If a file already exists for the current minute, abort the update as we would run into an timeout otherwise.
    if os.path.exists(f'./prices/{current_time_string}_dm2022_prices.csv'):
        return
    # Ensure that the file exists directly after checking if its not there. This ensures the avoidance of the timeouts.
    Path(f'./prices/{current_time_string}_dm2022_prices.csv').touch()

    # Create the urls for each card rarity
    urls_common = [f"https://www.cardmarket.com/en/Magic/Products/Singles/Double-Masters-2022?idCategory=1&idExpansion=5070&idRarity=22&site={i+1}" for i in range(5)]#[:1]
    urls_uncommon = [f"https://www.cardmarket.com/en/Magic/Products/Singles/Double-Masters-2022?idCategory=1&idExpansion=5070&&idRarity=21&site={i+1}" for i in range(4)]#[:1]
    urls_rare = [f"https://www.cardmarket.com/en/Magic/Products/Singles/Double-Masters-2022?idCategory=1&idExpansion=5070&idRarity=18&site={i+1}" for i in range(6)]#[:1]
    urls_mythic = [f"https://www.cardmarket.com/en/Magic/Products/Singles/Double-Masters-2022?idCategory=1&idExpansion=5070&idRarity=17&site={i+1}" for i in range(2)]#[:1]

    # Combine the lists into a single one
    urls = []
    urls.extend(urls_common)
    urls.extend(urls_uncommon)
    urls.extend(urls_rare)
    urls.extend(urls_mythic)

    # For each url, request it and save its content into the list
    html_pages = []
    for url in urls:
        html_text = requests.get(url).text
        html_pages.append(html_text)

    # Create the result list
    name_price_list = []

    # Iterate over all pages
    for page in html_pages:
        # Parse the current page with BeautifulSoup
        soup = BeautifulSoup(page, features="html.parser")
        # Extract all productRow divs from the page. They contain the card contents.
        cards = soup.find_all("div", {"class": "row no-gutters", "id": re.compile('^productRow.*')})
        
        # Iterate over all found cards
        for card in cards:
            try:
                # Extract all content from the div

                # Extract the normal price
                price = card.find_all("div", {"class": "col-price pr-sm-2"})
                price = price[0].contents[0]
                price = float(price[:-2].replace(",", "."))
                
                # Extract the foil price
                price_foil = card.find_all("div", {"class": "col-price d-none d-lg-flex pr-lg-2"})
                price_foil = price_foil[0].contents[0]
                price_foil = float(price_foil[:-2].replace(",", "."))

                # Extract the card name
                name = card.find_all("div", {"class": "col-10 col-md-8 px-2 flex-column align-items-start justify-content-center"})
                name = name[0].contents[0].contents[0]

                # Extract the card rarity
                rarity = card.find_all("span", {"class": "icon"})
                rarity = rarity[0]['data-original-title']
                rarity = rarity.lower()

                # Append the card to the result
                name_price_list.append((name, price, rarity, price_foil))

            except:
                # Card parsing failed. Ignore the card.
                continue

    # Remove duplicate entries (this may occur during spoiler season when the URLs content canges during request).
    name_price_list = list(set(name_price_list))
        
    # Write the results to a CSV file..
    with open(f'./prices/{current_time_string}_dm2022_prices.csv', 'a') as f:
        for name, price, rarity, price_foil in name_price_list:
            try:
                f.write(f"{name}; {price}; {rarity}; {price_foil}\n")
            except Exception as e:
                pass
