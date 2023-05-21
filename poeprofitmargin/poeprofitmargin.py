# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 14:47:10 2023

@author: Craig Wickizer
"""
import sys
import pandas as pd
import itertools
from tqdm import tqdm
import requests

from gem import GemData
from currency import CurrData
from uniques import UniqueData
import tradequery as tq

head = {"Content-Type": "application/json", "User-Agent": "NAME_YOU_CHOOSE"}

def unique_3to1(league,item,item_data):
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
    misc_filters = {'disabled': 'false', 'filters': {'corrupted': {'option': "false"}}}
    
    #Make query for base item with no maximized rolls from trade site
    query = tq.make_trade_query('online',item,misc_filters=misc_filters)
    try:
        response = tq.query_trade(league, query)
    except requests.exceptions.RequestException as e:
        SystemExit(e)
    
    try:
        response = tq.get_trade_results(response)
    except requests.exceptions.RequestException as e:
        SystemExit(e)
    #Calculate average profit on 3 to 1 trade
    base_item = response['result'][0]['item']['extended']['mods']['explicit']
    mods = [x['magnitudes'] for x in base_item]
    mods = list(itertools.chain.from_iterable(mods))
    min_max = [{'min':x['min'],'max':x['max']} for x in mods]
    ids = [x['hash'] for x in mods]

    return zip(ids,min_max)

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
    name = gem['Name']

    if gem['support']:
        regrade = gem_data.s_regrade
    else:
        regrade = gem_data.p_regrade

    #Get gem data
    gem_qualities = gem_data.qual_types
    cost = []
    for qual in gem_qualities:
        if gem[qual] > 0:
            data = gem_data.get_gem_data(name,qual)
            try:
                starter,conf = gem_data.get_entry_gem_value(data,name,qual,False,gem['exceptional'])
            except IndexError:
                raise IndexError(f"No Listings for gem {qual} {name}")
            except ValueError as ve:
                raise ve
            
            cost.append([qual,starter])
            gem_dict[qual] = {"cost":starter,"profit":0,"conf":conf}

    #Get Value of base gem
    for qual1, qual2 in itertools.permutations(gem_dict.keys(), 2):
        cost_str = qual1+"->"+qual2
        q1v = gem_dict[qual1].get("cost")
        q2v = gem_dict[qual2].get("cost")

        profit = q2v-regrade-q1v
        odds = gem[cost_str]
        gem_dict[qual1]["profit"] += (profit * odds)

    #Calculate best profit gem
    top = max(cost,key=lambda item:item[1])
    
    return top, gem_dict

def get_top_gem_regrade(gem_data):
    top_gems = []
    prime = []
    second = []
    i_error = []
    v_error = []
    for i in tqdm(gem_data,total=len(gem_data)):
        gem = i['Name']

        try:
            top, starter = gem_regrade(i,gem_data)
            starter = [{"name": name+" "+gem, "cost": v['cost'], \
                        "profit": v['profit'], "conf": v['conf']} \
                       for name, v in starter.items()]
            starter = pd.DataFrame(starter)
        except IndexError as ex:
            i_error.append(ex)
        except ValueError as vs:
            v_error.append(vs)
            
        top_gems.append([i['Name']]+top)
        if i['support']:
            second.append(starter)
        else:
            prime.append(starter)


    #print(starter)
    top_gems = pd.DataFrame(top_gems,columns=['name','top_target','top_cost'])
    prime_gems = pd.concat(prime).reset_index(drop=True)
    second_gems = pd.concat(second).reset_index(drop=True)
    
    return top_gems, prime_gems, second_gems

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
    
    league = 'Crucible'
    
    curr_data.get_data(league)
    gem_data.get_data(league)
    unique_data.get_data(league)
    
    print(gem_data)
#%%
    gem_data.set_regrading(curr_data)

    top_gems, prime_gems, second_gems = get_top_gem_regrade(gem_data)
    
#%%
    print(top_gems.sort_values('top_cost',ascending=False).head(10))
    print(prime_gems.sort_values('profit',ascending=False).head(10))
    print(second_gems.sort_values('profit',ascending=False).head(10))
    
#%%
    second_gems[second_gems['name'].str.contains('Mana')]
    
#%%
    uni = unique_3to1(league,"Thread of Hope", unique_data)
#%%
    for x, y in uni:
        print(x,y)
    
    misc_filters = {'disabled': 'false', 'filters': {'corrupted': {'option': "false"}}}
    stats = [{
  "id": "explicit.stat_3642528642",
  "value": {
    "min": 3,
    "max": 3
  },
  "disabled": False
}]
    #Make query for base item with no maximized rolls from trade site
    query = tq.make_trade_query('online','Thread of Hope',misc_filters=misc_filters,stat_filters=stats)
    try:
        response = tq.query_trade(league, query)
    except requests.exceptions.RequestException as e:
        SystemExit(e)
        
    print(response)
    
#%%
    try:
        response = tq.get_trade_results(response)
    except requests.exceptions.RequestException as e:
        SystemExit(e)
    print(response)
    #skin_of_the_loyal_3_to_1()