# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 19:41:49 2023

@author: wicki
"""

from tradequery import make_bulk_query
import requests
from time import sleep
from cachetools.func import ttl_cache

class Lifeforce():
    bulk_cost = {'Primal':0,
                'Wild':0,
                'Vivid':0}

class Scarabs():
    Type='Wild'
    MAX_STACK = 10
    COST = 30
    TIERS = ['Rusted','Polished','Gilded','Winged']
    SCARABS = ['Reliquary',
               'Divination',
               'Abyss',
               'Ambush',
               'Harbinger',
               'Blight',
               'Breach',
               'Cartography',
               'Legion',
               'Expedition',
               'Ultimatum',
               'Bestiary',
               'Elder',
               'Sulphite',
               'Torment',
               'Shaper']
    
class Essence():
    Type = 'Primal'
    MAX_STACK = 9
    COST = 30
    ESSENCE = ['Scorn',
               'Contempt',
               'Loathing',
               'Hatred',
               'Wrath',
               'Anger',
               'Spite',
               'Rage',
               'Envy',
               'Zeal',
               'Torment',
               'Sorrow',
               'Woe',
               'Fear',
               'Anguish',
               'Doubt',
               'Greed',
               'Misery',
               'Suffering',
               'Dread']
    SPECIAL_ESSENCE = ['']
    
class Delirium():
    TYPE = 'Primal'
    MAX_STACK = 10
    COST = 30
    NAMES = ["Skittering",
             "Diviner's",
             "Fine",
             "Abyssal",
             "Armoursmith's",
             "Blighted",
             "Cartographer's",
             "Foreboding",
             "Singular",
             "Blacksmith's",
             "Fossiled",
             "Jeweler's",
             "THaumaturge's",
             "Timeless",
             "Whispering",
             "Obscured"]

@ttl_cache(1,360)
def get_bulk_lifeforce(league):
    """
    Gather lifeforce count per divine from poe bulk trade site
    """
    head = {"Content-Type": "application/json", "User-Agent": "NAME_YOU_CHOOSE"}
    url = f'https://www.pathofexile.com/api/trade/exchange/{league}'
    listings = 20
    
    data = []
    for key in Lifeforce.bulk_cost.keys():
        #Get Bulk Cost
        low = key.lower()
        query = make_bulk_query(['divine'], [f'{low}-lifeforce'], 0)
        print(query)
        r = requests.post(url,json=query,headers=head).json()
        print(r)
        #Check for ratelimit
        if 'error' in r:
            print(r['error']['message'])
            break
        entry = r['result']
        total = 0    
        for key in list(entry.keys())[:listings]:
            cost = entry[key]['listing']['offers'][0]['exchange']['amount']
            print(cost)
            amount = entry[key]['listing']['offers'][0]['item']['amount']
            print(amount)
            total += amount/cost
        avg = total/listings
        data.append(r)
        #print(r['result'].keys()[:20])
        Lifeforce.bulk_cost[key] = avg
        sleep(2)
    
    return data

def reroll_scarabs():
    scarab_EV = 0
    
    return scarab_EV
    
if __name__=="__main__":
    league = 'Affliction'
    data = get_bulk_lifeforce(league)
#%%
    entry = data[0]['result']
#%%
    total = 0    
    for key in list(entry.keys())[:20]:
        cost = entry[key]['listing']['offers'][0]['exchange']['amount']
        print(cost)
        amount = entry[key]['listing']['offers'][0]['item']['amount']
        print(amount)
        total += amount/cost
    print(total/20)
#%%
    print(Lifeforce.bulk_cost)