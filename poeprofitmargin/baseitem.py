# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 21:12:19 2023

@author: Craig Wickizer
"""

#%%
import requests
import pandas as pd
import itertools

from tqdm import tqdm

#%%
class BaseItemData():
    def __init__(self,league=None):
        self.data = pd.DataFrame()
    
    def get_data(self,league:str,itype:str):
        response = requests.get(f"https://poe.ninja/api/data/itemoverview?league={league}&type={itype}") 
        if response.status_code==200:
            self.data = pd.DataFrame(response.json()['lines'])
        else:
            raise Exception("Response status code: {} searching {} league for {}".format(response.status_code,league,itype))
      
    def __getitem__(self,idx):
        return self.data.iloc[idx]
    
    def __len__(self):
        return len(self.data)
    
    def __str__(self):
        return "BaseItemData contains {} items".format(len(self.data))

#%%

if __name__ == "__main__":
    try:
        data = BaseItemData()
        data.get_data("Sanctum","UniqueAccessory")
    except Exception as err:
        print(err)
        exit(1)
        
    print(data[1])