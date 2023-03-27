# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 21:01:43 2023

@author: wicki
"""

#%%
import requests
import pandas as pd
import itertools

from tqdm import tqdm

#%%
class BaseCurrencyData():
    def __init__(self,league=None):
        self.data = pd.DataFrame()
    
    def get_data(self,league:str,ctype:str):
        response = requests.get(f"https://poe.ninja/api/data/currencyoverview?league={league}&type={ctype}") 
        if response.status_code==200:
            self.data = pd.DataFrame(response.json()['lines'])
        else:
            raise Exception("Response status code: {} searching {} league for {}".format(response.status_code,league,ctype))
      
    def __getitem__(self,idx):
        return self.data.iloc[idx]
    
    def __len__(self):
        return len(self.data)
    
    def __str__(self):
        return "BaseCurrencyData contains {} items".format(len(self.data))

#%%

if __name__ == "__main__":
    try:
        data = BaseCurrencyData()
        data.get_data("Sanctum","Fragment")
    except Exception as err:
        print(err)
        exit(1)
        
    print(data[1])