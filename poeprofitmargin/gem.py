# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 20:43:33 2023

@author: Craig Wickizer
"""
#%%
import sys
import os
import requests
import pandas as pd
from baseitem import BaseItemData
from currency import CurrData

from tqdm import tqdm

#%%
class GemData(BaseItemData):
    def __init__(self):  
        path = os.getcwd()
        dir = os.path.dirname(path)
        dir = os.path.join(dir, 'data')
        os.chdir(dir)

        self.data = pd.read_csv('gem_data.csv')
        self.gem_data = pd.DataFrame()
        self.qual_types = ['Superior','Anomalous','Divergent','Phantasmal']
        self.alt_qual_types = ['Anomalous','Divergent','Phantasmal']
        self.gcp = 1
        self.p_regrade = 0
        self.s_regrade = 0
        os.chdir(path)

    def get_data(self,league):
        response = requests.get(f"https://poe.ninja/api/data/itemoverview?league={league}&type=SkillGem")
        if response.status_code==200:
            self.gem_data = pd.DataFrame(response.json()['lines'])
            self.gem_data['corrupted'] = self.gem_data['corrupted'].fillna(False)
            self.gem_data['vaal'] = False
            self.gem_data.loc[self.gem_data['name'].str.contains('Vaal'),'vaal'] = True
            self.gem_data['gemQuality'] = self.gem_data['gemQuality'].fillna(0).astype(int)
        else:
            raise Exception("Response status code: {} searching {} \
                            league for Gems".format(response.status_code,league))

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
            entry = df[(df['corrupted']==False) & (df['corrupted']==False)]# & (df['gemLevel']>2)]
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

    def __str__(self):
        return "GemData contains {} items".format(len(self.data))

#%%

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
    curr_data.get_data("Sanctum")
    gem_data.get_data("Sanctum")
    #print(curr_data)
    #print(gem_data)

    gem_data.set_regrading(curr_data)
    #print(gem_data.p_regrade)

    regrade = 0
    data = []
    i_error = []
    v_error = []
    for i in tqdm(gem_data,total=len(gem_data)):
        gem = i['type']

        try:
            _, starter = gem_data.get_gem_regrade_profit_margin(i)
            starter = [{"name": name+" "+gem, "cost": v['cost'], "profit": v['profit'], "conf": v['conf']} for name, v in starter.items()]
            starter = pd.DataFrame(starter)
            data.append(starter)
        except IndexError as ex:
            i_error.append(ex)
        except ValueError as vs:
            v_error.append(vs)

    #print(starter)

    all_gems = pd.concat(data).reset_index(drop=True)

    print(all_gems.sort_values('profit',ascending=False).head())