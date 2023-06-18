# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 20:37:28 2023

@author: Craig Wickizer
"""
import os
import requests
import pandas as pd
import tradequery as tq
from baseitem import BaseItemData
import itertools

class UniqueData(BaseItemData):
    """
    A class to store data on unique items from poe.ninja.

    ...

    Attributes
    ----------
    data : DataFrame
        dataframe of all unique items currently in pathofexile
    unique_data :
        dataframe containing all item unique types pulled from poe.ninja

    Methods
    -------
    get_data(additional=""):
        Read current poe.ninja unique prices and update stored prices
    """
    @staticmethod
    def __get_item_mods(item):
        """
        Helper function to get the item mods and ranges from an individual item from poe.trade api
        -------------
        
        Parameters
        -------------
        item: json object containing info of item from trade site 
        -------------
        
        Returns
        -------------
        dataframe of mods and their values for trade site
        """
        base_item = item['item']['extended']['mods']['explicit']
        mods = [x['magnitudes'] for x in base_item]
        mods = list(itertools.chain.from_iterable(mods))
        item_dict = [{'id':x['hash'],'min':x['min'],'max':x['max']} for x in mods]
        df = pd.DataFrame(item_dict)
        return df
    
    def __init__(self,league):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        data_path = os.path.join(dir_path,"data")
        
        BaseItemData.__init__(self)
        self.league = league
        self.data = pd.read_csv(os.path.join(data_path,'uniques.csv'))
        self.mods = pd.read_csv(os.path.join(data_path,'mods.csv'))
        self.unique_types = ['Accessory','Armour','Weapon','Flask','Jewel']
        self.unique_data = pd.DataFrame()
        self.get_data()


    def get_data(self):
        dfs = []
        for item in self.unique_types:
            try:
                url = f"https://poe.ninja/api/data/itemoverview?league={self.league}&type=Unique{item}"
                response = requests.get(url).json()['lines']
                df = pd.DataFrame(response)
                df['basetype'] = item
                dfs.append(df)
            except:
                print(f"Error getting Unique {item} from poe.ninja")
        
        self.unique_data = pd.concat(dfs).reset_index(drop=True)
        
    def get_price_data(self,name):
        data = self.unique_data.loc[self.unique_data['name']==name]
        if ~data.empty:
            return data
        else:
            return None
    
    def get_item_info(self,item):
        """
        Parameters
        -------------
        item: item that is being checked for 3 to 1
        item_data: cost of items currently on poe.ninja
        -------------
        
        Returns
        -------------
        profit margin for three to one unique recipe for a certain unique targeting a certain roll
        returns none if item not found in league
        """
        data = self.get_price_data(item)
        
        if data.empty:
            return None
        
        misc_filters = {'disabled': 'false', 'filters': {'corrupted': {'option': "false"}}}
        
        #Make query for base item with no maximized rolls from trade site
        query = tq.make_trade_query('online',item,misc_filters=misc_filters)
        
        #Get first item from query
        response = tq.query_trade(self.league, query)
        base_item = response['result'][0]
        
        #Calculate average profit on 3 to 1 trade
        df = self.__get_item_mods(base_item)
        df['item'] = item
        
        cost = 100

        return len(response['result']), cost, df
    
    def set_league(self,league: str):
        self.league = league

    def __str__(self):
        return f"UniqueData contains {len(self.data)} items"

if __name__=="__main__":
    #GGG API Header
    data = UniqueData('Crucible')
    print(data)
    print(data.unique_data[~data.unique_data['links'].isna()])
#%%
    print("{}\n{}\n{}".format(*data.get_item_info("Ventor's Gamble")))
