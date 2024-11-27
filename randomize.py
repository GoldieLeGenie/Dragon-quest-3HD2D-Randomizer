from pythonnet import load
import json
import sys, random, subprocess
import os
load("coreclr")
import clr
sys.path.append(os.path.join(os.getcwd(), "netstandard2.0"))
clr.AddReference("UAssetAPI")
from UAssetAPI import UAsset
from UAssetAPI.UnrealTypes import EngineVersion
import tkinter as tk
from tkinter import messagebox
import utils


def randomize_buy_price(min_price, max_price):
    try:
        myAsset = UAsset("./uasset/GOP_Item.uasset", EngineVersion.VER_UE4_27)
        json_asset = json.loads(myAsset.SerializeJson())

        for data in json_asset["Exports"][0]["Table"]["Data"]:
            for BuyPrice in data["Value"]:
                if BuyPrice['Name'] == "BuyPrice":
                    if isinstance(BuyPrice["Value"], int) and BuyPrice["Value"]:
                        gold = random.randint(min_price, max_price)
                        BuyPrice['Value'] = gold

        ModifiedAsset = UAsset.DeserializeJson(json.dumps(json_asset))
        ModifiedAsset.Write("./Game-WindowsNoEditor_test/Game/Content/Nicola/Data/DataTable/GOP_Item.uasset")
    except Exception as e:
        messagebox.showerror("Error", f"An error occured : {e}")

def randomize_shop_items():
    try:
        myAsset = UAsset("./uasset/GOP_Shop.uasset", EngineVersion.VER_UE4_27)
        json_asset = json.loads(myAsset.SerializeJson())
        
        for data in json_asset["Exports"][0]["Table"]["Data"]:
            for prod in data["Value"]:
                if prod['Name'].startswith("Product_"):
                    if prod["Value"] != "None":
                        item = random.choice(utils.item_names)
                        prod["Value"] = item

        ModifiedAsset = UAsset.DeserializeJson(json.dumps(json_asset))
        ModifiedAsset.Write("./Game-WindowsNoEditor_test/Game/Content/Nicola/Data/DataTable/GOP_Shop.uasset")
    except Exception as e:
        messagebox.showerror("Error", f"An error occured : {e}")

def randomize_mini_medals_rewards():
    myAsset = UAsset("./uasset/GOP_Medal.uasset", EngineVersion.VER_UE4_27)
    json_asset = json.loads(myAsset.SerializeJson())

    for data in json_asset["Exports"][0]["Table"]["Data"]:
        for prod in data["Value"]:
            if prod['Name'] == "Product_0":
                new_value = random.choice(utils.item_names)
                prod["Value"] = new_value
            
    ModifiedAsset = UAsset.DeserializeJson(json.dumps(json_asset))
    ModifiedAsset.Write("./Game-WindowsNoEditor_test/Game/Content/Nicola/Data/DataTable/GOP_Medal.uasset")


def randomize_all_area_loot(min_price, max_price,gold_percentage, items_percentage, empty_percentage):
   
    directory = r".\uasset"
    files = [
        os.path.join(directory, file)
        for file in os.listdir(directory)
        if file.startswith("GOP_SearchObject") and file.endswith(".uasset")
    ]
    for file in files:
        try:
            myAsset = UAsset(file, EngineVersion.VER_UE4_27)
            json_asset = json.loads(myAsset.SerializeJson())

            for data in json_asset.get("Exports", [{}])[0].get("Table", {}).get("Data", []):
                draw_result = utils.items_or_golds_or_empty(gold_percentage, items_percentage, empty_percentage)

                for item in data.get("Value", []):
                    item_name = item.get("Name")
                    item_value = item.get("Value")

                    if item_name == "ItemId" and item_value in utils.important_items:
                        continue
                    if draw_result == "gold" and item_name == "Gold":
                        item["Value"] = random.randint(min_price, max_price)
                    elif draw_result == "gold" and item_name in {"ItemId", "ItemNum"}:
                        item["Value"] = 0 if item_name == "ItemNum" else "None"

                    elif draw_result == "item" and item_name == "ItemId":
                        item["Value"] = random.choice(utils.item_names)
                    elif draw_result == "item" and item_name == "ItemNum":
                        item["Value"] = 1
                    elif draw_result == "item" and item_name == "Gold":
                        item["Value"] = 0

                    elif draw_result == "empty" and item_name in {"ItemId", "ItemNum", "Gold"}:
                        item["Value"] = 0 if item_name != "ItemId" else "None"

                    elif draw_result == "empty" and item_name == "FlagName":
                        item["Value"] = "EGOPEnumSearchType::NONE"
            ModifiedAsset = UAsset.DeserializeJson(json.dumps(json_asset))
            ModifiedAsset.Write(f"./Game-WindowsNoEditor_test/Game/Content/Nicola/Data/DataTable/{os.path.basename(file)}")
        except Exception as e:
            print(f"ERROR : {e}")



def randomize_start_bag_items():
    myAsset = UAsset("./uasset/GOP_Unit_ItemBag.uasset", EngineVersion.VER_UE4_27)
    json_asset = json.loads(myAsset.SerializeJson())

    for data in json_asset["Exports"][0]["Table"]["Data"]:
        for item in data["Value"]:
            if item['Name'] == "GopIdItem1":
                if item['Value'] == "ITEM_EQUIP_WEAPON_COPPER_SWORD":
                    item_name = random.choice(utils.item_names)
                    item["Value"] = item_name
            if item['Name'] == "GopIdItem2":
                if item['Value'] == "ITEM_EQUIP_ARMOR_WAYFARERS_CLOTHES":
                    item_name = random.choice(utils.item_names)
                    item["Value"] = item_name
            if item['Name'] == "GopIdItem3":
                if item['Value'] == "ITEM_EQUIP_SHIELD_LEATHER_SHIELD":
                    item_name = random.choice(utils.item_names)
                    item["Value"] = item_name
          
            
    ModifiedAsset = UAsset.DeserializeJson(json.dumps(json_asset))
    ModifiedAsset.Write("./Game-WindowsNoEditor_test/Game/Content/Nicola/Data/DataTable/GOP_Unit_ItemBag.uasset")


def randomize_monster_drop():
    myAsset = UAsset("./uasset/GOP_Monster.uasset", EngineVersion.VER_UE4_27)
    json_asset = json.loads(myAsset.SerializeJson())

    for data in json_asset["Exports"][0]["Table"]["Data"]:
        for Drop_Item in data["Value"]:
            if Drop_Item['Name'] == "Drop_Item":
                if Drop_Item["Value"] != "None":
                    item = random.choice(utils.item_names)
                    Drop_Item["Value"] = item
                
          
            
    ModifiedAsset = UAsset.DeserializeJson(json.dumps(json_asset))
    ModifiedAsset.Write("./Game-WindowsNoEditor_test/Game/Content/Nicola/Data/DataTable/GOP_Monster.uasset")

def randomize_monster_spawn():
    myAsset = UAsset("./uasset/GOP_Encounter_Monster.uasset", EngineVersion.VER_UE4_27)

    json_asset = json.loads(myAsset.SerializeJson())
    with open("./jsonfile/monsters.json", "r") as json_file:
            monster_list = json.load(json_file) 
    
    for data in json_asset["Exports"][0]["Table"]["Data"]:
        for MonsterId in data["Value"]:
            if MonsterId['Name'] == "MonsterId1" or MonsterId['Name'] == "MonsterId2" or MonsterId['Name'] == "MonsterId3" or MonsterId['Name'] == "MonsterId4" or MonsterId['Name'] == "MonsterId5":
                if MonsterId["Value"] != "None":
                    monster = random.choice(monster_list)
                    MonsterId["Value"] =  monster
 
    ModifiedAsset = UAsset.DeserializeJson(json.dumps(json_asset))
    ModifiedAsset.Write("./Game-WindowsNoEditor_test/Game/Content/Nicola/Data/DataTable/GOP_Encounter_Monster.uasset")


def randomize_shine_items(min_gold, max_gold):
    myAsset = UAsset("./uasset/GOP_ShineSearchObject.uasset", EngineVersion.VER_UE4_27)
    json_asset = json.loads(myAsset.SerializeJson())

    for data in json_asset.get("Exports", [{}])[0].get("Table", {}).get("Data", []):
        for item in data.get("Value", []):
            item_name = item.get("Name")
            item_value = item.get("Value")
            if item_name in ["ItemId1", "ItemId2", "ItemId3"] and item_value in utils.important_items:
                continue

            if item_name in {"Gold1", "Gold2", "Gold3"}:
                if item["Value"] != 0:
                    item["Value"] = random.randint(min_gold, max_gold)
            if item_name in {"ItemId1", "ItemId2", "ItemId3"}:
                if item["Value"] != "None":
                    item["Value"] = random.choice(utils.item_names)

    ModifiedAsset = UAsset.DeserializeJson(json.dumps(json_asset))
    ModifiedAsset.Write(f"./Game-WindowsNoEditor_test/Game/Content/Nicola/Data/DataTable/GOP_ShineSearchObject")
        
