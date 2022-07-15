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


    current_time_string: str = datetime.datetime.now().strftime('%Y-%m-%dT%H%M')

    if os.path.exists(f'./prices/{current_time_string}_dm2022_prices.csv'):
        return
    Path(f'./prices/{current_time_string}_dm2022_prices.csv').touch()

    urls_common = [f"https://www.cardmarket.com/en/Magic/Products/Singles/Double-Masters-2022?idCategory=1&idExpansion=5070&idRarity=22&site={i+1}" for i in range(5)]#[:1]
    urls_uncommon = [f"https://www.cardmarket.com/en/Magic/Products/Singles/Double-Masters-2022?idCategory=1&idExpansion=5070&&idRarity=21&site={i+1}" for i in range(4)]#[:1]
    urls_rare = [f"https://www.cardmarket.com/en/Magic/Products/Singles/Double-Masters-2022?idCategory=1&idExpansion=5070&idRarity=18&site={i+1}" for i in range(6)]#[:1]
    urls_mythic = [f"https://www.cardmarket.com/en/Magic/Products/Singles/Double-Masters-2022?idCategory=1&idExpansion=5070&idRarity=17&site={i+1}" for i in range(2)]#[:1]

    urls = []
    urls.extend(urls_common)
    urls.extend(urls_uncommon)
    urls.extend(urls_rare)
    urls.extend(urls_mythic)

    html_pages = []

    # print("Fetching Pages")
    for url in urls:
        html_text = requests.get(url).text
        html_pages.append(html_text)
        # print(".", end='')
    #print()

    name_price_list = []

    for page in html_pages:
        soup = BeautifulSoup(page, features="html.parser")

        cards = soup.find_all("div", {"class": "row no-gutters", "id": re.compile('^productRow.*')})
        
        for card in cards:
            try:
                price = card.find_all("div", {"class": "col-price pr-sm-2"})
                price = price[0].contents[0]
                # print(">>>", price, "<<<")
                price = float(price[:-2].replace(",", "."))
                price_foil = card.find_all("div", {"class": "col-price d-none d-lg-flex pr-lg-2"})
                price_foil = price_foil[0].contents[0]
                # print(">>>", price_foil, "<<<")
                price_foil = float(price_foil[:-2].replace(",", "."))

                name = card.find_all("div", {"class": "col-10 col-md-8 px-2 flex-column align-items-start justify-content-center"})
                name = name[0].contents[0].contents[0]

                rarity = card.find_all("span", {"class": "icon"})
                rarity = rarity[0]['data-original-title']
                rarity = rarity.lower()
                
                # print(name, price, rarity, price_foil)

                name_price_list.append((name, price, rarity, price_foil))

            except:
                # print(card, "failed")
                continue

    name_price_list = list(set(name_price_list))
        

    with open(f'./prices/{current_time_string}_dm2022_prices.csv', 'a') as f:
        for name, price, rarity, price_foil in name_price_list:
            try:
                f.write(f"{name}; {price}; {rarity}; {price_foil}\n")
            except Exception as e:
                print(e)

    print("Fetched")

