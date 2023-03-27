# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 14:47:10 2023

@author: Craig Wickizer
"""
import sys
import pandas as pd
import itertools
from tqdm import tqdm

from gem import GemData
from currency import CurrData
from uniques import UniqueData

def unique_3to1(item,item_data):
    """
    Parameters
    -------------
    item: item that is being checked for 3 to 1
    item_data: cost of items currently on poe.ninja
    -------------
    
    Returns
    -------------
    profit margin for three to one unique recipe for a certain unique targeting a certain roll
    """
    data = item_data.get_price_data()
    data = data[data['name']==item]
    #Make regex for (#s) to #% with or without +
    #TODO
    
    #Make Query to trade with target stats maximized
    #TODO
    
    #Calculate average profit on 3 to 1 trade
    #TODO
    
    return data

def skin_of_the_loyal_3_to_1():
    """
    Parameters
    -------------
    item: item that is being checked for 3 to 1
    item_data: cost of items currently on poe.ninja
    -------------
    
    Returns
    -------------
    profit margin for three to one unique recipe for a certain unique targeting a certain roll
    """
    for i in itertools.combinations_with_replacement("rgb", 6):
        print(i)
    #Make regex for (#s) to #% with or without +
    #TODO
    
    #Make Query to trade with target stats maximized
    #TODO
    
    #Calculate average profit on 3 to 1 trade
    #TODO

def gem_regrade(gem,gem_data):
    """
    return profit margin for regrading a gem to a new quality type
    """
    #Set Starting Variables
    gem_dict = {}
    name = gem['type']

    if gem['support']:
        regrade = gem_data.s_regrade
    else:
        regrade = gem_data.p_regrade

    #Get gem data
    gem_qualities = gem_data.qual_types
    for qual in gem_qualities:
        if gem[qual] > 0:
            data = gem_data.get_gem_data(name,qual)
            try:
                starter,conf = gem_data.get_entry_gem_value(data,name,qual,False,gem['exceptional'])
            except IndexError:
                raise IndexError(f"No Listings for gem {qual} {name}")
            except ValueError as ve:
                raise ve

            gem_dict[qual] = {"cost":starter,"profit":0,"conf":conf}

    #Get Value of base gem
    best = float('-inf')
    for qual1, qual2 in itertools.permutations(gem_dict.keys(), 2):
        cost_str = qual1+"->"+qual2
        q1v = gem_dict[qual1].get("cost")
        q2v = gem_dict[qual2].get("cost")

        profit = q2v-regrade-q1v
        odds = gem[cost_str]
        gem_dict[qual1]["profit"] += (profit * odds)

    #Calculate best profit gem
    for qual in gem_dict.keys():
        prof = gem_dict[qual].get("profit")
        if prof > best:
            best = prof

    return best, gem_dict

def get_top_gem_regrade(gem_data):
    data = []
    i_error = []
    v_error = []
    for i in tqdm(gem_data,total=len(gem_data)):
        gem = i['type']

        try:
            _, starter = gem_regrade(i,gem_data)
            starter = [{"name": name+" "+gem, "cost": v['cost'], "profit": v['profit'], "conf": v['conf']} for name, v in starter.items()]
            starter = pd.DataFrame(starter)
            data.append(starter)
        except IndexError as ex:
            i_error.append(ex)
        except ValueError as vs:
            v_error.append(vs)

    #print(starter)

    all_gems = pd.concat(data).reset_index(drop=True)
    
    return all_gems

def gem_corrupt(gem,gem_data):
    """
    return profit margin for single corrupting and double corrupting gems
    """
    pass

def div_card_turn_in(div_card,div_data,item_data):
    """
    return profit margin for buying a stack of divination cards vs their turn in value
    """
    pass


if __name__ == "__main__":
    try:
        gem_data = GemData()
    except Exception as err:
        print(err)
        sys.exit(1)

    try:
        curr_data = CurrData()
    except Exception as err:
        print(err)
        sys.exit(1)
    
    try:
        unique_data = UniqueData()
    except Exception as err:
        print(err)
        sys.exit(1)
    
    curr_data.get_data("Sanctum")
    gem_data.get_data("Sanctum")
    unique_data.get_data("Sanctum")

    #print(curr_data)
    #print(gem_data)

    gem_data.set_regrading(curr_data)
    #print(gem_data.p_regrade)

    all_gems = get_top_gem_regrade(gem_data)
    
#%%
    print(all_gems.sort_values('profit',ascending=False).tail(10))
    
#%%
    uni = unique_3to1("Stasis Prison", unique_data)
    print(uni.iloc[0]['explicitModifiers'])
    
#%%
    skin_of_the_loyal_3_to_1()