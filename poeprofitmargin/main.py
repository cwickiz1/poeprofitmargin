# -*- coding: utf-8 -*-
"""
Created on Fri May 19 19:10:07 2023

@author: wicki
"""

import customtkinter
import time
from gem import GemData
from currency import CurrData
from poeprofitmargin import get_top_gem_regrade

class MenuFrame(customtkinter.CTkFrame):
    def __init__(self, master, gem_data, curr_data):
        super().__init__(master)
        
        self.gem_data = gem_data
        self.curr_data = curr_data

        self.button_1 = customtkinter.CTkButton(self, text="Regrade Gems", command=self.gem_regrade_click)
        self.button_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.button_2 = customtkinter.CTkButton(self, text="3 to 1 Uniques", command=self.unique_3to1)
        self.button_2.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        self.button_3 = customtkinter.CTkButton(self, text="Corrupt Gems", command=self.corrupt_gem)
        self.button_3.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")

    def gem_regrade_click(self):
        curr_time = time.time()
        if curr_time > self.gem_data.update_time + 300:
            self.gem_data.get_data('Crucible')
        
        if curr_time > self.curr_data.update_time + 300:
            self.curr_data.get_data('Crucible')
            
        self.gem_data.set_regrading(self.curr_data)
        
        top_gems, prime_gems, second_gems = get_top_gem_regrade(self.gem_data)

        print(top_gems.sort_values('top_cost',ascending=False).head(10))
        print(prime_gems.sort_values('profit',ascending=False).head(10))
        print(second_gems.sort_values('profit',ascending=False).head(10))
        
    def unique_3to1(self):
        print("unique_3to1")
        
    def corrupt_gem(self):
        print("corrupt")

class MyCheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.checkbox_1 = customtkinter.CTkCheckBox(self, text="checkbox 1")
        self.checkbox_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.checkbox_2 = customtkinter.CTkCheckBox(self, text="checkbox 2")
        self.checkbox_2.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        self.checkbox_3 = customtkinter.CTkCheckBox(self, text="checkbox 3")
        self.checkbox_3.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        
    def get(self):
        checked_checkboxes = []
        if self.checkbox_1.get() == 1:
            checked_checkboxes.append(self.checkbox_1.cget("text"))
        if self.checkbox_2.get() == 1:
            checked_checkboxes.append(self.checkbox_2.cget("text"))
        if self.checkbox_3.get() == 1:
            checked_checkboxes.append(self.checkbox_3.cget("text"))
        return checked_checkboxes
    

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.gem_data = GemData()
        self.gem_data.get_data('Crucible')
        
        self.curr_data = CurrData()
        self.curr_data.get_data('Crucible')

        self.title("my app")
        self.geometry("400x180")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.menu_frame = MenuFrame(self, self.gem_data, self.curr_data)
        self.menu_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")
        
        self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callback)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
    
    def button_callback(self):
        print("checked checkboxes:", self.menu_frame.get())

app = App()
app.mainloop()