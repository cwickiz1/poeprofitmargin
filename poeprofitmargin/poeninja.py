# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 22:28:12 2023

@author: wicki
"""
import pandas as pd
import requests

class POENinja():
    def __init__(self,url,league):
        self.url = f"https://poe.ninja/api/data/itemoverview?league={league}&type="
        self.league = league
        response = requests.get(url).json()
        self.data = pd.DataFrame(response)
        
    def get_data(self,items):
        dfs = []
        for item in items:
            try:
                url = self.url + item
                response = requests.get(url).json()['lines']
                df = pd.DataFrame(response)
                df['basetype'] = item
                dfs.append(df)
            except:
                print(f"Error getting Unique {item} from poe.ninja")
        
        self.unique_data = pd.concat(dfs).reset_index(drop=True)