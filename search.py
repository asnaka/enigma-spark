import json

with open('data/items.json', 'r', encoding='utf-8') as itemFile:
    items = json.load(itemFile)

def searchWeapons(search, items):
    for category in list(items['weapons'].values()):
        for group in list(category.values()):
            result = next((item for item in group if item["name"].lower() == search.lower()), None)
            if result: return result

def searchTools(search, items):
    result = next((item for item in items['tools'] if item["name"].lower() == search.lower()), None)
    if result: return result

def searchItems(search, items=items):
    for key in list(items.keys()):
        if key == 'weapons':
            result = searchWeapons(search, items)
            if result: return result
        elif key == 'tools':
            result = searchTools(search, items)
            if result: return result

itemFile.close()
