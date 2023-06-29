# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 01:07:14 2023

@author: Craig Wickizer

Structure of a bulk query
-------------------------

{ 
    exchange: {
        status: {
            option: "online";
        },
        have: [list of have currency],
        want: [list of want currency],
        minimum: mimimum stock from seller,
        account: "AccountName",
        fulfillable: null,
    }
}



Structure of an item query
--------------------------

{ 
    query: {
        status: {
            option: "online";
        },
        filters: {dictionary with keys of different filters},
        stats: [list of stat filters in format {type: and, filters: [stats]}]
    }
    sort: {price: asc}
}


Item FIlter Options
-------------------

armour_filters:
    ar: {min: 0, max: inf}
    base_defence_percentile: {min: 0, max: 100}
    block: {min: 0, max: inf}
    es: {min: 0, max: inf}
    ev: {min: 0, max: inf}
    ward: {min: 0, max: inf}
    
heist_filters:
    heist_agility: {min: 1, max: 5}
    heist_brute_force: {min: 1, max: 5}
    heist_counter_thaumaturgy: {max: 1, min: 5}
    heist_deception: {min: 1, max: 5}
    heist_demolition: {min: 1, max: 5}
    heist_engineering: {min: 1, max: 5}
    heist_escape_routes: {max: 1, min: 1}
    heist_lockpicking: {min: 1, max: 5}
    heist_max_escape_routes: {max: 1, min: 1}
    heist_max_reward_rooms: {min: 1, max: 1}
    heist_max_wings: {min: 1, max: 1}
    heist_objective_value: {option: ["moderate","high","precious","priceless"]}
    heist_perception: {min: 1, max: 5}
    heist_reward_rooms: {min: 1, max: 1}
    heist_trap_disarmament: {min: 1, max: 5}

map_filters:
    area_level: {min: 1, max: 1}
    map_blighted: {option: "false"}
    map_iiq: {min: 1, max: 1}
    map_iir: {min: 1, max: 1}
    map_packsize: {min: 1, max: 1}
    map_series: {option: "current"}
    map_tier: {min: 1, max: 1}
    map_uberblighted: {option: "false"}

misc_filters:
    alternate_art: {option: "false"}
    corrupted: {option: "false"}
    crafted: {option: "false"}
    foil_variation: {option: "voidborn"}
    fractured_item: {option: "false"}
    gem_alternate_quality: {option: "alternate"}
    gem_level: {max: 1, min: 21}
    gem_level_progress: {max: 1, min: 1}
    identified: {option: "false"}
    ilvl: {min: 1, max: 100}
    mirrored: {option: "false"}
    quality: {min: 1, max: 1}
    scourge_tier: {min: 1, max: 3}
    searing_item: {option: "false"}
    split: {option: "false"}
    stack_size: {max: 1, min: 1}
    stored_experience: {max: 1, min: 1}
    synthesised_item: {option: "false"}
    talisman_tier: {min: 1, max: 1}
    tangled_item: {option: "false"}
    veiled: {option: "false"}
    
req_filters:
    class: {option: "scion"}
    dex: {min: 1, max: 9}
    int: {min: 1, max: 9}
    lvl: {min: 1, max: 9}
    str: {min: 1, max: 9} 

socket_filters:
    links: {min: 0, max: 6, r: 0-6, g: 0-6, b: 0-6, w: 0-6}
    sockets: {min: 0, max: 6, r: 0-6, g: 0-6, b: 0-6, w: 0-6}
    
weapon_filters:
    aps: {min: 1, max: 9}
    crit: {min: 1, max: 9}
    damage: {min: 1, max: 9}
    dps: {min: 1, max: 9}
    edps: {min: 1, max: 9}
    pdps: {min: 1, max: 9}
    

"""

import requests

class TradeQuery():
    head = {"Content-Type": "application/json", "User-Agent": "NAME_YOU_CHOOSE"}
    item_trade_query_url = 'https://www.pathofexile.com/api/trade/search/'
    item_trade_fetch_url = 'https://www.pathofexile.com/api/trade/fetch/'

def post_trade(league,payload):
    """
    Parameters
    ----------
    league : str
        Name of Path of Exile trade league being queried for items.
    payload : dict
        JSON payload containing filters to POST to trade api.

    Returns
    -------
    response from trade api containing result ids to be used for fetch api call.
    """
    response = requests.post(TradeQuery.item_trade_query_url+league, json=payload, headers=TradeQuery.head).json()
    return response['id'],response['result']

def get_trade_results(trade_id,trade_ids):
    """
    Parameters
    ----------
    response : dict
        JSON ibject containing id info to be used to query fetch api from pathofexile.

    Returns
    -------
    JSON object containing response body from pathofexile item fetch.
    """
    #cache_key = (f'{url}/{payload}',)
    base = 0
    while len(trade_ids) > base+10:
        r_result = ','.join(trade_ids[base:base+10])
        result = f'{r_result}?query={trade_id}'
    
        response = requests.get(TradeQuery.item_trade_fetch_url+result, headers=TradeQuery.head)#, cache_key=cache_key)

    return response.json()

def query_trade(league,payload,listing=10):
    """
    Parameters
    ----------
    league : str
        Name of Path of Exile trade league being queried for items.
    payload : dict
        JSON payload containing filters to POST to trade api.

    Returns
    -------
    response from fetch api containing result of the items that fulfill the payload filter.
    """
    try:
        trade_id, trade_ids = post_trade(league, payload)
    except requests.exceptions.RequestException:
        raise requests.exceptions.RequestException()
    
    if len(trade_ids) < listing:
        listing = len(trade_ids)
    try:
        data = get_trade_results(trade_id,trade_ids[:listing])
    except requests.exceptions.RequestException:
        raise requests.exceptions.RequestException()
    
    return data

def make_filter(name):
    pass

def make_trade_query(status,name=None,misc_filters=None,stat_filters=None):
    """
    

    Parameters
    ----------
    status : TYPE
        DESCRIPTION.
    name : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    query = {
        "query": {
            "status": {
                "option": status
            },
            "filters": {},
            "stats": [{"type": "and", "filters": []}]
        },
        "sort": {"price": "asc"}
    }
    if stat_filters:
        query['query']['stats'][0]['filters'] = stat_filters
    if name:
        query['query']['name'] = name
    if misc_filters:
        query['query']['filters']['misc_filters'] = misc_filters
    return query

def make_bulk_query(have : list, want : list, minimum : int):
    """
    Parameters
    ----------
    have : list
        List containing the currency items you want to buy.
    want : list
        List containing the currency items you want to pay with.
    minimum : int
        Minimum stock of sellers for the currency you want to buy.

    Returns
    -------
    query : dict
        Dictionary that forms the query to pass to the post request to bulk trade.

    """
    query = {
        "exchange": {
            "status": {
                "option": "onlineleague"
            },
            "have": have,
            "want": want,
            "minimum": minimum,
        }
    }

    return query

if __name__ == "__main__":
    head = {"Content-Type": "application/json", "User-Agent": "NAME_YOU_CHOOSE"}
    
    #Test Bulk Exchange Query
    url = 'https://www.pathofexile.com/api/trade/exchange/Sanctum'
    query = make_bulk_query(['chaos'], ['exalted'], 0)
    print(query)
    r = requests.post(url,json=query,headers=head)
    print(r.json())
    
    #Test Item Trade Query
    url = 'https://www.pathofexile.com/api/trade/search/Sanctum'
    query = make_trade_query('online')
    print(query)
    r = requests.post(url,json=query,headers=head)
    print(r.json())
    
    #Test caching
    
    
#%%
    len(r.json()['result'])