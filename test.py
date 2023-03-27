# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 21:48:42 2023

@author: wicki
"""
import requests
import pandas as pd
from gem import GemData
from currency import CurrData

gem_data = GemData()
a = CurrData()
a.get_data("Sanctum")
gem_data.get_data("Sanctum")
print(a)
print(gem_data)

gem_data.set_regrading(a)
print(gem_data.p_regrade)

data = []
for i in gem_data:
    gem = i['type']

    try:
        best, starter = gem_data.get_gem_regrade_profit_margin(i)
        starter = [{"name": name+" "+gem, "cost": v['cost'], "profit": v['profit'], \
                    "conf": v['conf']} for name, v in starter.items()]
        starter = pd.DataFrame(starter)
        starter['best'] = best
        data.append(starter)
    except IndexError as ex:
        print(ex)
    except ValueError as vs:
        print(vs)

#print(starter)

all_gems = pd.concat(data).reset_index(drop=True)

print(all_gems.head(5))
