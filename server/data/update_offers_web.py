from sallinggroup.server.data.db_connection import *
import requests
import numpy as np
import time
import json
from sallinggroup.server.data.constants import salling_token
from datetime import datetime as dt
import datetime
import csv

def update_offers():

    def correct_date(p):
        if p[-7] == "4" and p[-8] == "2":
            p = list(p)
            p[-7]="3"
            p[-5]="5"
            p =''.join(p)
        return p


    centroids = np.load("./server/data/centroids.npy")

    headers = {"Authorization": salling_token}

    cache = {}


    timestamp = dt.now()

    opening_times = []
    with open('./server/data/opening_times.csv', mode ='r')as file:
        csv_file = csv.reader(file)
        for line in csv_file:
            opening_times.append(line)


    i = 0
    hits = 0

    new_opening_times = []

    for num, center in enumerate(centroids):
        time_opening = dt.strptime(opening_times[num][0],"%H:%M").time()
        time_close = dt.strptime(opening_times[num][1],"%H:%M").time()
        info_date = dt.strptime(opening_times[num][2],"%Y-%m-%d").date()

        if (timestamp.time() < time_close and timestamp.time() > time_opening) or info_date < dt.today().date():

            req = requests.get("https://api.sallinggroup.com/v1/food-waste/?geo="+str(center[1])+","+str(center[0])+"=10", headers=headers)

            j = json.loads(req.text)

            opening = dt.strptime("2024-06-01T23:45:00","%Y-%m-%dT%H:%M:%S")
            closing = dt.strptime("2024-06-01T01:00:00","%Y-%m-%dT%H:%M:%S")

            for store_offers in j:
                if store_offers["store"]["name"] in cache:
                    hits+=1
                else:
                    for time_store in store_offers["store"]["hours"]:
                        if dt.strptime(time_store["date"],"%Y-%m-%d").date()  ==  dt.today().date():
                            if time_store["open"] is not None and time_store["close"]:
                            
                                open_hour = dt.strptime(correct_date(time_store["open"]),"%Y-%m-%dT%H:%M:%S")
                                close_hour = dt.strptime(correct_date(time_store["close"]),"%Y-%m-%dT%H:%M:%S")
                                if open_hour.time()<opening.time():
                                    opening=open_hour
                                if close_hour.time()>closing.time():
                                    closing=close_hour

                cache[store_offers["store"]["name"]] = store_offers
            #time.sleep(60/len(centroids))
            print(str(round((i/len(centroids))*100)))
            time.sleep(1)

            i+=1
        
            new_opening_times.append([opening.strftime("%H:%M"),closing.strftime("%H:%M"), dt.strptime(time_store["date"],"%Y-%m-%d").strftime("%Y-%m-%d")])
        else:
            new_opening_times.append([opening_times[num][0],opening_times[num][1], opening_times[num][2]])



    with open('./server/data/opening_times.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(new_opening_times)

    print("hits:")
    print(hits)

    print("N. stores:")
    print(len(cache.keys()))

    #with open("cache/compressed_cache.json", "w") as outfile:
    #    json.dump(cache, outfile)


    cur, con = get_cursor_and_connection()


    #with open('./cache/compressed_cache.json', 'r') as openfile:
    #    cache = json.load(openfile)
    timestamp = dt.now().strftime("%Y-%m-%d (%H:%M:%S.%f)")

    for _, store_offers in cache.items():

        address = store_offers["store"]["address"]["city"]
        address = address + store_offers["store"]["address"]["country"] + ", "
        address = address + store_offers["store"]["address"]["street"] + ", "
        address = address + store_offers["store"]["address"]["zip"]

        create_store(cur, store_offers["store"]["id"], "0", address, store_offers["store"]["name"], store_offers["store"]["brand"], str(store_offers["store"]["coordinates"]), timestamp)

        for product_offer in store_offers["clearances"]:
            img = product_offer["product"]["image"]
            if img is None:
                img = "noImage"
            
            en = ""
            da = ""

            if "categories" in product_offer["product"]:
                if "en" in product_offer["product"]["categories"]:
                    en = product_offer["product"]["categories"]["en"]
                if "da" in product_offer["product"]["categories"]:
                    da = product_offer["product"]["categories"]["da"]

            create_product(cur, product_offer["product"]["ean"], en, da, product_offer["product"]["description"], img, timestamp)
            create_offer(cur,  product_offer["product"]["ean"], store_offers["store"]["id"], product_offer["offer"]["currency"], product_offer["offer"]["endTime"], str(product_offer["offer"]["newPrice"]), str(product_offer["offer"]["originalPrice"]), product_offer["offer"]["startTime"], str(product_offer["offer"]["stock"]), product_offer["offer"]["stockUnit"], timestamp)
    delete_past_offers(cur, timestamp)

    commit_and_close(con)
