# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 14:53:00 2023

@author: wicki
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup

def update_data():
    #Pull all items from GGG
    url = 'https://www.pathofexile.com/api/trade/data/items'
    head = {"Content-Type": "application/json", "User-Agent": "NAME_YOU_CHOOSE"}
    try:
        items = requests.get(url,headers=head).json()['result']
    except:
        raise Exception(f"Failed to pull data from {url}")
    #Update Uniques
    #collect_uniques(items)
    #Update Currency
    #collect_currency(items) 
    #Update Gems
    #collect_gems(items)
    return items

def collect_uniques(items):
    accessories = pd.DataFrame(items[0]['entries'])
    accessories = accessories.fillna(False)
    accessories = accessories[accessories['flags'] != False]
    accessories['category'] = "Accessory"
    armour = pd.DataFrame(items[1]['entries'])
    armour = armour.fillna(False)
    armour = armour[armour['flags'] != False]
    armour['category'] = "Armour"
    weapons = pd.DataFrame(items[8]['entries'])
    weapons = weapons.fillna(False)
    weapons = weapons[weapons['flags'] != False]
    weapons['category'] = "Weapon"
    jewels = pd.DataFrame(items[6]['entries'])
    jewels = jewels.fillna(False)
    jewels = jewels[jewels['flags'] != False]
    jewels['category'] = "Jewel"
    flasks = pd.DataFrame(items[4]['entries'])
    flasks = flasks.fillna(False)
    flasks = flasks[flasks['flags'] != False]
    flasks['category'] = "Flask"
    
    uniques = pd.concat([accessories,armour,weapons,jewels,flasks])
    uniques = uniques.drop('flags',axis=1)
    
    uniques.to_csv("uniques.csv",index=False)
    
def collect_gems():
    gems = pd.read_html("http://www.vhpg.com/poe-alternate-quality-gems/")[0]
    gem_names = gems['Name'].copy()
    gems = gems.rename({"Weight": "Superior"},axis=1)
    
    #Get alt qual values
    def alt_qual(qual,name):
        try:
            return gems[gems['Name'] == qual+" "+name].iloc[0]['Superior']
        except:
            return 0
    
    quals = ["Anomalous","Divergent","Phantasmal"]
    for qual in quals:
        gems[qual] = gems['Name'].apply(lambda x: alt_qual(qual,x))
    
    gems = gems.drop(gems[gems['Name'].str.contains('Awakened|Vaal|Old')].index)
    
    gems['awakened'] = ("Awakened " + gems['Name']).isin(gem_names)
    gems['vaal'] = ("Vaal " + gems['Name']).isin(gem_names)
    gems['support'] = gems['Name'].str.contains("Support")
    gems['exceptional'] = gems['Name'].str.contains('Enlighten Support|Empower Support|Enhance Support')
    
    gems = gems.drop(gems[gems['Name'].str.contains('|'.join(quals))].index).reset_index(drop=True)
    
    
    
    #ADD QUAL TYPE CONVERSIONS
    gems[["Superior","Anomalous","Divergent","Phantasmal"]] = gems[["Superior","Anomalous","Divergent","Phantasmal"]].astype(int)
    gems['total'] = gems['Superior'] + gems['Anomalous'] + gems['Divergent'] + gems['Phantasmal']
    
    types = ["Superior","Anomalous","Divergent","Phantasmal"]
    for i, qual in enumerate(types):
        types_c = types.copy()
        types_c.pop(i)
        for qual_c in types_c:
            comp = qual+"->"+qual_c
            gems[comp] = gems[qual_c] / (gems['total']-gems[qual])
    
    gems.to_csv("gems.csv",index=False)
    
def collect_div_cards(items):
    cards = pd.DataFrame(items[2]['entries'])
        
    cards.to_csv("cards.csv",index=False)

def collect_currency(items):
    accessories = pd.DataFrame(items[0]['entries'])
    accessories = accessories.fillna(False)
    accessories = accessories[accessories['flags'] != False]
    accessories['category'] = "Accessory"
    armour = pd.DataFrame(items[1]['entries'])
    armour = armour.fillna(False)
    armour = armour[armour['flags'] != False]
    armour['category'] = "Armour"
    weapons = pd.DataFrame(items[8]['entries'])
    weapons = weapons.fillna(False)
    weapons = weapons[weapons['flags'] != False]
    weapons['category'] = "Weapon"
    jewels = pd.DataFrame(items[6]['entries'])
    jewels = jewels.fillna(False)
    jewels = jewels[jewels['flags'] != False]
    jewels['category'] = "Jewel"
    flasks = pd.DataFrame(items[4]['entries'])
    flasks = flasks.fillna(False)
    flasks = flasks[flasks['flags'] != False]
    flasks['category'] = "Flask"
    
    uniques = pd.concat([accessories,armour,weapons,jewels,flasks])
    uniques = uniques.drop('flags',axis=1)
    
    uniques.to_csv("uniques.csv",index=False)
    
if __name__ == "__main__":
    items = update_data()
    cards = pd.DataFrame(items[2]['entries'])
    """
    card_url = 'https://poedb.tw/us/Divination_Cards'
    response = requests.get(card_url)
    soup = BeautifulSoup(response.text,"html.parser")
    tables = soup.find_all('table')
    dfs = []
    
    try:
        rows = []
        for row in tables[7].find_all('tr'):
            data = row.get_text(separator="\\", strip=True)
            dlist = data.split('\\')
            if len(dlist) > 2:
                stack_size = 1
                result = ""
                name = dlist[0]
                #Handle No Stack Size Rows
                if dlist[1] == "Stack Size:":
                    stack_size = dlist[2].split(" ")[-1]
                    result = "\n".join(dlist[3:])
                else:
                    result = "\n".join(dlist[1:])
                
                #TODO: EXTRACT AMOUNT OF REWARDS FROM RESULTS 
                
                #Append Row
                rows.append([name,stack_size,result])

        df = pd.DataFrame(rows)
    except:
        raise Exception("Failed to make card table")
    # Create a dataframe
    #dfs.append(rows)
    
    #cards = dfs[7]
    """
    
    #UPDATED CSV FILES
    #collect_gems()