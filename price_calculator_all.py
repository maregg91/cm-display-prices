 
import csv
import random
import numpy as np
from tqdm import tqdm
import os
import math
import numpy as np
from datetime import date
from matplotlib import pyplot as plt


def _calc_value_for_double_masters_booster(val_common, val_uncommon, val_rare, val_mythic, 
                                           val_common_foil, val_uncommon_foil, val_rare_foil, val_mythic_foil):
    """
    Method to calculate the overall value of a Double Masters booster for the given card prices. 
    The value can be any arbitrary value for the groups (in this program we use price, std. deviation and variance).
    """

    # Define the number of card occurences in the booster
    no_commons = 8  # Common slots
    no_uncommons = 3  # Uncommon slots
    no_rare_mythic = 2  # Rare/Mythic slots
    no_any = 2  # Foil slots

    # The final value will be constructed by adding all slots togeter
    # 1. add the value for the Common slot
    final_val = no_commons * val_common
    # 2. add the value for the Uncommon slot
    final_val += no_uncommons * val_uncommon
    # 3. add the value for the Rare/Mythic slot with given possibilites for each type.
    final_val += no_rare_mythic * (0.875 * val_rare + 0.125 * val_mythic)

    # Define the foil possibilities (Found on some forum posts)
    possibility_mythic = 0.077
    possibility_rare = 0.154
    possibility_uncommon = 0.308
    possibility_common = 1 - possibility_uncommon - possibility_rare - possibility_mythic

    # 4. add the value for the foil slots with the defined possibilities.
    final_val += no_any * (
        possibility_common * val_common_foil +
        possibility_uncommon * val_uncommon_foil +
        possibility_rare * val_rare_foil +
        possibility_mythic * val_mythic_foil
    )

    return final_val

def calc_average_booster_price(common_cards, uncommon_cards, rare_cards, mythic_cards):
    """
    Method for calculating the price, std. deviation and variance of a single booster of the set.
    """

    # Extract normal prices
    common_prices = [card[1] for card in common_cards]
    uncommon_prices = [card[1] for card in uncommon_cards]
    rare_prices = [card[1] for card in rare_cards]
    mythic_prices = [card[1] for card in mythic_cards]

    # Extract foil prices
    common_prices_foil = [card[2] for card in common_cards]
    uncommon_prices_foil = [card[2] for card in uncommon_cards]
    rare_prices_foil = [card[2] for card in rare_cards]
    mythic_prices_foil = [card[2] for card in mythic_cards]
    
    # Calculate all averages
    average_common = np.mean(common_prices)
    average_uncommon = np.mean(uncommon_prices)
    average_rare = np.mean(rare_prices)
    average_mythic = np.mean(mythic_prices) 
    average_common_foil = np.mean(common_prices_foil)
    average_uncommon_foil = np.mean(uncommon_prices_foil)
    average_rare_foil = np.mean(rare_prices_foil)
    average_mythic_foil = np.mean(mythic_prices_foil) 

    # Calculate all std. deviations
    std_common = np.std(common_prices)
    std_uncommon = np.std(uncommon_prices)
    std_rare = np.std(rare_prices)
    std_mythic = np.std(mythic_prices) 
    std_common_foil = np.std(common_prices_foil)
    std_uncommon_foil = np.std(uncommon_prices_foil)
    std_rare_foil = np.std(rare_prices_foil)
    std_mythic_foil = np.std(mythic_prices_foil) 

    # Calculate all variances
    var_common = np.var(common_prices)
    var_uncommon = np.var(uncommon_prices)
    var_rare = np.var(rare_prices)
    var_mythic = np.var(mythic_prices) 
    var_common_foil = np.var(common_prices_foil)
    var_uncommon_foil = np.var(uncommon_prices_foil)
    var_rare_foil = np.var(rare_prices_foil)
    var_mythic_foil = np.var(mythic_prices_foil) 

    # Calculate the value for a booster for the average, std. deviation and variance
    average = _calc_value_for_booster(average_common, average_uncommon, average_rare, average_mythic, average_common_foil, average_uncommon_foil, average_rare_foil, average_mythic_foil)
    std = _calc_value_for_booster(std_common, std_uncommon, std_rare, std_mythic, std_common_foil, std_uncommon_foil, std_rare_foil, std_mythic_foil)
    var = _calc_value_for_booster(var_common, var_uncommon, var_rare, var_mythic, var_common_foil, var_uncommon_foil, var_rare_foil, var_mythic_foil)
        
    return average, std, var




def get_price_chart():
    """
    Method that loads the card prices stored in the CSV files located under prices/, and calculates the different values per day.
    """

    dates = []
    dates_count = []
    date_numbers = []
    labels = []

    average_prices = []
    std_deviations = []

    last_date = None

    # List all files in the prices directory
    files = ["./prices/" + f for f in sorted(os.listdir("./prices/"))]

    # Iterate over the files and process all files that end with "_dm2022_prices.csv" which is the appendix for the Double Masters 2022 prices.
    for f in files:
        if "_dm2022_prices.csv" in f:
            common = []
            uncommon = []
            rare = []
            mythic = []
            # Open the file and store the cards in the lists depending on their rarity
            with open(f) as csvfile:
                card_prices = csv.reader(csvfile, delimiter=';')
                for row in card_prices:
                    name, price, rarity, price_foil = row
                    price = float(price)
                    name = name.strip()
                    rarity = rarity.strip()
                    price_foil = float(price_foil)

                    if rarity == 'common':
                        common.append((name, price, price_foil, rarity))
                    if rarity == 'uncommon':
                        uncommon.append((name, price, price_foil, rarity))
                    if rarity == 'rare':
                        rare.append((name, price, price_foil, rarity))
                    if rarity == 'mythic':
                        mythic.append((name, price, price_foil, rarity))

            # Calculate the values for a single booster given the read cards.
            average_per_booster, std_per_booster, var_per_booster = calc_average_booster_price(common, uncommon, rare, mythic)

            # Calculate the overall value for a display (each display contains 24 booster for Double Masters 2022)
            average = average_per_booster * 24
            std_dev = np.sqrt(var_per_booster * 24)

            # Receive the date of the processed file
            date_object = date.fromisoformat(f.split("_")[0].split("/")[2].split("T")[0])

            last_date = date_object
            # If the date is not listed in the dates added to the overall result, add it and the prices calculated
            if date_object not in dates:
                dates.append(date_object)
                dates_count.append(1)

                average_prices.append(average)
                std_deviations.append(std_dev)
            else:
                # If its already there, check for NaN values and calculate a interative mean for each value
                if not (math.isnan(average) or math.isnan(std_dev)):
                    
                    index_of_date = dates.index(date_object)
                    dates_count[index_of_date] = count = dates_count[index_of_date] + 1
                    average_prices[index_of_date] = average_prices[index_of_date] + (average - average_prices[index_of_date]) / count
                    std_deviations[index_of_date] = std_deviations[index_of_date] + (std_dev - std_deviations[index_of_date]) / count

    # Create the plot data
    x = np.asarray(dates)
    y = np.asarray(average_prices)
    e = np.asarray(std_deviations)

    # Plot the data
    fig, ax = plt.subplots()
    ax.errorbar(x, y, yerr=e, fmt='-o', capthick=2, capsize=10)

    # Update the plot so each date will be printed on the x-axis.
    ax.set_xticks(x)

    # Set the grid
    ax.grid(axis='y', which='minor', alpha=0.2)
    ax.grid(axis='y', which='major', alpha=0.5)
    ax.set_yticks(np.arange(200, 700, 50))
    ax.set_yticks(np.arange(200, 700, 10), minor=True)

    # Make some space to locate the dates
    fig.subplots_adjust(bottom=0.2)
    # Rotate the dates
    plt.xticks(rotation=90)

    # Increase figure resolution
    fig.set_size_inches(20, 20)
    fig.set_dpi(600)

    # Return the figure and a iterable containing a triplet with the prices per date
    return fig, zip(dates, average_prices, std_deviations)
    