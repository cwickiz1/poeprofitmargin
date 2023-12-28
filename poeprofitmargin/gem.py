# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 20:43:33 2023

@author: Craig Wickizer
"""
#%%
import sys
import time
import os
import requests
import pandas as pd
from baseitem import BaseItemData
from currency import CurrData
from functools import lru_cache

from tqdm import tqdm


#%%
class GemData(BaseItemData):
    def __init__(self, league):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(dir_path, 'data')
        
        self.league = league
        self.data = pd.read_csv(os.path.join(path,'gems.csv'))
        self.update_time = time.time()
        self.gem_data = pd.DataFrame()
        self.qual_types = ['Superior','Anomalous','Divergent','Phantasmal']
        self.alt_qual_types = ['Anomalous','Divergent','Phantasmal']
        self.gcp = 1
        self.p_regrade = 0
        self.s_regrade = 0

    def get_data(self):
        response = requests.get(f"https://poe.ninja/api/data/itemoverview?league={self.league}&type=SkillGem")
        if response.status_code==200:
            self.update_time = time.time()
            self.gem_data = pd.DataFrame(response.json()['lines'])
            self.gem_data['corrupted'] = self.gem_data['corrupted'].fillna(False)
            self.gem_data['vaal'] = False
            self.gem_data.loc[self.gem_data['name'].str.contains('Vaal'),'vaal'] = True
            self.gem_data['gemQuality'] = self.gem_data['gemQuality'].fillna(0).astype(int)
            
            #Reset gem_data Cache
            self.get_gem_data.cache_clear()

        else:
            raise Exception("Response status code: {} searching {} \
                            league for Gems".format(response.status_code,league))

    @lru_cache(maxsize=None)
    def get_gem_data(self,name,qual='Superior'):
        if qual != "Superior":
            name = qual + " " + name
        return self.gem_data[self.gem_data['name']==name].copy().reset_index(drop=True)

    def get_entry_gem_value(self,df,name,qual,awakened=None,exceptional=None):
        """
        parameters:
        df - pd.DataFrame - dataframe of various sale categories for gem from poe.ninja
        awakened - bool - whether the gem is an awakened gem or not
        exceptional - bool - whether the gem is an exceptional gem or not
        """
        level = 20
        if awakened and exceptional:
            level -= 16
        elif awakened:
            level -= 15
        elif exceptional:
            level -= 17
        try:
            entry = df[(df['corrupted']==False) & (df['gemQuality']==20)]# & (df['gemLevel']>2)]
            minimum = entry.iloc[-1]['chaosValue']
            #maximum = entry.iloc[0]['chaosValue']
        except IndexError:
            raise IndexError("No Listings for gem")
        #CHANGE CHECK TO ACCOUNT FOR COST OF GCP INSTEAD FOR LOW VALUE GEMS
        #if maximum>(6*(minimum+(20*self.gcp))):
            #raise ValueError(f"Listing for {qual} {name} is Low Confidence: Min={minimum}, Max={maximum}")
        return minimum,(entry.iloc[0]['listingCount']>10)

    def set_regrading(self,curr_data):
        #Get Secondary Regrading
        self.s_regrade = curr_data.curr_data[curr_data.curr_data["currencyTypeName"]=="Secondary Regrading Lens"].iloc[0]['chaosEquivalent']
        #Get Prime Regrading
        self.p_regrade = curr_data.curr_data[curr_data.curr_data["currencyTypeName"]=="Prime Regrading Lens"].iloc[0]['chaosEquivalent']
        
    def vaal_gem(self,name,qual='Superior'):
        data = self.get_gem_data(name,qual)
        return data
    def __str__(self):
        return "GemData contains {} items".format(len(self.data))

#%%

if __name__ == "__main__":
    
    league = 'Ancestor'
    try:
        gem_data = GemData(league)
    except Exception as err:
        print(err)
        sys.exit(1)

    try:
        curr_data = CurrData(league)
    except Exception as err:
        print(err)
        sys.exit(1)
    curr_data.get_data()
    gem_data.get_data()
    print(curr_data)
    print(gem_data)

#%%
    data = gem_data.vaal_gem('Tornado Shot','Divergent')
    print(data)

#%%
    gem_data.set_regrading(curr_data)
    print(gem_data.p_regrade)
#%%
    entry = gem_data.get_entry_gem_value(df, name, qual)
    print(starter)
