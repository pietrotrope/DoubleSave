import json
with open('server/cached.json', 'r') as openfile:
    req = json.load(openfile)


with open('server/catalog.json', 'r') as openfile:
    cat = json.load(openfile)



for store_offers in req:
    for product_offer in store_offers["clearances"]:
        prod = product_offer["product"]
        cat[prod["ean"]] = prod

with open("server/catalog.json", "w") as outfile:
    json.dump(cat, outfile)