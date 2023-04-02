# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 20:37:28 2023

@author: Craig Wickizer
"""
import os
import requests
import pandas as pd
from baseitem import BaseItemData

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
    def __init__(self):
        path = os.getcwd()
        dir = os.path.dirname(path)
        dir = os.path.join(dir, 'data')
        os.chdir(dir)
        
        BaseItemData.__init__(self)
        self.data = pd.read_csv('uniques.csv')
        self.unique_data = pd.DataFrame()
        self.unique_types = ['Accessory','Armour','Weapon','Flask','Jewel']
        os.chdir(path)


    def get_data(self,league):
        dfs = []
        for item in self.unique_types:
            try:
                url = f"https://poe.ninja/api/data/itemoverview?league={league}&type=Unique{item}"
                response = requests.get(url).json()['lines']
                df = pd.DataFrame(response)
                df['basetype'] = item
                dfs.append(df)
            except:
                print(f"Error getting Unique {item} from poe.ninja")
        
        self.unique_data = pd.concat(dfs).reset_index(drop=True)
        
    def get_price_data(self):
        return self.unique_data

    def __str__(self):
        return f"UniqueData contains {len(self.data)} items"

if __name__=="__main__":
    #GGG API Header
    data = UniqueData()
    data.get_data('Sanctum')
    print(data)
    print(data.unique_data[~data.unique_data['links'].isna()])
