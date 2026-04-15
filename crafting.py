import pygame 

RECIPES = {
    "Rad-Ointment": {"Filtered water": 1, "Glowing Aloe": 1 , "Scrap Fiber": 1},
    "Speed Serum": {"Bio-Fuel": 1, "Rusty Thorn": 1, "Filtered water": 1},
    "Lung-Clear": {"Filtered water":1, "Glowing Aloe": 1},
    "Blood-Stop":{"Scrap Fiber":1, "Rusty Thorn": 1},
    "Pain Killer":{"Bio_Fuel":1, "Glowing Aloe": 1, "Rusty Thorn": 1}
}

inventory = {"Filtered water": 999999, "Bio-Fuel": 999999, "Scrap Fiber": 999999, "Glowing Aloe": 0, "Rusty Thorn":0 }
