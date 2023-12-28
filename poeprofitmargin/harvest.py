# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 19:41:49 2023

@author: wicki
"""

from tradequery import make_bulk_query
import requests
from time import sleep

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
    
def get_bulk_lifeforce(league):
    """
    Gather lifeforce count per divine from poe bulk trade site
    """
    head = {"Content-Type": "application/json", "User-Agent": "NAME_YOU_CHOOSE"}
    url = f'https://www.pathofexile.com/api/trade/exchange/{league}'
    
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
        print(r['result'].keys()[:20])
        Lifeforce.bulk_cost[key] = 1000
        sleep(2)

def reroll_scarabs():
    scarab_EV = 0
    
    return scarab_EV
    
if __name__=="__main__":
    league = 'Affliction'
    get_bulk_lifeforce(league)
    print(Lifeforce.bulk_cost)