# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 19:41:49 2023

@author: wicki
"""
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
def get_bulk_lifeforce():
    """
    Gather lifeforce count per divine from poe bulk trade site
    """
    for key in Lifeforce.bulk_cost.keys():
        #Get Bulk Cost
        Lifeforce.bulk_cost[key] = 1000

def reroll_scarabs():
    scarab_EV = 0
    
    return scarab_EV
    
if __name__=="__main__":
    get_bulk_lifeforce()
    print(Lifeforce.bulk_cost)