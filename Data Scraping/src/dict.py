import json
import os.path

gameslist = []

mygame = {
        'title': "title",
        'price': "price",
        'discprice': "discprice"
    }
gameslist.append(mygame)

mygame = {
        'title': "title2",
        'price': "price2",
        'discprice': "discprice2"
    }
gameslist.append(mygame)

thisdict = {
    "Dic" : gameslist
}

with open(os.path.dirname(__file__) + '/../data/contohJSON.json', 'w') as f:
  json.dump(thisdict, f, indent=2)