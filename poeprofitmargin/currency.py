# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 21:16:22 2023

@author: Craig Wickizer
"""

import requests
import time
import pandas as pd

class CurrData():
    def __init__(self):
        self.update_time = time.time()
        self.curr_data = pd.DataFrame()
    
    def get_data(self,league):
        response = requests.get(f"https://poe.ninja/api/data/currencyoverview?league={league}&type=Currency") 
        if response.status_code==200:
            self.update_time = time.time()
            self.curr_data = pd.DataFrame(response.json()['lines'])
        else:
            raise Exception("Response status code: {} searching {} league for Currency".format(response.status_code,league))
            
    def __str__(self):
        return "CurrData contains {} items".format(len(self.curr_data))