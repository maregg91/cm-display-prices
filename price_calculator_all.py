 
import csv
import random
import numpy as np
from tqdm import tqdm
import os
import math
import numpy as np
from datetime import date
from matplotlib import pyplot as plt


def calculate_double_master_rare_possibilities(no_mythics, no_rares, no_uncommons, no_commons):
    """
    In a normal set, there are 53 rares and 15 mythics. These are printed on a single sheet, with each rare showing up twice and each mythic showing up once, which creates exactly a sheet of 121 cards (53+53+15). This sheet is then cut and distributed among packs, which creates a distribution wherein each booster pack has a 15/121, or 1:8.066~ chance of containing a mythic, which means 4.46 mythics in a normal 36-pack box or 2.98 mythics in a Masters-type 24-pack box.

    For Double Masters, there are a few changes to this formula. For starters, there are 121 rares, meaning there is a single sheet containing just rares. Then there are 40 mythics, which means that there's a sheet that almost certainly contains 3x of each mythic plus one "DISCARD" filler card. This means that, in order to maintain something close to the normal distribution, wherein each rare shows up twice for each mythic, there are 6 rare sheets printed for every mythic sheet. This means that the chances of opening a mythic in a rare slot are 120/846, or 1:7.05. The other major change is that there are two rare slots per booster. That means that in a box of 24 packs, there are 48 rare slots, which means the expected number of mythics is 6.809. The final wrinkle is that there are two box-toppers per box. There's a pool of 40, with half being mythic and half being "rare" (with 8 of those rares actually being commons or uncommons like the Tron Lands, Expedition Map, and Crop Rotation, but with a rare symbol). The rares show up twice as often as the mythics, meaning there's a 20/60, or 1:3 chance of opening a mythic in these slots. With two slots available, this adds an additional .666~ of a mythic expected per box, for a total expected mythics per box of 7.475. This means you should expect each box to have 7-8 mythics on average, and since this is only a quasi-random distribution, I wouldn't expect that to vary by more than 1-2 mythics in either direction. So 6-10 seems like a reasonable estimate.

    Note that I am not taking into account foil mythics in this equation, because I am not certain the frequency at which those show up. A "normal" box of 36 cards has approximately one foil rare or mythic, and foils show up in 1:3 packs normally. This would imply that 1:12 foils are rare or mythic, meaning you'd expect two rare or mythic foils in a 24-pack, foil-in-every-pack Masters set. This would also mean that for Double Masters, with two foils in every pack, you would expect to see four foil rares or mythics, which would add another 1.33~ mythics per box. However, in my experience and observations of previous Masters sets, there was only one foil rare or mythic per box on average, not two, which would imply that despite the increased drop rate of foils, the number of rare-slot foils is scaled down proportionally. If this is indeed the case, and that carries over to Double Masters at the exact same ratio (which is an assumption that may not bear out), we would expect to see another .666~ of a mythic from the Foil slot.

    So depending on how the foils actually play out, the expected number of mythics per box likely falls somewhere between ~8 (if there's only one foil rare or mythic per box) to ~9 (if there are four foil rares or mythics per box).    
    """

    cards_per_sheet = 121

    mythics_per_sheet = cards_per_sheet // no_mythics
    rare_sheets = 2 * mythics_per_sheet

    distribution = mythics_per_sheet * no_mythics / rare_sheets * no_rares

    pass

def _calc_value_for_booster(val_common, val_uncommon, val_rare, val_mythic, 
                            val_common_foil, val_uncommon_foil, val_rare_foil, val_mythic_foil):
    no_commons = 8
    no_uncommons = 3
    no_rare_mythic = 2
    no_any = 2

    final_val = no_commons * val_common
    final_val += no_uncommons * val_uncommon
    
    final_val += no_rare_mythic * (
        0.875 * val_rare + 
        0.125 * val_mythic)

    possibility_common = 1 - 0.308 - 0.154 - 0.077
    final_val += no_any * (
        possibility_common * val_common_foil +
        0.308 * val_uncommon_foil +
        0.154 * val_rare_foil +
        0.077 * val_mythic_foil
    )
    return final_val

def calc_average_booster_price():

    global common
    global uncommon
    global rare
    global mythic

    common_prices = [card[1] for card in common]
    uncommon_prices = [card[1] for card in uncommon]
    rare_prices = [card[1] for card in rare]
    mythic_prices = [card[1] for card in mythic]
    common_prices_foil = [card[2] for card in common]
    uncommon_prices_foil = [card[2] for card in uncommon]
    rare_prices_foil = [card[2] for card in rare]
    mythic_prices_foil = [card[2] for card in mythic]
    
    average_common = np.mean(common_prices)
    average_uncommon = np.mean(uncommon_prices)
    average_rare = np.mean(rare_prices)
    average_mythic = np.mean(mythic_prices) 
    average_common_foil = np.mean(common_prices_foil)
    average_uncommon_foil = np.mean(uncommon_prices_foil)
    average_rare_foil = np.mean(rare_prices_foil)
    average_mythic_foil = np.mean(mythic_prices_foil) 

    std_common = np.std(common_prices)
    std_uncommon = np.std(uncommon_prices)
    std_rare = np.std(rare_prices)
    std_mythic = np.std(mythic_prices) 
    std_common_foil = np.std(common_prices_foil)
    std_uncommon_foil = np.std(uncommon_prices_foil)
    std_rare_foil = np.std(rare_prices_foil)
    std_mythic_foil = np.std(mythic_prices_foil) 

    var_common = np.var(common_prices)
    var_uncommon = np.var(uncommon_prices)
    var_rare = np.var(rare_prices)
    var_mythic = np.var(mythic_prices) 
    var_common_foil = np.var(common_prices_foil)
    var_uncommon_foil = np.var(uncommon_prices_foil)
    var_rare_foil = np.var(rare_prices_foil)
    var_mythic_foil = np.var(mythic_prices_foil) 

    average = _calc_value_for_booster(average_common, average_uncommon, average_rare, average_mythic, average_common_foil, average_uncommon_foil, average_rare_foil, average_mythic_foil)
    std = _calc_value_for_booster(std_common, std_uncommon, std_rare, std_mythic, std_common_foil, std_uncommon_foil, std_rare_foil, std_mythic_foil)
    var = _calc_value_for_booster(var_common, var_uncommon, var_rare, var_mythic, var_common_foil, var_uncommon_foil, var_rare_foil, var_mythic_foil)
        
    return average, std, var



common = []
uncommon = []
rare = []
mythic = []


def get_price_chart():
    global common
    global uncommon
    global rare
    global mythic

    dates = []
    dates_count = []
    date_numbers = []
    labels = []

    average_prices = []
    std_deviations = []

    last_date = None


    files = ["./prices/" + f for f in sorted(os.listdir("./prices/"))]

    for f in files:
        if "_dm2022_prices.csv" in f:
            common = []
            uncommon = []
            rare = []
            mythic = []
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

            average_per_booster, std_per_booster, var_per_booster = calc_average_booster_price()

            average = average_per_booster * 24
            std_dev = np.sqrt(var_per_booster * 24)

            date_object = date.fromisoformat(f.split("_")[0].split("/")[2].split("T")[0])

            # print(date_object, average, std_dev)

            last_date = date_object
            if date_object not in dates:
                dates.append(date_object)
                dates_count.append(1)

                average_prices.append(average)
                std_deviations.append(std_dev)
            else:
                if not (math.isnan(average) or math.isnan(std_dev)):
                    
                    index_of_date = dates.index(date_object)
                    #print(index_of_date)
                    dates_count[index_of_date] = count = dates_count[index_of_date] + 1
                    #print(count)

                    #print("a", average_prices[index_of_date])
                    #print("b", average)
                    #print("c", average - average_prices[index_of_date])
                    average_prices[index_of_date] = average_prices[index_of_date] + (average - average_prices[index_of_date]) / count
                    #print(std_deviations[index_of_date])
                    #print((std_dev - std_deviations[index_of_date]))
                    std_deviations[index_of_date] = std_deviations[index_of_date] + (std_dev - std_deviations[index_of_date]) / count


    x = np.asarray(dates)
    y = np.asarray(average_prices)
    e = np.asarray(std_deviations)

    fig, ax = plt.subplots()

    ax.errorbar(x, y, yerr=e, fmt='-o', capthick=2, capsize=10)

    ax.set_xticks(x)

    ax.grid(axis='y', which='minor', alpha=0.2)
    ax.grid(axis='y', which='major', alpha=0.5)
    ax.set_yticks(np.arange(200, 700, 50))
    ax.set_yticks(np.arange(200, 700, 10), minor=True)

    fig.subplots_adjust(bottom=0.2)

    plt.xticks(rotation=90)

    return fig, zip(dates, average_prices, std_deviations)
    